# Field Quote Kit log

## 2026-10-16: launch
- Data: no keyword or traffic connector connected. Keyword Planner could not be opened (needs Krish's Google Ads sign-in). Volumes not measured.
- Picked the first three tools from competition research: top results for pressure washing, window cleaning and lawn mowing calculators were mostly scraped spam pages and software-company articles; Jobber and Housecall Pro already own "house cleaning price calculator" and handyman rate calculators, so those were skipped.
- Built and published: /tools/pressure-washing-estimate-calculator/, /tools/window-cleaning-price-calculator/, /tools/lawn-mowing-price-calculator/, hub at /tools/, sitemap.xml, robots.txt Sitemap line, homepage footer link to /tools/.
- Pricing sources: Jobber window cleaning pricing guide ($4–$8 per pane), Jobber lawn care pricing guide ($0.01–$0.06 per sq ft, $150–$200 per acre), Housecall Pro lawn mowing guide, typical published pressure washing per-sq-ft ranges.
- Affiliate economics checked: Jobber listed on FlexOffers at 48% of monthly sales or flat amounts per annual plan; Housecall Pro $40–$400 per sale plus per-lead payouts (US/Canada only). Partner links on the pages are plain links until affiliate URLs arrive.
- Weekly scheduled task "Weekly tool site run" created (Mondays 8:54am Pacific).
- Open items for Krish: (a) apply to Jobber and Housecall Pro affiliate programs (PartnerStack) and send links; (b) add paruchurilabs.com to Google Search Console and submit the sitemap; (c) connect Ubersuggest or Semrush and Supermetrics.

## 2026-10-16: affiliate applications
- Krish applied to the Jobber and Housecall Pro affiliate programs (PartnerStack). Waiting on approval. Item (a) is now: once approved, send the referral links from the PartnerStack dashboard. Do not ask him to apply again.

## 2026-10-16: Search Console
- Krish verified paruchurilabs.com as a Domain property in Google Search Console (DNS on Cloudflare). Sitemap submission in progress. Item (b) is done once the sitemap shows as submitted; do not ask again. Gmail connected (hello@paruchurilabs.com forwards to his Gmail via Cloudflare Email Routing).
- Sitemap https://paruchurilabs.com/sitemap.xml submitted in Search Console (2026-10-16). Item (b) done.

## 2026-10-16: Ubersuggest connected (free plan: 3 reports per day)
US monthly search volume / SEO difficulty (0–100, lower is easier):
- pressure washing estimate calculator: 480 / 11, CPC $5.03
- window cleaning price calculator: 210 / 20, CPC $7.26
- lawn mowing price calculator: 1,900 / 8, CPC $3.67 (seasonal: about 400 in Dec, peaks in spring)
All three are low difficulty; lawn mowing has the most demand. Daily limit hit on the 4th lookup, so spend the 3 reports on the most promising candidates each run.

## 2026-10-17: house cleaning calculator (for the Booked & Busy newsletter)
- Built /tools/house-cleaning-price-calculator/ on Krish's request. This tool exists to support his new email newsletter for cleaning business owners, Booked & Busy (Issue #1 links to it), not as an SEO bet: the 2026-10-16 entry still stands that Jobber and Housecall Pro own "house cleaning price calculator" in search. Do not count weak search traffic on this page as a reason to drop it.
- Model: labor hours = 0.5 + sq ft/1000 + 0.4 per bath + 0.15 per bedroom, times type of clean (standard 1, deep 1.75, move-in/out 2), condition (0.9 to 1.5) and pets (1 to 1.2), minimum 1.5 hrs, plus fixed add-on hours; priced at the hourly rate per cleaner, plus supplies and travel, then a $120 minimum. Time on site = labor hours / cleaners.
- Benchmarks (Housecall Pro house cleaning prices guide, https://www.housecallpro.com/resources/pricing/house-cleaning-prices/): $30–$80 per hour per cleaner (comparison band uses $30 low, $80 high, $45 default); standard clean $140–$220; whole-home deep clean $180–$375 (Angi figures cited there), deep clean up to about 2x standard; move-in/out $220–$400.
- Newsletter signup: tools with "newsletter": true in tools.json get a Booked & Busy signup box, but only once _tools_src/newsletter_embed.html exists (paste beehiiv's embed code there and run build.py). Until then no box is shown, so no form ever collects emails into nothing. Booked & Busy is for cleaning business owners, so only cleaning-related tools should set "newsletter": true.
- Changes now go through pull requests for Krish to review (this one included). Open item for Krish: create the beehiiv account and an inline subscribe form, then paste the embed code into a Claude chat.
- 2026-10-17: Krish created the beehiiv account; his inline subscribe form's embed code is saved in _tools_src/newsletter_embed.html, so the house cleaning calculator now shows the Booked & Busy signup box. Open item done; do not ask for it again.
