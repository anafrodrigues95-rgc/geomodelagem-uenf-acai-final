"""
Pipeline de treino e avaliação YOLO11-seg para o artigo do açaí (prova de conceito).

Responde aos itens do parecer técnico (seção 7):
  - re-divisão treino/validação/teste por GRUPO (imagem de origem), impedindo que
    variantes aumentadas da mesma foto atravessem partições;
  - aumento de dados apenas no treino (on-the-fly, pelo Ultralytics);
  - várias sementes, com média, desvio-padrão e IC 95%;
  - resultados no conjunto de TESTE, por classe (caixa e máscara);
  - matriz de confusão e curvas P-R (salvas pelo Ultralytics);
  - análise explícita de falsos negativos de triatomíneos;
  - registro de versões, pesos iniciais, sementes e critério de seleção.

Uso (Colab):  ver o notebook YOLO11_acai_triatomineos.ipynb
"""
from __future__ import annotations

import json
import math
import platform
import random
import re
import shutil
from collections import defaultdict
from pathlib import Path

import numpy as np
import yaml

IMG_EXT = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}


# ----------------------------------------------------------------------------
# 1. Coleta de imagens + rótulos de um ou mais datasets no formato YOLO
# ----------------------------------------------------------------------------
def group_key(stem: str) -> str:
    """Identifica a imagem de ORIGEM.

    O Roboflow nomeia arquivos como  IMG_1234_jpg.rf.<hash>.jpg ; versões
    aumentadas da mesma foto compartilham o prefixo antes de '.rf.'.
    Também remove sufixos comuns de frames de vídeo (ex.: video01_frame_0042),
    para que frames do mesmo vídeo fiquem no mesmo grupo.
    """
    base = stem.split(".rf.")[0]
    base = re.sub(r"_(jpg|jpeg|png)$", "", base, flags=re.I)
    base = re.sub(r"[_-]?(frame|f)[_-]?\d+$", "", base, flags=re.I)
    return base.lower()


def collect_items(dataset_dirs: list[str], source_tags: list[str] | None = None):
    """Varre pastas de datasets YOLO (com subpastas train/valid/test ou não)."""
    items = []
    for i, d in enumerate(dataset_dirs):
        d = Path(d)
        tag = source_tags[i] if source_tags else d.name
        for img in d.rglob("*"):
            if img.suffix.lower() not in IMG_EXT or "images" not in img.parts:
                continue
            parts = list(img.parts)
            idx = len(parts) - 1 - parts[::-1].index("images")
            parts[idx] = "labels"
            lbl = Path(*parts).with_suffix(".txt")
            classes = []
            if lbl.exists():
                for line in lbl.read_text().splitlines():
                    if line.strip():
                        classes.append(int(float(line.split()[0])))
            items.append({
                "img": str(img),
                "lbl": str(lbl) if lbl.exists() else None,
                "group": f"{tag}::{group_key(img.stem)}",
                "source": tag,
                "classes": classes,
            })
    return items


def dedupe_augmented(items, keep="first"):
    """Mantém uma única imagem por grupo (descarta variantes aumentadas
    pelo Roboflow). Recomendado: o aumento passa a ser feito só no treino."""
    seen, out = set(), []
    for it in sorted(items, key=lambda x: x["img"]):
        if it["group"] in seen:
            continue
        seen.add(it["group"])
        out.append(it)
    return out


# ----------------------------------------------------------------------------
# 2. Divisão por grupo, estratificada pela presença de classes
# ----------------------------------------------------------------------------
def group_split(items, fractions=(0.70, 0.15, 0.15), seed=0, holdout_sources=None, train_only_patterns=("gemini",)):
    """Divide por grupo. Se `holdout_sources` for dado (ex.: ['campo_2026']),
    essas fontes vão inteiras para o TESTE EXTERNO e o restante é dividido
    entre treino e validação."""
    rng = random.Random(seed)
    groups = defaultdict(list)
    for it in items:
        groups[it["group"]].append(it)

    split = {"train": [], "val": [], "test": []}
    pool = []
    for g, its in groups.items():
        # imagens sintéticas (geradas por IA) entram só no treino, nunca na validação/teste
        if train_only_patterns and any(pat in g.lower() for pat in train_only_patterns):
            split["train"].extend(its)
        elif holdout_sources and its[0]["source"] in holdout_sources:
            split["test"].extend(its)
        else:
            pool.append(g)

    # estrato = conjunto de classes presentes no grupo (ex.: (0,), (1,), (0,1), ())
    strata = defaultdict(list)
    for g in pool:
        cls = tuple(sorted({c for it in groups[g] for c in it["classes"]}))
        strata[cls].append(g)

    ftr, fva, fte = fractions
    if holdout_sources:
        ftr, fva, fte = ftr / (ftr + fva), fva / (ftr + fva), 0.0
    for cls, gs in strata.items():
        rng.shuffle(gs)
        n = len(gs)
        n_te = int(round(n * fte))
        n_va = int(round(n * fva))
        if n >= 3 and fte > 0 and n_te == 0:
            n_te = 1
        if n >= 3 and n_va == 0:
            n_va = 1
        for g in gs[:n_te]:
            split["test"].extend(groups[g])
        for g in gs[n_te:n_te + n_va]:
            split["val"].extend(groups[g])
        for g in gs[n_te + n_va:]:
            split["train"].extend(groups[g])
    return split


def check_no_leakage(split):
    gs = {k: {it["group"] for it in v} for k, v in split.items()}
    inter = (gs["train"] & gs["val"]) | (gs["train"] & gs["test"]) | (gs["val"] & gs["test"])
    assert not inter, f"Vazamento entre partições: {list(inter)[:5]}"
    return True


def materialize(split, out_dir, class_names):
    out = Path(out_dir)
    if out.exists():
        shutil.rmtree(out)
    for part, its in split.items():
        (out / part / "images").mkdir(parents=True, exist_ok=True)
        (out / part / "labels").mkdir(parents=True, exist_ok=True)
        for k, it in enumerate(its):
            name = f"{k:05d}_{Path(it['img']).stem[:60]}"
            shutil.copy2(it["img"], out / part / "images" / (name + Path(it["img"]).suffix.lower()))
            dst = out / part / "labels" / (name + ".txt")
            if it["lbl"]:
                shutil.copy2(it["lbl"], dst)
            else:
                dst.write_text("")
    data = {"path": str(out.resolve()), "train": "train/images", "val": "val/images",
            "test": "test/images", "names": {i: n for i, n in enumerate(class_names)}}
    (out / "data.yaml").write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False))
    return str(out / "data.yaml")


def split_summary(split, class_names):
    rows = []
    for part, its in split.items():
        inst = [0] * len(class_names)
        img_with = [0] * len(class_names)
        for it in its:
            for c in it["classes"]:
                if c < len(inst):
                    inst[c] += 1
            for c in set(it["classes"]):
                if c < len(img_with):
                    img_with[c] += 1
        row = {"particao": part, "imagens": len(its), "grupos": len({i["group"] for i in its})}
        for i, n in enumerate(class_names):
            row[f"inst_{n}"] = inst[i]
            row[f"imgs_{n}"] = img_with[i]
        rows.append(row)
    return rows


# ----------------------------------------------------------------------------
# 3. Treino e avaliação
# ----------------------------------------------------------------------------
def train_one(data_yaml, model_name, seed, epochs, imgsz, batch, patience, project, name, **hyp):
    from ultralytics import YOLO
    model = YOLO(model_name)
    model.train(data=data_yaml, epochs=epochs, imgsz=imgsz, batch=batch, patience=patience,
                seed=seed, deterministic=True, project=project, name=name, exist_ok=True,
                plots=True, verbose=False, **hyp)
    save_dir = Path(model.trainer.save_dir)   # robusto a mudanças de layout entre versões
    return str(save_dir / "weights" / "best.pt"), str(save_dir)


def evaluate(weights, data_yaml, split, imgsz, project, name, conf=0.001, iou=0.6):
    """Avalia em `split` ('val' ou 'test'); retorna métricas globais e por classe."""
    from ultralytics import YOLO
    m = YOLO(weights)
    r = m.val(data=data_yaml, split=split, imgsz=imgsz, conf=conf, iou=iou, plots=True,
              project=project, name=name, exist_ok=True, verbose=False)
    names = r.names
    out = {"global": {}, "per_class": {}, "save_dir": str(r.save_dir)}
    for kind, met in (("box", r.box), ("mask", getattr(r, "seg", None))):
        if met is None:
            continue
        out["global"][kind] = {"P": float(met.mp), "R": float(met.mr),
                               "mAP50": float(met.map50), "mAP50_95": float(met.map)}
        for j, c in enumerate(met.ap_class_index):
            cname = names[int(c)]
            out["per_class"].setdefault(cname, {})[kind] = {
                "P": float(met.p[j]), "R": float(met.r[j]),
                "AP50": float(met.ap50[j]), "AP50_95": float(met.ap[j])}
    cm = getattr(r, "confusion_matrix", None)
    if cm is not None:
        out["confusion_matrix"] = cm.matrix.astype(int).tolist()
        out["confusion_labels"] = [names[i] for i in range(len(names))] + ["background"]
    return out


def _iou_xyxy(a, b):
    x1, y1 = max(a[0], b[0]), max(a[1], b[1])
    x2, y2 = min(a[2], b[2]), min(a[3], b[3])
    inter = max(0, x2 - x1) * max(0, y2 - y1)
    ua = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return inter / ua if ua > 0 else 0.0


def false_negative_audit(weights, data_yaml, class_id, split="test", imgsz=640,
                         thresholds=(0.10, 0.25, 0.40, 0.50), iou_thr=0.5):
    """Para a classe `class_id` (ex.: triatomíneo), conta acertos e falsos
    negativos em diferentes limiares de confiança, e lista imagens com perdas.
    Usa caixas envolventes dos polígonos (suficiente para triagem)."""
    from ultralytics import YOLO
    cfg = yaml.safe_load(Path(data_yaml).read_text())
    img_dir = Path(cfg["path"]) / cfg[split]
    lbl_dir = img_dir.parent / "labels"
    m = YOLO(weights)
    res = {t: {"TP": 0, "FN": 0, "FP": 0, "missed": []} for t in thresholds}
    imgs = sorted(p for p in img_dir.iterdir() if p.suffix.lower() in IMG_EXT)
    for p in imgs:
        gts = []
        lf = lbl_dir / (p.stem + ".txt")
        if lf.exists():
            for line in lf.read_text().splitlines():
                v = line.split()
                if v and int(float(v[0])) == class_id:
                    xy = np.array(v[1:], dtype=float).reshape(-1, 2)
                    if xy.shape[0] == 2 and len(v) == 5:  # caixa xywh
                        cx, cy, w, h = map(float, v[1:5])
                        gts.append([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2])
                    else:
                        gts.append([xy[:, 0].min(), xy[:, 1].min(), xy[:, 0].max(), xy[:, 1].max()])
        pred = m.predict(str(p), imgsz=imgsz, conf=min(thresholds), verbose=False)[0]
        boxes = pred.boxes
        pb = boxes.xyxyn.cpu().numpy() if boxes is not None else np.zeros((0, 4))
        pc = boxes.cls.cpu().numpy().astype(int) if boxes is not None else np.zeros(0, int)
        ps = boxes.conf.cpu().numpy() if boxes is not None else np.zeros(0)
        for t in thresholds:
            cand = [b for b, c, s in zip(pb, pc, ps) if c == class_id and s >= t]
            used = set()
            for g in gts:
                hit = None
                for k, b in enumerate(cand):
                    if k not in used and _iou_xyxy(g, b) >= iou_thr:
                        hit = k
                        break
                if hit is None:
                    res[t]["FN"] += 1
                    res[t]["missed"].append(p.name)
                else:
                    used.add(hit)
                    res[t]["TP"] += 1
            res[t]["FP"] += len(cand) - len(used)
    for t in thresholds:
        tp, fn, fp = res[t]["TP"], res[t]["FN"], res[t]["FP"]
        res[t]["recall"] = tp / (tp + fn) if (tp + fn) else float("nan")
        res[t]["precision"] = tp / (tp + fp) if (tp + fp) else float("nan")
        res[t]["missed"] = sorted(set(res[t]["missed"]))
    return res


# ----------------------------------------------------------------------------
# 4. Estatísticas entre sementes
# ----------------------------------------------------------------------------
_T975 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365,
         8: 2.306, 9: 2.262, 10: 2.228}


def mean_ci(values):
    v = np.array([x for x in values if x is not None and not math.isnan(x)], dtype=float)
    n = len(v)
    if n == 0:
        return {"n": 0}
    mean = float(v.mean())
    sd = float(v.std(ddof=1)) if n > 1 else 0.0
    half = _T975.get(n - 1, 1.96) * sd / math.sqrt(n) if n > 1 else float("nan")
    return {"n": n, "mean": mean, "sd": sd, "ci95_low": mean - half, "ci95_high": mean + half}


def flatten_metrics(ev):
    flat = {}
    for kind, d in ev["global"].items():
        for k, v in d.items():
            flat[f"all/{kind}/{k}"] = v
    for cname, kinds in ev["per_class"].items():
        for kind, d in kinds.items():
            for k, v in d.items():
                flat[f"{cname}/{kind}/{k}"] = v
    return flat


def aggregate(runs):
    keys = sorted({k for r in runs for k in r})
    return {k: mean_ci([r.get(k) for r in runs]) for k in keys}


def environment_info(extra=None):
    info = {"python": platform.python_version(), "platform": platform.platform()}
    try:
        import torch
        import ultralytics
        info.update({"ultralytics": ultralytics.__version__, "torch": torch.__version__,
                     "cuda": torch.version.cuda,
                     "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"})
    except Exception as e:  # pragma: no cover
        info["error"] = str(e)
    if extra:
        info.update(extra)
    return info


def save_json(obj, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(obj, indent=2, ensure_ascii=False, default=str))
