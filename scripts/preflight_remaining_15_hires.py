import argparse
import json
import pathlib

from remaining_15_source_resolver import resolve_sheet

TARGETS = {"003","004","010","012","015","016","017","018","020","021","022","024","025","029","030"}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--pack", required=True)
    a = p.parse_args()
    pack = json.loads(pathlib.Path(a.pack).read_text())
    found = {}
    for item in pack.get("items", []):
        qid = str(item.get("item_id") or "")
        num = qid.rsplit("-", 1)[-1]
        if num not in TARGETS:
            continue
        if num in found:
            raise SystemExit(f"duplicate target {num}")
        project = item.get("project_group_id")
        image_path = item.get("image_path")
        if not project or not image_path:
            raise SystemExit(f"{qid}: missing project/image metadata")
        try:
            src = resolve_sheet(project, image_path)
        except RuntimeError as e:
            raise SystemExit(f"{qid}: {e}")
        found[num] = {"item_id": qid, "project": project, **src}
    missing = sorted(TARGETS - set(found))
    if missing or len(found) != 15:
        raise SystemExit(f"preflight failed: resolved={len(found)}/15 missing={missing}")
    for num in sorted(found):
        x = found[num]
        print(f"PASS {num}: {x['project']} -> {x['pdf']} page={x['pdf_page']} via={x['resolver']}")
    print("PREFLIGHT PASS 15/15")


if __name__ == "__main__":
    main()
