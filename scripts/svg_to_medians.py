#!/usr/bin/env python3
"""Convert open, ordered SVG stroke paths to this deck's strokes/medians JSON.

Standard library only. This samples existing centerlines; it does not extract
centerlines from filled outlines or infer stroke order from a character image.
"""

import argparse
import json
import math
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET


NUMBER = r"[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:[eE][-+]?\d+)?"
TOKEN = re.compile(r"[A-Za-z]|" + NUMBER)
IDENTITY = (1, 0, 0, 1, 0, 0)


def numbers(value):
    if re.sub(NUMBER, "", value).strip(" ,\t\r\n"):
        raise ValueError("Invalid numeric list: " + value)
    result = [float(n) for n in re.findall(NUMBER, value)]
    if not all(math.isfinite(n) for n in result):
        raise ValueError("Coordinates must be finite")
    return result


def multiply(a, b):
    """Compose affine matrices: apply b, then a."""
    return (
        a[0]*b[0] + a[2]*b[1], a[1]*b[0] + a[3]*b[1],
        a[0]*b[2] + a[2]*b[3], a[1]*b[2] + a[3]*b[3],
        a[0]*b[4] + a[2]*b[5] + a[4],
        a[1]*b[4] + a[3]*b[5] + a[5],
    )


def transform(value):
    matrix = IDENTITY
    pattern = r"([A-Za-z]+)\s*\(([^)]*)\)"
    if re.sub(pattern, "", value).strip(" ,\t\r\n"):
        raise ValueError("Invalid SVG transform: " + value)
    for name, args in re.findall(pattern, value):
        v = numbers(args)
        if name == "matrix" and len(v) == 6:
            part = tuple(v)
        elif name == "translate" and len(v) in (1, 2):
            part = (1, 0, 0, 1, v[0], v[1] if len(v) == 2 else 0)
        elif name == "scale" and len(v) in (1, 2):
            part = (v[0], 0, 0, v[-1], 0, 0)
        elif name == "rotate" and len(v) in (1, 3):
            angle = math.radians(v[0])
            c, s = math.cos(angle), math.sin(angle)
            part = (c, s, -s, c, 0, 0)
            if len(v) == 3:
                x, y = v[1:]
                part = multiply(multiply((1, 0, 0, 1, x, y), part),
                                (1, 0, 0, 1, -x, -y))
        elif name in ("skewX", "skewY") and len(v) == 1:
            skew = math.tan(math.radians(v[0]))
            part = (1, 0, skew, 1, 0, 0) if name == "skewX" else (1, skew, 0, 1, 0, 0)
        else:
            raise ValueError("Unsupported SVG transform: " + name)
        matrix = multiply(matrix, part)
    return matrix


def apply(matrix, point):
    x, y = point
    a, b, c, d, e, f = matrix
    result = (a*x + c*y + e, b*x + d*y + f)
    if not all(math.isfinite(v) for v in result):
        raise ValueError("Non-finite transformed coordinate")
    return result


def parse_path(data):
    """Expand relative/shorthand commands into absolute M, L and C commands."""
    if TOKEN.sub("", data).strip(" ,\t\r\n"):
        raise ValueError("Invalid path data")
    tokens = TOKEN.findall(data)
    index, command = 0, None
    point = (0, 0)
    cubic_control = quadratic_control = None
    output = []
    sizes = {"M": 2, "L": 2, "H": 1, "V": 1, "C": 6, "S": 4, "Q": 4, "T": 2}
    while index < len(tokens):
        if tokens[index].isalpha():
            command = tokens[index]
            index += 1
        if command is None:
            raise ValueError("Path must start with M")
        kind = command.upper()
        if kind not in sizes:
            raise ValueError("Unsupported path command " + command +
                             " (use open centerlines; convert arcs to Bezier curves)")
        count = sizes[kind]
        values = tokens[index:index + count]
        if len(values) != count or any(v.isalpha() for v in values):
            raise ValueError("Incomplete path command " + command)
        v = [float(n) for n in values]
        if not all(math.isfinite(n) for n in v):
            raise ValueError("Coordinates must be finite")
        index += count
        relative = command.islower()

        def xy(offset):
            return (v[offset] + (point[0] if relative else 0),
                    v[offset+1] + (point[1] if relative else 0))

        if not output and kind != "M":
            raise ValueError("Path must start with M")
        next_cubic = next_quadratic = None
        if kind == "M":
            if output:
                raise ValueError("Multiple subpaths: provide one open path per stroke")
            end = xy(0)
            output.append(("M", [end]))
            command = "l" if relative else "L"
        elif kind in ("L", "H", "V"):
            if kind == "H":
                end = (v[0] + (point[0] if relative else 0), point[1])
            elif kind == "V":
                end = (point[0], v[0] + (point[1] if relative else 0))
            else:
                end = xy(0)
            output.append(("L", [end]))
        else:
            if kind in ("C", "S"):
                first = xy(0) if kind == "C" else (
                    tuple(2*p-c for p, c in zip(point, cubic_control))
                    if cubic_control is not None else point)
                second, end = (xy(2), xy(4)) if kind == "C" else (xy(0), xy(2))
                next_cubic = second
            else:
                control = xy(0) if kind == "Q" else (
                    tuple(2*p-c for p, c in zip(point, quadratic_control))
                    if quadratic_control is not None else point)
                end = xy(2) if kind == "Q" else xy(0)
                first = tuple(p + 2*(c-p)/3 for p, c in zip(point, control))
                second = tuple(p + 2*(c-p)/3 for p, c in zip(end, control))
                next_quadratic = control
            output.append(("C", [first, second, end]))
        point = end
        cubic_control, quadratic_control = next_cubic, next_quadratic
    if len(output) < 2:
        raise ValueError("Stroke has no drawable segments")
    return output


def midpoint(a, b):
    return tuple((x+y)/2 for x, y in zip(a, b))


def flatten(points, tolerance, depth=0):
    """Subdivide until the control polygon stays close to its endpoint chord.

    Also check excess length so collinear reversals and tiny loops are retained.
    All measurements happen AFTER transforming to the output coordinate system.
    """
    a, b, c, d = points
    chord = math.dist(a, d)
    polygon = sum(math.dist(p, q) for p, q in zip(points, points[1:]))
    distance = max(abs((d[0]-a[0])*(p[1]-a[1]) - (d[1]-a[1])*(p[0]-a[0])) / chord
                   for p in (b, c)) if chord else polygon
    if distance <= tolerance and polygon - chord <= tolerance:
        return [d]
    if depth >= 24:
        raise ValueError("Curve exceeds subdivision limit; increase --tolerance")
    ab, bc, cd = midpoint(a, b), midpoint(b, c), midpoint(c, d)
    abc, bcd = midpoint(ab, bc), midpoint(bc, cd)
    middle = midpoint(abc, bcd)
    return (flatten((a, ab, abc, middle), tolerance, depth+1) +
            flatten((middle, bcd, cd, d), tolerance, depth+1))


def stroke_data(data, matrix, spacing, tolerance):
    commands = [(kind, [apply(matrix, p) for p in points])
                for kind, points in parse_path(data)]
    polyline = [commands[0][1][0]]
    for kind, points in commands[1:]:
        polyline.extend(points if kind == "L" else flatten((polyline[-1], *points), tolerance))
    # Preserve adaptive vertices and segment joins; subdivide long straight gaps.
    median = [list(polyline[0])]
    for start, end in zip(polyline, polyline[1:]):
        steps = max(1, math.ceil(math.dist(start, end) / spacing))
        if steps + len(median) > 100000:
            raise ValueError("Too many points; increase --spacing or check SVG coordinates")
        for step in range(1, steps+1):
            point = [round(a + (b-a)*step/steps, 6) for a, b in zip(start, end)]
            if point != median[-1]:
                median.append(point)
    median[0] = [round(v, 6) for v in median[0]]
    if len(median) < 2 or not any(math.dist(median[0], p) > 0 for p in median[1:]):
        raise ValueError("Zero-length stroke")
    path = " ".join(kind + " " + " ".join(f"{x:.6f},{y:.6f}" for x, y in points)
                    for kind, points in commands)
    return path, median


def convert(source, coordinates="hanzi", spacing=12, tolerance=0.5):
    root = ET.parse(source).getroot()
    if root.tag.split("}")[-1] != "svg":
        raise ValueError("Root element must be svg")
    matrix = IDENTITY
    if coordinates == "hanzi":
        box = numbers(root.get("viewBox", ""))
        if len(box) != 4 or box[2] <= 0 or box[3] <= 0:
            raise ValueError("A positive viewBox is required (or use --coordinates preserve)")
        x, y, width, height = box
        scale = 1024 / max(width, height)
        # Fit without stretching; Hanzi Writer uses y-up coordinates, top = 900.
        matrix = (scale, 0, 0, -scale,
                  (1024-width*scale)/2 - x*scale,
                  900 - (1024-height*scale)/2 + y*scale)
    groups = [node for node in root.iter() if "StrokePaths" in node.get("id", "")]
    allowed = {id(node) for group in groups for node in group.iter()} if groups else None
    strokes, medians = [], []

    def visit(node, parent_matrix):
        tag = node.tag.split("}")[-1]
        if tag in {"defs", "clipPath", "mask", "metadata", "title", "desc", "text"}:
            return
        if "StrokeNumbers" in node.get("id", ""):
            return
        style = dict(item.split(":", 1) for item in node.get("style", "").split(";") if ":" in item)
        style = {k.strip(): v.strip() for k, v in style.items()}
        if style.get("display", node.get("display")) == "none":
            return
        if tag == "style" or "transform" in style:
            raise ValueError("CSS stylesheets/transforms are unsupported; use SVG transform attributes")
        local = multiply(parent_matrix, transform(node.get("transform", "")))
        selected = allowed is None or id(node) in allowed
        if tag == "svg" and node is not root:
            raise ValueError("Nested SVG viewports are unsupported")
        if selected and tag in {"use", "line", "polyline", "polygon", "rect", "circle", "ellipse", "image"}:
            raise ValueError("Convert " + tag + " elements to open stroke paths first")
        if tag == "path" and selected:
            try:
                path, median = stroke_data(node.get("d", ""), local, spacing, tolerance)
            except ValueError as error:
                raise ValueError(f"Path {node.get('id', len(strokes)+1)}: {error}") from error
            strokes.append(path)
            medians.append(median)
        for child in node:
            visit(child, local)

    visit(root, matrix)
    if not strokes:
        raise ValueError("No open stroke paths found")
    return {"strokes": strokes, "medians": medians}


def positive(value):
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise argparse.ArgumentTypeError("must be a positive finite number")
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Folder containing SVG files")
    parser.add_argument("output", type=Path, help="Destination for one JSON file per SVG")
    parser.add_argument("--recursive", action="store_true", help="Include subfolders and preserve their layout")
    parser.add_argument("--coordinates", choices=("hanzi", "preserve"), default="hanzi",
                        help="hanzi: fit viewBox to 1024 units and flip Y; preserve: keep source coordinates")
    parser.add_argument("--spacing", type=positive, default=12,
                        help="Maximum point gap in output units (default: 12)")
    parser.add_argument("--tolerance", type=positive, default=0.5,
                        help="Curve flattening tolerance in output units (default: 0.5)")
    args = parser.parse_args()
    if not args.input.is_dir():
        parser.error("Input must be an existing folder")
    files = sorted(p for p in (args.input.rglob('*') if args.recursive else args.input.iterdir())
                   if p.is_file() and p.suffix.lower() == '.svg')
    if not files:
        parser.error("No SVG files found")
    converted = failed = 0
    for source in files:
        target = args.output / source.relative_to(args.input).with_suffix('.json')
        try:
            if target.exists():
                raise ValueError("Output already exists; choose a new output folder")
            data = convert(source, args.coordinates, args.spacing, args.tolerance)
            payload = json.dumps(data, ensure_ascii=False, separators=(',', ':'), allow_nan=False)
            target.parent.mkdir(parents=True, exist_ok=True)
            # Exclusive creation protects previous results, including name collisions.
            with target.open('x', encoding='utf-8') as output:
                output.write(payload + '\n')
            converted += 1
            print(f"OK {source.name}: {len(data['strokes'])} strokes, "
                  f"{sum(map(len, data['medians']))} median points")
        except (ValueError, OSError, ET.ParseError) as error:
            failed += 1
            print(f"ERROR {source}: {error}", file=sys.stderr)
    print(f"Converted {converted}; failed {failed}. Original SVGs were not changed.")
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
