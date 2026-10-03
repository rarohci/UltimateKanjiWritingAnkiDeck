# SVG to stroke medians

`svg_to_medians.py` converts a folder of SVG stroke centerlines into one
`{"strokes":[...],"medians":[...]}` JSON file per SVG, ready for this deck's
customized `svg_data` field. Requires Python 3.8 or newer; no packages to install.

From the repository folder:

```powershell
python scripts/svg_to_medians.py "C:\path\to\svg-folder" "C:\path\to\json-folder" --recursive
```

The script samples the actual Bézier curves, adding points around bends and
hooks. It retains segment joins, stroke direction, and document stroke order.
It does not correct a source drawing's geometry or stroke order.

For closer sampling (larger JSON files):

```powershell
python scripts/svg_to_medians.py "C:\path\to\svg-folder" "C:\path\to\precise-json" --recursive --spacing 6 --tolerance 0.25
```

- `--spacing`: maximum gap between adjacent points, in output coordinate units
  (default 12). Actual gaps vary so curve subdivision points and joins survive.
- `--tolerance`: adaptive curve flattening tolerance, in output units (default
  0.5). Smaller values add detail. Output is rounded to six decimal places.
- `--coordinates hanzi` (default): fits the SVG `viewBox` into a 1024-unit square,
  centers without stretching, and flips Y to Hanzi Writer coordinates (top 900,
  bottom -124). Applies the same transformation to paths and medians.
- `--coordinates preserve`: retains source coordinates after SVG transforms.
  Use only when the paths already use the coordinate system your renderer needs.
- `--recursive`: includes subfolders and preserves their structure in the output.

## Supported input

Use one **open centerline path per handwriting stroke**, in writing order.
KanjiVG's `StrokePaths` groups are selected automatically; stroke numbers and
definitions are ignored. Generic SVG files use their visible path elements in
document order. Inline `display:none` groups are skipped.

Supports absolute and relative `M L H V C S Q T` commands and nested SVG
`matrix`, `translate`, `scale`, `rotate`, `skewX`, and `skewY` transforms.
Shorthand commands are expanded without changing the intended curves.

Closed paths (`Z`), multiple subpaths, arcs (`A`), nested SVG viewports,
CSS stylesheets/transforms, and non-path drawing elements are rejected. Convert
arcs/shapes to open Bézier stroke paths in an SVG editor first. Inline stroke
styling is not copied: this deck's renderer supplies stroke thickness and color.

**Filled outlines are not centerlines.** This tool does not skeletonize font
outlines, trace bitmaps, or infer pen lifts. Even an unclosed path can describe
an outline; verify that your inputs really are stroke centerlines. The generated
open paths target this deck's custom renderer, not an unmodified outline-based
Hanzi Writer renderer.

## Results and verification

Original SVGs are untouched. Existing output files are never overwritten; use
a new output folder when changing settings. Files that fail produce an error
message while other files continue. Any failure gives the command exit code 1.
If interrupted during a write, a partial output may remain; remove that specific
JSON file or choose a new output folder before retrying.

Paste a generated JSON file's contents into a note's `svg_data` field. Preview
several characters, especially hooks and compound strokes, before updating many
notes. Denser geometry is not a guarantee of better handwriting acceptance;
recognition also depends on the customized writer's matching rules.

Run regression checks from the repository folder:

```powershell
python -m unittest discover -s tests -v
```

Format references: [KanjiVG SVG structure](https://kanjivg.tagaini.net/svg-format.html)
and [Hanzi coordinate conventions](https://github.com/skishore/makemeahanzi#graphics.txt-keys).
