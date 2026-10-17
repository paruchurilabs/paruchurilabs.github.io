"""Builds paruchurilabs.com/tools/ from template.html + tools.json.

Run from the repo root:  python3 _tools_src/build.py
Writes tools/<slug>/index.html for every tool, tools/index.html (hub),
sitemap.xml, and makes sure robots.txt points at the sitemap.
To add a tool: add its calculator logic to the TOOLS object in template.html
(same key), add its entry to tools.json, then run this script.
"""
import html, json, os, re, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "_tools_src")
SITE = "https://paruchurilabs.com"
esc = lambda s: html.escape(s, quote=True)

tools = json.load(open(os.path.join(SRC, "tools.json")))
tpl = open(os.path.join(SRC, "template.html")).read()

# Booked & Busy newsletter signup. beehiiv's embed code lives in
# _tools_src/newsletter_embed.html; every tool page (including new ones) shows
# the signup box automatically. If that file is missing, no box is shown.
embed_p = os.path.join(SRC, "newsletter_embed.html")
embed = open(embed_p).read().strip() if os.path.exists(embed_p) else ""
NEWSLETTER_BAND = (
    '\n      <div class="band" id="newsletter-box">'
    '<h3>Get one pricing tip a week</h3>'
    '<p><strong>Booked &amp; Busy</strong> is a free weekly email for home service business owners: '
    'one tip, one copy-paste script, one tool. Under 3 minutes to read.</p>'
    f'<div id="newsletter-slot">{embed}</div></div>') if embed else ""
style = re.search(r"<style>\n/\* Layout.*?</style>", tpl, re.S).group(0)


def nav(current):
    return "".join(
        f'<a href="/tools/{t["slug"]}/"{" aria-current=\"page\"" if t["key"] == current else ""}>{esc(t["nav"])}</a>'
        for t in tools)


def jsonld(t, url):
    data = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebApplication", "name": t["h1"], "url": url,
         "applicationCategory": "BusinessApplication", "operatingSystem": "Any",
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
         "publisher": {"@type": "Organization", "name": "Paruchuri Labs", "url": SITE + "/"}},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in t["faq"]]}]}
    return json.dumps(data).replace("</", "<\\/")


def notes(t):
    how = "".join(f"<li>{esc(x)}</li>" for x in t["how"])
    faq = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in t["faq"])
    return (f'<div><h2 class="nh">How the price is figured</h2><ul>{how}</ul></div>'
            f'<div><h2 class="nh">Common questions</h2>{faq}</div>')


for t in tools:
    url = f'{SITE}/tools/{t["slug"]}/'
    page = tpl
    for k, v in {"TITLE": esc(t["title"]), "DESC": esc(t["desc"]), "URL": url,
                 "JSONLD": jsonld(t, url), "NAV": nav(t["key"]), "H1": esc(t["h1"]),
                 "LEDE": esc(t["lede"]), "NOTES": notes(t), "KEY": t["key"],
                 "NEWSLETTER": NEWSLETTER_BAND}.items():
        page = page.replace("{{" + k + "}}", v)
    assert "{{" not in page, t["key"]
    out = os.path.join(ROOT, "tools", t["slug"])
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, "index.html"), "w").write(page)

# hub page
cards = "".join(
    f'<a class="hub-card" href="/tools/{t["slug"]}/"><b>{esc(t["h1"])}</b><span>{esc(t["desc"].split(". ", 1)[-1])}</span></a>'
    for t in tools)
hub_desc = "Free pricing calculators for pressure washing, window cleaning, lawn care, house cleaning and other service businesses. Set your rates, compare to typical US prices, and send a quote."
hub = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Field Quote Kit: Free Pricing Calculators for Service Businesses</title>
<meta name="description" content="{esc(hub_desc)}">
<link rel="canonical" href="{SITE}/tools/">
<style>:root{{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0;font:14px system-ui,sans-serif}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
{style}
<style>
.hub{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;margin-top:26px}}
.hub-card{{display:grid;gap:6px;text-decoration:none;color:var(--ink);background:var(--panel);border:1px solid var(--line);border-left:6px solid var(--accent);border-radius:4px;padding:18px}}
.hub-card b{{font-family:var(--f-display);font-size:24px;text-transform:uppercase;letter-spacing:.02em}}
.hub-card span{{color:var(--muted)}}
.hub-card:hover b{{text-decoration:underline}}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="brand">
      <a class="kit" href="/tools/">Field <span>Quote</span> Kit</a>
      <p>Free pricing tools for service businesses, by <a href="/" style="color:inherit">Paruchuri Labs</a>.</p>
    </div>
  </header>
  <section class="tool-head">
    <h1>Free pricing calculators for service businesses</h1>
    <p>Each calculator lets you set your own rates, shows how your price compares to typical US rates, and gives you a quote you can copy into a text or email.</p>
  </section>
  <div class="hub">{cards}</div>
  <footer>Built by <a href="/">Paruchuri Labs</a>, web design for local businesses.</footer>
</div>
</body>
</html>
'''
open(os.path.join(ROOT, "tools", "index.html"), "w").write(hub)

# sitemap: public pages only (previews stay out)
today = datetime.date.today().isoformat()
urls = [SITE + "/", SITE + "/tools/"] + [f'{SITE}/tools/{t["slug"]}/' for t in tools]
samples = os.path.join(ROOT, "samples")
if os.path.isdir(samples):
    urls += [f"{SITE}/samples/{d}/" for d in sorted(os.listdir(samples))
             if os.path.isfile(os.path.join(samples, d, "index.html"))]
xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
xml += "".join(f"  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls)
xml += "</urlset>\n"
open(os.path.join(ROOT, "sitemap.xml"), "w").write(xml)

robots_p = os.path.join(ROOT, "robots.txt")
robots = open(robots_p).read() if os.path.exists(robots_p) else "User-agent: *\n"
if "Sitemap:" not in robots:
    robots = robots.rstrip("\n") + f"\n\nSitemap: {SITE}/sitemap.xml\n"
    open(robots_p, "w").write(robots)

print("built", len(tools), "tools;", len(urls), "sitemap urls")
