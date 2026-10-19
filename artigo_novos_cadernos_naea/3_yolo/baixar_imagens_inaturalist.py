"""
Baixa fotos com licença aberta e georreferenciadas do iNaturalist para ampliar o banco do YOLO.
Rodar no Google Colab (ou no computador):   python baixar_imagens_inaturalist.py

Por que iNaturalist: cada foto tem autor, licença, data e coordenadas (resolve a crítica de que as
imagens "não têm data nem localização") e o grau "research" significa identificação confirmada pela
comunidade. Usamos apenas licenças que permitem reuso com atribuição (CC0, CC-BY, CC-BY-NC).

Saída: imagens_inat/<grupo>/*.jpg  +  imagens_inat/metadados.csv  (autor, licença, data, lat, lon, URL)
-> O metadados.csv deve ir para o material suplementar / repositório (créditos das imagens).
-> Depois, subir as imagens para o Roboflow e anotar com polígonos (classe "suspected triatomine" ou "açaí").
"""
import csv
import time
from pathlib import Path

import requests

API = "https://api.inaturalist.org/v1"
LICENSES = "cc0,cc-by,cc-by-nc"
OUT = Path("imagens_inat")
HEADERS = {"User-Agent": "acai-yolo-research (contato: inserir e-mail do grupo)"}

GRUPOS = {
    # nome da pasta : (táxon, lugar, máximo de observações)
    "triatomineos_brasil": ("Triatominae", "Brazil", 600),
    "acai_euterpe_oleracea": ("Euterpe oleracea", "Brazil", 600),
    # imagens de "fundo" (sem barbeiro) ajudam a reduzir falsos positivos: insetos parecidos
    "parecidos_reduviidae_brasil": ("Reduviidae", "Brazil", 150),
    "parecidos_coreidae_brasil": ("Coreidae", "Brazil", 150),
}


def get(url, **params):
    for tentativa in range(5):
        r = requests.get(url, params=params, headers=HEADERS, timeout=60)
        if r.status_code == 429:       # limite de requisições: espera e tenta de novo
            time.sleep(10 * (tentativa + 1)); continue
        r.raise_for_status()
        time.sleep(1.0)                # respeita o limite de ~1 requisição/s da API
        return r.json()
    raise RuntimeError("API indisponível")


def taxon_id(nome):
    res = get(f"{API}/taxa", q=nome, per_page=30, is_active="true")["results"]
    exato = [t for t in res if t["name"].lower() == nome.lower()]
    if not exato:   # nunca cair num táxon "parecido" (ex.: Reduviidae no lugar de Triatominae)
        raise SystemExit(f"Táxon '{nome}' não encontrado com nome exato: confira a grafia.")
    t = exato[0]
    print(f"  usando táxon {t['name']} ({t['rank']}, id {t['id']})")
    return t["id"]


def place_id(nome):
    res = get(f"{API}/places/autocomplete", q=nome)["results"]
    return res[0]["id"]


def main():
    OUT.mkdir(exist_ok=True)
    meta_path = OUT / "metadados.csv"
    novo = not meta_path.exists()
    with open(meta_path, "a", newline="", encoding="utf-8") as fmeta:
        w = csv.writer(fmeta)
        if novo:
            w.writerow(["arquivo", "grupo", "observacao_id", "especie", "data", "lat", "lon",
                        "licenca", "autor", "atribuicao", "url_observacao", "url_foto"])
        for pasta, (taxon, lugar, maximo) in GRUPOS.items():
            tid, pid = taxon_id(taxon), place_id(lugar)
            (OUT / pasta).mkdir(exist_ok=True)
            n, page = 0, 1
            while n < maximo:
                data = get(f"{API}/observations", taxon_id=tid, place_id=pid, quality_grade="research",
                           photos="true", photo_license=LICENSES, per_page=100, page=page,
                           order_by="observed_on")
                if not data["results"]:
                    break
                for obs in data["results"]:
                    # 1 foto por observação: evita várias fotos do mesmo inseto (o que causaria vazamento entre treino e teste)
                    foto = next((p for p in obs.get("photos", []) if p.get("license_code") in LICENSES.split(",")), None)
                    if not foto:
                        continue
                    url = foto["url"].replace("square", "large")
                    nome = f"inat_{obs['id']}_{foto['id']}.jpg"
                    destino = OUT / pasta / nome
                    if not destino.exists():
                        try:
                            img = requests.get(url, headers=HEADERS, timeout=60); img.raise_for_status()
                            destino.write_bytes(img.content); time.sleep(0.5)
                        except Exception as e:
                            print("falhou", url, e); continue
                    # confere se a observação pertence mesmo ao táxon pedido (ancestry contém o id)
                    if tid not in ((obs.get("taxon") or {}).get("ancestor_ids") or []) and (obs.get("taxon") or {}).get("id") != tid:
                        continue
                    lat, lon = (obs.get("location") or ",").split(",")
                    w.writerow([f"{pasta}/{nome}", pasta, obs["id"], (obs.get("taxon") or {}).get("name"),
                                obs.get("observed_on"), lat, lon, foto.get("license_code"),
                                (obs.get("user") or {}).get("login"), foto.get("attribution"),
                                obs.get("uri"), url])
                    n += 1
                    if n >= maximo:
                        break
                page += 1
            print(f"{pasta}: {n} imagens")


if __name__ == "__main__":
    main()
