import argparse
import json
import pathlib

TARGETS = {"003","004","010","012","015","016","017","018","020","021","022","024","025","029","030"}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--pack",required=True)
    a=p.parse_args()
    pack=json.loads(pathlib.Path(a.pack).read_text())
    found={}
    for it in pack.get("items",[]):
        qid=str(it.get("item_id") or "")
        num=qid.rsplit("-",1)[-1]
        if num not in TARGETS: continue
        if num in found: raise SystemExit(f"duplicate target {num}")
        project=it.get("project_group_id"); image_path=it.get("image_path")
        if not project or not image_path: raise SystemExit(f"{qid}: missing project/image metadata")
        base=pathlib.Path("datasets/validated-llm-v0.1")/project
        provpath=base/"provenance.json"
        if not provpath.is_file(): raise SystemExit(f"{qid}: missing {provpath}")
        prov=json.loads(provpath.read_text())
        img=pathlib.PurePosixPath(image_path)
        try: rel=img.relative_to(project).as_posix()
        except ValueError: rel=img.as_posix()
        matches=[s for s in prov.get("selected_sheets",[]) if s.get("image")==rel]
        if len(matches)!=1: raise SystemExit(f"{qid}: provenance matches={len(matches)} for {rel!r}")
        s=matches[0]; pdf=base/s["pdf"]
        if not pdf.is_file(): raise SystemExit(f"{qid}: missing PDF {pdf}")
        found[num]={"item_id":qid,"project":project,"image":rel,"pdf":str(pdf),"source_page":s.get("source_page"),"sheet":a.str(s.get("sheet"))} if False els`{"item_id":qid,"project":project,"image":rel,"pdf":str(pdf),"source_page":s.get("source_page"),"sheet":s.get("sheet")}`
    missing=sorted(TARGETS-set(found))
    if missing or len(found)!=15: raise SystemExit(f"preflight failed: resolved={len(found)}/15 missing={missing}")
    for n in sorted(found): print(f"PASS {n}: {found[n]['project']} -> {found[n]['pdf']}")
    print("PREFLIGHT PASS 15/15")

if __name__=="__main__": main()
