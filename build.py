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
VER = "7"
EMAIL = "jannie@hotelklippen.dk"
SOME = [("Instagram", "https://www.instagram.com/janniebuch"), ("TikTok", "https://www.tiktok.com/@janniebuch"),
        ("Facebook", "https://www.facebook.com/jannie.buch.1/"), ("LinkedIn", "https://www.linkedin.com/in/jannie-buch/"),
        ("X", "https://x.com/janniebuchace"), ("YouTube", "https://www.youtube.com/channel/UCEDfdpfjWoxPIUrtXDjT_kg")]
NAV = [("om-jannie", "Om Jannie"), ("mine-steder", "Mine steder"), ("historier", "Historier"), ("presse", "Presse"), ("kontakt", "Kontakt")]
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
          "image": DOMAIN + IMG + "jannie-australien.jpg",
          "knowsAbout": ["Iværksætteri", "IT", "Netværk", "Digital markedsføring", "SEO", "AI", "Hoteldrift"],
          "worksFor": [{"@type": "Hotel", "name": "Klippen Hotel", "url": "https://www.hotelklippen.com"},
                       {"@type": "BarOrPub", "name": "Jylkat", "url": "https://jylkat-bar.dk"},
                       {"@type": "Store", "name": "Førder", "url": "https://foerder.dk"},
                       {"@type": "Hostel", "name": "Therns Hostel", "url": "https://therns.dk"}],
          "sameAs": [u for _, u in SOME]}
    robots = '<meta name="robots" content="noindex">\n' if BASE or slug == "404" else ""
    some = "".join(f'<li><a href="{u}" rel="me noopener">{n}</a></li>' for n, u in SOME)
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
<link rel="preload" href="{L('/assets/fonts/source-sans.woff2')}" as="font" type="font/woff2" crossorigin>
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
<div class="fbig"><p class="fname">Jannie Buch Thorborg</p><p>Iværksætter, IT-nørd og hotelejer.</p></div>
<div><p class="flabel">Følg med</p><ul class="slist">{some}</ul></div>
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
    dict(n="Klippen Grevens Dal", k="Klippen Hotel", img="https://static.wixstatic.com/media/5cff14_1029a7b3bf0649f0ad2d07a48d6e06e7~mv2.jpg/v1/fill/w_1000,h_750,q_85/grevens-dal.jpg", alt="Klippen Grevens Dal med udsigt over Østersøen",
         d="Hotellet på klippen over Gudhjem – med havudsigt fra terrassen og morgenmad med udsigt.",
         b="Se Grevens Dal", u="https://www.hotelklippen.com/grevens-dal-gudhjem"),
    dict(n="Klippen Therns", k="Klippen Hotel", img="https://static.wixstatic.com/media/5cff14_b65fcc0177b94fbdbe156d2e14535509~mv2.jpeg/v1/fill/w_1000,h_750,q_85/therns.jpg", alt="Klippen Therns i Gudhjem",
         d="Det hvide hotel midt i Gudhjem, tæt på havnen, butikkerne og restauranterne.",
         b="Se Therns", u="https://www.hotelklippen.com/therns-hotel-gudhjem"),
    dict(n="Klippen Skt. Jørgens Gaard", k="Klippen Hotel", img="https://static.wixstatic.com/media/5cff14_9a2037fbb44947e8acf5610e9fca4b57~mv2.jpg/v1/fill/w_1000,h_750,q_85/skt-joergens-gaard.jpg", alt="Skt. Jørgens Gaard i Gudhjem en sommeraften",
         d="Det gamle vandrerhjem ved havnen, nu et hotel i gammel badehotelstil – med Jylkat lige uden for døren.",
         b="Se Skt. Jørgens Gaard", u="https://www.hotelklippen.com/skt-joergens-gaard-gudhjem"),
    dict(n="Jylkat", k="Baren ved havnen", img="https://jylkat-bar.dk/media/2026/09/Jylkat20aften20hygge20.jpg", alt="Aftenstemning på Jylkat i Gudhjem",
         d="En afslappet bar ved Gudhjem Havn med cocktails, vin og barmad – og musikbingo, når mørket falder på.",
         b="Besøg Jylkat", u="https://jylkat-bar.dk/"),
    dict(n="Førder", k="Butik og reception", img="https://foerder.dk/onewebmedia/Udefra.jpg", alt="Førder i Brøddegade 28, Gudhjem",
         d="Butik med bornholmske varer i et gammelt bindingsværkshus – og fælles reception for alle stederne.",
         b="Besøg Førder", u="https://foerder.dk/"),
    dict(n="Therns Hostel", k="Vandrerhjemmet", img="https://therns.dk/wp-content/uploads/2026/11/hostel-gudhjem-gaardhave-natur.webp", alt="Gårdhaven på Therns Hostel i Gudhjem",
         d="Vandrerhjemmet i Gudhjem – et enkelt sted at sove tæt på havnen og klipperne.",
         b="Besøg Therns Hostel", u="https://therns.dk/"),
    dict(n="Det Gamle Bryggeri", k="Sommerhuset", img="https://a0.muscache.com/im/pictures/dd9570e8-12f6-4079-a922-c1681b27099a.jpg?im_w=1200", alt="Det Gamle Bryggeri i Bryggerstræde, Gudhjem",
         d="Vores store røde sommerhus i Bryggerstræde – det gamle bryggeri midt i Gudhjem med havudsigt og egen klippe. Plads til 14, så hele familien eller vennerne kan være med.",
         b="Se huset på Airbnb", u="https://www.airbnb.dk/rooms/28063316"),
]
OTHER = [("Amino", "Iværksætterforum, hvor danske iværksættere deler viden og sparrer med hinanden.", "https://www.amino.dk/"),
         ("Capino", "Platform, der forbinder virksomheder med kapital og investorer.", "https://www.capino.dk/"),
         ("Saxis", "Platform for køb og salg af virksomheder.", "https://www.saxis.dk/"),
         ("Founderbasen", "Gratis service, hvor iværksættere finder en medstifter eller kompagnon.", "https://founderbasen.dk/")]
TIMELINE = [
    ("Barndom", "Blåvand", "Mine forældre drev hotel, restauranter og et diskotek. Branchen kom ind under huden tidligt.", ""),
    ("Start", "IT og netværk", "Den tekniske verden: systemer, netværk og infrastruktur.", ""),
    ("Barsel", "Første virksomhed", "Jeg startede min første virksomhed, mens jeg var på barsel.", ""),
    ("Udlandet", "Tyskland, Thailand, Spanien", "Firmaer i tre lande – blandt andet møbelvirksomheden RD Furniture Asia.", ""),
    ("2020", "Førder", "Butikken i Brøddegade åbner. Det første sted i Gudhjem.", "https://foerder.dk/"),
    ("2021", "Klippen", "Hotellet på klippen over Gudhjem havn bliver vores.", "https://www.hotelklippen.com/grevens-dal-gudhjem"),
    ("2022", "Therns og TV", "Therns og Therns Hostel kommer til, og TV-serien Buch Thorborg følger med.", "https://www.hotelklippen.com/therns-hotel-gudhjem"),
    ("2023", '<a href="https://www.amino.dk/">Amino</a>, <a href="https://www.capino.dk/">Capino</a> og <a href="https://www.saxis.dk/">Saxis</a>', "Medejer af iværksætterforummet Amino, kapitalplatformen Capino og virksomhedsbørsen Saxis.", ""),
    ("2025", "Skt. Jørgens Gaard og Jylkat", "Det gamle vandrerhjem bliver en del af Klippen Hotel, og Jylkat bliver baren ved havnen.", "https://jylkat-bar.dk/"),
    ("2026", "Founderbasen", "Sammen med Martin lancerer vi Founderbasen, en gratis service, hvor iværksættere finder en medstifter eller kompagnon.", "https://founderbasen.dk/"),
    ("2026", "Nyt liv i husene", "Hotellerne er renoveret, og AI er blevet en fast del af hverdagen. Vi bygger stadig videre.", ""),
    ("2027", "Fitnesscenter og restaurant", "Et nyt fitnesscenter og en ny restaurant åbner i Gudhjem.", ""),
]
def tl_item(y, h, t, u):
    hh = f'<a href="{u}">{h}</a>' if u else h
    return f'<li><span class="yr">{y}</span><h3>{hh}</h3><p>{t}</p></li>'


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
<h1>Jannie Buch Thorborg</h1>
<p class="roles">Jeg er <span class="role" data-roles="iværksætter|IT-nørd|hotelejer|AI-entusiast">iværksætter</span></p>
<div class="btns"><a class="btn" href="{L('/mine-steder')}">Se mine steder</a><a class="btn ghost light" href="{L('/om-jannie')}">Læs om mig</a></div>
</div>
</section>

<section class="intro"><div class="wrap intro-in">
<div class="me"><img src="{L(IMG + 'jannie-australien.jpg')}" alt="Jannie Buch Thorborg" loading="lazy"></div>
<div class="intro-txt"><p class="big">Jeg startede i IT og netværk. I dag driver jeg hoteller, en bar og en butik i Gudhjem – og bruger teknik og AI til at gøre det hele bedre.</p>
<div class="intro-side">
<p>Jeg har min baggrund i IT og digital markedsføring og bruger den forståelse i alt, jeg bygger. Sammen med mit team udvikler jeg steder og virksomheder, især i Gudhjem, med fokus på teknik, udvikling og drift.</p>
<p>Det, der binder det hele sammen, er nysgerrigheden og lysten til at bygge noget, der føles rigtigt.</p>
</div></div>
</div></section>

<section class="places-sec"><div class="wrap">
<div class="head"><h2>Mine steder på Bornholm</h2><a class="more" href="{L('/mine-steder')}">Alle steder og virksomheder</a></div>
<div class="places">{place_cards(PLACES)}</div>
</div></section>

<section class="road-sec"><div class="wrap">
<h2>Fra Blåvand til Gudhjem</h2>
<ol class="road">{''.join(tl_item(y, h, t, u) for y, h, t, u in TIMELINE)}</ol>
</div></section>

<section class="ai"><div class="wrap ai-in">
<div><h2>AI i hverdagen</h2>
<p>Jeg bruger en stor del af min tid på at optimere mine egne virksomheder med AI. Ikke som legetøj, men på helt konkrete opgaver.</p></div>
<ul class="ai-list">{''.join(f'<li><span class="chk" aria-hidden="true"></span><div><h3>{h}</h3><p>{t}</p></div></li>' for h, t in AI)}</ul>
</div></section>

<section class="biz"><div class="wrap">
<div class="head"><h2>Også medejer af</h2><a class="more" href="{L('/mine-steder')}">Alle mine virksomheder</a></div>
<div class="trio fire">{''.join(f'<a href="{u}" rel="noopener"><h3>{n} ↗</h3><p>{d}</p></a>' for n, d, u in OTHER)}</div>
</div></section>

<section class="quote"><div class="wrap">
<blockquote><p>”Det, jeg godt kan lide, er friheden, og at jeg kan styre det hele selv.”</p><cite>Jannie Buch Thorborg til Bornholms Tidende</cite></blockquote>
</div></section>


{contact_band()}""", dark_top=True)

OM = page("om-jannie", "Om Jannie – Jannie Buch Thorborg",
 "Om Jannie Buch Thorborg: opvokset med hotel og restauranter i Blåvand, IT og netværk, virksomheder i Tyskland, Thailand og Spanien – og i dag hoteller, bar og butik i Gudhjem.",
 f"""<section class="phead"><div class="wrap">
<h1>Fra IT til iværksætteri</h1>
<p class="lede">Jeg er iværksætteren, der aldrig rigtig har holdt mig til én branche. Fra netværk og systemer til møbler, markedsføring og i dag hoteldrift på Bornholm. Den røde tråd er nysgerrighed på, hvordan ting hænger sammen – og lyst til at bygge dem selv.</p>
</div></section>
<section><div class="wrap split">
<figure class="photo"><img src="{L(IMG + 'jannie-og-martin.jpg')}" alt="Jannie og Martin Buch Thorborg" loading="lazy"><figcaption>Med min mand, Martin.</figcaption></figure>
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
<ol class="road five">{''.join(tl_item(y, h, t, u) for y, h, t, u in TIMELINE[4:])}</ol>
<div class="btns"><a class="btn" href="{L('/mine-steder')}">Se stederne</a></div>
</div></section>
{contact_band()}""")

STEDER = page("mine-steder", "Mine steder – Jannie Buch Thorborg",
 "Stederne Jannie Buch Thorborg er med til at skabe på Bornholm: Klippen Hotel, baren Jylkat, butikken Førder og Therns Hostel i Gudhjem – og Amino, Capino og Saxis.",
 f"""<section class="phead"><div class="wrap">
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
<p class="lede narrow">Jeg står også bag fire virksomheder, der handler om iværksættere, partnere, kapital og handel med virksomheder.</p>
<div class="trio fire on-dark">{''.join(f'<a href="{u}" rel="noopener"><h3>{n} ↗</h3><p>{d}</p></a>' for n, d, u in OTHER)}</div>
</div></section>
{contact_band()}""")

POSTS = [
    dict(slug="julekalender", dato="28. november 2026", iso="2026-11-28",
         titel="Vi har tegnet Gudhjem som en gammeldags julekalender",
         intro="I år har Klippen Hotel en julekalender på nettet med 24 låger, 24 små historier fra Gudhjem og en præmie hver dag. Jeg har bygget den med AI.",
         tekst="""<p>Jeg ville gerne lave en julekalender, der ligner de gamle danske papkalendere med nisser, juletræer og julemænd. Ikke noget, der ligner AI. Noget, man får lyst til at åbne hver morgen.</p>
<p>Så det har jeg lavet til <a href="https://www.hotelklippen.com">Klippen Hotel</a>.</p>
<h2>Hele Gudhjem bag lågerne</h2>
<p>Kalenderen er en tegning af det rigtige Gudhjem med vores egne huse: hotellerne, baren <a href="https://jylkat-bar.dk/">Jylkat</a> ved havnen og butikken <a href="https://foerder.dk/">Førder</a> i Brøddegade. Der er julemusik, og lågerne åbner med en lille animation.</p>
<p>Bag hver låge er der en lille historie om nogen fra Gudhjem. Thomas skænker gløgg, Henrik står på en stige, Maiken sælger julesnaps i Førder, og Martin råber glædelig jul. Mit pindsvin Pind er også med. Det er ham, Jylkat er opkaldt efter. Og så er der Holkahesten og westien Muffi, som allerede er i gang med vægtene i vores nye fitnesscenter, før det overhovedet er færdigt.</p>
<h2>En præmie hver dag</h2>
<p>Hver dag fra 1. til 24. december er der en præmie. Det kan være gavekort til Førder, fadøl på Jylkat, brunch på Klippen Grevens Dal, en måned i fitnesscentret eller Martins nye bog. Præmierne hentes i Førder, for vi vil hellere se folk i butikken end sende pakker med posten.</p>
<p>Man er med, når man skriver sig op til vores nyhedsbrev. Så kan man også følge med i, hvad der sker hos os resten af året.</p>
<h2>AI klarer resten</h2>
<p>Jeg har bygget det hele sammen med AI, fra tegningen og lågerne til alt det, man ikke ser.</p>
<p>Hver morgen klokken 7 får dem, der har bedt om det, en mail om dagens låge. Lidt senere bliver der trukket en vinder til gårsdagens låge helt automatisk, og vinderen får en mail. Er præmien et gavekort, bliver det lavet og sendt med det samme i <a href="/historier/eget-gavekortsystem">vores eget gavekortsystem</a>.</p>
<p>Før havde sådan en kalender krævet et bureau og en programmør. Nu kunne jeg lave den selv, på vores egen måde.</p>
<p>Kalenderen åbner 1. december på <a href="https://www.hotelklippen.com/julekalender">hotelklippen.com/julekalender</a>. Du kan allerede nu skrive dig op, så du får besked, når den første låge åbner.</p>
<p>Du kan se alle mine steder <a href="/mine-steder">her</a>.</p>"""),
    dict(slug="founderbasen", dato="21. november 2026", iso="2026-11-21",
         titel="Founderbasen: hvor iværksættere finder deres forretningspartner",
         intro="Mange gode idéer bliver aldrig til noget, fordi den, der har idéen, står alene. Derfor har Martin og jeg lavet Founderbasen.",
         tekst="""<p>Jeg har aldrig bygget noget alene. Hotellerne i Gudhjem, baren, butikken – det hele er lavet sammen med andre, og først og fremmest sammen med Martin. Vi er gode til hver vores ting, og det er netop derfor, det virker.</p>
<p>Men det er svært at finde den rigtige at starte op med. Mange har en god idé, men ingen til at bygge den. Andre har en virksomhed, men står med det hele selv. Derfor har vi lavet <a href="https://founderbasen.dk/">Founderbasen</a>.</p>
<h2>Sådan virker det</h2>
<p>Founderbasen er gratis. Man opretter en profil på et par minutter og fortæller, hvad man er god til, og hvad man mangler. Har man en idé, kan man finde en <a href="https://founderbasen.dk/medstifter/">medstifter</a>. Har man en virksomhed, kan man finde en <a href="https://founderbasen.dk/kompagnon/">kompagnon</a>. Og vil man gerne være med på andres idé, kan man også det.</p>
<p>Founderbasen foreslår folk, der kan det, man selv mangler, og sender en mail, når der er et godt match. Man får først hinandens kontaktoplysninger, når begge har sagt ja, og man kan være anonym, hvis man ikke vil vise, at man søger.</p>
<h2>Vælg ikke en kopi af dig selv</h2>
<p>Det vigtigste råd, jeg kan give, er at lede efter en, der er anderledes end dig. To, der er gode til det samme, har ofte også de samme blinde vinkler. Er du god til at bygge, så find en, der kan sælge. Er du god til at sælge, så find en, der kan bygge.</p>
<p>Og tal om de svære ting fra starten: tid, ejerskab, penge og hvad der sker, hvis en af jer vil ud. På Founderbasen ligger der <a href="https://founderbasen.dk/guide/">guides</a> om netop det.</p>
<h2>AI hjælper med at blive fundet</h2>
<p>Ligesom med hotellerne bruger jeg AI til at gøre Founderbasen synlig: guides, søgeord og sider, der gør det lettere for både Google og AI-tjenester som ChatGPT at forstå, hvad siden kan.</p>
<p>Leder du selv efter en forretningspartner, så <a href="https://founderbasen.dk/opret/">opret en gratis profil</a>. Og kender du en, der går rundt med en god idé, så send dem gerne videre.</p>"""),
    dict(slug="ai-laeser-vores-anmeldelser", dato="18. november 2026", iso="2026-11-18",
         titel="AI læser alle vores anmeldelser – hver eneste dag",
         intro="Vi får anmeldelser på Google, Booking.com, Tripadvisor og mange andre steder. Jeg har bygget et dashboard med AI, der holder styr på dem alle.",
         tekst="""<p>Når man har tre hoteller under <a href="https://www.hotelklippen.com">Klippen Hotel</a>, baren <a href="https://jylkat-bar.dk/">Jylkat</a> og butikken <a href="https://foerder.dk/">Førder</a>, får man mange anmeldelser. På Google, Booking.com, Tripadvisor og flere til. Det er svært at holde øje med det hele, når man også skal passe gæsterne.</p>
<p>Så jeg byggede et dashboard med AI. Vi kalder det Gæsternes stemme.</p>
<h2>Det sker hver dag</h2>
<p>Hver dag henter AI de nye anmeldelser fra alle platformene og samler dem ét sted. Her kan vi se, hvordan det går for hvert sted, og hvordan det har udviklet sig over tid.</p>
<p>De gode anmeldelser uden kritik svarer AI selv på. Personligt, kort og forskelligt hver gang, så det lyder som os og ikke som en maskine.</p>
<p>Anmeldelser med kritik svarer AI ikke på. Dem tager vi selv, for der skal et menneske til. Men vi kan skrive svaret i dashboardet, og når en leder har godkendt det, bliver det lagt ud på platformen.</p>
<h2>De dårlige anmeldelser</h2>
<p>Hver dårlig anmeldelse bliver tjekket op mod platformens egne regler. Hvis den bryder reglerne, bliver den indberettet til platformen, og jeg får besked.</p>
<p>Det er ikke for at slippe for kritik. Den lærer vi af. Men en anmeldelse, der ikke burde være der, skal heller ikke trække ned.</p>
<h2>Hvorfor det betyder noget</h2>
<p>Anmeldelser er det første, mange gæster læser, før de booker. Når hver eneste anmeldelse bliver set og får et svar, kan gæsterne mærke, at vi lytter.</p>
<p>Og mine medarbejdere kan bruge deres tid på gæsterne i stedet for at hoppe rundt mellem en masse forskellige sider.</p>
<p>Du kan se alle mine steder <a href="/mine-steder">her</a>. Vil du høre mere om, hvordan jeg gjorde, så skriv endelig til mig.</p>"""),
    dict(slug="eget-gavekortsystem", dato="16. november 2026", iso="2026-11-16",
         titel="Jeg har bygget mit eget gavekortsystem – og det gør lidt ondt",
         intro="Jeg har solgt vores gavekort gennem Life Peaks og været rigtig glad for det. Nu har jeg bygget mit eget på en dag med AI.",
         tekst="""<p>Jeg har solgt vores gavekort gennem Life Peaks, og jeg har været rigtig glad for dem. Det har virket, de har været søde at have med at gøre, og jeg har anbefalet dem til andre.</p>
<p>Men de tager en procentdel af hvert gavekort, jeg sælger. Når man har tre hoteller, en bar, en butik og snart en restaurant, bliver det til mange penge over et år.</p>
<p>Så i dag satte jeg mig ned og byggede mit eget system sammen med AI. Det tog en dag.</p>
<h2>Det kan det</h2>
<p>Man vælger et gavekort til et ophold eller et beløb og betaler med kort eller MobilePay. Bagefter kan man sende det til sig selv og printe det, sende det direkte til en ven på en bestemt dato eller få det pakket pænt ind og sendt med posten for 49 kr.</p>
<p>Maiken i receptionen kan se alle gavekort, finde kunderne og indløse kortene i et admin, jeg også har bygget. Og gavekortene ser ud, som jeg selv vil have dem.</p>
<p>De gavekort, folk allerede har fra Life Peaks, gælder selvfølgelig stadig. Dem indløser vi stadig i Life Peaks.</p>
<h2>Lidt ondt i hjertet</h2>
<p>Det gør faktisk lidt ondt at sige farvel. Life Peaks har ikke gjort noget forkert. Men det er præcis det, AI ændrer lige nu for små virksomheder som vores. Ting, jeg før måtte betale andre for, kan jeg nu lave selv, hurtigt og på vores egen måde.</p>
<p>Jeg tror, mange små virksomheder slet ikke har opdaget det endnu.</p>
<p>Vil du høre mere om, hvordan jeg gjorde, så skriv endelig til mig.</p>"""),
]


def post_page(p):
    return page("historier/" + p["slug"], p["titel"] + " – Jannie Buch Thorborg", p["intro"],
 f"""<article class="post"><div class="wrap narrow-wrap">
<p class="crumb"><a href="{L('/historier')}">Historier</a> · <time datetime="{p['iso']}">{p['dato']}</time></p>
<h1>{p['titel']}</h1>
<div class="post-body">{p['tekst']}</div>
<p class="post-end"><a class="btn" href="mailto:{EMAIL}">Skriv til mig</a></p>
</div></article>""")


HIST = page("historier", "Historier – Jannie Buch Thorborg",
 "Jannie Buch Thorborg skriver om iværksætteri, hotellerne i Gudhjem og hvordan hun bruger AI i sine egne virksomheder.",
 f"""<section class="phead"><div class="wrap">
<h1>Historier</h1>
<p class="lede">Om hverdagen bag hotellerne i Gudhjem, om at være iværksætter og om hvordan jeg bruger AI i mine egne virksomheder.</p>
</div></section>
<section><div class="wrap">
<div class="postlist">{''.join(f'<a class="pcard" href="{L("/historier/" + p["slug"])}"><time datetime="{p["iso"]}">{p["dato"]}</time><h2>{p["titel"]}</h2><p>{p["intro"]}</p><span class="more">Læs historien</span></a>' for p in POSTS)}</div>
</div></section>""")

PRESSE = page("presse", "Presse – Jannie Buch Thorborg",
 "Pressemateriale om Jannie Buch Thorborg: kort og lang bio, fakta, pressebilleder og kontakt.",
 f"""<section class="phead"><div class="wrap">
<h1>Presse</h1>
<p class="lede">Jeg stiller gerne op, når det handler om hotellerne i Gudhjem, turisme på Bornholm, iværksætteri eller AI i små virksomheder. Jeg har blandt andet medvirket i Deadline, Go' morgen Danmark og mange gange i lokal-tv og radio.</p>
<div class="btns"><a class="btn" href="mailto:{EMAIL}">Skriv til {EMAIL}</a></div>
</div></section>
<section><div class="wrap kgrid">
<div class="kbox"><h2>Kort bio</h2><p>Jannie Buch Thorborg er iværksætter og hotelejer. Hun står bag Klippen Hotel i Gudhjem med Grevens Dal, Therns og Skt. Jørgens Gaard, baren Jylkat, butikken Førder og Therns Hostel. Hun har en baggrund i IT og bruger AI i den daglige drift.</p></div>
<div class="kbox"><h2>Fakta</h2><ul class="facts">
<li>Opvokset med forældre, der drev hotel, restauranter og diskotek i Blåvand</li>
<li>Baggrund i IT, netværk og digital markedsføring</li>
<li>Har haft virksomheder i Danmark, Tyskland, Thailand og Spanien</li>
<li>Åbnede Førder i Gudhjem i 2020 og Klippen i 2021</li>
<li>Medvirkede i TV-serien Buch Thorborg i 2022</li>
<li>Medejer af Amino, Capino og Saxis</li>
</ul></div>
</div></section>
<section class="pressbio"><div class="wrap narrow-wrap">
<h2>Lang bio</h2>
<p>Jannie Buch Thorborg voksede op i Blåvand, hvor hendes forældre drev hotel, restauranter og et diskotek. Hun startede selv sin karriere i IT og netværk og stiftede sin første virksomhed, mens hun var på barsel. Siden har hun haft virksomheder i Tyskland, Thailand og Spanien.</p>
<p>I 2020 åbnede hun butikken Førder i Gudhjem, og året efter overtog hun Klippen. I dag samler Klippen Hotel tre hoteller i Gudhjem: Grevens Dal, Therns og Skt. Jørgens Gaard. Dertil kommer baren Jylkat ved havnen, Førder og Therns Hostel. I 2022 fulgte TV-serien Buch Thorborg hende og hendes mand, Martin, mens de gjorde hotellerne klar til sæsonen.</p>
<p>Jannie bruger en stor del af sin tid på at gøre virksomhederne bedre med AI, fra hjemmesider og synlighed til gæsteinformation og arbejdsgange. Hun er desuden medejer af iværksætterforummet Amino, kapitalplatformen Capino og virksomhedsbørsen Saxis.</p>
</div></section>
<section class="presspics"><div class="wrap">
<h2>Pressebilleder</h2>
<p class="lede">Billederne må bruges i omtale af Jannie Buch Thorborg og hendes virksomheder.</p>
<div class="pics">
<figure><img src="{L(IMG + 'jannie-australien.jpg')}" alt="Jannie Buch Thorborg" loading="lazy"><figcaption><a href="{L(IMG + 'jannie-australien.jpg')}" download>Hent billede</a></figcaption></figure>
<figure><img src="{L(IMG + 'jannie-og-martin.jpg')}" alt="Jannie og Martin Buch Thorborg" loading="lazy"><figcaption>Jannie og Martin Buch Thorborg · <a href="{L(IMG + 'jannie-og-martin.jpg')}" download>Hent billede</a></figcaption></figure>
</div>
</div></section>""")

KONTAKT = page("kontakt", "Kontakt – Jannie Buch Thorborg",
 "Kontakt Jannie Buch Thorborg om samarbejde, presse eller hendes virksomheder på jannie@hotelklippen.dk.",
 f"""<section class="phead"><div class="wrap">
<h1>Kontakt</h1>
<p class="lede">Har du en henvendelse om samarbejde, presse eller en af mine virksomheder, så skriv til mig på mail.</p>
<div class="btns"><a class="btn" href="mailto:{EMAIL}">Skriv til {EMAIL}</a></div>
</div></section>
<section><div class="wrap kgrid">
<div class="kbox"><h2>Hotelophold og bordbestilling</h2><p>Spørgsmål om ophold og bordbestilling klarer teamet på Klippen Hotel.</p><p><a href="https://www.hotelklippen.com">hotelklippen.com</a><br><a href="mailto:info@hotelklippen.dk">info@hotelklippen.dk</a></p></div>
<div class="kbox"><h2>Følg med</h2><ul class="slist">{''.join(f'<li><a href="{u}" rel="me noopener">{n}</a></li>' for n, u in SOME)}</ul></div>
</div></section>""")

NOTFOUND = page("404", "Siden findes ikke – Jannie Buch Thorborg", "Siden findes ikke.",
 f"""<section class="phead"><div class="wrap"><h1>Siden findes ikke</h1>
<p class="lede">Linket virker ikke længere, eller adressen er skrevet forkert.</p>
<div class="btns"><a class="btn" href="{L('/')}">Gå til forsiden</a></div></div></section>""")


if __name__ == "__main__":
    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(ROOT / "site", DIST)
    if BASE:
        (DIST / ".htaccess").unlink()
    pages = [("index", HOME), ("om-jannie", OM), ("mine-steder", STEDER), ("historier", HIST), ("presse", PRESSE), ("kontakt", KONTAKT), ("404", NOTFOUND)]
    pages += [("historier/" + p["slug"], post_page(p)) for p in POSTS]
    for name, html in pages:
        (DIST / f"{name}.html").parent.mkdir(parents=True, exist_ok=True)
        (DIST / f"{name}.html").write_text(html, encoding="utf-8")
    today = date.today().isoformat()
    urls = "".join(f"<url><loc>{DOMAIN}/{s}</loc><lastmod>{today}</lastmod></url>" for s in ["", "om-jannie", "mine-steder", "historier", "presse", "kontakt"] + ["historier/" + p["slug"] for p in POSTS])
    (DIST / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + urls + "</urlset>\n", encoding="utf-8")
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /_ny/\nDisallow: /_aida-backup/\n\nSitemap: {DOMAIN}/sitemap.xml\n", encoding="utf-8")
    if not BASE:
        files = sorted(str(p.relative_to(DIST)) for p in DIST.rglob("*") if p.is_file())
        (ROOT / "filer.txt").write_text("\n".join(files) + "\n", encoding="utf-8")
    print("bygget", DIST.name)
