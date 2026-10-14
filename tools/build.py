#!/usr/bin/env python3
"""Senior Tech Foundation static site generator.

Edit content here (or events.json), then run:  python3 tools/build.py
Every page shares the same header/footer, so one edit updates the whole site.

When the site moves to its real domain, change SITE_URL and BASE below and rebuild.
"""
import json, html, os, re
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"

# ---- Site settings -------------------------------------------------------
SITE_URL = "https://wbbonds2-svg.github.io/yourseniortech-site"   # no trailing slash
BASE = "/yourseniortech-site"                                     # "" once on yourseniortech.org
GA4_ID = ""            # e.g. "G-XXXXXXX" — leave empty until Analytics is set up
GSC_VERIFY = ""        # Google Search Console HTML-tag verification code
BING_VERIFY = ""       # Bing Webmaster Tools verification code
ORG = "Senior Tech Foundation"
PHONE = "253-617-5848"
PHONE_TEL = "+12536175848"
EMAIL = "ashlyn@yourseniortech.com"
FORM_ACTION = f"https://formsubmit.co/{EMAIL}"
DONATE_URL = "https://givebutter.com/senior-tech-foundation"
CANDID_URL = "https://app.candid.org/profile/16534654/senior-tech-foundation-41-3502697/?pkId=623db530-bc49-486c-adfc-15c1859d2234"
CANDID_SEAL = "https://widgets.guidestar.org/prod/v1/pdp/transparency-seal/16534654/svg"
EIN = "41-3502697"
SOCIAL = [
    ("Facebook", "https://www.facebook.com/seniortechFDN"),
    ("Instagram", "https://www.instagram.com/seniortechfoundation"),
    ("LinkedIn", "https://www.linkedin.com/company/your-senior-tech/"),
    ("TikTok", "https://www.tiktok.com/@seniortechfoundation"),
]
TAGLINE = "It’s like having your grandkids help you with tech."

# Impact figures from the Foundation's 2026 Mobile Tech Clinic sponsorship packet.
IMPACT = [
    ("2,600+", "older adults served"),
    ("430+", "hours of one-on-one tech support"),
    ("100+", "community talks and workshops"),
    ("15+", "active student mentors"),
]
IMPACT_NOTE = "Totals reported by Senior Tech Foundation in its 2026 Mobile Tech Clinic sponsorship materials."

NAV = [
    ("Get free help", "/free-tech-help-for-seniors/"),
    ("Tech clinics", "/mobile-tech-clinics/"),
    ("Classes", "/technology-classes-for-seniors/"),
    ("Events", "/events/"),
    ("About", "/about/"),
    ("Partner with us", "/community-partnerships/"),
    ("Volunteer", "/volunteer/"),
    ("Contact", "/contact/"),
]

e = html.escape


def url(path):
    return BASE + path


def abs_url(path):
    return SITE_URL + path


def img(name, alt, sizes="(max-width: 960px) 100vw, 50vw", eager=False, cls=""):
    widths = [w for w in (800, 1200) if (ROOT / f"assets/img/{name}-{w}.webp").exists()]
    srcset = ", ".join(f"{url(f'/assets/img/{name}-{w}.webp')} {w}w" for w in widths)
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="{url(f"/assets/img/{name}-800.webp")}" srcset="{srcset}" sizes="{sizes}" '
            f'width="800" height="534" alt="{e(alt)}" {load}>')


# ---- Structured data ---------------------------------------------------------
def org_ld():
    return {
        "@context": "https://schema.org",
        "@type": "NGO",
        "@id": SITE_URL + "/#org",
        "name": ORG,
        "alternateName": "Senior Tech Foundation Washington",
        "url": SITE_URL + "/",
        "logo": abs_url("/assets/img/logo.png"),
        "description": "Washington nonprofit providing free technology help, Mobile Tech Clinics, and digital safety education for older adults in King and Pierce Counties, delivered by trained student mentors.",
        "slogan": TAGLINE,
        "nonprofitStatus": "Nonprofit501c3",
        "taxID": EIN,
        "email": EMAIL,
        "telephone": PHONE_TEL,
        "address": {"@type": "PostalAddress", "addressRegion": "WA", "addressCountry": "US"},
        "areaServed": [
            {"@type": "AdministrativeArea", "name": "King County, Washington"},
            {"@type": "AdministrativeArea", "name": "Pierce County, Washington"},
        ],
        "sameAs": [u for _, u in SOCIAL] + [CANDID_URL],
    }


def crumbs_ld(trail):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": abs_url(p)}
            for i, (n, p) in enumerate(trail)
        ],
    }


def faq_ld(items):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}}
            for q, a in items
        ],
    }


# ---- Layout ------------------------------------------------------------------
def header(active):
    items = "".join(
        f'<li><a href="{url(p)}"{" aria-current=\"page\"" if p == active else ""}>{e(n)}</a></li>' for n, p in NAV
    )
    items += f'<li><a class="btn-donate" href="{url("/donate/")}"{" aria-current=\"page\"" if active == "/donate/" else ""}>Donate</a></li>'
    return f"""<a class="skip" href="#main">Skip to main content</a>
<div class="topbar"><div class="wrap">
  <span>Free technology help for older adults in King &amp; Pierce Counties</span>
  <span>Questions? Call <a href="tel:{PHONE_TEL}">{PHONE}</a></span>
</div></div>
<header class="site-header"><div class="wrap">
  <a class="brand" href="{url('/')}"><img src="{url('/assets/img/logo-120.png')}" width="169" height="120" alt="{ORG} home"><span>{ORG}</span></a>
  <nav aria-label="Main">
    <details class="menu" open>
      <summary><span class="bars" aria-hidden="true"></span> Menu</summary>
      <ul class="nav-list">{items}</ul>
    </details>
  </nav>
</div></header>
<script>if(window.matchMedia("(max-width:1080px)").matches)document.querySelector(".menu").removeAttribute("open");</script>"""


def footer():
    social = "".join(f'<a href="{u}" rel="noopener" target="_blank">{n}</a>' for n, u in SOCIAL)
    return f"""<footer class="site-footer"><div class="wrap">
  <div class="foot-grid">
    <div>
      <img class="foot-logo" src="{url('/assets/img/logo-120.png')}" width="169" height="120" alt="{ORG}">
      <p>{ORG} is a Washington 501(c)(3) nonprofit. Trained student mentors give older adults free, patient technology help.</p>
      <p><a href="tel:{PHONE_TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a><br>Serving King &amp; Pierce Counties, WA</p>
      <div class="social">{social}</div>
    </div>
    <div>
      <h2>Get help</h2>
      <ul>
        <li><a href="{url('/free-tech-help-for-seniors/')}">Free tech help</a></li>
        <li><a href="{url('/mobile-tech-clinics/')}">Mobile Tech Clinics</a></li>
        <li><a href="{url('/technology-classes-for-seniors/')}">Classes &amp; Tech Talks</a></li>
        <li><a href="{url('/scam-prevention-for-seniors/')}">Scam prevention</a></li>
        <li><a href="{url('/ai-classes-for-seniors/')}">AI for older adults</a></li>
        <li><a href="{url('/events/')}">Upcoming events</a></li>
        <li><a href="{url('/faq/')}">Questions &amp; answers</a></li>
      </ul>
    </div>
    <div>
      <h2>Get involved</h2>
      <ul>
        <li><a href="{url('/community-partnerships/')}">Host a free program</a></li>
        <li><a href="{url('/sponsor/')}">Sponsor a clinic</a></li>
        <li><a href="{url('/volunteer/')}">Volunteer as a mentor</a></li>
        <li><a href="{url('/donate/')}">Donate</a></li>
      </ul>
    </div>
    <div>
      <h2>About</h2>
      <ul>
        <li><a href="{url('/about/')}">Our story</a></li>
        <li><a href="{url('/our-impact/')}">Our impact</a></li>
        <li><a href="{url('/contact/')}">Contact us</a></li>
        <li><a href="{url('/privacy/')}">Privacy policy</a></li>
      </ul>
    </div>
  </div>
  <div class="legal">
    <p>© {date.today().year} {ORG}, EIN {EIN}. {ORG} is separate from Your Senior Tech, a for-profit company.</p>
    <a class="seal" href="{CANDID_URL}" rel="noopener" target="_blank"><img src="{CANDID_SEAL}" width="110" height="110" alt="Candid Seal of Transparency" loading="lazy"></a>
  </div>
</div></footer>"""


def page(path, title, desc, body, trail=None, extra_ld=None, noindex=False, og_image="hero-1200.webp"):
    ld = [org_ld()]
    if trail:
        ld.append(crumbs_ld(trail))
    ld += extra_ld or []
    ld_html = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    ga = ""
    if GA4_ID:
        ga = f"""<script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA4_ID}');
document.addEventListener('click',function(ev){{var a=ev.target.closest('a');if(!a)return;var h=a.getAttribute('href')||'';
if(h.indexOf('tel:')===0)gtag('event','call_click');else if(h.indexOf('mailto:')===0)gtag('event','email_click');else if(h.indexOf('givebutter')>-1)gtag('event','donate_click');}});
document.addEventListener('submit',function(ev){{gtag('event','form_submit',{{form_name:ev.target.getAttribute('data-form')||'form'}});}});</script>"""
    verify = ""
    if GSC_VERIFY:
        verify += f'<meta name="google-site-verification" content="{GSC_VERIFY}">\n'
    if BING_VERIFY:
        verify += f'<meta name="msvalidate.01" content="{BING_VERIFY}">\n'
    robots = '<meta name="robots" content="noindex, follow">' if noindex else '<meta name="robots" content="index, follow, max-image-preview:large">'
    crumbs_html = ""
    if trail and len(trail) > 1:
        lis = "".join(
            f'<li><a href="{url(p)}">{e(n)}</a></li>' if i < len(trail) - 1 else f'<li aria-current="page">{e(n)}</li>'
            for i, (n, p) in enumerate(trail)
        )
        crumbs_html = f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{lis}</ol></nav>'
    body = body.replace("{{CRUMBS}}", crumbs_html)
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{abs_url(path)}">
{robots}
{verify}<meta property="og:type" content="website">
<meta property="og:site_name" content="{ORG}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{abs_url(path)}">
<meta property="og:image" content="{abs_url('/assets/img/' + og_image)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#10263a">
<link rel="icon" href="{url('/assets/img/favicon.png')}" type="image/png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible+Next:wght@400;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{url('/assets/site.css')}?v={STAMP}">
{ld_html}
{ga}
</head>
<body>
{header(path)}
<main id="main">
{body}
</main>
{footer()}
</body>
</html>
"""
    out = ROOT / (path.strip("/") + "/index.html" if path != "/" else "index.html")
    if path.endswith(".html"):
        out = ROOT / path.strip("/")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc)
    if not noindex:
        SITEMAP.append(path)


def redirect(old, new):
    out = ROOT / old.strip("/") / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Page moved — {ORG}</title><link rel="canonical" href="{abs_url(new)}">
<meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url={url(new)}">
<script>location.replace("{url(new)}")</script></head>
<body><p>This page has moved to <a href="{url(new)}">{abs_url(new)}</a>.</p></body></html>
""")


def page_head(h1, lead, extra=""):
    return f"""<section class="page-head"><div class="wrap">
{{{{CRUMBS}}}}
<h1>{h1}</h1>
<p class="lead">{lead}</p>{extra}
</div></section>"""


def cta_band(title, text, buttons):
    btns = "".join(f'<a class="btn {c}" href="{h}">{e(t)}</a>' for t, h, c in buttons)
    return f"""<section class="section section--navy"><div class="wrap band">
<div><h2>{title}</h2><p>{text}</p></div><div class="btn-row" style="margin-top:0">{btns}</div>
</div></section>"""


def faq_block(items):
    return '<div class="faq">' + "".join(f"<details><summary>{e(q)}</summary><div><p>{a}</p></div></details>" for q, a in items) + "</div>"


def hidden_fields(subject, form_name):
    return f"""<input type="hidden" name="_subject" value="{e(subject)}">
<input type="hidden" name="_next" value="{abs_url('/thank-you/')}">
<input type="hidden" name="_template" value="table">
<input type="hidden" name="form" value="{e(form_name)}">
<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">"""


def field(label, name, kind="text", required=False, hint="", auto="", options=None, rows=None):
    req = ' <span class="req" aria-hidden="true">*</span>' if required else ""
    r = " required" if required else ""
    h = f'<span class="hint" id="{name}-hint">{hint}</span>' if hint else ""
    desc = f' aria-describedby="{name}-hint"' if hint else ""
    ac = f' autocomplete="{auto}"' if auto else ""
    if kind == "select":
        opts = '<option value="">Choose one</option>' + "".join(f"<option>{e(o)}</option>" for o in options)
        ctrl = f'<select id="{name}" name="{name}"{r}{desc}>{opts}</select>'
    elif kind == "textarea":
        ctrl = f'<textarea id="{name}" name="{name}"{r}{desc}></textarea>'
    else:
        ctrl = f'<input id="{name}" name="{name}" type="{kind}"{r}{desc}{ac}>'
    return f'<div class="field"><label for="{name}">{e(label)}{req}{h}</label>{ctrl}</div>'


def checks(legend, name, options, kind="checkbox", required=False):
    req = ' <span class="req" aria-hidden="true">*</span>' if required else ""
    items = "".join(
        f'<label class="choice"><input type="{kind}" name="{name}" value="{e(o)}"{" required" if (required and kind == "radio") else ""}> {e(o)}</label>'
        for o in options
    )
    return f'<fieldset class="field"><legend>{e(legend)}{req}</legend>{items}</fieldset>'


# ---- Shared content ------------------------------------------------------------
GENERAL_FAQ = [
    ("Is the help really free?",
     "Yes. Senior Tech Foundation’s clinics, one-on-one help, and Tech Talks are free for older adults. Our programs are paid for by donations, grants, and sponsors, so there is never a charge to the people we help."),
    ("Who can get help?",
     "Older adults in King and Pierce Counties, plus the family members and caregivers who help them. You don’t need to know anything about technology to come. Beginners are welcome."),
    ("What devices can you help with?",
     "Phones, tablets, laptops, smartwatches, e-readers, and other personal technology. Common requests include apps, accounts, passwords, photos, email, settings, video calls, and checking whether a message is a scam."),
    ("Who will be helping me?",
     "Trained high school and college student mentors. They work side by side with you at your pace and explain each step so you can do it again on your own."),
    ("Where do programs happen?",
     "At senior centers, libraries, retirement and housing communities, and other community spaces in King and Pierce Counties. See the <a href=\"" + "{BASE}/events/" + "\">events page</a> for upcoming clinics, or call us to find the next one near you."),
    ("Do I need an appointment?",
     "Clinic details vary by location. Check the event listing or call <a href=\"tel:" + PHONE_TEL + "\">" + PHONE + "</a> and we’ll tell you how the next clinic near you works."),
    ("What should I bring?",
     "Bring your device, its charger, and any passwords you may need (for example, your Apple ID or Google account). A list of questions helps too. Never share your passwords out loud in a public space; mentors will show you how to type them privately."),
    ("Is Senior Tech Foundation the same as Your Senior Tech?",
     "No. Senior Tech Foundation is a nonprofit, and everything on this website is free. Your Senior Tech is a separate company that offers paid services."),
    ("How can my community host a free clinic or workshop?",
     "Fill out the <a href=\"" + "{BASE}/community-partnerships/" + "\">program request form</a>. We’ll follow up to plan a date, location, and topics."),
]


def faq_items():
    return [(q, a.replace("{BASE}", BASE)) for q, a in GENERAL_FAQ]


# ---- Pages -------------------------------------------------------------------
def home():
    stats = "".join(f'<div class="stat"><b>{n}</b><span>{l}</span></div>' for n, l in IMPACT)
    ev = upcoming_events()[:3]
    if ev:
        ev_html = "".join(event_html(x, compact=True) for x in ev)
    else:
        ev_html = f"""<div class="empty"><h3>New clinic dates are on the way</h3>
<p>We post clinics here as soon as host sites confirm them. To find the next clinic near you, call <a href="tel:{PHONE_TEL}">{PHONE}</a>, or ask us to bring one to your community.</p>
<div class="btn-row"><a class="btn btn--primary" href="{url('/events/')}">See the events page</a><a class="btn btn--outline" href="{url('/community-partnerships/')}">Request a clinic</a></div></div>"""
    body = f"""
<section class="hero"><div class="wrap">
  <div class="hero-grid">
    <div>
      <p class="tagline">{TAGLINE}</p>
      <h1>Free Technology Help for Seniors in King &amp; Pierce Counties</h1>
      <p class="lead">{ORG} is a Washington nonprofit. Our trained student mentors give older adults free, one-on-one help with phones, tablets, computers, and everyday technology at Mobile Tech Clinics and workshops in the community.</p>
      <div class="btn-row">
        <a class="btn btn--sun" href="{url('/events/')}">Find a free tech clinic</a>
        <a class="btn btn--outline" href="{url('/community-partnerships/')}">Bring a program to your community</a>
      </div>
    </div>
    <div class="laptop">
      <span class="laptop-dot" aria-hidden="true"></span>
      <div class="laptop-screen">{img('hero', 'A student mentor helps an older woman with her smartphone at a Senior Tech Foundation clinic', '(max-width: 960px) 100vw, 560px', eager=True)}</div>
      <div class="laptop-base" aria-hidden="true"></div>
    </div>
  </div>
  <nav class="hero-actions" aria-label="What would you like to do?">
    <a href="{url('/free-tech-help-for-seniors/')}"><strong>Find free tech help</strong><span>For older adults and families</span></a>
    <a href="{url('/community-partnerships/')}"><strong>Host a tech clinic</strong><span>For senior communities, libraries, and organizations</span></a>
    <a href="{url('/volunteer/')}"><strong>Volunteer</strong><span>For high school and college students</span></a>
    <a class="donate" href="{url('/donate/')}"><strong>Donate</strong><span>Keep every program free</span></a>
  </nav>
</div></section>

<section class="section"><div class="wrap">
  <h2>How to get free help</h2>
  <p class="lead">There is no cost, and you don’t need any tech experience.</p>
  <ol class="steps">
    <li><h3>Find a clinic or call us</h3><p>Check the <a href="{url('/events/')}">events page</a> for a Mobile Tech Clinic near you, or call <a href="tel:{PHONE_TEL}">{PHONE}</a>.</p></li>
    <li><h3>Bring your device</h3><p>Bring your phone, tablet, laptop, or other device, its charger, and any questions you have.</p></li>
    <li><h3>Get matched with a mentor</h3><p>A trained student mentor sits with you, helps at your pace, and explains each step so you can do it yourself later.</p></li>
  </ol>
</div></section>

<section class="section section--sky"><div class="wrap">
  <h2>Our three main programs</h2>
  <div class="program">
    {img('clinic', 'Student mentors working one-on-one with older adults at a community tech clinic', '(max-width: 960px) 100vw, 380px')}
    <div><span class="free-tag">Free</span><h3>Mobile Tech Clinics</h3>
    <p>Pop-up help sessions at senior centers, libraries, and community spaces. Bring any device and get one-on-one help from a trained student mentor, with Wi-Fi hotspots on site.</p>
    <a class="btn btn--primary" href="{url('/mobile-tech-clinics/')}">About tech clinics</a></div>
  </div>
  <div class="program">
    {img('one-on-one', 'A student mentor reviews a phone with an older man', '(max-width: 960px) 100vw, 380px')}
    <div><span class="free-tag">Free</span><h3>One-on-one technology help</h3>
    <p>Patient, side-by-side support with setting up devices, fixing problems, and using everyday apps like email, photos, and video calls.</p>
    <a class="btn btn--primary" href="{url('/free-tech-help-for-seniors/')}">About one-on-one help</a></div>
  </div>
  <div class="program">
    {img('tech-talk', 'Older adults attending a Tech Talk presentation in a community center', '(max-width: 960px) 100vw, 380px')}
    <div><span class="free-tag">Free</span><h3>Tech Talks &amp; workshops</h3>
    <p>Group classes, usually one to two hours, on device basics, scam prevention, online safety, and artificial intelligence. Every session includes time for questions.</p>
    <a class="btn btn--primary" href="{url('/technology-classes-for-seniors/')}">About classes</a></div>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <h2>Upcoming clinics</h2>
  {ev_html}
</div></section>

<section class="section section--navy"><div class="wrap">
  <h2>Our impact</h2>
  <p>Every number below is a real person or a real hour spent helping someone feel confident with technology.</p>
  <div class="stats">{stats}</div>
  <p class="note">{IMPACT_NOTE} <a href="{url('/our-impact/')}">How we measure impact</a>.</p>
</div></section>

<section class="section"><div class="wrap split">
  {img('mentors', 'A group of Senior Tech Foundation student mentors at a clinic')}
  <div>
    <h2>Meet our student mentors</h2>
    <p>Our mentors are trained high school and college students. Older adults get patient help from someone who takes time to listen. Students build leadership, empathy, and real-world communication skills. Two generations learn from each other at every clinic.</p>
    <p>Mentors are trained to explain each step clearly, never rush, and protect privacy. They don’t ask for your passwords, and they show you how to keep your accounts safe.</p>
    <a class="btn btn--primary" href="{url('/volunteer/')}">Become a mentor</a>
  </div>
</div></section>

<section class="section section--sky"><div class="wrap">
  <h2>Trusted community partners</h2>
  <p>We work with cities, libraries, senior living communities, and local businesses to bring free help where older adults already are.</p>
  {partner_logos()}
  <p style="margin-top:24px"><a href="{url('/community-partnerships/')}">Become a partner or sponsor</a></p>
</div></section>

<section class="section"><div class="wrap">
  <h2>What people say</h2>
  <div class="cols-2">
    <blockquote class="quote"><p>“I felt like the world was moving forward without me. Now I can keep up.”</p><footer>Clinic participant</footer></blockquote>
    <blockquote class="quote"><p>“I no longer feel helpless.”</p><footer>Clinic participant</footer></blockquote>
  </div>
</div></section>

<section class="section section--sky"><div class="wrap">
  <h2>Questions people ask</h2>
  {faq_block(faq_items()[:5])}
  <p style="margin-top:24px"><a href="{url('/faq/')}">See all questions and answers</a></p>
</div></section>

<section class="section"><div class="wrap">
  <h2>Get involved</h2>
  <div class="paths">
    <div class="path"><h3>Older adults &amp; families</h3><p>Get free help with any device at a clinic near you.</p><a href="{url('/free-tech-help-for-seniors/')}">Find free help</a></div>
    <div class="path"><h3>Host organizations</h3><p>Bring a free clinic or workshop to your residents, patrons, or members.</p><a href="{url('/community-partnerships/')}">Request a program</a></div>
    <div class="path"><h3>Student volunteers</h3><p>Help older adults and build skills that matter.</p><a href="{url('/volunteer/')}">Apply to volunteer</a></div>
    <div class="path"><h3>Donors &amp; sponsors</h3><p>Keep programs free and visible in your community.</p><a href="{url('/donate/')}">Donate</a> or <a href="{url('/sponsor/')}">sponsor a clinic</a></div>
  </div>
</div></section>
"""
    page("/", "Free Tech Help for Seniors in King & Pierce Counties | Senior Tech Foundation",
         "Senior Tech Foundation is a Washington nonprofit offering free one-on-one tech help, Mobile Tech Clinics, and Tech Talks for older adults in King and Pierce Counties.",
         body, extra_ld=[faq_ld(faq_items()[:5])] + [event_ld(x) for x in ev])


def partner_logos():
    logos = [
        ("partner-riverview.png", "Riverview Retirement Community"),
        ("partner-intech.png", "inTech Consulting"),
        ("partner-valley-spay.png", "Valley Spay and Neuter Clinic"),
    ]
    return '<div class="logos">' + "".join(
        f'<div><img src="{url("/assets/img/" + f)}" alt="{e(n)}" loading="lazy"></div>' for f, n in logos
    ) + "</div>"


def program_page(path, h1, crumb, title, desc, answer, photo, alt, sections, faqs, cta):
    body = page_head(h1, desc) + f"""
<section class="section"><div class="wrap">
  <div class="answer">{answer}</div>
  <div class="split" style="align-items:start">
    <div class="content">{sections}</div>
    <div>{img(photo, alt)}
      <div class="empty" style="margin-top:28px;border-style:solid">
        <h3>At a glance</h3>
        <ul class="small">
          <li><b>Cost:</b> Free</li>
          <li><b>Who:</b> Older adults, families, and caregivers</li>
          <li><b>Where:</b> King &amp; Pierce Counties, WA</li>
          <li><b>Questions:</b> <a href="tel:{PHONE_TEL}">{PHONE}</a></li>
        </ul>
      </div>
    </div>
  </div>
</div></section>
<section class="section section--sky"><div class="wrap">
  <h2>Common questions</h2>
  {faq_block(faqs)}
</div></section>
{cta}"""
    page(path, title, desc, body, trail=[("Home", "/"), (crumb, path)], extra_ld=[faq_ld(faqs)], og_image=f"{photo}-800.webp")


def build_programs():
    default_cta = cta_band("Ready for free help?", "Find a clinic near you or bring one to your community.",
                           [("Find a clinic", url("/events/"), "btn--sun"), ("Request a program", url("/community-partnerships/"), "btn--light")])
    fq = dict(faq_items())

    program_page(
        "/free-tech-help-for-seniors/", "Free Technology Help for Seniors", "Free tech help",
        "Free Tech Help for Seniors in King & Pierce Counties | Senior Tech Foundation",
        "Free, patient, one-on-one help with phones, tablets, computers, and apps for older adults in King and Pierce Counties.",
        f"<p><b>Where can an older adult get free, in-person tech help in King or Pierce County?</b> {ORG} offers free one-on-one help at Mobile Tech Clinics and community workshops. A trained student mentor works side by side with you on any device. Call <a href=\"tel:{PHONE_TEL}\">{PHONE}</a> or check the <a href=\"{url('/events/')}\">events page</a> to find the next clinic.</p>",
        "one-on-one", "A student mentor helps an older man with his phone",
        f"""<h2>What you can get help with</h2>
<ul>
<li>Setting up a new phone, tablet, or computer</li>
<li>Email, text messages, photos, and video calls with family</li>
<li>Apps, accounts, passwords, and settings</li>
<li>Making text bigger and devices easier to use</li>
<li>Checking whether a call, text, or email is a scam</li>
<li>Printers, smartwatches, e-readers, and other personal technology</li>
</ul>
<h2>How one-on-one help works</h2>
<p>You are matched with a trained high school or college student mentor. They sit with you, work at your pace, and explain what they are doing and why, so you can repeat it on your own. You can bring a list of questions or one specific problem.</p>
<h2>Who it’s for</h2>
<p>Older adults living independently, in senior living communities, or in housing communities, and the family members and caregivers who help them. No experience is needed.</p>
<h2>Ways to get help</h2>
<ul>
<li><a href="{url('/mobile-tech-clinics/')}">Mobile Tech Clinics</a>: drop-in style help at community locations</li>
<li><a href="{url('/technology-classes-for-seniors/')}">Tech Talks &amp; classes</a>: group learning on everyday topics</li>
<li><a href="{url('/scam-prevention-for-seniors/')}">Scam prevention workshops</a></li>
<li><a href="{url('/ai-classes-for-seniors/')}">AI for older adults</a></li>
</ul>""",
        [("Is the help really free?", fq["Is the help really free?"]),
         ("What devices can you help with?", fq["What devices can you help with?"]),
         ("What should I bring?", fq["What should I bring?"]),
         ("Is Senior Tech Foundation the same as Your Senior Tech?", fq["Is Senior Tech Foundation the same as Your Senior Tech?"])],
        default_cta)

    program_page(
        "/mobile-tech-clinics/", "Mobile Tech Clinics for Seniors", "Mobile Tech Clinics",
        "Free Mobile Tech Clinics for Seniors | Senior Tech Foundation",
        "Free pop-up tech clinics where older adults bring any device and get one-on-one help from trained student mentors.",
        "<p><b>What is a Mobile Tech Clinic?</b> A free, pop-up help session at a senior center, library, or community space. Older adults bring any device and get matched with a trained student mentor for one-on-one help. Clinics usually run two to four hours, with Wi-Fi hotspots and take-home safety guides.</p>",
        "clinic", "Student mentors help older adults at tables during a Mobile Tech Clinic",
        f"""<h2>What happens at a clinic</h2>
<ol>
<li><b>Bring any device.</b> Phones, tablets, laptops, smartwatches, e-readers, and other personal technology.</li>
<li><b>Get matched one-on-one.</b> A trained high school or college mentor gives patient, side-by-side support.</li>
<li><b>Connect and solve.</b> Our Wi-Fi hotspots support help with apps, accounts, passwords, photos, email, scams, AI, settings, and more.</li>
<li><b>Leave more confident.</b> Take home practical guides on scams, AI, online safety, accessibility, and device basics.</li>
</ol>
<h2>Who it’s for</h2>
<p>Older adults of any skill level, plus family members and caregivers. Mentor staffing scales to expected attendance, typically up to 10 trained student mentors, with more added for larger turnout.</p>
<h2>Where clinics happen</h2>
<p>Clinics are held at senior centers, libraries, retirement and housing communities, faith organizations, and other accessible community spaces in King and Pierce Counties. Past clinics include a Technology Help for Seniors pop-up at the Kent Senior Center with the City of Kent in August 2026. See <a href="{url('/events/')}">upcoming clinics</a>.</p>
<h2>Bring a clinic to your community</h2>
<p>Hosting is free for senior communities, libraries, and community organizations. Hosts provide tables, chairs, power, and Wi-Fi when available. <a href="{url('/community-partnerships/')}">Request a clinic</a>. Businesses can also <a href="{url('/sponsor/')}">sponsor a clinic</a> to keep it free for participants.</p>""",
        [("Is the help really free?", fq["Is the help really free?"]),
         ("Do I need an appointment?", fq["Do I need an appointment?"]),
         ("What should I bring?", fq["What should I bring?"]),
         ("How can my community host a free clinic or workshop?", fq["How can my community host a free clinic or workshop?"])],
        default_cta)

    program_page(
        "/technology-classes-for-seniors/", "Technology Classes & Tech Talks for Seniors", "Classes & Tech Talks",
        "Technology Classes & Tech Talks for Seniors | Senior Tech Foundation",
        "Free group technology classes for older adults on smartphones, email, apps, online safety, scams, and AI.",
        "<p><b>What are Tech Talks?</b> Free group workshops, usually one to two hours, that teach older adults everyday technology skills and digital safety. Topics include smartphones and tablets, email and messaging, common apps, scam prevention, and AI. Every session includes time for questions.</p>",
        "tech-talk", "Older adults attending a Tech Talk in a community room",
        f"""<h2>Topics we teach</h2>
<ul>
<li>Smartphone and tablet basics</li>
<li>Email, messaging, and video calls</li>
<li>Navigating common apps and settings</li>
<li>Passwords, passkeys, and account security</li>
<li><a href="{url('/scam-prevention-for-seniors/')}">Scam and fraud prevention</a></li>
<li><a href="{url('/ai-classes-for-seniors/')}">Artificial intelligence, explained simply</a></li>
</ul>
<h2>How sessions work</h2>
<p>Sessions can be one-time events or an ongoing series. We tailor each one to the group’s interests and comfort level, and we use real-world examples. Participants can ask questions and talk through real concerns.</p>
<h2>Designed for</h2>
<p>Senior centers, libraries, retirement communities, housing communities, faith organizations, caregivers, and families in King and Pierce Counties.</p>
<h2>Bring a workshop to your community</h2>
<p>Workshops are free for host organizations. <a href="{url('/community-partnerships/')}">Request a Tech Talk</a>.</p>""",
        [("Is the help really free?", fq["Is the help really free?"]),
         ("How long are workshops?", "Most workshops are one to two hours long and include time for questions."),
         ("How can my community host a free clinic or workshop?", fq["How can my community host a free clinic or workshop?"])],
        cta_band("Bring a Tech Talk to your community", "Free for senior centers, libraries, and community organizations.",
                 [("Request a workshop", url("/community-partnerships/"), "btn--sun")]))

    program_page(
        "/scam-prevention-for-seniors/", "Scam & Fraud Prevention for Seniors", "Scam prevention",
        "Scam Prevention Classes for Seniors | Senior Tech Foundation",
        "Free scam and fraud prevention workshops that help older adults spot phishing, impersonation, AI voice-cloning, and financial scams.",
        "<p><b>How can seniors learn to avoid scams?</b> Senior Tech Foundation offers free scam prevention workshops and one-on-one help. Older adults learn to recognize warning signs, pause and verify suspicious calls, texts, and emails, and protect their accounts and personal information.</p>",
        "scam", "A student mentor helps an older woman review a message on her phone",
        """<h2>Topics covered</h2>
<ul>
<li>Identity theft and identity protection</li>
<li>Current scams and new fraud trends</li>
<li>Artificial intelligence, deepfakes, and voice-cloning scams</li>
<li>Phishing emails, texts, and fake websites</li>
<li>Social media and online marketplace scams</li>
<li>Romance and impersonation scams</li>
<li>Banking, payment, and financial scams</li>
<li>Healthcare, Medicare, and government impersonation scams</li>
<li>Data breaches and personal information exposure</li>
<li>What to do after a scam or security breach</li>
</ul>
<h2>Practical skills you’ll leave with</h2>
<ul>
<li>Recognize common warning signs before responding</li>
<li>Pause and verify suspicious calls, texts, emails, and websites</li>
<li>Create stronger passwords and turn on multi-factor authentication</li>
<li>Check links, senders, and requests before sharing information</li>
<li>Adjust privacy and security settings on your own devices</li>
<li>Know where to report scams and what to do if an account is compromised</li>
</ul>
<h2>If you think you’ve been scammed</h2>
<p>Contact your bank right away, then report it to the FTC at <a href="https://reportfraud.ftc.gov/" rel="noopener">ReportFraud.ftc.gov</a> and to the FBI at <a href="https://www.ic3.gov/" rel="noopener">ic3.gov</a>. Our mentors can help you change passwords and secure your accounts at a clinic.</p>""",
        [("Is the help really free?", fq["Is the help really free?"]),
         ("Can a mentor tell me if a message is a scam?", "Yes. Bring the device with the message to a clinic and a mentor will go through it with you and explain the warning signs."),
         ("How can my community host a free clinic or workshop?", fq["How can my community host a free clinic or workshop?"])],
        default_cta)

    program_page(
        "/ai-classes-for-seniors/", "AI & Digital Literacy for Older Adults", "AI for older adults",
        "AI Classes for Older Adults | Senior Tech Foundation",
        "Free, plain-language introductions to artificial intelligence for older adults: what AI is, how to use it safely, and how to spot AI-generated scams.",
        "<p><b>Are there free AI classes for seniors near me?</b> Yes. Senior Tech Foundation’s Tech Talks introduce artificial intelligence in plain language: what it is, where it shows up in daily life, how to use it safely and responsibly, and how to spot AI-generated scams like deepfakes and voice cloning.</p>",
        "ai", "A student mentor talks with an older man at a tech clinic",
        f"""<h2>What you’ll learn</h2>
<ul>
<li>What AI is, without the jargon</li>
<li>Where you already use AI, like voice assistants, photo apps, and search</li>
<li>How to try AI tools safely and protect your privacy</li>
<li>How to spot deepfakes and AI voice-cloning scams</li>
</ul>
<h2>How it’s taught</h2>
<p>AI is covered in group <a href="{url('/technology-classes-for-seniors/')}">Tech Talks</a> and during one-on-one help at <a href="{url('/mobile-tech-clinics/')}">Mobile Tech Clinics</a>. Participants take home a practical AI and safety guide.</p>""",
        [("Is the help really free?", fq["Is the help really free?"]),
         ("Do I need to know anything about AI already?", "No. Sessions start from the basics and go at the group’s pace."),
         ("How can my community host a free clinic or workshop?", fq["How can my community host a free clinic or workshop?"])],
        default_cta)


# ---- Events ------------------------------------------------------------------
def load_events():
    f = TOOLS / "events.json"
    return json.loads(f.read_text()) if f.exists() else []


def upcoming_events():
    today = date.today().isoformat()
    return sorted([x for x in load_events() if x.get("date", "") >= today], key=lambda x: (x["date"], x.get("start", "")))


def event_html(x, compact=False):
    d = datetime.strptime(x["date"], "%Y-%m-%d")
    reg = f'<a class="btn btn--primary" href="{e(x["registration_url"])}">Register</a>' if x.get("registration_url") else ""
    access = f'<p class="small"><b>Accessibility:</b> {e(x["accessibility"])}</p>' if x.get("accessibility") and not compact else ""
    return f"""<article class="event">
  <div class="event-date"><span>{d.strftime('%b')}</span><b>{d.day}</b><span>{d.strftime('%a')}</span></div>
  <div><h3>{e(x['title'])}</h3>
  <p><b>{d.strftime('%A, %B')} {d.day}</b>, {e(x.get('start',''))}–{e(x.get('end',''))}<br>{e(x['location_name'])}, {e(x.get('address',''))}</p>
  <p>{e(x.get('description',''))}</p>{access}{reg}</div>
</article>"""


def event_ld(x):
    tz = "-07:00"
    def t(v):
        return datetime.strptime(v, "%I:%M %p").strftime("%H:%M") if v else "10:00"
    return {
        "@context": "https://schema.org", "@type": "Event", "name": x["title"],
        "startDate": f"{x['date']}T{t(x.get('start'))}:00{tz}", "endDate": f"{x['date']}T{t(x.get('end'))}:00{tz}",
        "eventStatus": "https://schema.org/EventScheduled", "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
        "location": {"@type": "Place", "name": x["location_name"], "address": x.get("address", "")},
        "description": x.get("description", ""), "isAccessibleForFree": True,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD", "availability": "https://schema.org/InStock", "url": x.get("registration_url") or abs_url("/events/")},
        "organizer": {"@type": "NGO", "name": ORG, "url": SITE_URL + "/"},
        "image": [abs_url("/assets/img/clinic-1200.webp")],
    }


def build_events():
    up = upcoming_events()
    if up:
        listing = "".join(event_html(x) for x in up)
    else:
        listing = f"""<div class="empty"><h2>New clinic dates are on the way</h2>
<p>We post Mobile Tech Clinics and workshops here as soon as host sites confirm them. To find out about the next clinic near you, call <a href="tel:{PHONE_TEL}">{PHONE}</a> or email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></div>"""
    body = page_head("Upcoming Tech Clinics &amp; Events",
                     "Free Mobile Tech Clinics and Tech Talks for older adults in King and Pierce Counties.") + f"""
<section class="section"><div class="wrap">
  <div class="answer"><p>All events are <b>free</b> for older adults, families, and caregivers. Bring any device you need help with, its charger, and your questions.</p></div>
  {listing}
</div></section>
<section class="section section--sky"><div class="wrap split">
  {img('events', 'Technology help sign welcoming seniors to a clinic at a senior center')}
  <div><h2>Want a clinic in your community?</h2>
  <p>Senior centers, libraries, retirement and housing communities, and other organizations can host a free clinic or workshop.</p>
  <a class="btn btn--primary" href="{url('/community-partnerships/')}">Request a program</a></div>
</div></section>"""
    page("/events/", "Upcoming Free Senior Tech Clinics & Events | Senior Tech Foundation",
         "Dates, times, and locations of free Mobile Tech Clinics and Tech Talks for older adults in King and Pierce Counties, Washington.",
         body, trail=[("Home", "/"), ("Events", "/events/")], extra_ld=[event_ld(x) for x in up], og_image="events-800.webp")


# ---- Partnerships / host a program --------------------------------------------
def build_partnerships():
    form = f"""<form class="form" action="{FORM_ACTION}" method="POST" data-form="program-request">
{hidden_fields('New free program request', 'Program request')}
<div class="row-2">{field('Your name', 'name', required=True, auto='name')}{field('Organization', 'organization', required=True, auto='organization')}</div>
<div class="row-2">{field('Email', 'email', 'email', required=True, auto='email')}{field('Phone', 'phone', 'tel', auto='tel')}</div>
{field('Type of organization', 'org_type', 'select', required=True, options=['Senior living or retirement community', 'Senior center', 'Library', 'Housing community', 'Faith organization', 'City or government', 'School', 'Other'])}
{checks('What would you like to host?', 'program', ['Mobile Tech Clinic (one-on-one help)', 'Tech Talk or workshop', 'Scam prevention workshop', 'AI for older adults', 'Recurring on-site support', 'Not sure yet'])}
<div class="row-2">{field('City', 'city', required=True, auto='address-level2')}{field('Expected number of attendees', 'attendees', 'number')}</div>
{field('Preferred dates or times', 'dates', hint='Give a few options if you can.')}
{field('Anything else we should know?', 'message', 'textarea', hint='For example: accessibility needs, room setup, languages spoken, or topics of interest.')}
<button class="btn btn--primary" type="submit">Send program request</button>
</form>"""
    body = page_head("Bring a Free Tech Program to Your Community",
                     "Senior living communities, libraries, senior centers, and organizations in King and Pierce Counties can host a free Mobile Tech Clinic or workshop.") + f"""
<section class="section"><div class="wrap split" style="align-items:start">
  <div class="content">
    <div class="answer"><p><b>How do we host a free tech program for seniors?</b> Fill out the form on this page. Senior Tech Foundation will follow up to plan a date, location, and topics. Hosting is free. Hosts provide tables, chairs, power, and Wi-Fi when available.</p></div>
    <h2>Programs you can host</h2>
    <ul>
      <li><a href="{url('/mobile-tech-clinics/')}">Mobile Tech Clinics</a> with one-on-one help from trained student mentors</li>
      <li><a href="{url('/technology-classes-for-seniors/')}">Tech Talks and workshops</a>, usually one to two hours</li>
      <li><a href="{url('/scam-prevention-for-seniors/')}">Scam and fraud prevention</a></li>
      <li><a href="{url('/ai-classes-for-seniors/')}">AI for older adults</a></li>
      <li>Recurring on-site support so residents have a familiar, trusted presence</li>
    </ul>
    <h2>Why communities partner with us</h2>
    <ul>
      <li>Residents gain confidence and independence with technology</li>
      <li>Scam prevention reduces risk and stress for residents, families, and staff</li>
      <li>Technology questions no longer fall on busy staff</li>
      <li>Intergenerational connection between residents and student mentors</li>
      <li>Programs are tailored to each community’s needs</li>
    </ul>
  </div>
  <div>{img('partners', 'A Senior Tech Foundation volunteer helps a visitor at an information table')}</div>
</div></section>
<section class="section section--sky" id="request"><div class="wrap">
  <h2>Request a free program</h2>
  <p>Fields marked <span class="req">*</span> are required. We usually reply within a few business days.</p>
  {form}
</div></section>
<section class="section"><div class="wrap">
  <h2>Sponsors &amp; community partners</h2>
  <p>Thank you to the organizations that help keep our programs free.</p>
  {partner_logos()}
  <div class="band" style="margin-top:40px">
    <p class="lead">Businesses can sponsor a Mobile Tech Clinic and get visible community impact.</p>
    <a class="btn btn--sun" href="{url('/sponsor/')}">Sponsor a clinic</a>
  </div>
</div></section>"""
    page("/community-partnerships/", "Host a Free Senior Tech Program | Senior Tech Foundation",
         "Senior living communities, libraries, and organizations in King and Pierce Counties can request a free Mobile Tech Clinic, Tech Talk, or scam prevention workshop.",
         body, trail=[("Home", "/"), ("Partner with us", "/community-partnerships/")], og_image="partners-800.webp")


# ---- Sponsorship (fillable version of the 2026 sponsorship PDF) ---------------
def build_sponsor():
    tiers = [
        ("Clinic Sponsor", "$499", "2-hour clinic", "A focused clinic for an older adult community, library, business, or neighborhood.",
         ["Mentors scaled to attendance", "Any-device help and Wi-Fi access", "Take-home AI and safety guides", "Logo on event marketing", "Supports 25–40 individuals"]),
        ("Community Partner", "$999", "4-hour clinic", "A deeper clinic experience with more time for hands-on support and community connection.",
         ["More mentor time and access", "Any-device help and Wi-Fi access", "Community outreach coordination", "Sponsor booth or branded table", "Supports 50–70 individuals", "Logo on all marketing materials"]),
        ("Impact Partner", "$2,699", "3-clinic series", "Best value: three 4-hour clinics. Save $298.",
         ["Mentors across each clinic", "Featured logo placement", "Sponsor booth or branded table", "Impact recap after each clinic", "Supports 30+ individuals at each clinic", "Social media and website acknowledgment", "Logo on all marketing materials"]),
    ]
    tier_html = "".join(
        f"""<div class="path"><h3>{n}</h3><p><b style="font-size:2rem;color:var(--navy)">{p}</b><br>{s}</p><p>{d}</p>
<ul class="small">{''.join(f'<li>{e(b)}</li>' for b in bl)}</ul></div>""" for n, p, s, d, bl in tiers)
    form = f"""<form class="form" action="{FORM_ACTION}" method="POST" data-form="sponsorship">
{hidden_fields('New Mobile Tech Clinic sponsorship form', 'Sponsorship form')}
<h3>1. Sponsor organization</h3>
{field('Organization name', 'organization', required=True, auto='organization')}
<div class="row-2">{field('Contact person', 'contact_person', required=True, auto='name')}{field('Title / role', 'title', auto='organization-title')}</div>
<div class="row-2">{field('Phone', 'phone', 'tel', required=True, auto='tel')}{field('Email', 'email', 'email', required=True, auto='email')}</div>
{field('Mailing address', 'mailing_address', 'textarea', auto='street-address')}
<h3>2. Sponsorship selection</h3>
{checks('Choose a sponsorship', 'sponsorship', ['Clinic Sponsor: $499, 2-hour clinic', 'Community Partner: $999, 4-hour clinic', 'Impact Partner: $2,699, 3-clinic series (save $298)'], kind='radio', required=True)}
<h3>3. Clinic details</h3>
<div class="row-2">{field('Preferred clinic date', 'preferred_date', 'date')}{field('Preferred location', 'preferred_location', hint='Your organization, a library, community center, or ask us to find one.')}</div>
{field('Accessibility or technology needs', 'accessibility_needs', 'textarea')}
{checks('Organization visibility', 'visibility', ['Sponsor booth or branded table', 'Logo on event marketing', 'On-site presence'])}
{field('Additional notes', 'notes', 'textarea')}
<h3>4. Authorization</h3>
<div class="row-2">{field('Authorized representative name', 'authorized_representative', required=True, auto='name')}{field('Type your full name as signature', 'signature', required=True, hint='Typing your name counts as your signature.')}</div>
{checks('Preferred payment method', 'payment_method', ['ACH', 'Check', 'Card'], kind='radio', required=True)}
<p class="small muted">Submitting this form doesn’t charge you. Ashlyn Sidhu will confirm details and send an invoice. Written acknowledgment is provided for every sponsorship.</p>
<button class="btn btn--primary" type="submit">Submit sponsorship form</button>
</form>"""
    body = page_head("Sponsor a Mobile Tech Clinic",
                     "Help older adults stay connected. Your sponsorship removes cost as a barrier for older adults and creates leadership opportunities for young people.") + f"""
<section class="section"><div class="wrap split">
  <div>
    <h2>Two generations, one impact</h2>
    <p>Older adults gain digital confidence, independence, and protection from scams. Student mentors gain leadership, patience, empathy, and real-world communication skills. Each clinic brings generations together around a practical need.</p>
    <h2>What your organization receives</h2>
    <ul>
      <li><b>Sponsorship recognition:</b> your name and logo featured as the clinic sponsor</li>
      <li><b>Community visibility:</b> printed and digital materials, social promotion, partner outreach, and event signage</li>
      <li><b>On-site presence:</b> a resource or branded table to connect with participants, caregivers, and partners</li>
      <li><b>Shareable impact:</b> attendance, approved highlights or photos, and impact language for your marketing</li>
    </ul>
  </div>
  {img('clinic', 'Student mentors helping older adults at a sponsored Mobile Tech Clinic')}
</div></section>
<section class="section section--sky"><div class="wrap">
  <h2>Choose your sponsorship</h2>
  <div class="paths paths--3">{tier_html}</div>
  <p class="note"><b>Location options:</b> host at your organization, a library, community center, or another accessible space. Hosts provide tables, chairs, power, and Wi-Fi when available. Need a venue? We can coordinate with a city or community partner and confirm the final location before invoicing.</p>
</div></section>
<section class="section" id="form"><div class="wrap">
  <h2>Sponsorship form</h2>
  <p>Fields marked <span class="req">*</span> are required. Prefer paper? <a href="{url('/assets/senior-tech-foundation-clinic-sponsorship-2026.pdf')}">Download the sponsorship packet (PDF)</a>.</p>
  {form}
</div></section>
<section class="section section--navy"><div class="wrap band">
  <div><h2>Questions about sponsoring?</h2><p>Contact Ashlyn Sidhu, Executive Director: <a href="tel:{PHONE_TEL}">{PHONE}</a> or <a href="mailto:{EMAIL}">{EMAIL}</a>. Senior Tech Foundation is a Washington 501(c)(3), EIN {EIN}.</p></div>
</div></section>"""
    page("/sponsor/", "Sponsor a Mobile Tech Clinic | Senior Tech Foundation",
         "Sponsor a free Mobile Tech Clinic for older adults in King and Pierce Counties. Clinic Sponsor $499, Community Partner $999, or Impact Partner $2,699.",
         body, trail=[("Home", "/"), ("Partner with us", "/community-partnerships/"), ("Sponsor a clinic", "/sponsor/")], og_image="clinic-1200.webp")


# ---- About / impact ------------------------------------------------------------
VALUES = [
    ("Patience and dignity", "Every older adult deserves to learn technology without pressure, judgment, or embarrassment. We honor each person’s pace, experience, and independence."),
    ("Access and inclusion", "Age, income, ability, or prior experience should never decide who benefits from technology. We work to reduce digital exclusion for older adults of all backgrounds."),
    ("Safety and protection", "Digital safety is part of independence. We help seniors recognize scams, protect their privacy, and use technology with confidence rather than fear."),
    ("Clarity and practical education", "Technology should be useful, not overwhelming. We focus on clear explanations and real-world skills that support everyday life."),
    ("Intergenerational connection", "Technology can bring generations together. Students and young adults supporting seniors builds mutual respect and stronger communities."),
    ("Community and trust", "We build long-term relationships by showing up consistently, listening, and delivering support communities can depend on."),
]


def build_about():
    vals = "".join(f"<div><h3>{n}</h3><p class=\"small\">{d}</p></div>" for n, d in VALUES)
    body = page_head("About Senior Tech Foundation",
                     "A Washington nonprofit helping older adults use technology confidently, safely, and independently, through patient support from trained student mentors.") + f"""
<section class="section"><div class="wrap split">
  <div class="content">
    <div class="answer"><p><b>What is Senior Tech Foundation?</b> {ORG} is a Washington 501(c)(3) nonprofit (EIN {EIN}) serving older adults in King and Pierce Counties. Trained high school and college mentors provide free one-on-one tech help, Mobile Tech Clinics, and digital safety workshops.</p></div>
    <h2>Our mission</h2>
    <p>{ORG} exists to make sure older adults are not left behind in an increasingly digital world. We help seniors use technology confidently, safely, and independently through patient support, practical education, inclusive access, and intergenerational connection.</p>
  </div>
  {img('about', 'Student mentors helping an older man at a Senior Tech Foundation clinic')}
</div></section>
<section class="section section--sky"><div class="wrap content">
  <h2>Our story</h2>
  <p>What started as helping with simple tech questions revealed a deeper problem. Seniors weren’t just struggling with devices. They were worried about clicking the wrong thing, falling for scams, losing access to important accounts, or feeling embarrassed to ask for help. Too often, support was rushed, impersonal, or simply unavailable.</p>
  <p>We saw how different things became when help was patient and personal. When someone sat down, explained things clearly, and answered questions without judgment, confidence grew. A confusing phone became manageable. A suspicious text became a teachable moment. Sometimes a single conversation prevented a scam.</p>
  <p>{ORG} was built around that approach. By pairing older adults with trained young mentors, we create an environment where learning feels comfortable, respectful, and human. Technology shouldn’t be something seniors fear or face alone.</p>
</div></section>
<section class="section"><div class="wrap">
  <h2>Our intergenerational model</h2>
  <div class="split">
    {img('mentors', 'Senior Tech Foundation student mentors standing together at a clinic')}
    <div>
      <p>Our mentors are high school and college students trained to give patient, side-by-side support. Seniors feel comfortable asking questions, and confidence grows. Mentors develop empathy, leadership, and communication skills working with older adults.</p>
      <h3>How we keep help safe</h3>
      <ul>
        <li>Mentors are trained before working with participants</li>
        <li>Mentors explain each step so participants stay in control of their own devices</li>
        <li>Participants enter their own passwords; mentors don’t collect or record them</li>
      </ul>
      <a class="btn btn--primary" href="{url('/volunteer/')}">Become a mentor</a>
    </div>
  </div>
</div></section>
<section class="section section--sky"><div class="wrap">
  <h2>Our values</h2>
  <div class="cols-3">{vals}</div>
</div></section>
<section class="section"><div class="wrap">
  <h2>Leadership</h2>
  <div class="cols-3"><div><h3>Ashlyn Sidhu</h3><p>Executive Director</p><p class="small"><a href="mailto:{EMAIL}">{EMAIL}</a></p></div></div>
</div></section>
{cta_band('See the difference we make', 'Read how we measure our impact across King and Pierce Counties.', [('Our impact', url('/our-impact/'), 'btn--sun'), ('Donate', url('/donate/'), 'btn--light')])}"""
    page("/about/", "About Senior Tech Foundation | Washington Nonprofit for Senior Tech Help",
         "Senior Tech Foundation is a Washington 501(c)(3) nonprofit pairing older adults with trained student mentors for free, patient technology help.",
         body, trail=[("Home", "/"), ("About", "/about/")], og_image="about-800.webp")

    stats = "".join(f'<div class="stat stat--light"><b>{n}</b><span>{l}</span></div>' for n, l in IMPACT)
    body = page_head("Our Impact", "Real people helped, real hours given, and real scams stopped in King and Pierce Counties.") + f"""
<section class="section section--sky"><div class="wrap">
  <h2>Impact to date</h2>
  <div class="stats" style="border-top-color:var(--teal)">{stats}</div>
  <p class="note">{IMPACT_NOTE}</p>
</div></section>
<section class="section"><div class="wrap content">
  <h2>What each number means</h2>
  <ul>
    <li><b>Older adults served:</b> people reached through one-on-one help, clinics, and group Tech Talks.</li>
    <li><b>Hours of one-on-one support:</b> time mentors spent side by side with an individual, recorded in service logs.</li>
    <li><b>Community talks and workshops:</b> group sessions on technology, digital safety, scams, and AI.</li>
    <li><b>Active student mentors:</b> trained high school and college volunteers currently serving.</li>
  </ul>
  <h2>How we measure impact</h2>
  <p>We track impact through scheduled programming, mentor service logs, and community education sessions. Hours are recorded for both group Tech Talks and one-on-one help. People reached is based on attendance at Tech Talks plus tracked individual support. We review and update these numbers regularly as programs grow.</p>
  <h2>What participants tell us</h2>
  <blockquote class="quote"><p>“I felt like the world was moving forward without me. Now I can keep up.”</p><footer>Clinic participant</footer></blockquote>
</div></section>
{cta_band('Help us reach more older adults', 'Your donation keeps every clinic and workshop free.', [('Donate', url('/donate/'), 'btn--sun'), ('Sponsor a clinic', url('/sponsor/'), 'btn--light')])}"""
    page("/our-impact/", "Our Impact | Senior Tech Foundation",
         "Senior Tech Foundation has served 2,600+ older adults with 430+ hours of one-on-one tech support and 100+ community talks across King and Pierce Counties.",
         body, trail=[("Home", "/"), ("Our impact", "/our-impact/")], og_image="clinic-1200.webp")


# ---- Volunteer -------------------------------------------------------------------
def build_volunteer():
    form = f"""<form class="form" action="{FORM_ACTION}" method="POST" data-form="volunteer">
{hidden_fields('New student mentor application', 'Volunteer application')}
<div class="row-2">{field('Full name', 'name', required=True, auto='name')}{field('Email', 'email', 'email', required=True, auto='email')}</div>
<div class="row-2">{field('Phone', 'phone', 'tel', auto='tel')}{field('City', 'city', required=True, auto='address-level2')}</div>
<div class="row-2">{field('School', 'school', required=True)}{field('Grade or year', 'grade', 'select', required=True, options=['9th grade', '10th grade', '11th grade', '12th grade', 'College', 'Other'])}</div>
{checks('Which devices are you comfortable helping with?', 'devices', ['iPhone / iPad', 'Android phones and tablets', 'Windows computers', 'Mac computers', 'Smartwatches', 'Printers and other devices'])}
{field('When are you usually available?', 'availability', hint='For example: weekends, weekday afternoons, summer.')}
{field('Why do you want to be a mentor?', 'why', 'textarea', required=True)}
{field('Parent or guardian email (if under 18)', 'guardian_email', 'email')}
<button class="btn btn--primary" type="submit">Submit application</button>
</form>"""
    body = page_head("Volunteer as a Student Tech Mentor",
                     "High school and college students: help older adults use technology with confidence, and build leadership and communication skills.") + f"""
<section class="section"><div class="wrap split">
  <div class="content">
    <h2>What mentors do</h2>
    <p>Mentors work one-on-one with older adults at Mobile Tech Clinics and help at Tech Talks. You’ll help with phones, tablets, laptops, apps, accounts, and scam questions, explaining each step so participants can do it on their own.</p>
    <h2>What you gain</h2>
    <ul>
      <li>Leadership, patience, and real-world communication skills</li>
      <li>Volunteer hours and experience for college and job applications</li>
      <li>Meaningful connections across generations</li>
    </ul>
    <h2>Training</h2>
    <p>All mentors are trained before they work with participants. Training covers patient teaching, privacy and safety, and common device questions.</p>
  </div>
  {img('volunteer', 'Student mentors working with older adults at a clinic')}
</div></section>
<section class="section section--sky" id="apply"><div class="wrap">
  <h2>Apply to be a mentor</h2>
  <p>Fields marked <span class="req">*</span> are required.</p>
  {form}
</div></section>"""
    page("/volunteer/", "Volunteer as a Student Tech Mentor | Senior Tech Foundation",
         "High school and college students in King and Pierce Counties can volunteer as tech mentors, helping older adults at free Mobile Tech Clinics.",
         body, trail=[("Home", "/"), ("Volunteer", "/volunteer/")], og_image="mentors-800.webp")


# ---- Donate, FAQ, contact, misc -------------------------------------------------
def build_misc():
    body = page_head("Donate to Senior Tech Foundation",
                     "Your gift keeps every clinic, workshop, and hour of one-on-one help free for older adults.") + f"""
<section class="section"><div class="wrap split">
  <div class="content">
    <h2>What your donation does</h2>
    <p>A single donation can mean an older adult gets one-on-one help with a device they’ve struggled with for months, finally understands a confusing setting, or recognizes a suspicious text before clicking a link.</p>
    <p>Donations also fund Tech Talks and digital safety workshops, take-home guides, Wi-Fi hotspots, and training for our student mentors.</p>
    <a class="btn btn--sun" href="{DONATE_URL}" rel="noopener">Donate securely on Givebutter</a>
    <p class="small muted" style="margin-top:20px">{ORG} is a Washington 501(c)(3) nonprofit, EIN {EIN}. Donations are separate from program registration; you never need to donate to receive help.</p>
    <p class="small">Businesses can also <a href="{url('/sponsor/')}">sponsor a Mobile Tech Clinic</a>.</p>
  </div>
  {img('clinic', 'Older adults receiving free help from student mentors')}
</div></section>"""
    page("/donate/", "Donate | Senior Tech Foundation",
         "Donate to Senior Tech Foundation to keep free tech help, Mobile Tech Clinics, and scam prevention education available to older adults in Washington.",
         body, trail=[("Home", "/"), ("Donate", "/donate/")], og_image="clinic-1200.webp")

    items = faq_items() + [
        ("Can my family member come with me?", "Yes. Family members and caregivers are welcome at clinics and workshops."),
        ("Do I have to donate to get help?", "No. Donations are completely separate from our programs. Help is always free."),
        ("How do I volunteer?", f"High school and college students can <a href=\"{url('/volunteer/')}\">apply to be a mentor</a>."),
    ]
    body = page_head("Questions &amp; Answers", "Answers to common questions from older adults, families, and community organizations.") + f"""
<section class="section"><div class="wrap content">{faq_block(items)}
<p style="margin-top:32px">Still have a question? Call <a href="tel:{PHONE_TEL}">{PHONE}</a> or <a href="{url('/contact/')}">send us a message</a>.</p></div></section>"""
    page("/faq/", "Senior Tech Help FAQ | Senior Tech Foundation",
         "Is senior tech help free? What devices do you help with? Where are clinics? Answers to common questions about Senior Tech Foundation.",
         body, trail=[("Home", "/"), ("FAQ", "/faq/")], extra_ld=[faq_ld(items)])

    form = f"""<form class="form" action="{FORM_ACTION}" method="POST" data-form="contact">
{hidden_fields('New website message', 'Contact form')}
<div class="row-2">{field('Your name', 'name', required=True, auto='name')}{field('Phone', 'phone', 'tel', auto='tel', hint='We’re happy to call you back.')}</div>
{field('Email', 'email', 'email', auto='email')}
{field('What is this about?', 'reason', 'select', required=True, options=['I need tech help', 'Hosting a program', 'Sponsorship', 'Volunteering', 'Media or press', 'Something else'])}
{field('Message', 'message', 'textarea', required=True)}
<button class="btn btn--primary" type="submit">Send message</button>
</form>"""
    body = page_head("Contact Us", "Call, email, or send a message. We’re happy to help.") + f"""
<section class="section"><div class="wrap split" style="align-items:start">
  <div>
    <h2>Call or email</h2>
    <p class="lead"><a href="tel:{PHONE_TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    <p>Serving King &amp; Pierce Counties, Washington.</p>
    <p>Looking for help with a device? The fastest way is to come to a <a href="{url('/events/')}">free tech clinic</a>.</p>
  </div>
  <div><h2>Send a message</h2>{form}</div>
</div></section>"""
    page("/contact/", "Contact Senior Tech Foundation",
         f"Contact Senior Tech Foundation by phone at {PHONE}, by email, or with our message form.",
         body, trail=[("Home", "/"), ("Contact", "/contact/")])

    body = page_head("Thank you!", "Your message was sent. We’ll get back to you within a few business days.") + f"""
<section class="section"><div class="wrap"><p>Need help sooner? Call <a href="tel:{PHONE_TEL}">{PHONE}</a>.</p>
<a class="btn btn--primary" href="{url('/')}">Back to the home page</a></div></section>"""
    page("/thank-you/", "Thank You | Senior Tech Foundation", "Your submission was received.", body, noindex=True)

    body = page_head("Privacy Policy", "How Senior Tech Foundation handles information you share on this website.") + f"""
<section class="section"><div class="wrap content">
<h2>Information we collect</h2>
<p>When you submit a form, we receive the information you enter, such as your name, contact details, and message. We use it only to respond to you and to run our programs.</p>
<h2>How forms are delivered</h2>
<p>Website forms are delivered to our email through FormSubmit, a form delivery service. Donations are processed by Givebutter, which has its own privacy policy.</p>
<h2>What we don’t do</h2>
<p>We never sell or trade your personal information. We don’t ask for passwords through this website, and mentors never collect or record passwords at clinics.</p>
<h2>Analytics</h2>
<p>We may use Google Analytics to understand how visitors use this website. This data is aggregated and doesn’t identify you personally.</p>
<h2>Contact</h2>
<p>Questions about privacy? Email <a href="mailto:{EMAIL}">{EMAIL}</a> or call <a href="tel:{PHONE_TEL}">{PHONE}</a>.</p>
<p class="small muted">Last updated {date.today().strftime('%B %Y')}.</p>
</div></section>"""
    page("/privacy/", "Privacy Policy | Senior Tech Foundation", "Privacy policy for the Senior Tech Foundation website.",
         body, trail=[("Home", "/"), ("Privacy", "/privacy/")])

    body = page_head("Page not found", "Sorry, we couldn’t find that page.") + f"""
<section class="section"><div class="wrap"><p>Try one of these instead:</p>
<ul><li><a href="{url('/')}">Home</a></li><li><a href="{url('/free-tech-help-for-seniors/')}">Get free tech help</a></li><li><a href="{url('/events/')}">Upcoming events</a></li><li><a href="{url('/contact/')}">Contact us</a></li></ul>
<p>Or call <a href="tel:{PHONE_TEL}">{PHONE}</a>.</p></div></section>"""
    page("/404.html", "Page Not Found | Senior Tech Foundation", "Page not found.", body, noindex=True)


def build_seo_files():
    today = date.today().isoformat()
    urls = "".join(f"<url><loc>{abs_url(p)}</loc><lastmod>{today}</lastmod></url>" for p in SITEMAP if p != "/404.html")
    (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    (ROOT / "robots.txt").write_text(f"""User-agent: *
Allow: /
Disallow: /tools/
Disallow: /thank-you/

User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: OAI-SearchBot
Allow: /

Sitemap: {abs_url('/sitemap.xml')}
""")


SITEMAP = []
STAMP = datetime.now().strftime("%Y%m%d%H%M")

if __name__ == "__main__":
    (ROOT / "assets").mkdir(exist_ok=True)
    (ROOT / "assets/site.css").write_text((TOOLS / "site.css").read_text())
    home()
    build_programs()
    build_events()
    build_partnerships()
    build_sponsor()
    build_about()
    build_volunteer()
    build_misc()
    for old, new in {"/our-story/": "/about/", "/our-team/": "/about/", "/programs/": "/free-tech-help-for-seniors/",
                     "/how-we-help/": "/free-tech-help-for-seniors/", "/contact-us/": "/contact/",
                     "/become-a-volunteer/": "/volunteer/", "/partner-with-us/": "/community-partnerships/",
                     "/donation/": "/donate/", "/core-values/": "/about/", "/gallery/": "/about/",
                     "/blog/": "/", "/social-media/": "/contact/", "/career/": "/volunteer/",
                     "/podcast/": "/", "/all-forms/": "/contact/", "/page-404/": "/"}.items():
        redirect(old, new)
    build_seo_files()
    print("Built", len(SITEMAP), "pages")
