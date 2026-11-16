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
VER = "2"
EMAIL = "jannie@hotelklippen.dk"
SOME = [("Instagram", "https://www.instagram.com/janniebuch"), ("TikTok", "https://www.tiktok.com/@janniebuch"),
        ("Facebook", "https://www.facebook.com/jannie.buch.1/"), ("LinkedIn", "https://www.linkedin.com/in/jannie-buch/"),
        ("YouTube", "https://www.youtube.com/channel/UCEDfdpfjWoxPIUrtXDjT_kg")]
NAV = [("om-jannie", "Om Jannie"), ("mine-steder", "Mine steder"), ("historier", "Historier"), ("kontakt", "Kontakt")]
IMG = "/assets/img/"


def L(path):
    # testudgaven (/_ny) ligger bag Aidas gamle .htaccess, så her bruges .html-adresser
    if BASE and path not in ("/", "") and "." not in path.rsplit("/", 1)[-1] and "#" not in path:
        return BASE + path + ".html"
    return BASE + path


def page(slug, title, desc, body, dark_top=False):
    canon = DOMAIN + "/" + slug
    nav = "".join(f'<a href="{L("/" + s)}"{" aria-current=\"page\"" if s == slug else ""}>{n}</a>' for s, n in NAV)
    ld = {"@context": "https://schema.org", "@type": "Person", "@id": DOMAIN + "/#jannie", "name": "Jannie Buch Thorborg",
          "url": DOMAIN + "/", "jobTitle": "Iværksætter og hotelejer", "email": "mailto:" + EMAIL,
          "description": "Iværksætter, IT-nørd og hotelejer på Bornholm.",
          "image": DOMAIN + IMG + "gudhjem-havn.jpg",
          "address": {"@type": "PostalAddress", "addressLocality": "Gudhjem", "addressRegion": "Bornholm", "addressCountry": "DK"},
          "knowsAbout": ["Iværksætteri", "IT", "Netværk", "Digital markedsføring", "SEO", "AI", "Hoteldrift"],
          "worksFor": [{"@type": "Hotel", "name": "Klippen Hotel", "url": "https://www.hotelklippen.com"},
                       {"@type": "BarOrPub", "name": "Jylkat", "url": "https://jylkat-bar.dk"},
                       {"@type": "Store", "name": "Førder", "url": "https://foerder.dk"},
                       {"@type": "Hostel", "name": "Therns Hostel", "url": "https://www.therns.dk"}],
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
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{canon}">
<meta property="og:image" content="{DOMAIN}{IMG}gudhjem-havn.jpg"><meta property="og:locale" content="da_DK">
<meta name="theme-color" content="#22392c">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%2322392c'/%3E%3Ctext x='32' y='43' font-family='Georgia,serif' font-weight='700' font-size='28' fill='%23e6dccb' text-anchor='middle'%3EJB%3C/text%3E%3C/svg%3E">
<link rel="preload" href="{L('/assets/fonts/source-serif.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{L('/assets/site.css')}?v={VER}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body{' class="dark-top"' if dark_top else ''}>
<a class="skip" href="#indhold">Gå til indhold</a>
<header class="top"><div class="wrap">
<a class="brand" href="{L('/')}"><span class="mono">JBT</span><span class="name">Jannie Buch Thorborg</span></a>
<nav aria-label="Menu">{nav}</nav>
</div></header>
<main id="indhold">
{body}
</main>
<footer><div class="wrap">
<div class="fbig"><p class="fname">Jannie Buch Thorborg</p><p>Iværksætter, IT-nørd og hotelejer.<br>Gudhjem, Bornholm · 55°12′N 14°58′Ø</p></div>
<div><p class="flabel">Følg med</p><div class="some">{some}</div></div>
<div><p class="flabel">Skriv til mig</p><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
</div></footer>
<script>
(function(){{var h=document.querySelector('.top');if(!h)return;var f=function(){{h.classList.toggle('scrolled',window.scrollY>40)}};f();addEventListener('scroll',f,{{passive:true}});
var w=document.querySelector('[data-roles]');if(!w||matchMedia('(prefers-reduced-motion: reduce)').matches)return;
var r=w.getAttribute('data-roles').split('|'),i=0;setInterval(function(){{i=(i+1)%r.length;w.classList.add('out');setTimeout(function(){{w.textContent=r[i];w.classList.remove('out')}},280)}},2400)}})();
</script>
<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token": "{CF_TOKEN}"}}'></script>
</body>
</html>
"""


# ---------- indhold ----------
PLACES = [
    dict(n="Klippen Hotel", k="Hoteller i Gudhjem", img=IMG + "klippen-terrasse.jpg", alt="Terrassen på Klippen Hotel med udsigt over Østersøen",
         d="Tre særskilte overnatningssteder i Gudhjem – Grevens Dal, Therns og Skt. Jørgens Gaard – under samme tag. Alle tre er renoveret i 2026.",
         b="Besøg Klippen Hotel", u="https://www.hotelklippen.com/"),
    dict(n="Jylkat", k="Baren ved havnen", img="https://jylkat-bar.dk/media/2026/09/Jylkat20aften20hygge20.jpg", alt="Aftenstemning på Jylkat i Gudhjem",
         d="En afslappet bar ved Gudhjem Havn med cocktails, vin og barmad – og musikbingo, når mørket falder på.",
         b="Besøg Jylkat", u="https://jylkat-bar.dk/"),
    dict(n="Førder", k="Butik og reception", img="https://foerder.dk/onewebmedia/Udefra.jpg", alt="Førder i Brøddegade 28, Gudhjem",
         d="Butik med bornholmske varer i et gammelt bindingsværkshus – og fælles reception for alle stederne.",
         b="Besøg Førder", u="https://foerder.dk/"),
    dict(n="Therns Hostel", k="Vandrerhjemmet", img="", alt="",
         d="Vandrerhjemmet i Gudhjem – et enkelt sted at sove tæt på havnen og klipperne.",
         b="Besøg Therns Hostel", u="https://www.therns.dk/"),
    dict(n="Det Gamle Bryggeri", k="Sommerhuset", img="", alt="",
         d="Vores store røde sommerhus i Bryggerstræde – det gamle bryggeri midt i Gudhjem. Det kan lejes til ferie med familie og venner.",
         b="Spørg om leje", u="mailto:jannie@hotelklippen.dk?subject=Leje%20af%20Det%20Gamle%20Bryggeri"),
]
OTHER = [("Amino", "Iværksætterforum, hvor danske iværksættere deler viden og sparrer med hinanden.", "https://www.amino.dk/"),
         ("Capino", "Platform, der forbinder virksomheder med kapital og investorer.", "https://www.capino.dk/"),
         ("Saxis", "Platform for køb og salg af virksomheder.", "https://www.saxis.dk/")]
TIMELINE = [
    ("Barndom", "Blåvand", "Mine forældre drev hotel, restauranter og et diskotek. Branchen kom ind under huden tidligt."),
    ("Start", "IT og netværk", "Den tekniske verden: systemer, netværk og infrastruktur."),
    ("Barsel", "Første virksomhed", "Jeg startede min første virksomhed, mens jeg var på barsel."),
    ("Udlandet", "Tyskland, Thailand, Spanien", "Firmaer i tre lande – blandt andet møbelvirksomheden RD Furniture Asia."),
    ("2020", "Førder", "Butikken i Brøddegade åbner. Det første sted i Gudhjem."),
    ("2021", "Klippen", "Hotellet på klippen over Gudhjem havn bliver vores."),
    ("2022", "Therns og TV", "Therns og Therns Hostel kommer til, og TV-serien Buch Thorborg følger med."),
    ("2023", "Amino og Saxis", "Medejer af iværksætterforummet Amino og virksomhedsbørsen Saxis."),
    ("2025", "Skt. Jørgens Gaard", "Det gamle vandrerhjem bliver en del af Klippen Hotel."),
    ("2026", "Alt på plads", "Hotellerne er renoveret, og AI er en fast del af hverdagen."),
]
PRESS = [
    ("TV-serie", "Buch Thorborg", "Seerne fulgte os, da vi købte tre hoteller i Gudhjem og skulle nå at åbne til sæsonen.", "https://www.billedbladet.dk/kendte/danmark/tv/jannie-og-martin-buch-thorborgs-foerste-moede-saadan-havde-jesper-buch-en-finger"),
    ("Bornholms Tidende", "Arbejdsdagen starter kl. 7 og slutter kl. 22", "Om virksomheder i flere lande og et nyt erhvervseventyr i Gudhjem.", "https://tidende.dk/navne/jannie-buch-thorborgs-arbejdsdag-starter-klokken-7-og-slutter-klokken-22/124728"),
    ("Bornholms Tidende", "Butik, bar og nu også et hotel", "Om friheden ved at være iværksætter – og hvad der var på vej.", "https://tidende.dk/navne/hun-ejer-butik-bar-og-nu-ogsaa-et-hotel-i-gudhjem-snart-er-der-mere-paa-vej/113877"),
    ("TV 2", "Mystisk firma ville filme skibe i Østersøen", "Da en usædvanlig henvendelse til Klippen Hotel fik mig til at grave dybere.", "https://nyheder.tv2.dk/krimi/2026-11-02-mystisk-firma-ville-filme-skibe-i-oestersoeen-fra-bornholmsk-hotel"),
]
AI = [("Synlighed", "Søgeord, Google og AI-søgning – så gæsterne finder os."),
      ("Hjemmesider", "Hurtige sider, vi selv ejer og selv kan rette."),
      ("Gæsteinformation", "En digital gæsteguide med alt fra check-in til byens events."),
      ("Arbejdsgange", "Mails, anmeldelser og opgaver, der klarer sig mere af sig selv.")]


def place_cards(items):
    out = []
    for p in items:
        ph = (f'<div class="ph"><img src="{p["img"] if p["img"].startswith("http") else L(p["img"])}" alt="{e(p["alt"])}" loading="lazy"></div>'
              if p["img"] else f'<div class="ph type"><span>{p["n"].replace(" ", "<br>", 1)}</span></div>')
        out.append(f'<a class="place" href="{p["u"]}">{ph}<div class="tx"><p class="k">{p["k"]}</p><h3>{p["n"]}</h3><p>{p["d"]}</p><span class="go">{p["b"]}</span></div></a>')
    return "".join(out)


def press_block(dark=False):
    cards = "".join(f'<a class="press" href="{u}" rel="noopener"><p class="k">{k}</p><h3>{h}</h3><p>{d}</p><span class="go">Læs mere</span></a>' for k, h, d, u in PRESS)
    return f"""<section class="press-sec"><div class="wrap">
<div class="head"><h2>Kendt fra</h2><p class="lede" style="max-width:520px">TV, aviser og sociale medier – over 5.000 følger med på Instagram.</p></div>
<div class="press-grid">{cards}</div>
</div></section>"""


def contact_band():
    return f"""<section class="band"><div class="wrap band-in">
<h2>Har du en idé, vi skal tale om?</h2>
<div><p>Skriv til mig om samarbejde, presse eller mine virksomheder.</p>
<div class="btns"><a class="btn dark" href="mailto:{EMAIL}">{EMAIL}</a><a class="btn ghost light" href="{L('/kontakt')}">Kontakt</a></div></div>
</div></section>"""


HOME = page("", "Jannie Buch Thorborg – iværksætter og hotelejer på Bornholm",
 "Jannie Buch Thorborg er iværksætter, IT-nørd og hotelejer i Gudhjem på Bornholm – bag Klippen Hotel, baren Jylkat, butikken Førder og Therns Hostel.",
 f"""<section class="hero">
<img class="bg" src="{L(IMG + 'gudhjem-havn.jpg')}" alt="Gudhjem havn set fra luften" fetchpriority="high">
<div class="wrap hero-in">
<p class="coords">55°12′N 14°58′Ø · Gudhjem, Bornholm</p>
<h1><span>Jannie</span> <span>Buch</span> <span>Thorborg</span></h1>
<p class="roles">Jeg er <span class="role" data-roles="iværksætter|IT-nørd|hotelejer|AI-entusiast">iværksætter</span></p>
<div class="btns"><a class="btn" href="{L('/mine-steder')}">Se mine steder</a><a class="btn ghost light" href="{L('/om-jannie')}">Læs om mig</a></div>
</div>
</section>

<section class="intro"><div class="wrap intro-in">
<p class="big">Jeg startede i IT og netværk. I dag driver jeg hoteller, en bar og en butik i Gudhjem – og bruger teknik og AI til at gøre det hele bedre.</p>
<div class="intro-side">
<p>Jeg har min baggrund i IT og digital markedsføring og bruger den forståelse i alt, jeg bygger. Sammen med mit team udvikler jeg steder og virksomheder, især i Gudhjem, med fokus på teknik, udvikling og drift.</p>
<p>Det, der binder det hele sammen, er nysgerrigheden og lysten til at bygge noget, der føles rigtigt.</p>
</div>
</div></section>

<section class="places-sec"><div class="wrap">
<div class="head"><h2>Mine steder på Bornholm</h2><a class="more" href="{L('/mine-steder')}">Alle steder og virksomheder</a></div>
<div class="places">{place_cards(PLACES)}</div>
</div></section>

<section class="road-sec"><div class="wrap">
<h2>Fra Blåvand til Gudhjem</h2>
<ol class="road">{''.join(f'<li><span class="yr">{y}</span><h3>{h}</h3><p>{t}</p></li>' for y, h, t in TIMELINE)}</ol>
</div></section>

<section class="ai"><div class="wrap ai-in">
<div><h2>AI i hverdagen</h2>
<p>Jeg bruger en stor del af min tid på at optimere mine egne virksomheder med AI. Ikke som legetøj, men på helt konkrete opgaver.</p></div>
<ul class="ai-list">{''.join(f'<li><span class="chk" aria-hidden="true"></span><div><h3>{h}</h3><p>{t}</p></div></li>' for h, t in AI)}</ul>
</div></section>

<section class="biz"><div class="wrap">
<div class="head"><h2>Også medejer af</h2><a class="more" href="{L('/mine-steder')}">Alle mine virksomheder</a></div>
<div class="trio">{''.join(f'<a href="{u}" rel="noopener"><h3>{n} ↗</h3><p>{d}</p></a>' for n, d, u in OTHER)}</div>
</div></section>

<section class="quote"><div class="wrap">
<blockquote><p>”Det, jeg godt kan lide, er friheden, og at jeg kan styre det hele selv.”</p><cite>Jannie Buch Thorborg til Bornholms Tidende</cite></blockquote>
</div></section>


{contact_band()}""", dark_top=True)

OM = page("om-jannie", "Om Jannie – Jannie Buch Thorborg",
 "Om Jannie Buch Thorborg: opvokset med hotel og restauranter i Blåvand, IT og netværk, virksomheder i Tyskland, Thailand og Spanien – og i dag hoteller, bar og butik i Gudhjem.",
 f"""<section class="phead"><div class="wrap">
<p class="coords dark">Om Jannie</p>
<h1>Fra IT til iværksætteri</h1>
<p class="lede">Jeg er iværksætteren, der aldrig rigtig har holdt mig til én branche. Fra netværk og systemer til møbler, markedsføring og i dag hoteldrift på Bornholm. Den røde tråd er nysgerrighed på, hvordan ting hænger sammen – og lyst til at bygge dem selv.</p>
</div></section>
<section><div class="wrap split">
<div class="photo"><img src="{L(IMG + 'solnedgang.jpg')}" alt="Solnedgang over Østersøen set fra Gudhjem" loading="lazy"></div>
<div class="steps">
<div><h3>Hotelbranchen i blodet</h3><p>Da jeg var lille, drev mine forældre i en periode sæsonforretninger i Blåvand: et hotel, to restauranter og et populært diskotek. Så hotel- og restaurationsbranchen kom ind under huden fra en tidlig alder.</p></div>
<div><h3>IT og netværk</h3><p>Jeg startede min karriere i IT-branchen, hvor jeg arbejdede med netværk og teknik. Den tekniske forståelse er stadig en del af måden, jeg griber nye projekter an på: Jeg kan lide at forstå systemet, før jeg bygger videre på det.</p></div>
<div><h3>Iværksætter – i flere lande</h3><p>Min første virksomhed startede jeg, mens jeg var på barsel. Siden har jeg startet firmaer i Tyskland, Thailand og Spanien – blandt andet møbelvirksomheden RD Furniture Asia og udlejning af luksusboliger i Spanien.</p></div>
<div><h3>Digital markedsføring og SEO</h3><p>Undervejs har jeg opbygget erfaring med digital markedsføring og SEO – hvordan man gør en virksomhed synlig og fortæller dens historie, så den bliver hørt.</p></div>
<div><h3>AI i hverdagen</h3><p>Jeg bruger en stor del af min tid på at optimere mine egne virksomheder med AI: synlighed, hjemmesider, gæsteinformation og arbejdsgange. Konkrete områder, hvor jeg løbende afprøver, hvordan teknologien kan gøre hverdagen lettere.</p></div>
<div><h3>Medejer af flere virksomheder</h3><p>Jeg er desuden medejer af Amino, Capino og Saxis og bruger min brede erfaring til at være med, hvor der er noget nyt at bygge.</p></div>
<div><h3>Gudhjem</h3><p>I 2020 åbnede jeg Førder i Brøddegade, fordi jeg simpelthen elsker byen og dens kuperede omgivelser. Året efter fulgte Klippen, og i 2022 kunne man følge os i TV-serien Buch Thorborg, mens vi gjorde tre hoteller klar til sæsonen.</p></div>
</div>
</div></section>
<section class="road-sec"><div class="wrap">
<h2>Hverdagen på Bornholm</h2>
<p class="lede narrow">I dag arbejder jeg med Klippen Hotel i Gudhjem, som samler tre særskilte overnatningssteder – Grevens Dal, Therns og Skt. Jørgens Gaard. Jeg står også bag baren Jylkat ved Gudhjem Havn, butikken og den fælles reception Førder og Therns Hostel.</p>
<ol class="road five">{''.join(f'<li><span class="yr">{y}</span><h3>{h}</h3><p>{t}</p></li>' for y, h, t in TIMELINE[4:])}</ol>
<div class="btns"><a class="btn" href="{L('/mine-steder')}">Se stederne</a></div>
</div></section>
{contact_band()}""")

STEDER = page("mine-steder", "Mine steder – Jannie Buch Thorborg",
 "Stederne Jannie Buch Thorborg er med til at skabe på Bornholm: Klippen Hotel, baren Jylkat, butikken Førder og Therns Hostel i Gudhjem – og Amino, Capino og Saxis.",
 f"""<section class="phead"><div class="wrap">
<p class="coords dark">Mine steder</p>
<h1>Stederne jeg er med til at skabe</h1>
<p class="lede">Hvert sted har sit eget udtryk og sin egen historie. Det, de har til fælles, er at jeg udvikler dem sammen med mit team.</p>
</div></section>
<section class="places-sec"><div class="wrap"><div class="places">{place_cards(PLACES)}</div></div></section>
<section><div class="wrap">
<h2>Klippen Hotel – tre steder, hver sin identitet</h2>
<div class="trio">
<a href="https://www.hotelklippen.com/grevens-dal-gudhjem"><h3>Grevens Dal</h3><p>Hotellet på klippen med udsigt over havnen og Østersøen.</p></a>
<a href="https://www.hotelklippen.com/therns-hotel-gudhjem"><h3>Therns</h3><p>Et af de tre overnatningssteder under Klippen Hotel i Gudhjem.</p></a>
<a href="https://www.hotelklippen.com/skt-joergens-gaard-gudhjem"><h3>Skt. Jørgens Gaard</h3><p>Det tidligere vandrerhjem, nu en del af Klippen Hotel.</p></a>
</div></div></section>
<section class="ai"><div class="wrap">
<h2>Uden for Bornholm</h2>
<p class="lede narrow">Jeg er også medejer af tre virksomheder, der handler om iværksættere, kapital og handel med virksomheder.</p>
<div class="trio on-dark">{''.join(f'<a href="{u}" rel="noopener"><h3>{n} ↗</h3><p>{d}</p></a>' for n, d, u in OTHER)}</div>
</div></section>
{contact_band()}""")

HIST = page("historier", "Historier – Jannie Buch Thorborg",
 "Kommende historier om iværksætteri, om stederne på Bornholm, og om hvordan Jannie bruger AI i sine egne virksomheder.",
 f"""<section class="phead"><div class="wrap">
<p class="coords dark">Historier</p>
<h1>Historier fra Bornholm og bagved</h1>
<p class="lede">Om vejen fra IT til hoteldrift, om stederne i Gudhjem og om hverdagen bag dem. De første historier er på vej.</p>
</div></section>
<section><div class="wrap">
<ol class="soon">
<li><span class="yr">Snart</span><h3>Fra IT og digital markedsføring til hoteller i Gudhjem</h3></li>
<li><span class="yr">Snart</span><h3>Hvordan Grevens Dal, Therns og Skt. Jørgens Gaard får hver deres identitet</h3></li>
<li><span class="yr">Snart</span><h3>Hverdagen bag Jylkat og Førder</h3></li>
<li><span class="yr">Snart</span><h3>Sådan bruger jeg AI i mine egne virksomheder</h3></li>
</ol>
<p class="lede" style="margin-top:36px">Følg med på <a href="https://www.instagram.com/janniebuch">Instagram</a> og <a href="https://www.linkedin.com/in/jannie-buch/">LinkedIn</a>, så du ser dem først.</p>
</div></section>""")

KONTAKT = page("kontakt", "Kontakt – Jannie Buch Thorborg",
 "Kontakt Jannie Buch Thorborg om samarbejde, presse eller hendes virksomheder på jannie@hotelklippen.dk.",
 f"""<section class="phead"><div class="wrap">
<p class="coords dark">Kontakt</p>
<h1>Skriv til mig</h1>
<p class="lede">Ved konkrete henvendelser om samarbejde, presse eller mine virksomheder kan du skrive til mig på mail.</p>
<p class="mailbig"><a href="mailto:{EMAIL}">{EMAIL}</a></p>
</div></section>
<section><div class="wrap split top">
<div><h2>Hotelophold og bordbestilling</h2><p>Spørgsmål om ophold og reservationer klares af <a href="https://www.hotelklippen.com">Klippen Hotel</a> på info@hotelklippen.dk.</p></div>
<div><h2>Følg med</h2><div class="some big">{''.join(f'<a href="{u}" rel="me noopener">{n}</a>' for n, u in SOME)}</div></div>
</div></section>""")

NOTFOUND = page("404", "Siden findes ikke – Jannie Buch Thorborg", "Siden findes ikke.",
 f"""<section class="phead"><div class="wrap"><p class="coords dark">404</p><h1>Siden findes ikke</h1>
<p class="lede">Linket virker ikke længere, eller adressen er skrevet forkert.</p>
<div class="btns"><a class="btn" href="{L('/')}">Gå til forsiden</a></div></div></section>""")


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
