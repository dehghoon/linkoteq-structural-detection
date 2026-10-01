import json
import pathlib

DATASET_ROOT = pathlib.Path("datasets/validated-llm-v0.1")


def _relative_image(project, image_path):
    image = pathlib.PurePosixPath(image_path)
    try:
        return image.relative_to(project).as_posix()
    except ValueError:
        return image.as_posix().lstrip("/")


def resolve_sheet(project, image_path):
    base = DATASET_ROOT / project
    prov_path = base / "provenance.json"
    if not prov_path.is_file():
        raise RuntimeError(f"{project}: missing {prov_path}")
    prov = json.loads(prov_path.read_text())
    rel = _relative_image(project, image_path)

    selected = prov.get("selected_sheets")
    if isinstance(selected, list) and selected:
        matches = [x for x in selected if x.get("image") == rel]
        if len(matches) != 1:
            raise RuntimeError(
                f"{project}: selected_sheets matches={len(matches)} for {rel!r}"
            )
        sheet = matches[0]
        pdf = base / sheet["pdf"]
        if not pdf.is_file():
            raise RuntimeError(f"{project}: missing provenance PDF {pdf}")
        return {
            "pdf": pdf,
            "pdf_page": 1,
            "source_page": sheet.get("source_page"),
            "sheet": sheet.get("sheet"),
            "title": sheet.get("title"),
            "resolver": "selected_sheets",
        }

    image_name = pathlib.PurePosixPath(rel).name
    marker = "_no_titleblock-"
    if marker not in image_name:
        raise RuntimeError(
            f"{project}: legacy provenance has no selected_sheets and image name "
            f"cannot identify split PDF: {image_name!r}"
        )
    stem, suffix = image_name.rsplit(marker, 1)
    page_token = pathlib.PurePosixPath(suffix).stem
    if not page_token.isdigit():
        raise RuntimeError(f"{project}: invalid legacy image page token {page_token!r}")
    pdf_matches = sorted((base / "originals").glob(f"{stem}_original.pdf"))
    if len(pdf_matches) != 1:
        raise RuntimeError(
            f"{project}: legacy split PDF matches={len(pdf_matches)} "
            f"for stem {stem!r}"
        )
    pdf = pdf_matches[0]
    return {
        "pdf": pdf,
        "pdf_page": int(page_token),
        "source_page": None,
        "sheet": stem,
        "title": None,
        "resolver": "legacy-split-pdf",
    }
