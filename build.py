#!/usr/bin/env python3
"""Build the homepage and CV PDFs from data/cv.yaml.

    pip install pyyaml jinja2 typst
    python build.py            # writes index.html and cv/Jaesub_Park_CV.pdf in the repo root
"""
import datetime as dt
import re
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader
from markupsafe import Markup, escape

ROOT = Path(__file__).resolve().parent
DATA = yaml.safe_load((ROOT / "data" / "cv.yaml").read_text(encoding="utf-8"))
ME = DATA["me"]
TODAY = dt.date.today()


# ---------- helpers shared by both outputs ----------
def split_me(authors: str):
    """Split an author string around the first occurrence of ME (incl. a trailing '*')."""
    m = re.search(re.escape(ME) + r"\*?", authors)
    if not m:
        return authors, None, ""
    return authors[: m.start()], m.group(0), authors[m.end():]


# ---------- HTML ----------
def html_authors(a):
    pre, me, post = split_me(a)
    if me is None:
        return escape(a)
    return Markup(f"{escape(pre)}<strong class=\"me\">{escape(me)}</strong>{escape(post)}")


# ---------- Typst ----------
_TYP_SPECIAL = re.compile(r"([\\#$*_@<>`\[\]~=/-])")


def typ(s) -> str:
    """Escape a plain string for Typst markup."""
    s = str(s)
    return _TYP_SPECIAL.sub(lambda m: "\\" + m.group(1), s)


def typ_authors(a):
    pre, me, post = split_me(a)
    if me is None:
        return typ(a)
    return f"{typ(pre)}#strong[{typ(me)}]{typ(post)}"


def make_env(autoescape):
    env = Environment(
        loader=FileSystemLoader(ROOT / "templates"),
        autoescape=autoescape,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["authors"] = html_authors if autoescape else typ_authors
    env.filters["t"] = typ
    env.tests["first_author"] = lambda p: p["authors"].startswith(ME) and not p.get("cofirst")
    return env


def main():
    n_first = sum(1 for p in DATA["publications"]["journal"] if p.get("cofirst") or p["authors"].startswith(ME))
    ctx = dict(cv=DATA, updated=TODAY.strftime("%-d %B %Y"), year=TODAY.year, n_first=n_first)

    # Homepage
    html = make_env(True).get_template("index.html.j2").render(**ctx)
    (ROOT / "index.html").write_text(html, encoding="utf-8")
    print("wrote index.html")

    # CV PDF
    import typst

    out = ROOT / "cv"
    out.mkdir(exist_ok=True)
    env = make_env(False)
    variants = {"Jaesub_Park_CV.pdf": dict(variant="full")}
    for fname, extra in variants.items():
        src = env.get_template("cv.typ.j2").render(**ctx, **extra)
        tmp = out / (fname.replace(".pdf", ".typ"))
        tmp.write_text(src, encoding="utf-8")
        typst.compile(str(tmp), output=str(out / fname), font_paths=[str(ROOT / "fonts")])
        tmp.unlink()
        print("wrote cv/" + fname)


if __name__ == "__main__":
    main()
