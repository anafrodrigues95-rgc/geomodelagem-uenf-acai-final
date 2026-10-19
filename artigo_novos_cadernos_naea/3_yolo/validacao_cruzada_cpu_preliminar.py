import sys, json, time, random
sys.path.insert(0,'/home/claude/yolo')
import acai_yolo_pipeline as P
from pathlib import Path
from sklearn.model_selection import StratifiedGroupKFold
MODEL=sys.argv[1] if len(sys.argv)>1 else "yolo11s-seg.pt"
EPOCHS=int(sys.argv[2]) if len(sys.argv)>2 else 150
FOLDS=[int(x) for x in sys.argv[3].split(',')] if len(sys.argv)>3 else [0,1,2,3,4]
IMGSZ=int(sys.argv[4]) if len(sys.argv)>4 else 416; NAMES=["acai","suspected_triatomine"]
items=P.dedupe_augmented(P.collect_items(["/home/claude/data/v2-barbeiro-e-acai"],["v2"]))
synth=[it for it in items if 'gemini' in it['group']]
real=[it for it in items if 'gemini' not in it['group']]
strat=[ (0 in it['classes'])*1 + (1 in it['classes'])*2 for it in real]
cv=StratifiedGroupKFold(n_splits=5,shuffle=True,random_state=42)
splits=list(cv.split(real,strat,[it['group'] for it in real]))
out=Path("results"); out.mkdir(exist_ok=True)
HYP=dict(fliplr=0.5,degrees=15,hsv_v=0.15,mosaic=1.0,mixup=0.0,close_mosaic=10,cos_lr=True,workers=2,device="cpu")
for k in FOLDS:
    tr,te=splits[k]
    tr_items=[real[i] for i in tr]
    inner=P.group_split(tr_items,(0.85,0.15,0.0),seed=k)
    sp={"train":inner["train"]+synth,"val":inner["val"],"test":[real[i] for i in te]}
    P.check_no_leakage(sp)
    y=P.materialize(sp,f"/home/claude/cv/ds_fold{k}",NAMES)
    summ=P.split_summary(sp,NAMES)
    t0=time.time()
    best,tdir=P.train_one(y,MODEL,k,EPOCHS,IMGSZ,8,25,"/home/claude/cv/runs",f"fold{k}",**HYP)
    ev=P.evaluate(best,y,"test",IMGSZ,"/home/claude/cv/runs",f"fold{k}_test")
    fn=P.false_negative_audit(best,y,1,"test",IMGSZ)
    import pandas as pd
    df=pd.read_csv(Path(tdir)/"results.csv"); df.columns=df.columns.str.strip()
    rec={"fold":k,"seed":k,"model":MODEL,"split":summ,"epochs_run":int(df.epoch.max()),
         "best_epoch":int(df.loc[(0.1*df["metrics/mAP50(M)"]+0.9*df["metrics/mAP50-95(M)"]+0.1*df["metrics/mAP50(B)"]+0.9*df["metrics/mAP50-95(B)"]).idxmax(),"epoch"]),
         "train_dir":tdir,"test":ev,"fn":{str(t):v for t,v in fn.items()},"minutes":(time.time()-t0)/60,
         "test_images":[Path(i['img']).name for i in sp['test']]}
    P.save_json(rec,out/f"fold{k}.json"); print("FOLD",k,"done",rec["minutes"],ev["global"],flush=True)
P.save_json(P.environment_info({"model":MODEL,"epochs":EPOCHS,"patience":25,"imgsz":IMGSZ,"batch":8,"hyp":HYP,"cv":"StratifiedGroupKFold(5, random_state=42); Gemini images train-only"}),out/"env.json")
