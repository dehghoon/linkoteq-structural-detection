#!/usr/bin/env python3
import argparse, json
from pathlib import Path
from PIL import Image, ImageDraw
from ultralytics import YOLO

ap = argparse.ArgumentParser()
ap.add_argument("--model", required=True)
args = ap.parse_args()
root = Path("runs/36530901509/review-batches/remaining-29/work")
manifest = json.loads((root / "manifest.json").read_text())
model = YOLO(args.model)
names = {int(k): str(v).lower() for k, v in model.names.items()}
expected = {0: "column", 1: "beam", 2: "wall"}
if names != expected:
    raise SystemExit(f"model class map must be exactly {expected}; got {names}")

cand_dir, overlay_dir = root / "candidates", root / "overlays"
cand_dir.mkdir(exist_ok=True); overlay_dir.mkdir(exist_ok=True)
for it in manifest["items"]:
    image_path = Path(it["materialized_image"])
    img = Image.open(image_path).convert("RGB")
    w, h = img.size
    result = model(source=str(image_path), verbose=False)[0]
    anns = []
    for box, conf, cls in zip(result.boxes.xyxy.cpu().tolist(), result.boxes.conf.cpu().tolist(), result.boxes.cls.cpu().tolist()):
        x1,y1,x2,y2 = map(float, box); c = int(cls)
        if c not in expected or not (0 <= x1 < x2 <= w and 0 <= y1 < y2 <= h):
            continue
        anns.append({
            "class": expected[c], "confidence": float(conf),
            "bbox_xyxy": [x1,y1,x2,y2], "coordinate_space": "source-page",
            "review_state": "candidate-pending-human-qa"
        })
    payload = {
        "item_id": it["item_id"], "source_path": it["source_path"],
        "source_sha256": it["source_sha256"], "coordinate_space": "source-page",
        "model_name": Path(args.model).name, "review_state": "candidate-pending-human-qa",
        "training_enabled": False, "candidates": anns
    }
    (cand_dir / f"{it['item_id']}.json").write_text(json.dumps(payload, indent=2) + "\n")
    draw = ImageDraw.Draw(img)
    for a in anns:
        x1,y1,x2,y2 = a["bbox_xyxy"]
        draw.rectangle((x1,y1,x2,y2), outline="red", width=2)
        draw.text((x1,max(0,y1-12)), f"{a['class']} {a['confidence']:.2f}", fill="red")
    img.save(overlay_dir / f"{it['item_id']}.jpg", quality=90)
