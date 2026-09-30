import argparse
import json
import pathlib


CLASS_TO_ID = {"column": 0, "beam": 1, "wall": 2}


def yolo_line(class_name, box, width, height):
    xmin, ymin, xmax, ymax = [float(box[k]) for k in ("x_min", "y_min", "x_max", "y_max")]
    if not (0 <= xmin < xmax <= width and 0 <= ymin < ymax <= height):
        raise ValueError(f"Invalid source-page box: {box}")
    xc = ((xmin + xmax) / 2.0) / width
    yc = ((ymin + ymax) / 2.0) / height
    bw = (xmax - xmin) / width
    bh = (ymax - ymin) / height
    return f"{CLASS_TO_ID[class_name]} {xc:.8f} {yc:.8f} {bw:.8f} {bh:.8f}"


def export(payload, out_path):
    if payload.get("coordinate_space") != "source-page":
        raise ValueError("coordinate_space must be source-page")
    if payload.get("review_state") != "human-approved":
        raise ValueError("review_state must be human-approved")
    width = int(payload["image"]["width"])
    height = int(payload["image"]["height"])
    annotations = payload.get("annotations",  [])
    if not annotations:
        raise ValueError("No human-approved bbox annotations to export")
    lines = []
    for ann in annotations:
        cls = ann["class"]
        if cls not in CLASS_TO_ID:
            raise ValueError(f"Unapproved class: {cls}")
        if ann.get("review_state") != "human-approved":
            raise ValueError("Every annotation must be human-approved")
        lines.append(yolo_line(cls, ann["bbox"], width, height))
    out = pathlib.Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("input")
    p.add_argument("output")
    a = p.parse_args()
    with open(a.input, encoding="utf-8") as f:
        payload = json.load(f)
    export(payload, a.output)


if __name__ == "__main__":
    main()
