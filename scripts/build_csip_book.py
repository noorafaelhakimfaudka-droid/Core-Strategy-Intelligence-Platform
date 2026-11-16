"""Compile docs/BUKU_INDUK_CSIP_LENGKAP.tex into docs/BUKU_INDUK_CSIP_LENGKAP.pdf via LaTeX (Tectonic)."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path

import pymupdf

REPO_ROOT = Path(__file__).resolve().parent.parent
TEX_PATH = REPO_ROOT / "docs" / "BUKU_INDUK_CSIP_LENGKAP.tex"
PDF_PATH = REPO_ROOT / "docs" / "BUKU_INDUK_CSIP_LENGKAP.pdf"
MIN_PAGES = 50

FORBIDDEN_RENDER_ARTIFACTS = [
    r"\begin",
    r"\end",
    r"\frac",
    r"\hat",
    "≤ft",
    "∈fty",
    r"\right",
    r"\$",
    "_{",
    "^{",
    r"\_",
    r"\&",
]


def find_latex_compiler() -> tuple[str, str]:
    """Locate Tectonic, XeLaTeX, or PDFLaTeX on the current machine."""
    tectonic_bin = shutil.which("tectonic")
    if tectonic_bin:
        return ("tectonic", tectonic_bin)

    local_appdata = os.environ.get("LOCALAPPDATA")
    if local_appdata:
        win_tectonic = Path(local_appdata) / "Programs" / "tectonic" / "tectonic.exe"
        if win_tectonic.exists():
            return ("tectonic", str(win_tectonic))

    for fallback in ("xelatex", "pdflatex"):
        found = shutil.which(fallback)
        if found:
            return (fallback, found)

    raise RuntimeError(
        "LaTeX compiler not found. Install Tectonic (recommended), XeLaTeX, or PDFLaTeX and ensure it is on PATH."
    )


def compile_latex(tex_path: Path, pdf_path: Path) -> None:
    """Invoke the LaTeX compiler to build the output PDF cleanly."""
    if not tex_path.exists():
        raise FileNotFoundError(f"LaTeX source file missing: {tex_path}")

    engine_name, engine_bin = find_latex_compiler()
    out_dir = pdf_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Compiling {tex_path.name} -> {pdf_path.name} using {engine_name} ({engine_bin})...")
    if engine_name == "tectonic":
        cmd = [engine_bin, "--outdir", str(out_dir), str(tex_path)]
        res = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True, encoding="utf-8", errors="replace")
        if res.returncode != 0:
            raise RuntimeError(f"Tectonic compilation failed:\n{res.stdout}\n{res.stderr}")
    else:
        cmd = [engine_bin, "-interaction=nonstopmode", "-output-directory", str(out_dir), str(tex_path)]
        for _pass in range(2):
            res = subprocess.run(cmd, cwd=str(out_dir), capture_output=True, text=True, encoding="utf-8", errors="replace")
            if res.returncode != 0:
                raise RuntimeError(f"{engine_name} compilation failed:\n{res.stdout[-3000:]}\n{res.stderr}")

    if not pdf_path.exists():
        raise RuntimeError(f"Expected output PDF was not created: {pdf_path}")


def audit_pdf_quality(pdf_path: Path) -> int:
    """Verify minimum page count, non-blank pages, resolved references, and zero raw TeX artifacts."""
    doc = pymupdf.open(str(pdf_path))
    try:
        total_pages = doc.page_count
        blank_pages: list[tuple[int, int]] = []
        unresolved_refs: list[tuple[int, str]] = []
        symbol_issues: list[tuple[int, str, str]] = []

        for idx, page in enumerate(doc, start=1):
            raw_text = page.get_text("text")
            body_lines = [
                ln.strip()
                for ln in raw_text.splitlines()
                if ln.strip()
                and "Buku Induk Proyek & Skrip Presentasi Master" not in ln
                and "Core Strategy & Intelligence Platform" not in ln
                and not re.fullmatch(r"Halaman\s+[ivxlcdm\d]+", ln.strip(), flags=re.IGNORECASE)
            ]
            body_text = "\n".join(body_lines)

            if len(body_text) < 15:
                blank_pages.append((idx, len(body_text)))

            if re.search(r"(?<![?])\?\?(?![?])", body_text):
                pos = body_text.find("??")
                unresolved_refs.append((idx, body_text[max(0, pos - 20) : pos + 30].replace("\n", " ")))

            for token in FORBIDDEN_RENDER_ARTIFACTS:
                if token in body_text:
                    pos = body_text.find(token)
                    snippet = body_text[max(0, pos - 20) : pos + 35].replace("\n", " ")
                    symbol_issues.append((idx, token, snippet))

        # Verify zero bounding-box overlaps across all pages
        overlaps: list[tuple[int, str, str]] = []
        for pno, page in enumerate(doc, start=1):
            spans = []
            for blk in page.get_text("dict").get("blocks", []):
                if blk.get("type") != 0:
                    continue
                for ln in blk.get("lines", []):
                    for sp in ln.get("spans", []):
                        txt = sp.get("text", "").strip()
                        if txt:
                            x0, y0, x1, y1 = sp["bbox"]
                            spans.append((y0, y1, x0, x1, txt))
            spans.sort()
            for i, (y0a, y1a, x0a, x1a, ta) in enumerate(spans):
                for j in range(i + 1, len(spans)):
                    y0b, y1b, x0b, x1b, tb = spans[j]
                    if y0b >= y1a - 2.0:
                        break
                    if (min(x1a, x1b) - max(x0a, x0b)) > 3.0 and (min(y1a, y1b) - max(y0a, y0b)) > 3.0:
                        overlaps.append((pno, ta[:30], tb[:30]))

        print(
            f"PDF Quality Audit: {total_pages} pages | "
            f"{len(blank_pages)} blank pages | "
            f"{len(unresolved_refs)} unresolved refs | "
            f"{len(overlaps)} text overlaps | "
            f"{len(symbol_issues)} broken symbol artifacts"
        )
        if total_pages < MIN_PAGES:
            raise RuntimeError(f"Book has {total_pages} pages, below required minimum {MIN_PAGES} pages.")
        if blank_pages:
            raise RuntimeError(f"Detected blank pages: {blank_pages}")
        if unresolved_refs:
            raise RuntimeError(f"Detected unresolved LaTeX ?? references: {unresolved_refs[:5]}")
        if overlaps:
            raise RuntimeError(f"Detected colliding/overlapping text spans: {overlaps[:5]}")
        if symbol_issues:
            raise RuntimeError(f"Detected raw LaTeX rendering artifacts: {symbol_issues[:5]}")
        return total_pages
    finally:
        doc.close()


def build_pdf() -> int:
    """Compile LaTeX source into PDF and audit output quality."""
    compile_latex(TEX_PATH, PDF_PATH)
    total_pages = audit_pdf_quality(PDF_PATH)
    print(f"Generated LaTeX PDF: {PDF_PATH} ({total_pages} pages, {PDF_PATH.stat().st_size:,} bytes)")
    return total_pages


if __name__ == "__main__":
    build_pdf()
