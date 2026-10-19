"""Listing photos for the stained-glass wedding sign pattern (2700x2025)."""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import gen

S = 60  # px per inch in r_*.png
BG = (245, 239, 230); INK = (46, 42, 38); GR = (63, 90, 69); RU = (160, 82, 45); SO = (226, 216, 200); CARD = (255, 253, 249)
F = '/home/claude/glass/fonts/'; G = '/usr/share/fonts/truetype/google-fonts/'
def cg(s):
    f = ImageFont.truetype(F + 'CormorantGaramond[wght].ttf', s)
    try: f.set_variation_by_axes([600])
    except Exception: pass
    return f
def gv(s): return ImageFont.truetype(F + 'GreatVibes-Regular.ttf', s)
def pop(s, b='Regular'): return ImageFont.truetype(G + f'Poppins-{b}.ttf', s)
W, H = 2700, 2025


def arch_cut(path):
    im = Image.open(path).convert('RGBA')
    poly = [(x * S, (gen.H - y) * S) for x, y in gen.arch(gen.W / 2, 1.0, gen.W - 2, gen.H - 2)]
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).polygon(poly, fill=255)
    m = m.filter(ImageFilter.GaussianBlur(0.6)); im.putalpha(m)
    return im.crop((int(1 * S) - 4, int(1 * S) - 4, int((gen.W - 1) * S) + 4, int((gen.H - 1) * S) + 4))


def sheet(path):  # flat paper sheet (pattern print)
    return Image.open(path).convert('RGBA')


def fit(im, h): return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)


def drop(base, im, x, y, rot=0, r=28, a=95, off=(18, 26)):
    if rot: im = im.rotate(rot, expand=True, resample=Image.BICUBIC)
    sh = Image.new('RGBA', (im.width + 160, im.height + 160), (0, 0, 0, 0))
    s = Image.new('RGBA', im.size, (40, 30, 20, a)); sh.paste(s, (80 + off[0], 80 + off[1]), im.split()[3])
    sh = sh.filter(ImageFilter.GaussianBlur(r)); base.alpha_composite(sh, (x - 80, y - 80)); base.alpha_composite(im, (x, y))


def canvas(bg=BG): return Image.new('RGBA', (W, H), bg + (255,))


def ctext(d, cx, y, t, f, fill):
    d.text((cx - d.textlength(t, font=f) / 2, y), t, font=f, fill=fill)


def mountains(d, b, h):  # same shop motif
    pts = [(0, b), (0, b - h * .55), (W * .15, b - h * .95), (W * .28, b - h * .6), (W * .42, b - h), (W * .59, b - h * .5), (W * .74, b - h * .88), (W * .87, b - h * .55), (W, b - h * .7), (W, b)]
    d.polygon(pts, fill=(232, 222, 205))


rc, rp, mc, mp = arch_cut('r_rose_color.png'), sheet('r_rose_pattern.png'), arch_cut('r_meadow_color.png'), sheet('r_meadow_pattern.png')

# 1 hero
im = canvas(); d = ImageDraw.Draw(im)
d.text((170, 380), 'PERSONALIZED PRINTABLE PATTERN', font=pop(44, 'Medium'), fill=RU)
y = 470
for ln in ['Faux Stained', 'Glass Wedding', 'Welcome Sign']:
    d.text((165, y), ln, font=cg(150), fill=INK); y += 158
d.rectangle([170, y + 30, 320, y + 40], fill=RU)
y += 90
for b in ['Add your names online in minutes', 'Print 24×36, 18×24 or 12×18', 'Trace & paint on acrylic or mirror', 'Instant download · 2 designs']:
    d.ellipse([175, y + 16, 203, y + 44], fill=GR); d.text((230, y), b, font=pop(50), fill=INK); y += 86
drop(im, fit(rp, 1420), 1430, 360, rot=7, a=60)
drop(im, fit(rc, 1600), 1560, 220, rot=-2)
im.convert('RGB').save('ph_01.jpg', quality=92)

# 2 trace -> paint
im = canvas(); d = ImageDraw.Draw(im)
ctext(d, W / 2, 80, 'Trace it. Paint it. Keep it forever.', cg(120), INK)
ctext(d, W / 2, 245, 'THE PATTERN GOES UNDER CLEAR ACRYLIC · YOU FILL IT IN WITH GLASS PAINT', pop(40, 'Medium'), GR)
drop(im, fit(rp, 1560), 230, 380, a=55)
drop(im, fit(rc, 1560), 1460, 380)
d = ImageDraw.Draw(im)
for k, (x, t) in enumerate([(720, 'YOUR PATTERN'), (1950, 'FINISHED SIGN')]):
    ctext(d, x, 1960 - 10, t, pop(40, 'Medium'), RU)
ax, ay = 1350, 1150; d.polygon([(ax - 60, ay - 50), (ax + 40, ay), (ax - 60, ay + 50)], fill=GR)
im.convert('RGB').save('ph_02.jpg', quality=92)

# 3 personalize online (mock of the page)
im = canvas(); d = ImageDraw.Draw(im)
d.text((160, 330), 'STEP 1', font=pop(44, 'Medium'), fill=RU)
y = 410
for ln in ['Add your', 'names online']:
    d.text((155, y), ln, font=cg(150), fill=INK); y += 158
d.rectangle([160, y + 30, 310, y + 40], fill=RU); y += 90
for t in ['Type your names, date and', 'top line. The preview updates', 'live, and the names resize to fit.', '', 'Choose from 5 script fonts.', 'Nothing to install, no waiting', 'for the seller to send a proof.']:
    d.text((160, y), t, font=pop(46), fill=(93, 85, 77)); y += 66
# browser mock
bx, by, bw, bh = 1180, 170, 1380, 1690
win = Image.new('RGBA', (bw, bh), (255, 255, 255, 255)); wd = ImageDraw.Draw(win)
wd.rectangle([0, 0, bw, 70], fill=(236, 230, 221))
for i, c in enumerate([(232, 106, 94), (241, 191, 66), (98, 189, 104)]): wd.ellipse([24 + i * 40, 24, 48 + i * 40, 48], fill=c)
wd.rounded_rectangle([170, 16, bw - 40, 54], 12, fill=(255, 255, 255)); wd.text((195, 20), 'Stained Glass Sign Personalizer', font=pop(24), fill=(110, 100, 90))
wd.rectangle([0, 70, bw, bh], fill=BG)
ctext(wd, bw / 2, 100, 'Stained Glass Sign Personalizer', cg(64), INK)
px, py = 50, 230; wd.rounded_rectangle([px, py, px + 520, bh - 50], 18, fill=CARD, outline=(226, 216, 200), width=2)
fy = py + 40
for lab, val, font in [('NAMES', 'Olivia & James', pop(30)), ('DATE', '06.20.2027', pop(30)), ('NAME FONT', 'Great Vibes', pop(30)), ('PRINT SIZE', '24 × 36 in', pop(30))]:
    wd.text((px + 30, fy), lab, font=pop(22, 'Medium'), fill=GR); fy += 40
    wd.rounded_rectangle([px + 30, fy, px + 490, fy + 70], 10, fill=(255, 255, 255), outline=(226, 216, 200), width=2)
    wd.text((px + 50, fy + 16), val, font=font, fill=INK); fy += 110
wd.rounded_rectangle([px + 30, fy + 10, px + 490, fy + 90], 12, fill=GR); ctext(wd, px + 260, fy + 30, 'Print full size', pop(30, 'Medium'), (255, 255, 255))
fy += 115
wd.rounded_rectangle([px + 30, fy, px + 490, fy + 80], 12, fill=(255, 255, 255), outline=GR, width=3); ctext(wd, px + 260, fy + 20, 'Print on letter paper', pop(30, 'Medium'), GR)
pv = fit(rp, 1150); win.alpha_composite(pv, (600 + (bw - 600 - pv.width) // 2, 300))
drop(im, win, bx, by, r=30, a=70)
im.convert('RGB').save('ph_03.jpg', quality=92)

# 4 two designs
im = canvas(); d = ImageDraw.Draw(im)
ctext(d, W / 2, 80, 'Two designs included', cg(120), INK)
ctext(d, W / 2, 245, 'ROSE ARCH  ·  WILDFLOWER MEADOW  ·  EACH WITH A PATTERN AND A COLOR GUIDE', pop(40, 'Medium'), GR)
drop(im, fit(rc, 1580), 300, 360); drop(im, fit(mc, 1580), 1430, 360)
im.convert('RGB').save('ph_04.jpg', quality=92)

# 5 print options
im = canvas(); d = ImageDraw.Draw(im)
ctext(d, W / 2, 80, 'Print it your way', cg(120), INK)
ctext(d, W / 2, 245, 'ONE SHEET AT A PRINT SHOP, OR TILES ON YOUR HOME PRINTER', pop(40, 'Medium'), GR)
base_y = 1650
for k, (inch, label) in enumerate([(36, '24 × 36 in'), (24, '18 × 24 in'), (18, '12 × 18 in')]):
    h = int(inch * 31); wpx = fit(rp, h).width; x = [470, 1110, 1580][k] - 210
    drop(im, fit(rp, h), x + (420 - fit(rp, h).width) // 2, base_y - h, a=50, r=18)
    ctext(ImageDraw.Draw(im), x + 210, base_y + 40, label, pop(42, 'Medium'), INK)
# tiles graphic
d = ImageDraw.Draw(im); tx, ty, tw, th = 1900, 540, 600, 900
tile = fit(rp, th)
im.alpha_composite(tile, (tx + (tw - tile.width) // 2, ty))
d = ImageDraw.Draw(im); cols, rows = 4, 4; x0 = tx + (tw - tile.width) // 2
for c in range(1, cols): d.line([(x0 + tile.width * c / cols, ty), (x0 + tile.width * c / cols, ty + th)], fill=RU, width=4)
for r in range(1, rows): d.line([(x0, ty + th * r / rows), (x0 + tile.width, ty + th * r / rows)], fill=RU, width=4)
ctext(d, tx + tw / 2, base_y + 40, 'Letter-size tiles', pop(42, 'Medium'), INK)
ctext(d, tx + tw / 2, ty + th + 40, 'print · trim · tape', pop(36), (110, 100, 90))
im.convert('RGB').save('ph_05.jpg', quality=92)

# 6 how it works
im = canvas(GR); d = ImageDraw.Draw(im)
ctext(d, W / 2, 110, 'How it works', cg(130), BG)
steps = [('1', 'Personalize', 'Open the link in your\ndownload and add\nyour names'), ('2', 'Print', 'Print shop or home\nprinter, at 100% scale'),
         ('3', 'Trace', 'Lay clear acrylic on top\nand trace the lines with\nblack liner'), ('4', 'Paint', 'Fill each piece with\nglass paint. Let it dry\nand display it!')]
for k, (n, h, t) in enumerate(steps):
    cx = 380 + k * 650; cy = 820
    d.ellipse([cx - 140, cy - 140, cx + 140, cy + 140], fill=BG)
    ctext(d, cx, cy - 110, n, cg(170), RU)
    ctext(d, cx, cy + 200, h, pop(62, 'Medium'), BG)
    for j, ln in enumerate(t.split('\n')): ctext(d, cx, cy + 300 + j * 66, ln, pop(44), (226, 232, 222))
ctext(d, W / 2, 1830, 'Digital download · no physical item will be shipped · paints and acrylic not included', pop(40, 'Medium'), (233, 211, 155))
im.convert('RGB').save('ph_06.jpg', quality=92)

# 7 detail close-up
full = Image.open('r_rose_color.png').convert('RGB')
crop = full.crop((60, 1240, 60 + 1100, 1240 + 825)).resize((W, H), Image.LANCZOS)
im = crop.convert('RGBA'); d = ImageDraw.Draw(im)
d.rounded_rectangle([90, 1690, 1260, 1900], 24, fill=(255, 253, 249, 235))
d.text((140, 1720), 'Bold, clean lines', font=cg(84), fill=INK)
d.text((142, 1820), 'big pieces that are easy to paint', font=pop(40), fill=GR)
im.convert('RGB').save('ph_07.jpg', quality=92)
print('ok')
