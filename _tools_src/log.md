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
- Newsletter signup: every tool page shows a Booked & Busy signup box, built from the beehiiv embed code in _tools_src/newsletter_embed.html (if that file is missing, no box is shown). New tools get it automatically through build.py; never remove it.
- Changes now go through pull requests for Krish to review (this one included). Open item for Krish: create the beehiiv account and an inline subscribe form, then paste the embed code into a Claude chat.
- 2026-10-17: Krish created the beehiiv account; his inline subscribe form's embed code is saved in _tools_src/newsletter_embed.html, so the house cleaning calculator now shows the Booked & Busy signup box. Open item done; do not ask for it again.
- 2026-10-17: Krish broadened Booked & Busy from cleaning business owners to all home service business owners (cleaning, lawn care, pressure washing, window cleaning and the trades of future tools), so every calculator page feeds one subscriber list. Goal: growth that needs no manual posting; search traffic to the tools is the main channel.

## 2026-10-19: weekly run
- Data sources: Gmail (read only), web search, Ubersuggest (free plan). No Search Console / Analytics / Supermetrics connector, so no traffic numbers this week (site is 3 days into Search Console anyway).
- Affiliate status (checked 2026-10-19): Jobber pending, Housecall Pro pending. Only the 2026-10-16 PartnerStack "Your Application to join ..." receipts in the inbox; no approval or rejection yet. affiliates.json not created; partner box keeps the plain links, no disclosure.
- Keyword volume: Ubersuggest returned the daily-limit error on the first call (quota already used today), so nothing was measured. Stopped, did not retry. Next run, spend the 3 reports on: gutter cleaning price calculator, junk removal price calculator, car detailing price calculator.
- SERP check (web search, US): "gutter cleaning price calculator" top results are mostly scraped spam pages plus one local company page and a Connecteam free tool (weak). "junk removal estimate calculator": nearly all spam/scraped pages and a WordPress plugin (very weak). "car detailing price calculator": Jobber and Housecall Pro pricing articles, a Paperform template and a few thin calculators (weak-to-medium; detailers are a Jobber audience). "carpet cleaning price calculator": Housecall Pro has its own working calculator (skip for now). "airbnb cleaning fee calculator": Airbtics, Mashvisor and BNBCalc own it and the audience is hosts, not service businesses (skip). "house painting estimate calculator": several invoicing-app calculators (Invoicer, InvoiceFly, Method) (medium; later).
- Decision: built 1 tool, gutter cleaning, without a measured volume: weakest SERP of the shortlist apart from junk removal, gutter companies are a Jobber/Housecall Pro audience, and demand peaks in fall and again in spring, so it has the winter to start ranking before the spring season. Held the second slot until volumes can be measured. If next week's lookup shows "gutter cleaning price calculator" under ~50/month, note it as a rework candidate.
- Built: /tools/gutter-cleaning-price-calculator/ (linear feet by story at per-foot rates, condition 1/1.2/1.5, steep roof 1.15, downspout flushing per downspout, flat add-ons for roof blow-off $100, guard check $40, minor resealing $75, $125 minimum). Defaults: 150 ft single story at $1.10/ft = $165, in line with Angi's $168 national average. Benchmark band per story: 1 story $0.95–$1.25, 2 stories $1.00–$1.85, 3 stories $1.25–$2.25. Newsletter box present on all 5 tool pages; all inline scripts pass node --check; tested in headless Chromium with no page errors.
- Pricing sources: Angi, "How Much Does Gutter Cleaning Cost? [2026 Data]" https://www.angi.com/articles/how-much-does-gutter-cleaning-cost.htm (avg $168, range $119–$234; per linear foot by story as above; 125–200 ft typical; steep roof +15%; neglected gutters 10–50% more; downspout cleaning $50–$100). Housecall Pro, "Gutter Cleaning Price Guide 2026" https://www.housecallpro.com/?p=75328 (jobs $125–$320; $0.80–$2/linear ft; single story $100–$180, two story $150–$275, three story $250–$400+; downspout flushing $25–$75 each; roof debris blow-off $75–$200; guard check $25–$50; minor repairs/resealing $50–$150).
- Traffic: none available. No page is old enough for drop/rework decisions.
- Open items for Krish: none new. (Affiliate approvals still pending; nothing for him to do yet. Supermetrics/Search Console connector to be suggested around 4–8 weeks in, once impressions show.)
