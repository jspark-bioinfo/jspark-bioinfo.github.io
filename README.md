# jspark-bioinfo.github.io

Personal academic homepage of Jaesub Park. Live at https://jspark-bioinfo.github.io

Everything is generated from **`data/cv.yaml`**:

| Output | Source |
|---|---|
| `index.html` (homepage) | `templates/index.html.j2` |
| `cv/Jaesub_Park_CV.pdf` (full CV) | `templates/cv.typ.j2`  |

## Update

1. Edit `data/cv.yaml`.
2. `pip install pyyaml jinja2 typst && python build.py`
3. Commit and push. GitHub Pages serves the repository root.
