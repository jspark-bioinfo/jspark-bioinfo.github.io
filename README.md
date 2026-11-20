# jspark-bioinfo.github.io

Personal academic homepage of Jaesub Park. Live at https://jspark-bioinfo.github.io

Everything is generated from **`data/cv.yaml`**:

| Output | Source |
|---|---|
| `index.html` (homepage) | `templates/index.html.j2` |
| `cv/Jaesub_Park_CV.pdf` (full CV) | `templates/cv.typ.j2` (variant `full`) |
| `cv/Jaesub_Park_CV_short.pdf` (2-page) | `templates/cv.typ.j2` (variant `short`) |
| `cv/Jaesub_Park_Publications.pdf` | `templates/cv.typ.j2` (variant `pubs`) |

## Update

1. Edit `data/cv.yaml`.
2. `pip install pyyaml jinja2 typst && python build.py`
3. Commit and push. GitHub Pages serves the repository root.

Publications marked `selected: true` appear in the 2-page CV.
