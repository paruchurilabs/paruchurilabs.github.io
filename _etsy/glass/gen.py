"""Faux stained-glass wedding welcome sign generator (original designs, code-generated).
python3 gen.py --seed 7 --style color|pattern --out file.(png|pdf) [--names "Olivia & James"] [--date "06.20.2027"]
Canvas 24x36 in (2:3). Scales exactly to 18x24 and 12x18.
"""
import argparse, math, random
import numpy as np
from scipy.spatial import Voronoi
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, PathPatch
from matplotlib.path import Path
from matplotlib import font_manager as fm

W, H = 24.0, 36.0
LEAD = 0.16  # inches
PT = 72.0

PALETTES = {
    'blush': dict(bg=['#F6E3E1', '#EEF0E2', '#F7EEDC', '#E4ECEF', '#F3E6EE', '#EAF1E6'],
                  frame=['#C9D8C5', '#E8C9C6', '#D9CFE6'],
                  petal=['#D9727F', '#E79A8E', '#C45B6D', '#F0B9A8'], inner=['#B2475B', '#D6837C'],
                  leaf=['#7FA37E', '#94B48D', '#6A8F6E'], center=['#E9C46A'], plaque='#FFFBF4'),
    'wildflower': dict(bg=['#F4EFD9', '#E6EEF4', '#EFF4E4', '#F7E7DA', '#ECE6F2'],
                       frame=['#A9C3D9', '#E9D39B', '#C7D9B7'],
                       petal=['#E7A54B', '#8EA9D6', '#D97B6C', '#B79AD1', '#F2C94C'], inner=['#C9783A', '#6C86BF'],
                       leaf=['#6E9A62', '#8DB27A', '#5F8558'], center=['#7A4E2D', '#F2C94C'], plaque='#FFFDF6'),
}


def arch(cx, base, w, h, n=120):
    """Convex arch polygon: rectangle with semicircular top. base = bottom y, h = total height."""
    r = w / 2; top_c = base + h - r
    pts = [(cx - r, base), (cx + r, base), (cx + r, top_c)]
    for i in range(1, n):
        a = math.pi * i / n
        pts.append((cx + r * math.cos(a), top_c + r * math.sin(a)))
    pts.append((cx - r, top_c))
    return pts


def clip(poly, clipper):
    """Sutherland-Hodgman: clip polygon by convex clipper (CCW)."""
    def inside(p, a, b): return (b[0]-a[0])*(p[1]-a[1]) - (b[1]-a[1])*(p[0]-a[0]) >= 0
    def inter(p, q, a, b):
        x1, y1, x2, y2, x3, y3, x4, y4 = *p, *q, *a, *b
        d = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
        if abs(d) < 1e-12: return q
        t = ((x1-x3)*(y3-y4) - (y1-y3)*(x3-x4)) / d
        return (x1 + t*(x2-x1), y1 + t*(y2-y1))
    out = poly
    for i in range(len(clipper)):
        a, b = clipper[i], clipper[(i+1) % len(clipper)]
        inp, out = out, []
        if not inp: break
        s = inp[-1]
        for e in inp:
            if inside(e, a, b):
                if not inside(s, a, b): out.append(inter(s, e, a, b))
                out.append(e)
            elif inside(s, a, b): out.append(inter(s, e, a, b))
            s = e
    return out


def in_poly(p, poly):
    x, y = p; c = False
    for i in range(len(poly)):
        x1, y1 = poly[i]; x2, y2 = poly[i-1]
        if (y1 > y) != (y2 > y) and x < (x2-x1)*(y-y1)/(y2-y1) + x1: c = not c
    return c


def voronoi_cells(region, n, rng, relax=3):
    xs = [p[0] for p in region]; ys = [p[1] for p in region]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    pts = []
    while len(pts) < n:
        p = (rng.uniform(x0, x1), rng.uniform(y0, y1))
        if in_poly(p, region): pts.append(p)
    pts = np.array(pts)
    for it in range(relax + 1):
        far = 200
        allp = np.vstack([pts, [[-far, -far], [far, -far], [far, far], [-far, far]]])
        vor = Voronoi(allp)
        cells = []
        for i in range(len(pts)):
            reg = vor.regions[vor.point_region[i]]
            if -1 in reg or not reg: cells.append([]); continue
            poly = [tuple(vor.vertices[k]) for k in reg]
            # order CCW
            cx = sum(p[0] for p in poly)/len(poly); cy = sum(p[1] for p in poly)/len(poly)
            poly.sort(key=lambda p: math.atan2(p[1]-cy, p[0]-cx))
            cells.append(clip(poly, region))
        if it < relax:
            pts = np.array([(sum(p[0] for p in c)/len(c), sum(p[1] for p in c)/len(c)) if c else tuple(pts[i]) for i, c in enumerate(cells)])
    return [c for c in cells if len(c) >= 3]


def petal(cx, cy, ang, length, width, n=24):
    """Teardrop petal from center outward."""
    pts = []
    for i in range(n + 1):
        t = i / n * math.pi
        r = length * (0.5 - 0.5 * math.cos(t))  # 0..length
        wv = width * math.sin(t) ** 0.8 * (0.6 + 0.4 * (r / length))
        pts.append((r, wv / 2))
    pts += [(r, -w) for r, w in reversed(pts)]
    ca, sa = math.cos(ang), math.sin(ang)
    return [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts]


def leaf(x, y, ang, length, width, n=20):
    pts = []
    for i in range(n + 1):
        t = i / n
        pts.append((t * length, width / 2 * math.sin(math.pi * t) ** 0.9))
    pts += [(px, -py) for px, py in reversed(pts)]
    ca, sa = math.cos(ang), math.sin(ang)
    return [(x + px * ca - py * sa, y + px * sa + py * ca) for px, py in pts], \
           [(x + 0.08 * length * ca, y + 0.08 * length * sa), (x + 0.85 * length * ca, y + 0.85 * length * sa)]


def circle(cx, cy, r, n=48):
    return [(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


def build(seed, pal_name):
    rng = random.Random(seed); P = PALETTES[pal_name]
    shapes = []  # (poly, fill, kind)
    lines = []   # polylines (lead), drawn on top of their layer
    M = 1.0
    outer = arch(W / 2, M, W - 2 * M, H - 2 * M)
    band = 1.1
    inner = arch(W / 2, M + band, W - 2 * M - 2 * band, H - 2 * M - 2 * band)
    # frame: segment the band into blocks
    shapes.append((outer, rng.choice(P['frame']), 'frame'))
    r_o = (W - 2 * M) / 2; topc = M + (H - 2 * M) - r_o
    segs = []
    for y in np.linspace(M, topc, 7):
        segs.append([(M, y), (M + band, max(y, M + band) if y > M else M + band)])
        segs.append([(W - M, y), (W - M - band, max(y, M + band) if y > M else M + band)])
    for i in range(1, 12):
        a = math.pi * i / 12
        segs.append([(W/2 + r_o*math.cos(a), topc + r_o*math.sin(a)), (W/2 + (r_o-band)*math.cos(a), topc + (r_o-band)*math.sin(a))])
    segs.append([(M, M + band), (W - M, M + band)])
    # alternate frame colors by painting band pieces: approximate with small quads along band
    # colored frame blocks between the cut lines
    ys = list(np.linspace(M, topc, 7))
    for k in range(6):
        col = P['frame'][k % len(P['frame'])]
        for xa, xb in ((M, M + band), (W - M - band, W - M)):
            shapes.append(([(xa, max(ys[k], M)), (xb, max(ys[k], M)), (xb, ys[k+1]), (xa, ys[k+1])], col, 'frameblk'))
    for i in range(12):
        a0, a1 = math.pi * i / 12, math.pi * (i + 1) / 12
        arc = [(W/2 + r_o*math.cos(a0 + (a1-a0)*t/8), topc + r_o*math.sin(a0 + (a1-a0)*t/8)) for t in range(9)]
        arc += [(W/2 + (r_o-band)*math.cos(a1 - (a1-a0)*t/8), topc + (r_o-band)*math.sin(a1 - (a1-a0)*t/8)) for t in range(9)]
        shapes.append((arc, P['frame'][(i + 1) % len(P['frame'])], 'frameblk'))
    shapes.append(([(M, M), (W - M, M), (W - M, M + band), (M, M + band)], P['frame'][1], 'frameblk'))
    shapes.append((inner, '#FFFFFF', 'inner'))
    # background cells
    cells = voronoi_cells(inner, 62, rng)
    for c in cells: shapes.append((c, rng.choice(P['bg']), 'bg'))
    fg = []
    # plaque (arched-top panel) at 47..72% height
    pw, ph = 14.4, 9.6; px, py = W / 2, 14.6
    plaque = arch(px, py, pw, ph, 80)
    # garland flowers
    def flower(x, y, s, rot):
        col = rng.choice(P['petal']); inn = rng.choice(P['inner'])
        k = rng.choice([5, 6])
        for i in range(k):
            fg.append((petal(x, y, rot + 2 * math.pi * i / k, s, s * 0.95), col, 'petal'))
        for i in range(k):
            fg.append((petal(x, y, rot + math.pi / k + 2 * math.pi * i / k, s * 0.62, s * 0.62), inn, 'petal'))
        fg.append((circle(x, y, s * 0.2), rng.choice(P['center']), 'center'))
    def add_leaf(x, y, ang, L):
        poly, vein = leaf(x, y, ang, L, L * 0.42)
        fg.append((poly, rng.choice(P['leaf']), 'leaf')); fg.append((vein, None, 'vein'))
    # leaves first (under flowers)
    spots = []
    # two corner bouquets (big blooms), plus a few smaller fillers along the bottom
    for side in (-1, 1):
        bx = W / 2 + side * (W / 2 - 4.6)
        spots += [(bx, 4.6, 2.5), (bx - side * 3.9, 3.7, 1.9), (bx + side * 0.6, 8.6, 1.9), (bx - side * 0.3, 12.0, 1.35)]
    spots.append((W / 2, 3.5, 1.7))
    # crown at the arch top
    for i, a in enumerate([math.pi * 0.5, math.pi * 0.3, math.pi * 0.7]):
        rr = r_o - band - 2.3 - (0 if i == 0 else 0.4)
        spots.append((W / 2 + rr * math.cos(a), topc + rr * math.sin(a), 2.1 if i == 0 else 1.5))
    for (x, y, s) in spots:
        for k in range(2):
            ang = rng.uniform(0, 2 * math.pi)
            add_leaf(x + math.cos(ang) * s * 0.6, y + math.sin(ang) * s * 0.6, ang, s * rng.uniform(1.5, 2.0))
    for (x, y, s) in spots: flower(x, y, s, rng.uniform(0, 2 * math.pi))
    # keep everything inside inner arch: clip fg polys to inner
    fg2 = []
    for poly, col, kind in fg:
        if kind == 'vein':
            if all(in_poly(p, inner) for p in poly): fg2.append((poly, col, kind))
            continue
        c = clip(poly, inner) if not all(in_poly(p, inner) for p in poly) else poly
        if len(c) >= 3: fg2.append((c, col, kind))
    return dict(shapes=shapes, fg=fg2, segs=segs, plaque=plaque, P=P, outer=outer, inner=inner)


def render(d, style, out, names, date, line1):
    fig = plt.figure(figsize=(W, H), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis('off')
    fig.patch.set_facecolor('white')
    lw = LEAD * PT
    def fill(col): return 'white' if style == 'pattern' else col
    for poly, col, kind in d['shapes']:
        ax.add_patch(Polygon(poly, closed=True, facecolor=fill(col), edgecolor='black', linewidth=lw * (1.25 if kind == 'frame' else (0.0 if kind == 'frameblk' else 1)), joinstyle='round'))
    for s in d['segs']:
        ax.plot([s[0][0], s[1][0]], [s[0][1], s[1][1]], color='black', linewidth=lw, solid_capstyle='round')
    for zi, (poly, col, kind) in enumerate(d['fg']):
        z = 3 + zi * 0.001
        if kind == 'vein':
            ax.plot([poly[0][0], poly[1][0]], [poly[0][1], poly[1][1]], color='black', linewidth=lw * 0.6, solid_capstyle='round', zorder=z)
        else:
            ax.add_patch(Polygon(poly, closed=True, facecolor=fill(col), edgecolor='black', linewidth=lw * 0.8, joinstyle='round', zorder=z))
    ax.add_patch(Polygon(d['plaque'], closed=True, zorder=10, facecolor='white' if style == 'pattern' else d['P']['plaque'], edgecolor='black', linewidth=lw * 1.1, joinstyle='round'))
    # text (matches the personalizer page: Cormorant Garamond + Great Vibes)
    F = '/home/claude/glass/fonts/'
    gv = fm.FontProperties(fname=F + 'GreatVibes-Regular.ttf')
    cg = fm.FontProperties(fname=F + 'CormorantGaramond[wght].ttf', weight='semibold')
    r = fig.canvas.get_renderer()
    def fit_text(y, txt, fp, size_in, maxw, minsize):
        size = size_in * PT
        while True:
            t = ax.text(W / 2, H - y, txt, zorder=11, ha='center', va='baseline', fontproperties=fp, fontsize=size, color='black')
            bb = t.get_window_extent(renderer=r).transformed(ax.transData.inverted())
            if bb.width <= maxw or size <= minsize * PT: return t
            t.remove(); size *= 0.96
    fit_text(15.55, line1.upper(), cg, 0.66, 11.2, 0.35)
    fit_text(18.05, names, gv, 2.6, 12.6, 1.0)
    if date: fit_text(20.25, date, cg, 0.85, 11.2, 0.4)
    dpi = 300 if out.endswith('.pdf') else globals().get('PNG_DPI', 60)
    fig.savefig(out, dpi=dpi, facecolor='white')
    plt.close(fig)


if __name__ == '__main__':
    a = argparse.ArgumentParser()
    a.add_argument('--seed', type=int, default=7); a.add_argument('--pal', default='blush')
    a.add_argument('--style', default='color'); a.add_argument('--out', default='out.png')
    a.add_argument('--names', default='Olivia & James'); a.add_argument('--date', default='06.20.2027')
    a.add_argument('--line1', default='Welcome to the wedding of')
    o = a.parse_args()
    d = build(o.seed, o.pal)
    render(d, o.style, o.out, o.names, o.date, o.line1)
    print('ok', o.out)


def to_svg(d, style, include_text=False):
    """SVG in inches (viewBox 0 0 24 36), y flipped. Text layer is left to the personalizer page."""
    def pts(poly): return ' '.join(f'{x:.3f},{H - y:.3f}' for x, y in poly)
    def f(col): return '#fff' if style == 'pattern' else col
    L = LEAD
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:g} {H:g}" width="{W:g}in" height="{H:g}in">',
           '<rect width="100%" height="100%" fill="#fff"/>',
           f'<g stroke="#000" stroke-linejoin="round" stroke-linecap="round">']
    for poly, col, kind in d['shapes']:
        sw = 0 if kind == 'frameblk' else (L * 1.25 if kind == 'frame' else L)
        out.append(f'<polygon points="{pts(poly)}" fill="{f(col)}" stroke-width="{sw:.3f}"/>')
    for s in d['segs']:
        out.append(f'<line x1="{s[0][0]:.3f}" y1="{H - s[0][1]:.3f}" x2="{s[1][0]:.3f}" y2="{H - s[1][1]:.3f}" stroke-width="{L:.3f}"/>')
    for poly, col, kind in d['fg']:
        if kind == 'vein':
            out.append(f'<line x1="{poly[0][0]:.3f}" y1="{H - poly[0][1]:.3f}" x2="{poly[1][0]:.3f}" y2="{H - poly[1][1]:.3f}" stroke-width="{L * 0.6:.3f}"/>')
        else:
            out.append(f'<polygon points="{pts(poly)}" fill="{f(col)}" stroke-width="{L * 0.8:.3f}"/>')
    pl = '#fff' if style == 'pattern' else d['P']['plaque']
    out.append(f'<polygon id="plaque" points="{pts(d["plaque"])}" fill="{pl}" stroke-width="{L * 1.1:.3f}"/>')
    out.append('</g></svg>')
    return '\n'.join(out)
