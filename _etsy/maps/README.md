# Lake map posters (Etsy shop ParuchuriStudio) — pipeline and custom-order SOP

Not published by GitHub Pages (underscore folder). Never store buyer names, addresses or messages here.

## Rendering (lp3.js)
- Data: OpenFreeMap vector tiles (OSM, OpenMapTiles schema) + Nominatim lookup. Overpass is NOT used (it blocks us; Printify's CSP also blocks it).
- Run in a Chrome tab whose page has no strict CSP, e.g. https://overpass-api.de/api/status (any static page works).
- Paste lp3.js into that tab. Then:
  `await LP3.make({q:'<Lake>, <County or town>, <State>', title:'<Title>', sub:'<Second line>', fit:0.82, zmax:13})`
  - small lakes: zmax 14; long thin lakes: fit 0.9–0.96.
  - Check `LP3.out[title].hit.name` is the right lake (Nominatim display name) before using it.
  - `LP3.show(title)` overlays a preview for a screenshot; `LP3.rerender(title,{title,sub})` changes text without refetching.
  - Output: 5400x7200 PNG (12x16 / 18x24 at 300+ dpi), same look as the shop's other lake posters.
- To get the PNG into Printify: in the render tab replace the body with a button whose onclick does
  `window.__pw = window.open('https://printify.com/app/store/products/1','lp_printify')`, click it (needs a real click),
  then in the new Printify tab add a `message` listener (origin https://overpass-api.de) that stores `e.data.blob` in IndexedDB `lp_store/files`,
  and call `LP3.send(title)` from the render tab. In the Printify editor, patch HTMLInputElement.prototype.click so a file input receives
  `window.__uploadFiles` via DataTransfer, then Upload > My device.
- Printify product to duplicate: any "Lake ... Map Poster" (Printify Choice, Vertical and Horizontal Matte Posters, 12x16 + 18x24, free shipping, $29.99/$47.99).

## Custom lake map orders (Etsy listing 4598314463, SKUs CUSTOM-LAKE-12x16 / CUSTOM-LAKE-18x24)
This listing is NOT synced to Printify, so its orders are not auto-fulfilled. For each new order:
1. Read the order's personalization: lake + town + state, title line, optional second line (blank = state name). Size from the variation.
2. Render with lp3.js (title = title line, sub = second line or the state). Confirm the Nominatim hit is the right lake. If the lake is missing/too small, draft a message offering a nearby lake or a full refund.
3. Draft an Etsy message to the buyer with the proof image (preview JPEG) asking them to reply "approve" or request changes. Krish must OK sending it.
4. After the buyer approves (their reply in the Etsy thread): duplicate a lake poster product in Printify, swap in the full PNG, title it "CUSTOM order <Etsy order number>", Save — do NOT publish to Etsy (keep it unpublished/hidden).
5. Printify > Create order > manual order with that product, the purchased size, and the buyer's shipping address from the Etsy order. This charges Krish's Printify payment method, so it needs Krish's explicit OK for that specific order before submitting.
6. When Printify ships, add tracking to the Etsy order (Printify does not do this for manual orders): Etsy order > Complete order > carrier + tracking number.
Processing profile on the listing is 5–10 business days.

## Displate versions (lpd.js)
4200x5880 JPG (1.4:1), full-bleed map, no frame line, text inside a 260px safe margin.
Render in a tab on https://tiles.openfreemap.org/planet: fetch raw.githubusercontent.com/.../_etsy/maps/lpd.js and eval,
then LPD.make(job) for each job below. Open the uploader with a button click (window.open keeps opener),
postMessage blobs, and set the uploader's file input via DataTransfer.
Jobs: Lake Tahoe (California · Nevada), Lake Norman, North Carolina / Lake of the Ozarks, Missouri / Lake Lanier, Georgia /
Lake Winnipesaukee, New Hampshire / Smith Mountain Lake, Virginia / Lake Travis, Texas / Table Rock Lake, Missouri /
Geneva Lake, Wisconsin (title Lake Geneva, zmax 14, fit 0.96) / Lake Minnetonka, Minnesota (zmax 14) / Torch Lake, Michigan /
Lake Keowee, South Carolina. Defaults fit 0.82, zmax 13. All 12 rendered fine on 2026-10-18.
Blocker: Displate asks the artist to confirm the first upload by phone (SMS/WhatsApp) - Krish has to do that once.

### Displate upload status / flow (2026-10-19)
Phone confirmation done. New artists: max 4 artworks in the validation queue.
Submitted 2026-10-19: Lake Tahoe, Lake Norman, Lake of the Ozarks, Lake Lanier (collection "Lake Maps", category Maps, art type Digital Art).
Remaining: Winnipesaukee, Smith Mountain, Travis, Table Rock, Geneva, Minnetonka, Torch, Keowee.
Flow per artwork (uploader at /artist/artwork-uploader): set file input via DataTransfer -> wait for "All systems are a go" -> Next (JS click ok)
-> wait up to ~60s for input[name=title] -> set title "<Lake> Map", description, art_type value 10 -> Next (needs a REAL click)
-> click "Add tag", focus input, type lake house / cabin decor / lake map + Enter each (Displate pre-fills ~10 tags) -> Next (real click)
-> focus react-select inputs [0] type "Maps"+Enter, [1] type "Lake"+Enter -> tick input[name=accept] -> Next (real click).
Keep each javascript_exec under 45s (CDP timeout).
