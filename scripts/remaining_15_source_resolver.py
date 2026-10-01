import json
import pathlib

DATASET_ROOT = pathlib.Path("datasets/validated-llm-v0.1")


def _relative_image(project, image_path):
    image = pathlib.PurePosixPath(image_path)
    try:
        return image.relative_to(project).as_posix()
    except ValueError:
        return image.as_posix().lstrip("/")


def _finish(project, pdf, source_page=None, sheet=None, title=None, resolver=None, pdf_page=1):
    if not pdf.is_file():
        raise RuntimeError(f"{project}: missing provenance PDF {pdf}")
    return {
        "pdf": pdf,
        "pdf_page": pdf_page,
        "source_page": source_page,
        "sheet": sheet,
        "title": title,
        "resolver": resolver,
    }


def resolve_sheet(project, image_path):
    base = DATASET_ROOT / project
    prov_path = base / "provenance.json"
    if not prov_path.is_file():
        raise RuntimeError(f"{project}: missing {prov_path}")
    prov = json.loads(prov_path.read_text())
    rel = _relative_image(project, image_path)

    selected_sheets = prov.get("selected_sheets")
    if isinstance(selected_sheets, list) and selected_sheets:
        matches = [x for x in selected_sheets if x.get("image") == rel]
        if len(matches) != 1:
            raise RuntimeError(f"{project}: selected_sheets matches={len(matches)} for {rel!r}")
        x = matches[0]
        return _finish(project, base / x["pdf"], x.get("source_page"), x.get("sheet"), x.get("title"), "selected_sheets", 1)

    selected = prov.get("selected")
    if isinstance(selected, list) and selected:
        image_name = pathlib.PurePosixPath(rel).name
        stem_from_image = image_name.split("_no_titleblock", 1)[0]
        matches = [x for x in selected if x.get("name") == stem_from_image]
        if len(matches) != 1:
            raise RuntimeError(f"{project}: selected matches={len(matches)} for {stem_from_image!r}")
        x = matches[0]
        output = x.get("output")
        if not output:
            raise RuntimeError(f"{project}: selected record missing output")
        return _finish(project, base / output, x.get("source_page"), x.get("name"), x.get("name"), "selected-output", 1)

    image_name = pathlib.PurePosixPath(rel).name
    marker = "_no_titleblock-"
    if marker not in image_name:
        raise RuntimeError(f"{project}: no supported provenance mapping for {image_name!r}")
    stem, suffix = image_name.rsplit(marker, 1)
    page_token = pathlib.PurePosixPath(suffix).stem
    if not page_token.isdigit():
        raise RuntimeError(f"{project}: invalid legacy image page token {page_token!r}")
    pdf_matches = sorted((base / "originals").glob(f"{stem}_original.pdf"))
    if len(pdf_matches) != 1:
        raise RuntimeError(f"{project}: legacy split PDF matches={len(pdf_matches)} for stem {stem!r}")
    return _finish(project, pdf_matches[0], None, stem, None, "legacy-split-pdf", int(page_token))
