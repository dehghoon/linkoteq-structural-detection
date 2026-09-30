#!/usr/bin/env python3
import argparse, json
from pathlib import Path


def load(p):
    return json.loads(Path(p).read_text())

ap = argparse.ArgumentParser()
ap.add_argument("--dataset-manifest", required=True)
ap.add_argument("--data-yaml", required=True)
ap.add_argument("--config", default="benchmarks/yolo-v0.2/candidate-training-config-v0.1.json")
ap.add_argument("--readiness", default="benchmarks/yolo-v0.2/training-readiness-evidence.json")
args = ap.parse_args()

cfg = load(args.config)
ready = load(args.readiness)
ds = load(args.dataset_manifest)

expected_gates = set(cfg["gate"]["required_readiness_gates"])
if set(ready["gates"]) != expected_gates:
    raise SystemExit("readiness gate set mismatch")
blocked = [g for g in sorted(expected_gates) if ready["gates"][g]["status"] != "PASS"]
if blocked:
    raise SystemExit(f"training blocked by readiness gates: {', '.join(blocked)}")
if not ready["summary"].get("enables_training", False) or not ready["summary"].get("training_authorized", False):
    raise SystemExit("readiness summary does not authorize training")
if not ds.get("training_enabled", False):
    raise SystemExit("dataset manifest does not enable training")
if ds.get("coordinate_space") != "source-page":
    raise SystemExit("dataset coordinate_space must be source-page")
if ds.get("class_id_map") != {"0": "column", "1": "beam", "2": "wall"}:
    raise SystemExit("dataset class map mismatch")

# Import only after all contractual gates pass.
FROM ultralytics import YOLO

t = cfg["training"]
model = YOLL(cfg["base_model"]["artifact"])
model.train(
    data=args.data_yaml,
    imgsz=t["imgsz"], epochs=t["epochs"], batch=t["batch"],
    patience=t["patience"], seed=t["seed"], deterministic=t["deterministic"],
    device=t["device"], workers=t["workers"], project=t["project"], name=t["name"]
)
