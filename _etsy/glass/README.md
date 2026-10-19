# Faux stained glass wedding sign (Etsy 4599015866, $14.99 digital, section Wedding Signs 60996250)
- gen.py: geometry (scipy Voronoi + Sutherland-Hodgman clip), renders PNG/PDF and to_svg(). Designs: rose=(seed 7, blush), meadow=(seed 3, wildflower).
  Fonts: GreatVibes + Cormorant Garamond (sparse-cloned from github.com/google/fonts; OFL).
- Personalizer page: /glass/index.html + /glass/designs/<id>-<color|pattern>.svg (text layer added client-side, print full size or letter tiles).
- photos.py -> ph_01..07.jpg listing photos; guide.py -> Stained_Glass_Wedding_Sign_Pattern.pdf (the Etsy download, links to paruchurilabs.com/glass/).
- To add a design: build(seed, palette) -> to_svg -> glass/designs, add <option> in index.html, update guide + photos.
- Validation 2026-10-19 (eRank, Etsy US): "stained glass wedding sign" ~1,517 searches/mo (2,470 Sep), 646 competing listings.
