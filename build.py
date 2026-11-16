"""Bygger janniebuchthorborg.dk som statiske filer i dist/.

Kør:  python3 build.py          (den rigtige side, dist/)
      python3 build.py /_ny     (testudgave, dist-_ny/)
Teksterne står i build.py. Upload: se README.md.
"""
import json, shutil, sys
from datetime import date
from pathlib import Path
from html import escape as e

ROOT = Path(__file__).parent
BASE = sys.argv[1] if len(sys.argv) > 1 else ""
DIST = ROOT / ("dist" if not BASE else "dist" + BASE.replace("/", "-"))
DOMAIN = "https://janniebuchthorborg.dk"
CF_TOKEN = "88172b9894d4401780304b7d6843ed58"   # Cloudflare Web Analytics (cookiefri)
VER = "1"
EMAIL = "jannie@hotelklippen.dk"
SOME = [("Instagram", "https://www.instagram.com/janniebuch"), ("TikTok", "https://www.tiktok.com/@janniebuch"),
        ("Facebook", "https://www.facebook.com/jannie.buch.1/"), ("LinkedIn", "https://www.linkedin.com/in/jannie-buch/")]
NAV = [("om-jannie", "Om Jannie"), ("mine-steder", "Mine steder"), ("historier", "Historier"), ("kontakt", "Kontakt")]


def L(path):
    return BASE + path


def page(slug, title, desc, body):
    canon = DOMAIN + "/" + slug
    nav = "".join(f'<a href="{L("/" + s)}"{" aria-current=\"page\"" if s == slug else ""}>{n}</a>' for s, n in NAV)
    ld = {"@context": "https://schema.org", "@type": "Person", "@id": DOMAIN + "/#jannie", "name": "Jannie Buch Thorborg",
          "url": DOMAIN + "/", "jobTitle": "Iværksætter og hotelejer", "email": "mailto:" + EMAIL,
          "description": "Iværksætter, IT-nørd og hotelejer på Bornholm.",
          "address": {"@type": "PostalAddress", "addressLocality": "Gudhjem", "addressRegion": "Bornholm", "addressCountry": "DK"},
          "worksFor": [{"@type": "Hotel", "name": "Klippen Hotel", "url": "https://www.hotelklippen.com"},
                       {"@type": "BarOrPub", "name": "Jylkat", "url": "https://jylkat-bar.dk"},
                       {"@type": "Store", "name": "Førder", "url": "https://foerder.dk"}],
          "sameAs": [u for _, u in SOME]}
    robots = '<meta name="robots" content="noindex">\n' if BASE or slug == "404" else ""
    some = "".join(f'<a href="{u}" rel="me noopener">{n}</a>' for n, u in SOME)
    return f"""<!DOCTYPE html>
<html lang="da">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{robots}<link rel="canonical" href="{canon}">
<meta property="og:type" content="profile"><meta property="og:site_name" content="Jannie Buch Thorborg">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{canon}"><meta property="og:locale" content="da_DK">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%23a8452a'/%3E%3Ctext x='32' y='43' font-family='Georgia,serif' font-size='30' fill='%23fff' text-anchor='middle'%3EJB%3C/text%3E%3C/svg%3E">
<link rel="preload" href="{L('/assets/fonts/source-serif.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{L('/assets/site.css')}?v={VER}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<header class="top"><div class="wrap">
<a class="brand" href="{L('/')}">Jannie Buch Thorborg</a>
<nav>{nav}</nav>
</div></header>
<main>
{body}
</main>
<footer><div class="wrap">
<div><p class="fname">Jannie Buch Thorborg</p><p>Iværksætter, IT-nørd og hotelejer på Bornholm.</p></div>
<div><p class="flabel">Følg med</p><div class="some">{some}</div></div>
<div><p class="flabel">Kontakt</p><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
</div></footer>
<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token": "{CF_TOKEN}"}}'></script>
</body>
</html>
"""


PLACES = [("Klippen Hotel", "Hoteller i Gudhjem", "Klippen Hotel samler tre særskilte overnatningssteder i Gudhjem: Grevens Dal, Therns og Skt. Jørgens Gaard.", "Besøg Klippen Hotel", "https://www.hotelklippen.com/"),
          ("Jylkat", "Baren", "Jylkat er en afslappet bar ved Gudhjem Havn, som Jannie står bag.", "Besøg Jylkat", "https://jylkat-bar.dk/"),
          ("Førder", "Butikken og receptionen", "Førder er butik og fælles reception for stederne på Bornholm.", "Besøg Førder", "https://foerder.dk/"),
          ("Therns Hostel", "Vandrerhjemmet", "Jeg ejer også Therns Hostel.", "Besøg Therns Hostel", "https://www.therns.dk/")]
OTHER = [("Amino", "Iværksætterforum, hvor danske iværksættere deler viden og sparrer med hinanden.", "https://www.amino.dk/"),
         ("Capino", "Platform, der forbinder virksomheder med kapital og investorer.", "https://www.capino.dk/"),
         ("Saxis", "Platform for køb og salg af virksomheder.", "https://www.saxis.dk/")]
ROAD = [("IT og netværk", "Startede i den tekniske verden, med systemer og infrastruktur."),
        ("RD Furniture Asia", "Stiftede egen møbelvirksomhed og lærte at bygge forretning fra bunden."),
        ("Digital markedsføring", "Arbejdede med synlighed, SEO og hvordan gode historier når ud."),
        ("Steder på Bornholm", "I dag hoteldrift, bar og butik, sammen med flere andre virksomheder.")]


def cta():
    return f"""<section class="band"><div class="wrap narrow center">
<h2>Samarbejde eller presse?</h2>
<p>Skriv til mig, hvis du har en konkret idé til et samarbejde eller en presseforespørgsel.</p>
<div class="btns center"><a class="btn" href="{L('/kontakt')}">Gå til kontakt</a></div></div></section>"""


HOME = page("", "Jannie Buch Thorborg – iværksætter og hotelejer på Bornholm",
 "Jannie Buch Thorborg er iværksætter, IT-nørd og hotelejer i Gudhjem på Bornholm – bag Klippen Hotel, baren Jylkat og butikken Førder.",
 f"""<section class="hero"><div class="wrap narrow">
<p class="eyebrow">Bornholm · Iværksætter · IT-nørd</p>
<h1>Jannie Buch Thorborg</h1>
<p class="tagline">Iværksætter, IT-nørd og hotelejer på Bornholm.</p>
<p>Jeg har min baggrund i IT og digital markedsføring, og bruger den forståelse i alt, jeg bygger i dag. Jeg interesserer mig meget for AI og bruger en stor del af min tid på at optimere mine egne virksomheder med det, blandt andet synlighed, hjemmesider, gæsteinformation og arbejdsgange. Sammen med mit team udvikler jeg steder og virksomheder, især i Gudhjem, med fokus på teknik, udvikling og drift.</p>
<div class="btns"><a class="btn" href="{L('/om-jannie')}">Læs om Jannie</a><a class="btn ghost" href="{L('/mine-steder')}">Se mine steder</a></div>
</div></section>
<section><div class="wrap">
<p class="big">Jeg startede med IT og netværk. I dag er jeg med i flere forskellige virksomheder, fra en møbelvirksomhed jeg stiftede i Asien til hoteller, en bar og en butik på Bornholm. Det, der binder det hele sammen, er nysgerrigheden og lysten til at bygge noget, der føles rigtigt.</p>
<dl class="facts"><div><dt>Baggrund</dt><dd>IT, netværk og digital markedsføring</dd></div><div><dt>I dag</dt><dd>Hoteldrift, bar og butik i Gudhjem</dd></div><div><dt>Også med i</dt><dd>Flere virksomheder på tværs af brancher</dd></div></dl>
</div></section>
<section class="soft"><div class="wrap">
<p class="eyebrow">Mine steder</p><h2>Det jeg er med til at skabe på Bornholm</h2>
<div class="cards">{''.join(f'<a class="card" href="{u}"><span class="num">0{i}</span><h3>{n}</h3><p>{d}</p></a>' for i, (n, _, d, _, u) in enumerate(PLACES[:3], 1))}</div>
<div class="btns"><a class="btn ghost" href="{L('/mine-steder')}">Se alle stederne</a></div>
</div></section>
<section><div class="wrap">
<p class="eyebrow">Vejen hertil</p><h2>Fra IT til virksomheder</h2>
<ol class="road">{''.join(f'<li><h3>{h}</h3><p>{t}</p></li>' for h, t in ROAD)}</ol>
</div></section>
{cta()}""")

OM = page("om-jannie", "Om Jannie – Jannie Buch Thorborg",
 "Om Jannie Buch Thorborg: fra IT og netværk til RD Furniture Asia, digital markedsføring og i dag hoteldrift i Gudhjem. Medejer af Amino, Capino og Saxis.",
 f"""<section class="hero"><div class="wrap narrow">
<p class="eyebrow">Om Jannie</p><h1>Fra IT til iværksætteri</h1>
<p class="tagline">Jeg er Jannie Buch Thorborg, iværksætteren, der aldrig rigtig har holdt mig til én branche.</p>
<p>Fra netværk og systemer til møbler, markedsføring og i dag hoteldrift på Bornholm, den røde tråd er nysgerrighed på hvordan ting hænger sammen, og lyst til at bygge dem selv.</p>
</div></section>
<section><div class="wrap narrow">
<p class="eyebrow">Baggrund</p><h2>Fra teknik til egne virksomheder</h2>
<div class="steps">
<div><h3>IT og netværk</h3><p>Jeg startede min karriere i IT-branchen, hvor jeg arbejdede med netværk og teknik. Den tekniske forståelse er stadig en del af måden, jeg griber nye projekter an på, jeg kan lide at forstå systemet, før jeg bygger videre på det.</p></div>
<div><h3>RD Furniture Asia</h3><p>Springet til iværksætteri kom med RD Furniture Asia, en virksomhed jeg stiftede.</p></div>
<div><h3>Digital markedsføring og SEO</h3><p>Undervejs har jeg opbygget erfaring med digital markedsføring og SEO, hvordan man gør en virksomhed synlig og fortæller dens historie, så den bliver hørt.</p></div>
<div><h3>AI i hverdagen</h3><p>Jeg interesserer mig meget for AI og bruger en stor del af min tid på at optimere mine egne virksomheder med det. Det handler om synlighed, hjemmesider, gæsteinformation og arbejdsgange, konkrete områder, hvor jeg løbende afprøver, hvordan teknologien kan gøre hverdagen lettere.</p></div>
<div><h3>Medejer af flere virksomheder</h3><p>I dag er jeg desuden medejer af Amino, Capino og Saxis, og bruger min brede erfaring til at være med, hvor der er noget nyt at bygge.</p></div>
</div></div></section>
<section class="soft"><div class="wrap narrow">
<p class="eyebrow">I dag</p><h2>Hverdagen på Bornholm</h2>
<p>I dag arbejder jeg blandt andet med Klippen Hotel i Gudhjem, som samler tre særskilte overnatningssteder, Grevens Dal, Therns og Skt. Jørgens Gaard. Jeg står også bag baren Jylkat ved Gudhjem Havn og butikken og den fælles reception Førder.</p>
<div class="btns"><a class="btn" href="{L('/mine-steder')}">Udforsk stederne</a></div>
</div></section>""")

STEDER = page("mine-steder", "Mine steder – Jannie Buch Thorborg",
 "Stederne Jannie Buch Thorborg er med til at skabe på Bornholm: Klippen Hotel, baren Jylkat, butikken Førder og Therns Hostel i Gudhjem.",
 f"""<section class="hero"><div class="wrap narrow">
<p class="eyebrow">Mine steder</p><h1>Stederne jeg er med til at skabe på Bornholm</h1>
<p class="tagline">Hvert sted har sit eget udtryk og sin egen historie. Det, de har til fælles, er at jeg udvikler dem sammen med mit team.</p>
</div></section>
<section><div class="wrap">
<div class="places">{''.join(f'<article><span class="num">0{i}</span><div><p class="eyebrow">{k}</p><h2>{n}</h2><p>{d}</p><a class="btn ghost" href="{u}">{b}</a></div></article>' for i, (n, k, d, b, u) in enumerate(PLACES, 1))}</div>
</div></section>
<section class="soft"><div class="wrap">
<p class="eyebrow">Under Klippen Hotel</p><h2>Tre steder, hver sin identitet</h2>
<p class="intro">Klippen Hotel i Gudhjem samler tre særskilte steder, som hver har fået lov til at holde fast i deres eget udtryk.</p>
<div class="cards">
<a class="card" href="https://www.hotelklippen.com/grevens-dal-gudhjem"><h3>Grevens Dal</h3><p>Et af de tre overnatningssteder i Gudhjem under Klippen Hotel.</p></a>
<a class="card" href="https://www.hotelklippen.com/therns-hotel-gudhjem"><h3>Therns</h3><p>Et af de tre overnatningssteder i Gudhjem under Klippen Hotel.</p></a>
<a class="card" href="https://www.hotelklippen.com/skt-joergens-gaard-gudhjem"><h3>Skt. Jørgens Gaard</h3><p>Et af de tre overnatningssteder i Gudhjem under Klippen Hotel.</p></a>
</div></div></section>
<section><div class="wrap">
<p class="eyebrow">Uden for Bornholm</p><h2>Andre virksomheder</h2>
<p class="intro">Jeg er også medejer af Amino, Capino og Saxis.</p>
<div class="cards">{''.join(f'<a class="card" href="{u}" rel="noopener"><h3>{n} ↗</h3><p>{d}</p></a>' for n, d, u in OTHER)}</div>
</div></section>""")

HIST = page("historier", "Historier – Jannie Buch Thorborg",
 "Kommende historier om iværksætteri, om stederne på Bornholm, og om hvordan Jannie bruger AI i sine egne virksomheder.",
 f"""<section class="hero"><div class="wrap narrow">
<p class="eyebrow">Historier</p><h1>Historier fra Bornholm og bagved</h1>
<p class="tagline">Historier om vejen fra IT til hoteldrift, om stederne på Bornholm, og om hverdagen bag dem.</p>
</div></section>
<section><div class="wrap narrow">
<h2>På vej</h2>
<p>Der er endnu ingen udgivne historier. Her er de første, som er på vej:</p>
<ul class="soon">
<li>Fra IT og digital markedsføring til hoteller i Gudhjem</li>
<li>Hvordan Grevens Dal, Therns og Skt. Jørgens Gaard får hver deres identitet</li>
<li>Hverdagen bag Jylkat og Førder</li>
<li>Hvordan jeg bruger AI til at optimere mine egne virksomheder, hjemmesider, synlighed og arbejdsgange</li>
</ul>
</div></section>""")

KONTAKT = page("kontakt", "Kontakt – Jannie Buch Thorborg",
 "Kontakt Jannie Buch Thorborg om samarbejde, presse eller hendes virksomheder på jannie@hotelklippen.dk.",
 f"""<section class="hero"><div class="wrap narrow">
<p class="eyebrow">Kontakt</p><h1>Kontakt Jannie Buch Thorborg</h1>
<p class="tagline">Ved konkrete henvendelser om samarbejde, presse eller mine virksomheder kan du skrive til mig på <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
</div></section>
<section><div class="wrap narrow">
<dl class="facts two">
<div><dt>E-mail</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
<div><dt>Hotelophold og reservationer</dt><dd>Spørgsmål om hotelophold og reservationer håndteres af <a href="https://www.hotelklippen.com">Klippen Hotel</a>.</dd></div>
</dl>
<h2 style="margin-top:48px">Følg med</h2>
<div class="some big">{''.join(f'<a href="{u}" rel="me noopener">{n}</a>' for n, u in SOME)}</div>
</div></section>""")

NOTFOUND = page("404", "Siden findes ikke – Jannie Buch Thorborg", "Siden findes ikke.",
 f"""<section class="hero"><div class="wrap narrow center"><h1>Siden findes ikke</h1>
<p class="tagline">Linket virker ikke længere, eller adressen er skrevet forkert.</p>
<div class="btns center"><a class="btn" href="{L('/')}">Gå til forsiden</a></div></div></section>""")


if __name__ == "__main__":
    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(ROOT / "site", DIST)
    if BASE:
        (DIST / ".htaccess").unlink()
    for name, html in [("index", HOME), ("om-jannie", OM), ("mine-steder", STEDER), ("historier", HIST), ("kontakt", KONTAKT), ("404", NOTFOUND)]:
        (DIST / f"{name}.html").write_text(html, encoding="utf-8")
    today = date.today().isoformat()
    urls = "".join(f"<url><loc>{DOMAIN}/{s}</loc><lastmod>{today}</lastmod></url>" for s in ["", "om-jannie", "mine-steder", "historier", "kontakt"])
    (DIST / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + urls + "</urlset>\n", encoding="utf-8")
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /_ny/\nDisallow: /_aida-backup/\n\nSitemap: {DOMAIN}/sitemap.xml\n", encoding="utf-8")
    if not BASE:
        files = sorted(str(p.relative_to(DIST)) for p in DIST.rglob("*") if p.is_file())
        (ROOT / "filer.txt").write_text("\n".join(files) + "\n", encoding="utf-8")
    print("bygget", DIST.name)
