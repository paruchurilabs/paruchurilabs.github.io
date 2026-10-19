from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
from reportlab.lib.utils import ImageReader

G = '/usr/share/fonts/truetype/google-fonts/'
pdfmetrics.registerFont(TTFont('Pop', G + 'Poppins-Regular.ttf'))
pdfmetrics.registerFont(TTFont('PopM', G + 'Poppins-Medium.ttf'))
pdfmetrics.registerFont(TTFont('Lora', G + 'Lora-Variable.ttf'))
pdfmetrics.registerFont(TTFont('GV', '/home/claude/glass/fonts/GreatVibes-Regular.ttf'))
INK, GR, RU, BG = HexColor('#2E2A26'), HexColor('#3F5A45'), HexColor('#A0522D'), HexColor('#F5EFE6')
URL = 'https://paruchurilabs.com/glass/'
Wp, Hp = letter
c = canvas.Canvas('Stained_Glass_Wedding_Sign_Pattern.pdf', pagesize=letter)
c.setTitle('Faux Stained Glass Wedding Sign Pattern - ParuchuriStudio')


def page_bg():
    c.setFillColor(BG); c.rect(0, 0, Wp, Hp, stroke=0, fill=1)


def head(kick, title, y=Hp - 90):
    c.setFillColor(RU); c.setFont('PopM', 11); c.drawString(60, y, kick.upper())
    c.setFillColor(INK); c.setFont('Lora', 30); c.drawString(60, y - 40, title)
    c.setFillColor(RU); c.rect(60, y - 58, 60, 3, stroke=0, fill=1)


def para(lines, x, y, size=12, lead=19, font='Pop', col=INK):
    c.setFont(font, size); c.setFillColor(col)
    for ln in lines: c.drawString(x, y, ln); y -= lead
    return y


def footer():
    c.setFont('Pop', 8.5); c.setFillColor(HexColor('#8A8079'))
    c.drawCentredString(Wp / 2, 30, 'ParuchuriStudio  ·  For personal use with your purchase  ·  Please do not share or resell the pattern')


# 1 cover
page_bg()
img = ImageReader('r_rose_color.png'); h = 470; w = h * 2 / 3
c.drawImage(img, (Wp - w) / 2, Hp - 120 - h, w, h, mask='auto')
c.setFillColor(INK); c.setFont('Lora', 28); c.drawCentredString(Wp / 2, 150, 'Faux Stained Glass Wedding Sign')
c.setFont('PopM', 11); c.setFillColor(GR); c.drawCentredString(Wp / 2, 125, 'PERSONALIZED PATTERN  ·  ROSE ARCH & WILDFLOWER MEADOW')
c.setFont('GV', 26); c.setFillColor(RU); c.drawCentredString(Wp / 2, 80, 'Thank you for your order!')
footer(); c.showPage()

# 2 personalize
page_bg(); head('Step 1', 'Add your names')
y = para(['Open the personalizer on any computer, tablet or phone:'], 60, Hp - 190, 13)
c.setFillColor(GR); c.roundRect(60, y - 40, Wp - 120, 50, 10, stroke=0, fill=1)
c.setFillColor(HexColor('#FFFFFF')); c.setFont('PopM', 17); c.drawCentredString(Wp / 2, y - 22, URL)
c.linkURL(URL, (60, y - 40, Wp - 60, y + 10), relative=0)
q = qr.QrCodeWidget(URL); b = q.getBounds(); s = 150
d = Drawing(s, s, transform=[s / (b[2] - b[0]), 0, 0, s / (b[3] - b[1]), 0, 0]); d.add(q)
y = para(['1.  Choose a design: Rose Arch or Wildflower Meadow.',
          '2.  Type your top line, names and date. The names shrink',
          '     automatically to fit the panel.',
          '3.  Pick a script font and a print size (24×36, 18×24 or 12×18).',
          '4.  Switch between "Pattern" (to trace) and "Color guide".',
          '5.  Click Print full size and choose "Save as PDF", or',
          '     Print on letter paper to print tiles at home.',
          '', 'Your details never leave your browser.',
          'You can come back and print again any time,', 'for example a matching table number or a gift.'], 60, y - 80, 12.5, 22)
renderPDF.draw(d, c, 60, y - s - 10)
para(['Scan to open on your phone'], 60 + s + 16, y - s / 2, 11, 18, 'Pop', GR)
footer(); c.showPage()

# 3 printing
page_bg(); head('Step 2', 'Print your pattern')
y = para(['Option A: one big sheet (easiest)', ], 60, Hp - 190, 15, 24, 'PopM', GR)
y = para(['Save the full-size PDF and take it to a print shop or office store.',
          'Ask for a black & white engineering print (also called a blueprint',
          'print). It is the cheapest large-format option.',
          'Make sure it prints at 100% / actual size.'], 60, y - 4, 12.5, 21)
y = para(['Option B: letter-size tiles at home'], 60, y - 24, 15, 24, 'PopM', GR)
y = para(['Use "Print on letter paper". Each page is labeled (A1, A2 ...).',
          'In the print window set Scale to 100% (or "Actual size") and',
          'turn off "Fit to page". Trim one edge of each page along the',
          'dashed line, overlap by 1/4 inch and tape the pages in order.'], 60, y - 4, 12.5, 21)
y = para(['Tip: a sign that is 18×24 or bigger reads best from a distance.',
          'Most welcome-sign easels hold 24×36 or 18×24.'], 60, y - 30, 12, 20, 'Pop', RU)
footer(); c.showPage()

# 4 paint
page_bg(); head('Step 3', 'Trace & paint')
y = para(['You will need'], 60, Hp - 190, 15, 24, 'PopM', GR)
y = para(['•  Clear acrylic sheet or a mirror in your sign size',
          '•  Black glass-paint liner (outliner / leading paste)',
          '•  Transparent glass paints in your colors',
          '•  Small brushes, painter\'s tape, isopropyl alcohol & cloth'], 60, y - 4, 12.5, 21)
y = para(['How to'], 60, y - 20, 15, 24, 'PopM', GR)
y = para(['1.  Clean the acrylic with alcohol. Peel off its protective film.',
          '2.  Tape the pattern under the acrylic, face up.',
          '     For a mirror, use "Mirror image" and transfer paper instead.',
          '3.  Trace every black line with the liner. Let it dry fully',
          '     (usually a few hours).',
          '4.  Fill each piece with glass paint, using the color guide.',
          '     Work from the top down so you don\'t smudge wet areas.',
          '5.  Paint the lettering black, or leave the panel clear and add',
          '     vinyl lettering.',
          '6.  Dry for 24 hours, then display on an easel.'], 60, y - 4, 12.5, 21)
footer(); c.showPage()

# 5-6 color guides
for name, img in [('Rose Arch', 'r_rose_color.png'), ('Wildflower Meadow', 'r_meadow_color.png')]:
    page_bg(); head('Color guide', name)
    h = 560; w = h * 2 / 3
    c.drawImage(ImageReader(img), (Wp - w) / 2, 70, w, h, mask='auto')
    footer(); c.showPage()
c.save(); print('ok')
