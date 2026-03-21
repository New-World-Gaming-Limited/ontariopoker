#!/usr/bin/env python3
"""
OntarioPoker.com Site Builder
Generates all HTML pages from data.json using the sweepstakesites.com architecture.
"""

import json, os, html, hashlib, datetime

SRC = os.path.join(os.path.dirname(__file__), "src")
OUT = os.path.join(os.path.dirname(__file__), "OntarioPoker.com")
BASE_URL = "https://ontariopoker.com"
SITE_NAME = "OntarioPoker"
NOW = datetime.datetime.now()
DATE_STR = NOW.strftime("%B %d, %Y")
MONTH_YEAR = NOW.strftime("%B %Y")
ISO_DATE = NOW.strftime("%Y-%m-%d")

with open(os.path.join(SRC, "data.json"), "r") as f:
    DATA = json.load(f)

BRANDS = DATA["brands"]
AUTHORS = DATA["authors"]
P1_BRANDS = [b for b in BRANDS if b["priority"] == 1]
P2_BRANDS = [b for b in BRANDS if b["priority"] == 2]

os.makedirs(OUT, exist_ok=True)
os.makedirs(os.path.join(OUT, "images"), exist_ok=True)
for b in BRANDS:
    os.makedirs(os.path.join(OUT, b["id"]), exist_ok=True)

# ── Shared HTML Components ──────────────────────────────────────────

CRITICAL_CSS = open(os.path.join(os.path.dirname(__file__), "critical.css")).read() if os.path.exists(os.path.join(os.path.dirname(__file__), "critical.css")) else ""

CHEVRON_SVG = '<svg width="10" height="10" viewBox="0 0 10 10" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 4l3 3 3-3"/></svg>'
SEARCH_SVG = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>'
MOON_SVG = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>'
MENU_SVG = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12h18M3 6h18M3 18h18"/></svg>'
SHIELD_SVG = '<svg fill="none" stroke="currentColor" stroke-width="2" style="width:32px;height:32px;flex-shrink:0;" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>'
FOOTER_CHEVRON = '<svg class="footer-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><path d="M6 9l6 6 6-6"/></svg>'
FAQ_CHEVRON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18"><path d="M6 9l6 6 6-6"/></svg>'

def head(title, desc, canonical, prefix="./", extra_json_ld="", is_root=True):
    ga = ""
    if DATA.get("gaId"):
        ga = f'''<script async src="https://www.googletagmanager.com/gtag/js?id={DATA["gaId"]}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{DATA["gaId"]}');</script>'''
    css_path = f'{prefix}style.min.css'
    return f'''<!DOCTYPE html>
<html lang="en-CA">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preload" href="https://api.fontshare.com/v2/css?f[]=general-sans@400,600,700&display=swap" as="style">
<link rel="preconnect" href="https://api.fontshare.com" crossorigin>
<link href="https://api.fontshare.com/v2/css?f[]=general-sans@400,600,700&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@800&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
<title>{html.escape(title)} | {SITE_NAME}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}">
<style>{CRITICAL_CSS}</style>
<link href="{css_path}" rel="stylesheet" media="print" onload="this.media='all'">
<noscript><link href="{css_path}" rel="stylesheet"></noscript>
{extra_json_ld}
<meta property="og:title" content="{html.escape(title)} | {SITE_NAME}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:image" content="{BASE_URL}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/svg+xml" href="{prefix}favicon.svg">
<link rel="icon" type="image/png" href="{prefix}favicon.png" sizes="32x32">
<link rel="apple-touch-icon" href="{prefix}apple-touch-icon.png">
{ga}
</head>'''

def disclosure_bar(prefix="./"):
    return f'''<div class="disclosure-bar">
  {DATA["disclosureText"]} <a href="{prefix}affiliate-disclosure.html">Affiliate Disclosure</a>
</div>'''

def header_nav(prefix="./"):
    brand_links = "\n".join([f'          <a href="{prefix}{b["id"]}/index.html">{b["name"]}</a>' for b in BRANDS])
    review_links = "\n".join([f'          <a href="{prefix}{b["id"]}/review.html">{b["name"]} Review</a>' for b in BRANDS])
    promo_links = "\n".join([f'          <a href="{prefix}{b["id"]}/promo-code.html">{b["name"]} Promo</a>' for b in BRANDS])

    guide_cols = ""
    for b in P1_BRANDS:
        guide_cols += f'''          <div class="nav-dropdown-col">
            <span class="nav-dropdown-heading">{b["name"]}</span>
            <a href="{prefix}{b["id"]}/review.html">Review</a>
            <a href="{prefix}{b["id"]}/promo-code.html">Promo/Offer Status</a>
          </div>
'''

    return f'''<header class="site-header">
  <div class="container">
    <a href="{prefix}index.html" class="site-logo">
      <img src="{prefix}images/ontariopoker-logo.svg" alt="{SITE_NAME}" style="height:32px;width:auto;">
    </a>
    <nav class="nav-desktop" aria-label="Main navigation">
      <div class="nav-dropdown">
        <button class="nav-dropdown-trigger">Poker Rooms {CHEVRON_SVG}</button>
        <div class="nav-dropdown-menu">
{brand_links}
        </div>
      </div>
      <div class="nav-dropdown">
        <button class="nav-dropdown-trigger">Reviews {CHEVRON_SVG}</button>
        <div class="nav-dropdown-menu">
{review_links}
          <div class="nav-dropdown-divider"></div>
          <a href="{prefix}compare.html">Compare All</a>
        </div>
      </div>
      <div class="nav-dropdown">
        <button class="nav-dropdown-trigger">Promotions {CHEVRON_SVG}</button>
        <div class="nav-dropdown-menu">
{promo_links}
          <div class="nav-dropdown-divider"></div>
          <a href="{prefix}ontario-poker-promo-codes.html">All Promo Codes</a>
        </div>
      </div>
      <a href="{prefix}is-online-poker-legal-in-ontario.html" class="nav-link">Legal Guide</a>
    </nav>
    <div class="nav-actions">
      <button class="search-btn" aria-label="Search site">{SEARCH_SVG}</button>
      <button class="theme-toggle" data-theme-toggle aria-label="Toggle dark mode">{MOON_SVG}</button>
      <a href="{prefix}best-poker-sites-ontario.html" class="header-cta">Best Poker Sites</a>
      <button class="mobile-menu-btn" aria-label="Open menu" aria-expanded="false">{MENU_SVG}</button>
    </div>
  </div>
</header>'''

def mobile_nav(prefix="./"):
    brand_links = "\n".join([f'    <a href="{prefix}{b["id"]}/index.html">{b["name"]}</a>' for b in BRANDS])
    review_links = "\n".join([f'    <a href="{prefix}{b["id"]}/review.html">{b["name"]} Review</a>' for b in BRANDS])
    promo_links = "\n".join([f'    <a href="{prefix}{b["id"]}/promo-code.html">{b["name"]} Promo</a>' for b in BRANDS])
    return f'''<nav class="mobile-nav" aria-label="Mobile navigation">
  <div class="mobile-nav-section">
    <span class="mobile-nav-heading">Poker Rooms</span>
{brand_links}
  </div>
  <div class="mobile-nav-section">
    <span class="mobile-nav-heading">Reviews</span>
{review_links}
    <a href="{prefix}compare.html">Compare All</a>
  </div>
  <div class="mobile-nav-section">
    <span class="mobile-nav-heading">Promotions</span>
{promo_links}
    <a href="{prefix}ontario-poker-promo-codes.html">All Promo Codes</a>
  </div>
  <div class="mobile-nav-section">
    <span class="mobile-nav-heading">Guides</span>
    <a href="{prefix}is-online-poker-legal-in-ontario.html">Legal Guide</a>
    <a href="{prefix}ontario-poker-apps.html">Poker Apps</a>
    <a href="{prefix}ontario-poker-tournaments.html">Tournaments</a>
    <a href="{prefix}ontario-poker-freerolls.html">Freerolls</a>
    <a href="{prefix}responsible-gambling.html">Responsible Gambling</a>
  </div>
  <a href="{prefix}best-poker-sites-ontario.html" class="nav-cta-mobile">Best Poker Sites &rarr;</a>
</nav>'''

def footer(prefix="./"):
    return f'''<footer class="site-footer">
<div class="container">
<div class="footer-rg">
{SHIELD_SVG}
<p>Poker is supposed to be fun. If it stops feeling that way, step away. Help is available at ConnexOntario: 1-866-531-2600.</p>
<a class="btn btn--sm" href="{prefix}responsible-gambling.html" style="background:rgba(255,255,255,0.15);color:inherit;white-space:nowrap;">Responsible Gambling</a>
</div>
<div class="footer-brand">
<a class="site-logo" href="{prefix}index.html" style="margin-bottom:var(--space-2);">
<img src="{prefix}images/ontariopoker-logo.svg" alt="{SITE_NAME}" style="height:26px;width:auto;">
</a>
<p>Your regulated Ontario poker resource online. Reviews, promotions, and guides for all six licensed poker rooms. Published by {DATA["operator"]["name"]}.</p>
<p style="margin-top:var(--space-2);font-size:var(--text-xs);color:var(--color-text-faint);">ontariopoker.com &middot; {DATA["operator"]["address"]} &middot; <a href="mailto:{DATA["operator"]["email"]}" style="color:inherit;">{DATA["operator"]["email"]}</a></p>
</div>
<div class="footer-columns">
<div class="footer-col">
<h4 class="footer-col-toggle">Poker Rooms{FOOTER_CHEVRON}</h4>
<div class="footer-col-links">
{"".join([f'<a href="{prefix}{b["id"]}/index.html">{b["name"]}</a>' for b in BRANDS])}
<a href="{prefix}compare.html">Compare All Rooms</a>
<a href="{prefix}best-poker-sites-ontario.html">Best Poker Sites</a>
</div>
</div>
<div class="footer-col">
<h4 class="footer-col-toggle">Guides{FOOTER_CHEVRON}</h4>
<div class="footer-col-links">
<a href="{prefix}ontario-poker-promo-codes.html">Promo Codes</a>
<a href="{prefix}ontario-poker-tournaments.html">Tournaments</a>
<a href="{prefix}ontario-poker-freerolls.html">Freerolls</a>
<a href="{prefix}ontario-poker-apps.html">Poker Apps</a>
<a href="{prefix}ontario-poker-withdrawal-times.html">Withdrawal Times</a>
<a href="{prefix}ontario-poker-payment-methods.html">Payment Methods</a>
<a href="{prefix}ontario-poker-rakeback-rewards.html">Rakeback &amp; Rewards</a>
</div>
</div>
<div class="footer-col">
<h4 class="footer-col-toggle">Transparency{FOOTER_CHEVRON}</h4>
<div class="footer-col-links">
<a href="{prefix}editorial-policy.html">Editorial Policy</a>
<a href="{prefix}fact-checking.html">Fact Checking</a>
<a href="{prefix}corrections-policy.html">Corrections Policy</a>
<a href="{prefix}affiliate-disclosure.html">Affiliate Disclosure</a>
<a href="{prefix}complaints-policy.html">Complaints Policy</a>
</div>
</div>
<div class="footer-col">
<h4 class="footer-col-toggle">Responsible Gambling{FOOTER_CHEVRON}</h4>
<div class="footer-col-links">
<a href="{prefix}responsible-gambling.html">Responsible Gambling</a>
<a href="{prefix}self-exclusion-resources.html">Self-Exclusion Resources</a>
<a href="{prefix}how-to-complain-about-an-ontario-poker-site.html">How to Complain</a>
<a href="{prefix}contact.html">Contact &amp; Support</a>
</div>
</div>
<div class="footer-col">
<h4 class="footer-col-toggle">Legal{FOOTER_CHEVRON}</h4>
<div class="footer-col-links">
<a href="{prefix}about.html">About Us</a>
<a href="{prefix}management-team.html">Our Authors</a>
<a href="{prefix}privacy.html">Privacy Policy</a>
<a href="{prefix}cookie-policy.html">Cookie Policy</a>
<a href="{prefix}terms.html">Terms &amp; Conditions</a>
<a href="{prefix}accessibility.html">Accessibility</a>
</div>
</div>
</div>
<div class="ftc-footer">
<p><strong>Affiliate Disclosure:</strong> OntarioPoker.com is owned and operated by {DATA["operator"]["name"]}. This site contains affiliate links. If you click through and register using our links, we may receive compensation at no additional cost to you. All editorial ratings are our own. See our <a href="{prefix}affiliate-disclosure.html" style="color:inherit;text-decoration:underline;">Affiliate Disclosure</a>.</p>
<p><strong>Disclaimer:</strong> Online poker in Ontario is regulated by the Alcohol and Gaming Commission of Ontario (AGCO) and operated through iGaming Ontario. You must be 19+ and physically located in Ontario to play. If you or someone you know has a gambling problem, call ConnexOntario at 1-866-531-2600.</p>
</div>
<div class="footer-bottom">
<span>&copy; 2026 {DATA["operator"]["name"]} &middot; ontariopoker.com. All rights reserved.</span>
</div>
</div>
</footer>'''

def search_overlay(prefix="./"):
    return f'''<div id="searchOverlay" class="search-overlay">
  <div class="search-box">
    <div class="search-input-wrap">{SEARCH_SVG}
      <input type="text" class="search-input" placeholder="Search reviews, guides, promotions..." autocomplete="off">
      <button class="search-close" aria-label="Close search"><span aria-hidden="true">&#x2715;</span></button>
    </div>
    <div class="search-results"></div>
  </div>
</div>'''

def page_shell(title, desc, canonical, content, prefix="./", extra_json_ld="", sticky_cta=False, sticky_brand=None):
    sticky = ""
    if sticky_cta and sticky_brand:
        b = sticky_brand
        sticky = f'''<div id="stickyCta" class="sticky-cta">
  <div class="container" style="display:flex;align-items:center;justify-content:space-between;gap:var(--space-4);">
    <div style="font-weight:700;color:#fff;font-size:var(--text-sm);">{b["name"]}: {b["welcomeBonusShort"]}</div>
    <a href="{b["exitLink"]}" class="btn btn--sm" target="_blank" rel="sponsored noopener noreferrer" style="background:#fff;color:var(--color-primary);font-weight:700;">Visit {b["name"]} &rarr;</a>
  </div>
</div>'''
    return f'''{head(title, desc, canonical, prefix, extra_json_ld)}
<body>
{disclosure_bar(prefix)}
{header_nav(prefix)}
{mobile_nav(prefix)}
<main>
{content}
</main>
{footer(prefix)}
{search_overlay(prefix)}
{sticky}
<script src="{prefix}app.min.js" defer></script>
</body>
</html>'''

def breadcrumb_html(crumbs, prefix="./"):
    parts = []
    for c in crumbs:
        if c.get("url"):
            parts.append(f'<a href="{prefix}{c["url"]}">{c["name"]}</a>')
        else:
            parts.append(f'<span>{c["name"]}</span>')
    return '<div class="breadcrumb">' + ' <span>/</span> '.join(parts) + '</div>'

def breadcrumb_jsonld(crumbs):
    items = []
    for i, c in enumerate(crumbs):
        item = {"@type": "ListItem", "position": i+1, "name": c["name"]}
        if c.get("canonical"):
            item["item"] = c["canonical"]
        items.append(item)
    return json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items})

def faq_html(faqs):
    items = ""
    for q, a in faqs:
        items += f'''<div class="faq-item">
  <button class="faq-question">{html.escape(q)}{FAQ_CHEVRON}</button>
  <div class="faq-answer"><p>{a}</p></div>
</div>
'''
    return f'<div class="faq-list">{items}</div>'

def faq_jsonld(faqs):
    entities = []
    for q, a in faqs:
        entities.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities})

def score_bars(brand):
    cats = [
        ("Bonus & Promotions", brand["ratingBonus"]),
        ("Software & Features", brand["ratingSoftware"]),
        ("Tournament Offering", brand["ratingTournaments"]),
        ("Cash Games", brand["ratingCashGames"]),
        ("Payments", brand["ratingPayments"]),
        ("Support", brand["ratingSupport"]),
    ]
    rows = ""
    for label, score in cats:
        pct = int(score * 10)
        rows += f'''<div class="score-row"><div class="score-label">{label}</div><div class="score-bar-track"><div class="score-bar-fill" data-width="{pct}"></div></div><div class="score-value">{score}/10</div></div>
'''
    overall_pct = int(brand["overallRating"] * 10)
    rows += f'''<div class="score-row"><div class="score-label">Overall</div><div class="score-bar-track"><div class="score-bar-fill" data-width="{overall_pct}" style="background:var(--color-success);"></div></div><div class="score-value" style="color:var(--color-success);">{brand["overallRating"]}/10</div></div>'''
    return f'<div class="card card--flat" style="margin:var(--space-6) 0;">{rows}</div>'

def promo_status_badge(status):
    if status == "verified_public":
        return '<span class="badge badge--success">Verified Public Code</span>'
    elif status == "none_captured":
        return '<span class="badge badge--warning">No Public Code Identified</span>'
    else:
        return '<span class="badge badge--muted">Unverified</span>'

def write_page(path, content):
    filepath = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Built: {path}")


# ══════════════════════════════════════════════════════════════════════
#  PAGE GENERATORS
# ══════════════════════════════════════════════════════════════════════

def build_homepage():
    brand_cards = ""
    for i, b in enumerate(BRANDS[:4]):
        rank = i + 1
        code_html = ""
        if b["promoCode"]:
            code_html = f'''<div class="hero-card-code"><span class="code-mono">{b["promoCode"]}</span></div>'''
        features = "".join([f"<li>{f}</li>" for f in b["keyFeatures"][:3]])
        brand_cards += f'''<div class="hero-card" style="--card-accent:{b['baseColour']};">
  <div class="hero-card-rank">{rank}</div>
  <div class="hero-card-header">
    <h3>{b["name"]}</h3>
    <span class="hero-card-badge" style="background:{b['baseColour']};color:{b['textColour']};">{b["overallRating"]}/10</span>
  </div>
  <div class="hero-card-bonus">{b["welcomeBonusShort"]}</div>
  {code_html}
  <ul class="hero-card-features">{features}</ul>
  <a href="{b["exitLink"]}" class="btn btn--primary" target="_blank" rel="sponsored noopener noreferrer">Visit {b["name"]} &rarr;</a>
  <a href="{b["id"]}/review.html" class="hero-card-review-link">Read Full Review</a>
</div>'''

    comparison_rows = ""
    for b in BRANDS:
        status = promo_status_badge(b["promoCodeStatus"])
        code = b["promoCode"] if b["promoCode"] else "N/A"
        comparison_rows += f'''<tr>
  <td><strong>{b["name"]}</strong></td>
  <td>{b["overallRating"]}/10</td>
  <td>{b["welcomeBonusShort"]}</td>
  <td>{code}</td>
  <td>{status}</td>
  <td><a href="{b["id"]}/review.html">Review</a></td>
</tr>'''

    faqs = [
        ("Is online poker legal in Ontario?", "Yes. Online poker is legal and regulated in Ontario through iGaming Ontario (iGO), which launched the regulated market on April 4, 2022. Only operators registered with the AGCO and iGO are permitted to offer online poker to Ontario residents."),
        ("How many regulated poker sites are there in Ontario?", f"As of {DATA['marketData']['directoryDate']}, there are six live regulated poker brands: GGPoker, 888poker, BetMGM Poker, PokerStars Ontario, PartyPoker Ontario, and Bwin Ontario."),
        ("Do I need to be in Ontario to play?", "Yes. Geolocation technology verifies that you are physically located within Ontario before you can play. You must be 19 or older."),
        ("Can I play on unregulated poker sites from Ontario?", "While some offshore sites may still accept Ontario players, iGaming Ontario advises players to 'Make the safer choice' and play only on sites offered by fully registered and approved operators. This site covers regulated operators exclusively."),
    ]

    faq_ld = f'<script type="application/ld+json">{faq_jsonld(faqs)}</script>'
    org_ld = f'''<script type="application/ld+json">{json.dumps({
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": SITE_NAME,
        "url": BASE_URL,
        "description": "Ontario's regulated poker guide covering all six licensed poker rooms.",
        "address": {"@type": "PostalAddress", "streetAddress": DATA["operator"]["address"]},
        "contactPoint": {"@type": "ContactPoint", "email": DATA["operator"]["email"]}
    })}</script>'''

    content = f'''
<section class="hero">
  <div class="container">
    <div class="hero-badge">Regulated Ontario Poker</div>
    <h1>Ontario Poker Sites: All 6 Regulated Rooms Reviewed</h1>
    <p class="hero-subtitle">Independent reviews, verified promotions, and honest comparisons. Every room on this site is fully registered with iGaming Ontario.</p>
    <div class="hero-trust">
      <span class="trust-item">&#x2713; 6 Regulated Rooms</span>
      <span class="trust-item">&#x2713; Verified {MONTH_YEAR}</span>
      <span class="trust-item">&#x2713; 19+ Only</span>
    </div>
    <div class="hero-cards-grid">
{brand_cards}
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-header">
      <h2>Quick Comparison: All Ontario Poker Rooms</h2>
      <p>Last updated <span class="dynamic-date-full">{DATE_STR}</span>. All operators verified against the official iGO directory.</p>
    </div>
    <div class="compare-table-wrap">
      <table class="compare-table">
        <thead><tr><th>Room</th><th>Rating</th><th>Welcome Offer</th><th>Code</th><th>Status</th><th>Review</th></tr></thead>
        <tbody>{comparison_rows}</tbody>
      </table>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="container container--default">
    <div class="section-header">
      <h2>Why Only Regulated Rooms?</h2>
    </div>
    <div class="prose">
      <p>iGaming Ontario tells players to "Make the safer choice and play on sites offered by fully registered and approved Operators in Ontario." That is our editorial policy too. Every poker room on this site is verified against the official iGO operator directory.</p>
      <p>The regulated market represents the majority of Ontario's online gambling activity, with a channelization rate of {DATA["marketData"]["channelizationRate"]} in FY2024-25. That means most Ontario players are already choosing regulated sites. This portal covers all six of them, and nothing else.</p>
      <p>Ontario's regulated poker vertical generated approximately {DATA["marketData"]["totalNAGGR2025"]} of NAGGR in 2025, from {DATA["marketData"]["totalWagers2025"]} in wagers. While poker is a small share of the total market ({DATA["marketData"]["pokerShareNAGGR"]}), these are high-intent players who value verified information over generic listicles.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="container container--default">
    <div class="section-header">
      <h2>Explore by Category</h2>
    </div>
    <div style="display:grid;gap:var(--space-3);grid-template-columns:repeat(auto-fit,minmax(min(260px,100%),1fr));">
      <a href="ontario-poker-tournaments.html" class="card" style="text-decoration:none;color:inherit;padding:var(--space-4) var(--space-5);border-left:4px solid var(--color-primary);">
        <h3 style="font-size:var(--text-base);font-weight:700;margin-bottom:var(--space-1);">Ontario Poker Tournaments</h3>
        <p style="font-size:var(--text-sm);color:var(--color-text-muted);margin:0;">Daily schedules, festival trackers, and qualifier guides.</p>
      </a>
      <a href="ontario-poker-freerolls.html" class="card" style="text-decoration:none;color:inherit;padding:var(--space-4) var(--space-5);border-left:4px solid var(--color-primary);">
        <h3 style="font-size:var(--text-base);font-weight:700;margin-bottom:var(--space-1);">Freerolls</h3>
        <p style="font-size:var(--text-sm);color:var(--color-text-muted);margin:0;">Free-entry tournaments across all Ontario rooms.</p>
      </a>
      <a href="ontario-poker-rakeback-rewards.html" class="card" style="text-decoration:none;color:inherit;padding:var(--space-4) var(--space-5);border-left:4px solid var(--color-primary);">
        <h3 style="font-size:var(--text-base);font-weight:700;margin-bottom:var(--space-1);">Rakeback and Rewards</h3>
        <p style="font-size:var(--text-sm);color:var(--color-text-muted);margin:0;">Loyalty programs, rakeback deals, and reward calculators.</p>
      </a>
      <a href="is-online-poker-legal-in-ontario.html" class="card" style="text-decoration:none;color:inherit;padding:var(--space-4) var(--space-5);border-left:4px solid var(--color-primary);">
        <h3 style="font-size:var(--text-base);font-weight:700;margin-bottom:var(--space-1);">Is Online Poker Legal?</h3>
        <p style="font-size:var(--text-sm);color:var(--color-text-muted);margin:0;">Complete guide to Ontario's regulated poker framework.</p>
      </a>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="container container--default">
    <h2>Frequently Asked Questions</h2>
    {faq_html(faqs)}
  </div>
</section>
'''

    write_page("index.html", page_shell(
        "Best Ontario Poker Sites 2026 | All 6 Regulated Rooms",
        f"Compare all 6 regulated Ontario poker rooms: GGPoker, 888poker, BetMGM, PokerStars, PartyPoker, Bwin. Verified promotions and honest reviews. Updated {MONTH_YEAR}.",
        f"{BASE_URL}/",
        content,
        "./",
        faq_ld + "\n" + org_ld
    ))


def build_brand_review(brand):
    bid = brand["id"]
    prefix = "../"

    bc = [
        {"name": "Home", "url": "index.html", "canonical": f"{BASE_URL}/"},
        {"name": brand["name"], "url": f"{bid}/index.html", "canonical": f"{BASE_URL}/{bid}/"},
        {"name": "Review"}
    ]
    bc_ld = f'<script type="application/ld+json">{breadcrumb_jsonld(bc)}</script>'

    review_ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "Review",
        "name": f"{brand['name']} Review 2026",
        "author": {"@type": "Person", "name": AUTHORS[0]["name"]},
        "reviewRating": {"@type": "Rating", "ratingValue": str(brand["overallRating"]), "bestRating": "10"},
        "itemReviewed": {"@type": "WebApplication", "name": brand["name"]},
        "datePublished": "2026-01-15",
        "dateModified": ISO_DATE,
        "publisher": {"@type": "Organization", "name": SITE_NAME}
    })

    faqs = [
        (f"Is {brand['name']} legal in Ontario?", f"Yes. {brand['name']} is operated by {brand['legalEntity']} and is fully registered with iGaming Ontario. It appears on the official iGO operator directory."),
        (f"What is the {brand['name']} welcome offer?", f"The current public welcome offer is: {brand['welcomeBonus']}. Check the operator site for the most current terms."),
        (f"Can I play {brand['name']} on mobile?", f"{brand['name']} offers: {brand['mobileApp']}. Both cash games and tournaments are accessible on mobile."),
        (f"How do I deposit at {brand['name']} Ontario?", f"Available deposit methods include: {brand['depositMethods']}. Minimum deposit is typically {brand['minDeposit']}."),
    ]
    faq_ld = f'<script type="application/ld+json">{faq_jsonld(faqs)}</script>'

    pros = "".join([f"<li><strong>{p.split('.')[0]}.</strong> {''.join(p.split('.')[1:])}</li>" if '.' in p else f"<li>{p}</li>" for p in brand["pros"]])
    cons = "".join([f"<li><strong>{c.split('.')[0]}.</strong> {''.join(c.split('.')[1:])}</li>" if '.' in c else f"<li>{c}</li>" for c in brand["cons"]])

    features_rows = f'''
<tr><td>Cash Games</td><td>{brand["cashGameFormats"]}</td></tr>
<tr><td>Tournaments</td><td>{brand["tournamentFormats"]}</td></tr>
<tr><td>Jackpot Format</td><td>{brand["jackpotFormat"]}</td></tr>
<tr><td>Software</td><td>{brand["softwareFeatures"]}</td></tr>
<tr><td>Rewards</td><td>{brand["rewards"]}</td></tr>
<tr><td>Deposits</td><td>{brand["depositMethods"]}</td></tr>
<tr><td>Withdrawals</td><td>{brand["withdrawalMethods"]}</td></tr>
<tr><td>Support</td><td>{brand["customerSupport"]}</td></tr>
<tr><td>Mobile</td><td>{brand["mobileApp"]}</td></tr>'''

    sidebar_items = ""
    if brand["promoCode"]:
        sidebar_items += f'''<div class="sidebar-promo-item"><div class="sidebar-promo-rank">&#10003;</div><div class="sidebar-promo-details"><div class="sidebar-promo-name">Code: {brand["promoCode"]}</div></div></div>'''
    sidebar_items += f'''<div class="sidebar-promo-item"><div class="sidebar-promo-rank">&#10003;</div><div class="sidebar-promo-details"><div class="sidebar-promo-name">{brand["welcomeBonusShort"]}</div></div></div>'''
    sidebar_items += f'''<div class="sidebar-promo-item"><div class="sidebar-promo-rank">&#10003;</div><div class="sidebar-promo-details"><div class="sidebar-promo-name">Regulated by iGO</div></div></div>'''
    sidebar_items += f'''<div class="sidebar-promo-item"><div class="sidebar-promo-rank">&#10003;</div><div class="sidebar-promo-details"><div class="sidebar-promo-name">{brand["legalEntity"]}</div></div></div>'''

    content = f'''
<section class="page-hero" data-brand="{brand["name"]}">
  <div class="container">
    {breadcrumb_html(bc, prefix)}
    <h1>{brand["name"]} Review 2026</h1>
    <p class="page-hero-subtitle">{brand["bestFor"]}</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="content-layout content-layout--sidebar">
      <div class="content-main prose">

        <h2>Overview</h2>
        <p>{brand["name"]} is operated by {brand["legalEntity"]} and is fully registered with iGaming Ontario. It is best for: {brand["bestFor"].lower()}.</p>
        <p>The current welcome offer is: <strong>{brand["welcomeBonus"]}</strong>. {f'Use promo code <span class="code-badge">{brand["promoCode"]}</span> at signup.' if brand["promoCode"] else 'No public promo code was captured in this research.'}</p>

        {score_bars(brand)}

        <h2>Feature Breakdown</h2>
        <div class="card card--flat">
          <table class="promos-table"><tbody>{features_rows}</tbody></table>
        </div>

        <h2>Bonus and Offer Details</h2>
        <div class="card card--flat" style="margin:var(--space-4) 0;">
          <table class="promos-table"><tbody>
            <tr><td>Welcome Offer</td><td>{brand["welcomeBonus"]}</td></tr>
            <tr><td>Promo Code</td><td>{brand["promoCode"] if brand["promoCode"] else "No public code captured"} {promo_status_badge(brand["promoCodeStatus"])}</td></tr>
            <tr><td>Unlock Rate</td><td>{brand["bonusUnlockRate"]}</td></tr>
            <tr><td>Clear Window</td><td>{brand["bonusClearWindow"]}</td></tr>
            <tr><td>Withdrawal Effect</td><td>{brand["bonusWithdrawalNote"]}</td></tr>
            <tr><td>Min Deposit</td><td>{brand["minDeposit"]}</td></tr>
          </tbody></table>
        </div>

        <h2>What We Like</h2>
        <ul>{pros}</ul>

        <h2>What Could Be Better</h2>
        <ul>{cons}</ul>

        <h2>Who Should Play at {brand["name"]}?</h2>
        <p>{brand["bestFor"]}. If this matches what you are looking for, {brand["name"]} is a strong choice among Ontario's six regulated poker rooms.</p>

        <div style="text-align:center;margin:var(--space-6) 0;">
          <a href="{brand["exitLink"]}" class="btn btn--primary" target="_blank" rel="sponsored noopener noreferrer">Visit {brand["name"]} &rarr;</a>
        </div>

        <h2>Frequently Asked Questions</h2>
        {faq_html(faqs)}

        <div style="margin-top:var(--space-8);">
          <h2 style="font-size:var(--text-base);font-weight:700;margin-bottom:var(--space-3);">Sources</h2>
          <ul style="font-size:var(--text-sm);color:var(--color-text-muted);list-style:disc;padding-left:var(--space-5);">
            <li><a href="{brand["sourceUrl"]}" target="_blank" rel="noopener noreferrer" style="color:inherit;">{brand["name"]} official site</a>, verified <span class="dynamic-month-year">{MONTH_YEAR}</span></li>
            <li><a href="https://igamingontario.ca/en/operator-list" target="_blank" rel="noopener noreferrer" style="color:inherit;">iGaming Ontario Operator Directory</a>, status confirmed {DATA["marketData"]["directoryDate"]}</li>
          </ul>
          <p style="text-align:center;margin-top:var(--space-4);"><strong>- {AUTHORS[0]["name"]}, {AUTHORS[0]["role"]}</strong></p>
        </div>
      </div>

      <div class="content-sidebar">
        <div class="sidebar-sticky">
          <div class="sidebar-promo">
            <h3>{brand["name"]}</h3>
            <p style="font-size:var(--text-sm);color:var(--color-text-muted);margin-bottom:var(--space-3);">Verified <span class="dynamic-month-year">{MONTH_YEAR}</span></p>
            {sidebar_items}
            <a href="{brand["exitLink"]}" class="btn btn--primary" target="_blank" rel="sponsored noopener noreferrer" style="width:100%;margin-top:var(--space-4);">Visit {brand["name"]} &rarr;</a>
          </div>
          <div style="margin-top:var(--space-4);">
            <div class="sidebar-promo">
              <h3>Quick Links</h3>
              <div class="sidebar-promo-item"><div class="sidebar-promo-rank">&rarr;</div><div class="sidebar-promo-details"><a href="promo-code.html" style="color:var(--color-text);text-decoration:none;font-weight:600;font-size:var(--text-sm);">Offer Status</a></div></div>
              <div class="sidebar-promo-item"><div class="sidebar-promo-rank">&rarr;</div><div class="sidebar-promo-details"><a href="{prefix}compare.html" style="color:var(--color-text);text-decoration:none;font-weight:600;font-size:var(--text-sm);">Compare All 6 Rooms</a></div></div>
              <div class="sidebar-promo-item"><div class="sidebar-promo-rank">&rarr;</div><div class="sidebar-promo-details"><a href="{prefix}best-poker-sites-ontario.html" style="color:var(--color-text);text-decoration:none;font-weight:600;font-size:var(--text-sm);">Best Poker Sites</a></div></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="container">
    <div class="section-header"><h2>Explore Other Rooms</h2></div>
    <div style="display:grid;gap:var(--space-3);grid-template-columns:repeat(auto-fit,minmax(min(260px,100%),1fr));">
      {"".join([f'''<a href="{prefix}{ob["id"]}/review.html" class="card" style="text-decoration:none;color:inherit;padding:var(--space-4) var(--space-5);border-left:4px solid {ob["baseColour"]};"><h3 style="font-size:var(--text-base);font-weight:700;margin-bottom:var(--space-1);">{ob["name"]} Review</h3><p style="font-size:var(--text-sm);color:var(--color-text-muted);margin:0;">{ob["bestFor"][:60]}.</p></a>''' for ob in BRANDS if ob["id"] != bid][:3])}
    </div>
  </div>
</section>
'''
    write_page(f"{bid}/review.html", page_shell(
        f"{brand['name']} Review 2026 | Honest Rating",
        f"Independent {brand['name']} Ontario review with scoring breakdown, bonus details, pros, cons, and feature analysis. Regulated by iGO. Updated {MONTH_YEAR}.",
        f"{BASE_URL}/{bid}/review",
        content, prefix,
        bc_ld + "\n" + f'<script type="application/ld+json">{review_ld}</script>' + "\n" + faq_ld,
        sticky_cta=True, sticky_brand=brand
    ))


def build_brand_promo(brand):
    bid = brand["id"]
    prefix = "../"
    bc = [
        {"name": "Home", "url": "index.html", "canonical": f"{BASE_URL}/"},
        {"name": brand["name"], "url": f"{bid}/index.html", "canonical": f"{BASE_URL}/{bid}/"},
        {"name": "Offer Status"}
    ]
    bc_ld = f'<script type="application/ld+json">{breadcrumb_jsonld(bc)}</script>'

    code_cutout = ""
    if brand["promoCode"]:
        code_cutout = f'''<div class="promo-code-cutout">
  <div class="promo-code-label">Verified Public Code</div>
  <div class="promo-code-value"><span class="code-mono">{brand["promoCode"]}</span></div>
  <button class="copy-btn btn btn--primary" data-code="{brand["promoCode"]}" data-url="{brand["exitLink"]}">Copy Code &amp; Visit Site</button>
  <div class="promo-code-meta">Last verified: <span class="dynamic-month-year">{MONTH_YEAR}</span></div>
</div>'''
    else:
        code_cutout = f'''<div class="promo-code-cutout" style="border-color:var(--color-text-faint);">
  <div class="promo-code-label">{promo_status_badge(brand["promoCodeStatus"])}</div>
  <div class="promo-code-value" style="font-size:var(--text-base);font-family:var(--font-body);">No public promo code was captured in this research for {brand["name"]}.</div>
  <a href="{brand["exitLink"]}" class="btn btn--primary" target="_blank" rel="sponsored noopener noreferrer">Visit {brand["name"]} to Check Current Offers &rarr;</a>
  <div class="promo-code-meta">Last checked: <span class="dynamic-month-year">{MONTH_YEAR}</span></div>
</div>'''

    content = f'''
<section class="page-hero" data-brand="{brand["name"]}">
  <div class="container">
    {breadcrumb_html(bc, prefix)}
    <h1>{brand["name"]} Ontario: Offer Status and Promo Code</h1>
    <p class="page-hero-subtitle">Verified against official operator pages. Updated <span class="dynamic-month-year">{MONTH_YEAR}</span>.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="content-layout content-layout--sidebar">
      <div class="content-main prose">

        {code_cutout}

        <h2>Current Welcome Offer</h2>
        <div class="card card--flat" style="margin:var(--space-4) 0;">
          <table class="promos-table"><tbody>
            <tr><td>Operator</td><td>{brand["name"]}</td></tr>
            <tr><td>Legal Entity</td><td>{brand["legalEntity"]}</td></tr>
            <tr><td>Offer Status</td><td>{promo_status_badge(brand["promoCodeStatus"])}</td></tr>
            <tr><td>Public Code</td><td>{brand["promoCode"] if brand["promoCode"] else "None captured"}</td></tr>
            <tr><td>Welcome Offer</td><td>{brand["welcomeBonus"]}</td></tr>
            <tr><td>Min Deposit</td><td>{brand["minDeposit"]}</td></tr>
            <tr><td>Unlock Rate</td><td>{brand["bonusUnlockRate"]}</td></tr>
            <tr><td>Clear Window</td><td>{brand["bonusClearWindow"]}</td></tr>
            <tr><td>Withdrawal Effect</td><td>{brand["bonusWithdrawalNote"]}</td></tr>
            <tr><td>Source</td><td><a href="{brand["sourceUrl"]}" target="_blank" rel="noopener noreferrer">{brand["name"]} official site</a></td></tr>
            <tr><td>Last Verified</td><td><span class="dynamic-month-year">{MONTH_YEAR}</span></td></tr>
          </tbody></table>
        </div>

        <h2>Important Fine Print</h2>
        <p>Ontario poker promotions operate under AGCO marketing standards. Advertising that communicates gambling inducements, bonuses and credits is prohibited except on an operator's gaming site. This page summarizes publicly available offer terms as a factual reference. Always confirm current terms directly on the operator's site before making any decisions.</p>

        <h2>How We Verify Offers</h2>
        <p>Each operator's offer status is checked against its official Ontario-facing pages. We distinguish between:</p>
        <ul>
          <li><strong>Verified Public Code:</strong> A promo code found on the operator's official public-facing page.</li>
          <li><strong>No Public Code Identified:</strong> The operator has a welcome offer but no specific public code was found.</li>
          <li><strong>Unverified:</strong> Public source material was insufficient to confirm current offer details.</li>
        </ul>

        <div style="text-align:center;margin:var(--space-6) 0;">
          <a href="{brand["exitLink"]}" class="btn btn--primary" target="_blank" rel="sponsored noopener noreferrer">Check Current Offers at {brand["name"]} &rarr;</a>
        </div>

      </div>
      <div class="content-sidebar">
        <div class="sidebar-sticky">
          <div class="sidebar-promo">
            <h3>{brand["name"]}</h3>
            <p style="font-size:var(--text-sm);color:var(--color-text-muted);margin-bottom:var(--space-3);">{brand["overallRating"]}/10 Rating</p>
            <div class="sidebar-promo-item"><div class="sidebar-promo-rank">&rarr;</div><div class="sidebar-promo-details"><a href="review.html" style="color:var(--color-text);text-decoration:none;font-weight:600;font-size:var(--text-sm);">Full Review</a></div></div>
            <div class="sidebar-promo-item"><div class="sidebar-promo-rank">&rarr;</div><div class="sidebar-promo-details"><a href="{prefix}compare.html" style="color:var(--color-text);text-decoration:none;font-weight:600;font-size:var(--text-sm);">Compare All Rooms</a></div></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
'''
    write_page(f"{bid}/promo-code.html", page_shell(
        f"{brand['name']} Ontario Promo Code and Offer Status 2026",
        f"Current {brand['name']} Ontario offer status, promo code verification, and bonus terms. Verified against official operator pages. Updated {MONTH_YEAR}.",
        f"{BASE_URL}/{bid}/promo-code",
        content, prefix, bc_ld,
        sticky_cta=True, sticky_brand=brand
    ))


def build_brand_hub(brand):
    bid = brand["id"]
    prefix = "../"
    bc = [
        {"name": "Home", "url": "index.html", "canonical": f"{BASE_URL}/"},
        {"name": brand["name"]}
    ]
    bc_ld = f'<script type="application/ld+json">{breadcrumb_jsonld(bc)}</script>'

    features = "".join([f"<li>{f}</li>" for f in brand["keyFeatures"]])

    content = f'''
<section class="page-hero" data-brand="{brand["name"]}">
  <div class="container">
    {breadcrumb_html(bc, prefix)}
    <h1>{brand["name"]}: Ontario Poker Guide</h1>
    <p class="page-hero-subtitle">{brand["bestFor"]}</p>
  </div>
</section>

<section class="section">
  <div class="container container--default">
    <div class="prose">
      <p>{brand["name"]} is operated by {brand["legalEntity"]} and is a fully regulated Ontario poker room. It scores {brand["overallRating"]}/10 in our review. Best for: {brand["bestFor"].lower()}.</p>

      <h2>Key Features</h2>
      <ul>{features}</ul>

      <h2>Current Offer</h2>
      <p><strong>{brand["welcomeBonus"]}</strong></p>
      <p>{f'Public promo code: <span class="code-badge">{brand["promoCode"]}</span>' if brand["promoCode"] else promo_status_badge(brand["promoCodeStatus"])}</p>

      <h2>Explore {brand["name"]}</h2>
      <div style="display:grid;gap:var(--space-3);grid-template-columns:repeat(auto-fit,minmax(min(260px,100%),1fr));">
        <a href="review.html" class="card" style="text-decoration:none;color:inherit;padding:var(--space-4) var(--space-5);border-left:4px solid var(--color-primary);">
          <h3 style="font-size:var(--text-base);font-weight:700;margin-bottom:var(--space-1);">Full Review</h3>
          <p style="font-size:var(--text-sm);color:var(--color-text-muted);margin:0;">Detailed scoring, pros, cons, and feature breakdown.</p>
        </a>
        <a href="promo-code.html" class="card" style="text-decoration:none;color:inherit;padding:var(--space-4) var(--space-5);border-left:4px solid var(--color-primary);">
          <h3 style="font-size:var(--text-base);font-weight:700;margin-bottom:var(--space-1);">Offer Status and Promo Code</h3>
          <p style="font-size:var(--text-sm);color:var(--color-text-muted);margin:0;">Verified bonus terms and code status.</p>
        </a>
      </div>
    </div>
  </div>
</section>
'''
    write_page(f"{bid}/index.html", page_shell(
        f"{brand['name']} Ontario Guide 2026",
        f"Complete {brand['name']} Ontario guide: review, promo code status, bonus terms, and features. Regulated by iGaming Ontario.",
        f"{BASE_URL}/{bid}/",
        content, prefix, bc_ld
    ))


def build_comparison_page():
    rows = ""
    for b in BRANDS:
        code = b["promoCode"] if b["promoCode"] else "N/A"
        rows += f'''<tr>
  <td><strong><a href="{b["id"]}/review.html">{b["name"]}</a></strong><br><span style="font-size:var(--text-xs);color:var(--color-text-muted);">{b["legalEntity"]}</span></td>
  <td style="text-align:center;"><span class="badge badge--rating">{b["overallRating"]}</span></td>
  <td>{b["welcomeBonusShort"]}</td>
  <td>{code}</td>
  <td>{b["cashGameFormats"]}</td>
  <td>{b["jackpotFormat"]}</td>
  <td>{b["mobileApp"]}</td>
  <td><a href="{b["id"]}/review.html">Review</a></td>
</tr>'''

    content = f'''
<section class="page-hero">
  <div class="container">
    {breadcrumb_html([dict(name="Home", url="index.html"), dict(name="Compare All Rooms")])}
    <h1>Compare All Ontario Poker Rooms</h1>
    <p class="page-hero-subtitle">Side-by-side comparison of all six regulated Ontario poker rooms. Updated <span class="dynamic-month-year">{MONTH_YEAR}</span>.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="compare-table-wrap">
      <table class="compare-table">
        <thead><tr><th>Room</th><th>Rating</th><th>Welcome Offer</th><th>Code</th><th>Cash Games</th><th>Jackpot</th><th>Mobile</th><th>Review</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="container container--default">
    <h2>How to Read This Table</h2>
    <div class="prose">
      <p>All six rooms are fully regulated by iGaming Ontario. Ratings are based on our editorial assessment across bonus value, software quality, tournament offering, cash games, payments, and support.</p>
      <p>Promo code status reflects what was publicly verifiable at the time of our last check. "N/A" means no public code was captured, not that the operator has no welcome offer. Always confirm current terms on the operator's site.</p>
    </div>
  </div>
</section>
'''
    bc_ld = f'<script type="application/ld+json">{breadcrumb_jsonld([dict(name="Home", canonical=BASE_URL + "/"), dict(name="Compare")])}</script>'
    write_page("compare.html", page_shell(
        "Compare All Ontario Poker Rooms 2026",
        f"Side-by-side comparison of all 6 regulated Ontario poker sites. Ratings, bonuses, features, and promo codes. Updated {MONTH_YEAR}.",
        f"{BASE_URL}/compare",
        content, "./", bc_ld
    ))


def build_best_poker_sites():
    cards = ""
    for i, b in enumerate(BRANDS):
        rank = i + 1
        code_text = f'Code: <span class="code-badge">{b["promoCode"]}</span>' if b["promoCode"] else promo_status_badge(b["promoCodeStatus"])
        features = "".join([f"<li>{f}</li>" for f in b["keyFeatures"][:3]])
        cards += f'''
<div class="ranking-card" style="border-left:4px solid {b["baseColour"]};">
  <div class="ranking-card-header">
    <span class="ranking-number">{rank}</span>
    <div>
      <h3>{b["name"]}</h3>
      <span style="font-size:var(--text-xs);color:var(--color-text-muted);">{b["legalEntity"]}</span>
    </div>
    <span class="badge badge--rating">{b["overallRating"]}/10</span>
  </div>
  <p><strong>{b["welcomeBonusShort"]}</strong></p>
  <p>{code_text}</p>
  <ul style="font-size:var(--text-sm);margin:var(--space-3) 0;">{features}</ul>
  <div style="display:flex;gap:var(--space-3);flex-wrap:wrap;">
    <a href="{b["exitLink"]}" class="btn btn--primary btn--sm" target="_blank" rel="sponsored noopener noreferrer">Visit {b["name"]} &rarr;</a>
    <a href="{b["id"]}/review.html" class="btn btn--outline btn--sm">Read Review</a>
  </div>
</div>'''

    content = f'''
<section class="page-hero">
  <div class="container">
    {breadcrumb_html([dict(name="Home", url="index.html"), dict(name="Best Poker Sites")])}
    <h1>Best Ontario Poker Sites 2026</h1>
    <p class="page-hero-subtitle">All six regulated Ontario poker rooms, ranked by our editorial team. Updated <span class="dynamic-month-year">{MONTH_YEAR}</span>.</p>
  </div>
</section>

<section class="section">
  <div class="container container--default">
    {cards}
  </div>
</section>
'''

    il_ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Best Ontario Poker Sites 2026",
        "itemListElement": [
            {"@type": "ListItem", "position": i+1, "name": b["name"], "url": f"{BASE_URL}/{b['id']}/review"}
            for i, b in enumerate(BRANDS)
        ]
    })
    bc_ld = f'<script type="application/ld+json">{breadcrumb_jsonld([dict(name="Home", canonical=BASE_URL+"/"), dict(name="Best Poker Sites")])}</script>'
    write_page("best-poker-sites-ontario.html", page_shell(
        "Best Ontario Poker Sites 2026 | Ranked",
        f"All 6 regulated Ontario poker rooms ranked. GGPoker, 888poker, BetMGM, PokerStars, PartyPoker, Bwin. Reviews, promos, ratings. Updated {MONTH_YEAR}.",
        f"{BASE_URL}/best-poker-sites-ontario",
        content, "./",
        bc_ld + f'\n<script type="application/ld+json">{il_ld}</script>'
    ))


def build_promo_hub():
    rows = ""
    for b in BRANDS:
        code = f'<span class="code-badge">{b["promoCode"]}</span>' if b["promoCode"] else "N/A"
        rows += f'''<tr>
  <td><strong><a href="{b["id"]}/promo-code.html">{b["name"]}</a></strong></td>
  <td>{code}</td>
  <td>{promo_status_badge(b["promoCodeStatus"])}</td>
  <td>{b["welcomeBonusShort"]}</td>
  <td>{b["bonusClearWindow"]}</td>
  <td><a href="{b["id"]}/promo-code.html">Details</a></td>
</tr>'''

    content = f'''
<section class="page-hero">
  <div class="container">
    {breadcrumb_html([dict(name="Home", url="index.html"), dict(name="Promo Codes")])}
    <h1>Ontario Poker Promo Codes and Offer Status</h1>
    <p class="page-hero-subtitle">Verified against official operator pages. Last checked <span class="dynamic-month-year">{MONTH_YEAR}</span>.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="compare-table-wrap">
      <table class="compare-table">
        <thead><tr><th>Room</th><th>Code</th><th>Status</th><th>Welcome Offer</th><th>Clear Window</th><th>Details</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="container container--default prose">
    <h2>How We Verify Promo Codes</h2>
    <p>Ontario poker promotions operate under AGCO marketing standards. We verify each code against the operator's official Ontario-facing pages and categorize them as Verified Public Code, No Public Code Identified, or Unverified.</p>
    <p>This page is updated weekly. If an operator changes their offer, we update within 48 hours of detection.</p>
  </div>
</section>
'''
    write_page("ontario-poker-promo-codes.html", page_shell(
        "Ontario Poker Promo Codes 2026 | Verified Offers",
        f"All Ontario poker promo codes and bonus status for 6 regulated rooms. Verified against official operator sites. Updated {MONTH_YEAR}.",
        f"{BASE_URL}/ontario-poker-promo-codes",
        content
    ))


def build_content_page(filename, title, desc, h1, body_html, canonical_slug=None):
    slug = canonical_slug or filename.replace(".html", "")
    bc = [{"name": "Home", "url": "index.html"}, {"name": h1}]
    bc_ld = f'<script type="application/ld+json">{breadcrumb_jsonld([dict(name="Home", canonical=BASE_URL+"/"), dict(name=h1)])}</script>'
    content = f'''
<section class="page-hero">
  <div class="container">
    {breadcrumb_html(bc)}
    <h1>{h1}</h1>
  </div>
</section>
<section class="section">
  <div class="container container--default">
    <div class="prose">{body_html}</div>
  </div>
</section>
'''
    write_page(filename, page_shell(title, desc, f"{BASE_URL}/{slug}", content, "./", bc_ld))


# ── BUILD ALL PAGES ─────────────────────────────────────────────────

print("Building OntarioPoker.com...")
print("=" * 60)

# Homepage
build_homepage()

# Brand pages (hub, review, promo for each)
for b in BRANDS:
    build_brand_hub(b)
    build_brand_review(b)
    build_brand_promo(b)

# Comparison and ranking
build_comparison_page()
build_best_poker_sites()
build_promo_hub()

# ── DECISION-SUPPORT PAGES ──────────────────────────────────────────

build_content_page("ontario-poker-apps.html",
    "Best Ontario Poker Apps 2026",
    f"Compare mobile poker apps from all 6 regulated Ontario rooms. iOS, Android, browser play. Updated {MONTH_YEAR}.",
    "Ontario Poker Apps",
    f'''<p>All six regulated Ontario poker rooms offer mobile access. Here is how they compare:</p>
<div class="card card--flat" style="margin:var(--space-4) 0;">
<table class="promos-table"><tbody>
{"".join([f'<tr><td><a href="{b["id"]}/review.html">{b["name"]}</a></td><td>{b["mobileApp"]}</td></tr>' for b in BRANDS])}
</tbody></table></div>
<p>GGPoker and PokerStars have the most feature-rich mobile apps, while BetMGM and 888poker also offer dedicated iOS and Android clients. PartyPoker has mobile apps available, while Bwin's poker offering is accessible via mobile browser.</p>
<p>All mobile apps require geolocation verification to confirm you are in Ontario before play.</p>''')

build_content_page("ontario-poker-tournaments.html",
    "Ontario Poker Tournaments 2026 | Schedule and Guides",
    f"Tournament schedules, festival trackers, and qualifier guides for all regulated Ontario poker rooms. Updated {MONTH_YEAR}.",
    "Ontario Poker Tournaments",
    f'''<p>Ontario's regulated poker rooms offer a range of tournament formats, from daily schedules to major festival series.</p>
<h2>Tournament Offerings by Room</h2>
<div class="card card--flat" style="margin:var(--space-4) 0;">
<table class="promos-table"><tbody>
{"".join([f'<tr><td><a href="{b["id"]}/review.html">{b["name"]}</a></td><td>{b["tournamentFormats"]}</td></tr>' for b in BRANDS])}
</tbody></table></div>
<h2>Key Tournament Series</h2>
<ul>
<li><strong>GGPoker:</strong> WSOP Super Circuit Ontario events and recurring microFestival series. GGPoker has called these "Ontario's largest micro stakes poker festival" and "The Biggest Prize Pool of any Ontario Circuit Stop."</li>
<li><strong>PokerStars Ontario:</strong> Claims "more daily tournaments than anywhere else." Power Path offers qualifiers to live PokerStars events.</li>
<li><strong>888poker:</strong> Daily schedule plus BLAST jackpot format. Freeroll schedule exceeds C$12,000 weekly.</li>
<li><strong>BetMGM Poker:</strong> Regular MTTs, Spins, and daily schedule.</li>
</ul>''')

build_content_page("ontario-poker-freerolls.html",
    "Ontario Poker Freerolls 2026 | Free-Entry Tournaments",
    f"Free-entry poker tournaments across all regulated Ontario poker rooms. Weekly freeroll schedules and guides. Updated {MONTH_YEAR}.",
    "Ontario Poker Freerolls",
    '''<p>Freerolls are tournaments with no entry fee that award real prizes. Several Ontario rooms offer substantial freeroll schedules.</p>
<h2>Best Rooms for Freerolls</h2>
<ul>
<li><strong>888poker:</strong> Advertises "Play for free for over $12,000 every week!" with regular freeroll tournaments. Also offers no-deposit tournament tickets over seven days for new players, with each ticket expiring 24 hours after issue.</li>
<li><strong>GGPoker:</strong> Runs freerolls as part of its broader tournament schedule and Honeymoon for Newcomers program.</li>
<li><strong>PokerStars Ontario:</strong> Traditionally strong freeroll schedule, leveraging its position as the room with the most daily tournaments.</li>
</ul>
<p>Freerolls are a strong way to build a bankroll at no cost. 888poker currently offers the most prominent public freeroll schedule among Ontario's regulated rooms.</p>''')

build_content_page("ontario-poker-withdrawal-times.html",
    "Ontario Poker Withdrawal Times 2026",
    f"Withdrawal speeds and methods for all 6 regulated Ontario poker rooms. Interac, bank transfer, e-wallet options. Updated {MONTH_YEAR}.",
    "Ontario Poker Withdrawal Times",
    f'''<p>Withdrawal speed is a key factor when choosing an Ontario poker room. Here is a comparison of available withdrawal methods:</p>
<div class="card card--flat" style="margin:var(--space-4) 0;">
<table class="promos-table"><tbody>
{"".join([f'<tr><td><a href="{b["id"]}/review.html">{b["name"]}</a></td><td>{b["withdrawalMethods"]}</td></tr>' for b in BRANDS])}
</tbody></table></div>
<p>Interac is the most common withdrawal method across Ontario poker rooms and typically offers the fastest processing times. Most rooms also support bank transfers, though these may take longer to process.</p>
<p>Verification requirements (KYC) can affect your first withdrawal. All regulated Ontario rooms require identity verification before processing withdrawals, as mandated by AGCO regulations.</p>''')

build_content_page("ontario-poker-payment-methods.html",
    "Ontario Poker Payment Methods 2026",
    f"Deposit and withdrawal options for all regulated Ontario poker sites. Interac, Visa, Mastercard, PayPal, and more. Updated {MONTH_YEAR}.",
    "Ontario Poker Payment Methods",
    f'''<p>Ontario poker rooms support a range of deposit and withdrawal methods. Interac is available at nearly every regulated room.</p>
<h2>Deposit Methods by Room</h2>
<div class="card card--flat" style="margin:var(--space-4) 0;">
<table class="promos-table"><tbody>
{"".join([f'<tr><td><a href="{b["id"]}/review.html">{b["name"]}</a></td><td>{b["depositMethods"]}</td><td>Min: {b["minDeposit"]}</td></tr>' for b in BRANDS])}
</tbody></table></div>
<p>Most Ontario poker rooms have a minimum deposit of C$10. BetMGM Poker is notable for accepting PayPal in addition to traditional methods.</p>''')

build_content_page("ontario-poker-rakeback-rewards.html",
    "Ontario Poker Rakeback and Rewards 2026",
    f"Loyalty programs, rakeback deals, and rewards across all regulated Ontario poker rooms. Detailed comparison. Updated {MONTH_YEAR}.",
    "Ontario Poker Rakeback and Rewards",
    f'''<p>Rakeback and reward programs vary significantly across Ontario's six regulated poker rooms. Here is what each offers:</p>
<h2>Rewards Comparison</h2>
<div class="card card--flat" style="margin:var(--space-4) 0;">
<table class="promos-table"><tbody>
{"".join([f'<tr><td><a href="{b["id"]}/review.html">{b["name"]}</a></td><td>{b["rewards"]}</td></tr>' for b in BRANDS])}
</tbody></table></div>
<h2>Best Rooms for Rewards</h2>
<ul>
<li><strong>BetMGM Poker:</strong> Grind Rewards up to C$6,500 with a visible BRP ladder. The clearest rewards math in the market.</li>
<li><strong>GGPoker:</strong> Maple Rewards program with monthly Ontario-exclusive rewards, plus the Honeymoon for Newcomers 30-day mission structure.</li>
<li><strong>888poker:</strong> Early Bird Rakeback, Gift Drops, Winner Spinner, and Hand of the Day promotions.</li>
<li><strong>PartyPoker:</strong> Up to 20% cashback (per secondary sources).</li>
</ul>''')

build_content_page("ontario-poker-cash-games.html",
    "Ontario Poker Cash Games 2026 | Format Guide",
    f"Cash game formats, stakes, and availability across all regulated Ontario poker rooms. Updated {MONTH_YEAR}.",
    "Ontario Poker Cash Games",
    f'''<p>Ontario's regulated poker rooms offer various cash game formats, from standard tables to fast-fold variants.</p>
<div class="card card--flat" style="margin:var(--space-4) 0;">
<table class="promos-table"><tbody>
{"".join([f'<tr><td><a href="{b["id"]}/review.html">{b["name"]}</a></td><td>{b["cashGameFormats"]}</td></tr>' for b in BRANDS])}
</tbody></table></div>
<p>Every room offers No Limit Hold'em and Pot Limit Omaha. The differentiator is fast-fold formats: GGPoker has Rush & Cash, PokerStars has Zoom, 888poker has SNAP, BetMGM has FastForward, and PartyPoker has Fast Forward.</p>''')

build_content_page("how-geolocation-works-for-ontario-poker.html",
    "How Geolocation Works for Ontario Poker",
    "Understanding geolocation requirements for playing regulated online poker in Ontario. VPN, location, and eligibility explained.",
    "How Geolocation Works for Ontario Poker",
    '''<p>All regulated Ontario poker rooms use geolocation technology to verify that players are physically located within Ontario before allowing real-money play. Here is what you need to know:</p>
<h2>How It Works</h2>
<ul>
<li>When you open a poker client or mobile app, the software checks your physical location using GPS, WiFi, and IP-based geolocation.</li>
<li>You must be within Ontario's borders to play. This applies even if you have an Ontario address but are travelling outside the province.</li>
<li>Location checks may occur at login, when joining a table, and periodically during play.</li>
</ul>
<h2>Common Issues</h2>
<ul>
<li><strong>VPNs:</strong> Using a VPN to mask your location violates the terms of service of every regulated operator and can result in account suspension.</li>
<li><strong>Border areas:</strong> Players near provincial borders may experience occasional location-check failures.</li>
<li><strong>Mobile data:</strong> Connecting to WiFi generally provides more reliable geolocation than mobile data.</li>
</ul>
<h2>Age Requirement</h2>
<p>You must be 19 or older to play regulated online poker in Ontario. All operators verify age and identity as part of their KYC (Know Your Customer) process.</p>''')

# ── TRUST AND REGULATION PAGES ──────────────────────────────────────

build_content_page("is-online-poker-legal-in-ontario.html",
    "Is Online Poker Legal in Ontario? | Complete Guide",
    "Complete guide to Ontario online poker legality. AGCO regulation, iGaming Ontario, operator registration, and player protections explained.",
    "Is Online Poker Legal in Ontario?",
    f'''<p>Yes. Online poker is legal and regulated in Ontario. The regulated market launched on April 4, 2022, under the oversight of the Alcohol and Gaming Commission of Ontario (AGCO) and iGaming Ontario (iGO).</p>
<h2>How Ontario Poker Regulation Works</h2>
<p>iGaming Ontario, a subsidiary of the AGCO, serves as the conduct and manage entity for Ontario's regulated internet gaming market. Operators must register with the AGCO and enter into an operating agreement with iGO before offering online poker to Ontario residents.</p>
<p>At launch, iGO said Ontario players could use sites that are "fully registered and approved." Its current homepage still tells players to "Make the safer choice" by playing on sites offered by fully registered and approved operators.</p>
<h2>Current Market Size</h2>
<p>As of {DATA["marketData"]["directoryDate"]}, the iGO operator directory lists {DATA["marketData"]["operatorCount"]}. Six of these offer live regulated poker: GGPoker, 888poker, BetMGM Poker, PokerStars Ontario, PartyPoker Ontario, and Bwin Ontario.</p>
<p>In FY2024-25, iGO reported {DATA["marketData"]["totalMarketRevenue"]} in total gaming revenue across all verticals, with poker contributing approximately {DATA["marketData"]["totalNAGGR2025"]} of NAGGR.</p>
<h2>Player Protections</h2>
<ul>
<li>All operators must comply with AGCO's Registrar's Standards for Internet Gaming</li>
<li>Advertising and marketing materials that communicate gambling inducements, bonuses and credits are prohibited, except on an operator's gaming site</li>
<li>Unresolved disputes can be escalated to iGO after the player first tries the operator, though iGO cannot directly settle bets, refund wagers or award compensation</li>
<li>iGO selected vendors for a centralized self-exclusion system in August 2024, which all operators will have to use once the system goes live</li>
</ul>''')

build_content_page("regulated-vs-unregulated-poker-sites-ontario.html",
    "Regulated vs Unregulated Poker Sites in Ontario",
    "Why playing on regulated Ontario poker sites matters. Player protections, dispute resolution, and the channelization argument explained.",
    "Regulated vs Unregulated Poker Sites in Ontario",
    f'''<p>Ontario's regulated online poker market exists alongside offshore sites that operate without AGCO registration. Here is why the distinction matters for players.</p>
<h2>The Regulatory Position</h2>
<p>AGCO has stated that any "marketing affiliates" advertising for the Ontario market must not also advertise gaming sites that operate in Ontario without AGCO registration. This site follows that principle. We cover only the six regulated poker rooms.</p>
<h2>What Regulated Means for Players</h2>
<ul>
<li><strong>Dispute resolution:</strong> iGO provides a dispute escalation path for players who cannot resolve issues directly with an operator.</li>
<li><strong>Responsible gambling:</strong> All regulated operators must offer deposit limits, self-exclusion tools, and responsible gambling resources.</li>
<li><strong>Fund protection:</strong> Regulated operators must meet AGCO's standards for player fund segregation.</li>
<li><strong>Advertising standards:</strong> AGCO's marketing standards and Ad Standards' administration of the Canadian Gaming Association's Code for Responsible Gaming Advertising (effective January 1, 2026) provide additional consumer protections.</li>
</ul>
<h2>The Channelization Picture</h2>
<p>In FY2024-25, the channelization rate was {DATA["marketData"]["channelizationRate"]}, meaning the vast majority of Ontario's online gambling activity already happens on regulated sites. Playing on regulated sites aligns with where most Ontario players already are.</p>''')

build_content_page("how-ontario-online-poker-regulation-works.html",
    "How Ontario Online Poker Regulation Works",
    "Inside Ontario's online poker regulatory framework. AGCO, iGaming Ontario, operator requirements, and market oversight explained.",
    "How Ontario Online Poker Regulation Works",
    '''<p>Ontario's online poker regulation operates through a layered system involving the AGCO and iGaming Ontario.</p>
<h2>The Regulatory Structure</h2>
<ul>
<li><strong>AGCO (Alcohol and Gaming Commission of Ontario):</strong> The regulator that sets standards, issues registrations, and enforces compliance.</li>
<li><strong>iGaming Ontario (iGO):</strong> A subsidiary of the AGCO that serves as the "conduct and manage" entity. Operators enter into operating agreements with iGO.</li>
</ul>
<h2>Operator Requirements</h2>
<p>To offer online poker in Ontario, an operator must register with the AGCO and execute an operating agreement with iGO. The operator must comply with the Registrar's Standards for Internet Gaming, which cover responsible gambling, advertising, player verification, and fund management.</p>
<h2>Revenue Sharing</h2>
<p>Operators share a portion of their gaming revenue with iGO under their operating agreements. This funds the regulatory framework and contributes to Ontario's public finances.</p>''')

build_content_page("how-to-complain-about-an-ontario-poker-site.html",
    "How to Complain About an Ontario Poker Site",
    "Step-by-step guide to resolving disputes with regulated Ontario poker operators. iGO escalation, AGCO reporting, and player rights.",
    "How to Complain About an Ontario Poker Site",
    '''<p>If you have a complaint about a regulated Ontario poker site, here is the process:</p>
<h2>Step 1: Contact the Operator</h2>
<p>Start by using the operator's own customer support and complaints process. All regulated operators are required to have a complaints procedure.</p>
<h2>Step 2: Escalate to iGaming Ontario</h2>
<p>iGO says unresolved disputes can be escalated to it after the player first tries the operator. However, iGO cannot directly settle bets, refund wagers, or award compensation. It can facilitate communication and investigate whether the operator followed its own procedures.</p>
<h2>Step 3: Report to AGCO</h2>
<p>If you believe an operator is violating regulatory standards, you can report concerns directly to the AGCO, which has the authority to investigate and take enforcement action.</p>
<h2>Document Everything</h2>
<p>Keep screenshots of transactions, chat logs, and email correspondence. Clear documentation strengthens any complaint.</p>''')

build_content_page("responsible-gambling-tools-ontario-poker.html",
    "Responsible Gambling Tools for Ontario Poker",
    "Deposit limits, self-exclusion, time-out tools, and responsible gambling resources for Ontario poker players.",
    "Responsible Gambling Tools for Ontario Poker",
    '''<p>All regulated Ontario poker rooms are required to offer responsible gambling tools. Here is what is available:</p>
<h2>Available Tools</h2>
<ul>
<li><strong>Deposit limits:</strong> Set daily, weekly, or monthly deposit caps on your account.</li>
<li><strong>Session time limits:</strong> Set reminders or automatic logouts after a specified period of play.</li>
<li><strong>Self-exclusion:</strong> Voluntarily exclude yourself from one or all regulated operators. iGO selected vendors for a centralized self-exclusion system in August 2024, which all operators will have to use once the system goes live.</li>
<li><strong>Reality checks:</strong> Periodic pop-ups showing your session duration and activity.</li>
</ul>
<h2>Getting Help</h2>
<p>If you or someone you know has a gambling problem:</p>
<ul>
<li><strong>ConnexOntario:</strong> 1-866-531-2600 (24/7)</li>
<li><strong>Gambling, Gaming, and Technology Use Service:</strong> <a href="https://www.connexontario.ca" target="_blank" rel="noopener noreferrer">connexontario.ca</a></li>
</ul>''')

build_content_page("ontario-poker-market-size-and-trends.html",
    "Ontario Poker Market Size and Trends 2026",
    f"Ontario poker market data: wagers, revenue, NAGGR, player accounts, and channelization trends. Official iGO data analysis.",
    "Ontario Poker Market Size and Trends",
    f'''<p>Ontario's regulated online poker market is small in share but high in intent. Here are the key numbers from official iGO data.</p>
<h2>Market Overview (FY2024-25)</h2>
<div class="card card--flat" style="margin:var(--space-4) 0;">
<table class="promos-table"><tbody>
<tr><td>Total market wagers</td><td>{DATA["marketData"]["totalMarketWagers"]}</td></tr>
<tr><td>Total gaming revenue</td><td>{DATA["marketData"]["totalMarketRevenue"]}</td></tr>
<tr><td>Active player accounts</td><td>{DATA["marketData"]["activePlayerAccounts"]}</td></tr>
<tr><td>Channelization rate</td><td>{DATA["marketData"]["channelizationRate"]}</td></tr>
<tr><td>Operators / gaming websites</td><td>{DATA["marketData"]["operatorCount"]} (as of {DATA["marketData"]["directoryDate"]})</td></tr>
</tbody></table></div>
<h2>Poker-Specific Data (2025)</h2>
<div class="card card--flat" style="margin:var(--space-4) 0;">
<table class="promos-table"><tbody>
<tr><td>Poker wagers</td><td>{DATA["marketData"]["totalWagers2025"]}</td></tr>
<tr><td>Poker NAGGR</td><td>{DATA["marketData"]["totalNAGGR2025"]}</td></tr>
<tr><td>Poker share of total wagers</td><td>{DATA["marketData"]["pokerShareWagers"]}</td></tr>
<tr><td>Poker share of total NAGGR</td><td>{DATA["marketData"]["pokerShareNAGGR"]}</td></tr>
<tr><td>Regulated poker brands</td><td>{DATA["marketData"]["regulatedPokerBrands"]}</td></tr>
</tbody></table></div>
<h2>Key Trends</h2>
<ul>
<li>Poker wagers remained essentially stable between 2024 (C$1.683B) and 2025 ({DATA["marketData"]["totalWagers2025"]})</li>
<li>Poker NAGGR grew slightly from C$67.7M (2024) to {DATA["marketData"]["totalNAGGR2025"]} (2025)</li>
<li>Poker's share of total wagers and NAGGR declined, but this is because casino and betting are growing faster, not because poker is shrinking</li>
</ul>
<h2>Precision Notes</h2>
<p><strong>NAGGR vs Gaming Revenue:</strong> The iGO annual report uses "gaming revenue" while the monthly workbook uses NAGGR (Net After-Game Gross Revenue). These are not interchangeable. NAGGR measures operator revenue after player winnings but before operating costs.</p>
<p><strong>Active Player Accounts vs Unique Players:</strong> Active player accounts do not equal unique players. One person may hold accounts at multiple operators.</p>
<p>Source: iGO Annual Report 2024-2025; iGO Monthly Market Performance Report (January 2026 workbook).</p>''')

# ── POLICY AND TRUST PAGES ──────────────────────────────────────────

policy_pages = [
    ("about.html", "About OntarioPoker.com", "About OntarioPoker.com, Ontario's regulated poker guide. Published by NWG PTY Limited.",
     "About OntarioPoker.com",
     f'''<p>OntarioPoker.com is an independent review site covering all six regulated poker rooms in Ontario, Canada. We focus exclusively on operators that are fully registered with the Alcohol and Gaming Commission of Ontario (AGCO) and operate under agreements with iGaming Ontario (iGO).</p>
<h2>Our Approach</h2>
<p>We believe the strongest Ontario poker portal is not the one that publishes the broadest list. It is the one that becomes the most reliable operating manual for the six rooms that actually matter. Our coverage includes detailed reviews, verified promotion tracking, payment guides, tournament schedules, and regulatory explainers.</p>
<h2>Published By</h2>
<p>OntarioPoker.com is published by {DATA["operator"]["name"]}, {DATA["operator"]["address"]}.</p>
<p>Contact: <a href="mailto:{DATA["operator"]["email"]}">{DATA["operator"]["email"]}</a></p>'''),

    ("editorial-policy.html", "Editorial Policy", "OntarioPoker.com editorial policy. How we review, rate, and verify Ontario poker rooms.",
     "Editorial Policy",
     '''<p>OntarioPoker.com covers only poker rooms that are fully registered with the AGCO and operate under iGaming Ontario. We do not review or promote unregulated or offshore poker sites.</p>
<h2>How We Rate</h2>
<p>Each poker room is scored across six categories: Bonus and Promotions, Software and Features, Tournament Offering, Cash Games, Payments, and Support. The overall rating is a weighted average. Ratings are updated quarterly or when operators make significant changes.</p>
<h2>Promotion Verification</h2>
<p>Promo codes and offer terms are verified against official operator pages. We distinguish between verified public codes, offers with no public code identified, and unverified offers. We never fabricate promo codes or publish offers we cannot source.</p>
<h2>Commercial Relationships</h2>
<p>This site contains affiliate links. If you click through and register using our links, we may receive compensation. Commercial relationships never affect editorial ratings or rankings.</p>'''),

    ("fact-checking.html", "Fact-Checking Process", "How OntarioPoker.com verifies facts, promo codes, and operator information.",
     "Fact-Checking Process",
     '''<p>Every factual claim on OntarioPoker.com must be verifiable against a primary source. Here is our process:</p>
<ul>
<li>Operator details verified against the official iGO operator directory</li>
<li>Promo codes and bonus terms checked against official operator pages</li>
<li>Market data sourced from official iGO reports and workbooks</li>
<li>Regulatory quotes sourced from AGCO and iGO publications</li>
<li>Each verification carries a date stamp and source reference</li>
</ul>
<p>If you believe any information on this site is incorrect, please contact us at <a href="mailto:help@ontariopoker.com">help@ontariopoker.com</a>.</p>'''),

    ("corrections-policy.html", "Corrections Policy", "How OntarioPoker.com handles corrections and updates to published content.",
     "Corrections Policy",
     '''<p>We take accuracy seriously. When we identify an error, we correct it promptly and transparently.</p>
<h2>How We Handle Corrections</h2>
<ul>
<li>Factual errors are corrected as soon as identified</li>
<li>Significant corrections include a note explaining what changed and when</li>
<li>Minor updates (e.g., refreshed verification dates) are made without separate correction notices</li>
</ul>
<p>To report an error, email <a href="mailto:help@ontariopoker.com">help@ontariopoker.com</a> with the page URL and a description of the issue.</p>'''),

    ("affiliate-disclosure.html", "Affiliate Disclosure", "OntarioPoker.com affiliate disclosure. How we earn revenue and how it affects our content.",
     "Affiliate Disclosure",
     f'''<p>OntarioPoker.com is owned and operated by {DATA["operator"]["name"]}. This site contains affiliate links to regulated Ontario poker operators.</p>
<h2>How We Earn Revenue</h2>
<p>When you click through to a poker room using our links and create an account, we may earn a referral commission. This compensation comes from the operator, not from you. You pay nothing extra for using our links.</p>
<h2>How This Affects Our Content</h2>
<p>Commercial relationships do not affect editorial ratings, rankings, or review content. Our scores are based on our evaluation methodology, applied consistently across all operators. We cover all six regulated Ontario poker rooms regardless of whether we have a commercial relationship with each one.</p>'''),

    ("complaints-policy.html", "Complaints Policy", "How to file a complaint about OntarioPoker.com content or services.",
     "Complaints Policy",
     '''<p>If you have a complaint about content published on OntarioPoker.com, here is how to reach us:</p>
<ul>
<li>Email: <a href="mailto:help@ontariopoker.com">help@ontariopoker.com</a></li>
<li>Include the specific page URL and nature of your complaint</li>
<li>We aim to acknowledge complaints within 48 hours</li>
<li>We aim to resolve or provide a substantive response within 7 business days</li>
</ul>
<p>For complaints about a specific poker operator, see our guide on <a href="how-to-complain-about-an-ontario-poker-site.html">how to complain about an Ontario poker site</a>.</p>'''),

    ("responsible-gambling.html", "Responsible Gambling", "Responsible gambling resources, tools, and help for Ontario poker players.",
     "Responsible Gambling",
     '''<p>Poker is supposed to be fun. If it stops feeling that way, step away. Help is always available.</p>
<h2>Know the Signs</h2>
<ul>
<li>Spending more time or money on poker than you intended</li>
<li>Chasing losses or playing to recover money</li>
<li>Neglecting other responsibilities or relationships</li>
<li>Borrowing money or selling possessions to fund play</li>
<li>Feeling anxious, irritable, or restless when not playing</li>
</ul>
<h2>Tools Available at Every Regulated Room</h2>
<p>All regulated Ontario poker rooms offer deposit limits, session time limits, self-exclusion, and reality checks. Use them. Setting limits before you start playing is always easier than trying to set them after a session.</p>
<h2>Get Help</h2>
<ul>
<li><strong>ConnexOntario:</strong> 1-866-531-2600 (24/7)</li>
<li><strong>Online:</strong> <a href="https://www.connexontario.ca" target="_blank" rel="noopener noreferrer">connexontario.ca</a></li>
<li><strong>Crisis Services Canada:</strong> 1-833-456-4566</li>
</ul>'''),

    ("self-exclusion-resources.html", "Self-Exclusion Resources", "Self-exclusion options for Ontario poker players. How to exclude yourself from regulated poker sites.",
     "Self-Exclusion Resources",
     '''<p>Self-exclusion allows you to voluntarily ban yourself from one or more regulated poker sites for a defined period.</p>
<h2>How Self-Exclusion Works in Ontario</h2>
<p>Each regulated operator offers its own self-exclusion tool. iGaming Ontario selected vendors for a centralized self-exclusion system in August 2024, which all operators will have to use once the system goes live. Until then, you can self-exclude at each operator individually through their responsible gambling settings.</p>
<h2>Steps to Self-Exclude</h2>
<ol>
<li>Log in to the poker room's website or app</li>
<li>Navigate to account settings or responsible gambling section</li>
<li>Select the self-exclusion option and choose your exclusion period</li>
<li>Confirm your choice. During the exclusion period, your account will be inaccessible.</li>
</ol>
<h2>Additional Support</h2>
<p>ConnexOntario: 1-866-531-2600 | <a href="https://www.connexontario.ca" target="_blank" rel="noopener noreferrer">connexontario.ca</a></p>'''),

    ("privacy.html", "Privacy Policy", "OntarioPoker.com privacy policy. How we handle visitor data, cookies, and analytics.",
     "Privacy Policy",
     f'''<p>This privacy policy explains how OntarioPoker.com collects, uses, and protects information from visitors.</p>
<h2>Information We Collect</h2>
<p>We collect standard web analytics data including page views, referral sources, browser type, and geographic region. We do not collect personal information such as names, email addresses, or payment details unless you voluntarily provide them through our contact form.</p>
<h2>Cookies</h2>
<p>This site uses cookies for analytics, theme preferences, and affiliate link tracking. See our <a href="cookie-policy.html">Cookie Policy</a> for details.</p>
<h2>Third-Party Links</h2>
<p>This site contains links to regulated Ontario poker operators. When you click these links, you leave OntarioPoker.com and are subject to the operator's own privacy policy.</p>
<h2>Contact</h2>
<p>{DATA["operator"]["name"]}, {DATA["operator"]["address"]}. Email: <a href="mailto:{DATA["operator"]["email"]}">{DATA["operator"]["email"]}</a></p>'''),

    ("cookie-policy.html", "Cookie Policy", "OntarioPoker.com cookie policy. Types of cookies used and how to manage them.",
     "Cookie Policy",
     '''<p>OntarioPoker.com uses cookies to improve your experience. Here is what we use and why.</p>
<h2>Types of Cookies</h2>
<ul>
<li><strong>Essential:</strong> Theme preference (dark/light mode). Stored locally in your browser.</li>
<li><strong>Analytics:</strong> Google Analytics cookies to understand site usage and improve content.</li>
<li><strong>Affiliate tracking:</strong> Cookies set by poker operators when you click affiliate links, used to track referrals.</li>
</ul>
<h2>Managing Cookies</h2>
<p>You can disable cookies in your browser settings. Note that disabling essential cookies may affect site functionality (e.g., theme preference will not persist).</p>'''),

    ("terms.html", "Terms and Conditions", "OntarioPoker.com terms of use. Eligibility, disclaimers, and legal information.",
     "Terms and Conditions",
     f'''<p>By using OntarioPoker.com, you agree to these terms.</p>
<h2>Eligibility</h2>
<p>This site is intended for users aged 19 and older who are physically located in Ontario, Canada. Online poker in Ontario is regulated by the AGCO and iGaming Ontario.</p>
<h2>Disclaimer</h2>
<p>OntarioPoker.com provides information and reviews for educational purposes. We are not a poker operator and do not accept wagers. Always confirm offer terms, eligibility, and regulations directly with each operator before signing up.</p>
<h2>Affiliate Links</h2>
<p>This site contains affiliate links. See our <a href="affiliate-disclosure.html">Affiliate Disclosure</a> for details.</p>
<h2>Intellectual Property</h2>
<p>All content on this site is the property of {DATA["operator"]["name"]} unless otherwise noted. Operator names, logos, and trademarks belong to their respective owners.</p>'''),

    ("accessibility.html", "Accessibility Statement", "OntarioPoker.com accessibility commitment and features.",
     "Accessibility Statement",
     '''<p>OntarioPoker.com is committed to making our site accessible to all users.</p>
<h2>Accessibility Features</h2>
<ul>
<li>Semantic HTML structure with proper heading hierarchy</li>
<li>Keyboard navigation support throughout the site</li>
<li>Dark and light theme options for visual comfort</li>
<li>Alt text on all meaningful images</li>
<li>Sufficient color contrast ratios</li>
<li>Focus indicators on interactive elements</li>
</ul>
<h2>Feedback</h2>
<p>If you encounter accessibility barriers on this site, please contact us at <a href="mailto:help@ontariopoker.com">help@ontariopoker.com</a>. We take all feedback seriously and will work to address issues promptly.</p>'''),

    ("contact.html", "Contact Us", "Contact OntarioPoker.com. Questions, corrections, and partnership inquiries.",
     "Contact Us",
     f'''<p>We are here to help. Reach out with questions, corrections, or partnership inquiries.</p>
<h2>General Contact</h2>
<p>Email: <a href="mailto:{DATA["operator"]["email"]}">{DATA["operator"]["email"]}</a></p>
<h2>Corrections</h2>
<p>If you spot an error on our site, email us with the page URL and a description of the issue. We aim to respond within 48 hours.</p>
<h2>Partnerships</h2>
<p>For partnership, advertising, or affiliate inquiries, email <a href="mailto:{DATA["operator"]["email"]}">{DATA["operator"]["email"]}</a> with "Partnership" in the subject line.</p>
<p>{DATA["operator"]["name"]}, {DATA["operator"]["address"]}</p>'''),
]

for filename, title, desc, h1, body in policy_pages:
    build_content_page(filename, title, desc, h1, body)

# ── AUTHOR PAGES ────────────────────────────────────────────────────

def build_author_page(author):
    content = f'''
<section class="page-hero">
  <div class="container">
    {breadcrumb_html([dict(name="Home", url="index.html"), dict(name="Our Authors", url="management-team.html"), dict(name=author["name"])])}
    <h1>{author["name"]}</h1>
    <p class="page-hero-subtitle">{author["role"]}, {author["location"]}</p>
  </div>
</section>
<section class="section">
  <div class="container container--narrow">
    <div class="prose">
      <p>{author["bio"]}</p>
      <p>Previously at: {", ".join(author["previousEmployers"])}</p>
      <h2>Articles by {author["name"]}</h2>
      <ul>
        {"".join([f'<li><a href="{b["id"]}/review.html">{b["name"]} Review</a></li>' for b in BRANDS])}
        <li><a href="compare.html">Compare All Ontario Poker Rooms</a></li>
        <li><a href="best-poker-sites-ontario.html">Best Ontario Poker Sites 2026</a></li>
        <li><a href="is-online-poker-legal-in-ontario.html">Is Online Poker Legal in Ontario?</a></li>
      </ul>
    </div>
  </div>
</section>
'''
    bc_ld = f'<script type="application/ld+json">{breadcrumb_jsonld([dict(name="Home", canonical=BASE_URL+"/"), dict(name="Authors", canonical=BASE_URL+"/management-team"), dict(name=author["name"])])}</script>'
    person_data = {"@context":"https://schema.org","@type":"Person","name":author["name"],"jobTitle":author["role"],"worksFor":{"@type":"Organization","name":SITE_NAME}}
    person_ld = f'<script type="application/ld+json">{json.dumps(person_data)}</script>'
    write_page(f'{author["id"]}.html', page_shell(
        f'{author["name"]} | {author["role"]}',
        f'{author["name"]}, {author["role"]} at {SITE_NAME}. {author["bio"][:100]}',
        f'{BASE_URL}/{author["id"]}',
        content, "./", bc_ld + "\n" + person_ld
    ))

def build_management_team():
    author_cards = ""
    for a in AUTHORS:
        author_cards += f'''
<div class="card" style="padding:var(--space-5);">
  <h3><a href="{a["id"]}.html" style="color:inherit;text-decoration:none;">{a["name"]}</a></h3>
  <p style="font-size:var(--text-sm);color:var(--color-text-muted);margin-bottom:var(--space-2);">{a["role"]} | {a["location"]}</p>
  <p style="font-size:var(--text-sm);">{a["bio"]}</p>
  <p style="font-size:var(--text-xs);color:var(--color-text-faint);margin-top:var(--space-2);">Previously at: {", ".join(a["previousEmployers"])}</p>
</div>'''

    content = f'''
<section class="page-hero">
  <div class="container">
    {breadcrumb_html([dict(name="Home", url="index.html"), dict(name="Our Authors")])}
    <h1>Our Authors</h1>
    <p class="page-hero-subtitle">The editorial team behind OntarioPoker.com.</p>
  </div>
</section>
<section class="section">
  <div class="container container--default">
    <div style="display:grid;gap:var(--space-4);grid-template-columns:repeat(auto-fit,minmax(min(300px,100%),1fr));">
      {author_cards}
    </div>
  </div>
</section>
'''
    write_page("management-team.html", page_shell(
        "Our Authors | OntarioPoker Editorial Team",
        "Meet the OntarioPoker.com editorial team. Experienced poker journalists covering Ontario's regulated market.",
        f"{BASE_URL}/management-team",
        content
    ))

build_management_team()
for a in AUTHORS:
    build_author_page(a)


# ── SITEMAP & ROBOTS ────────────────────────────────────────────────

def build_sitemap():
    pages = []
    # Collect all HTML files
    for root, dirs, files in os.walk(OUT):
        for f in files:
            if f.endswith(".html"):
                rel = os.path.relpath(os.path.join(root, f), OUT)
                slug = rel.replace("\\", "/").replace("index.html", "").replace(".html", "")
                if slug.endswith("/"): slug = slug[:-1]
                url = f"{BASE_URL}/{slug}" if slug else f"{BASE_URL}/"

                # Priority
                if not slug or slug == "":
                    prio = "1.0"
                elif slug in ["compare", "best-poker-sites-ontario", "ontario-poker-promo-codes"]:
                    prio = "0.9"
                elif "/review" in slug or "/promo-code" in slug or "/index" in slug:
                    prio = "0.8"
                elif slug.startswith("ontario-poker-") or slug.startswith("is-online-") or slug.startswith("how-"):
                    prio = "0.7"
                elif slug in ["about", "contact", "management-team"] or slug.endswith("-drummond") or slug.endswith("-chen"):
                    prio = "0.5"
                else:
                    prio = "0.3"

                pages.append((url, prio))

    urls = "\n".join([f"  <url><loc>{u}</loc><lastmod>{ISO_DATE}</lastmod><changefreq>weekly</changefreq><priority>{p}</priority></url>" for u, p in sorted(pages)])
    sitemap = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>'''
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write(sitemap)
    print("  Built: sitemap.xml")

def build_robots():
    robots = f'''User-agent: *
Allow: /
Sitemap: {BASE_URL}/sitemap.xml'''
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(robots)
    print("  Built: robots.txt")

def build_search_index():
    index = []
    for root, dirs, files in os.walk(OUT):
        for f in files:
            if f.endswith(".html"):
                filepath = os.path.join(root, f)
                rel = os.path.relpath(filepath, OUT).replace("\\", "/")
                with open(filepath, "r", encoding="utf-8") as fh:
                    content = fh.read()
                # Extract title
                import re
                title_m = re.search(r"<title>(.*?)</title>", content)
                h1_m = re.search(r"<h1>(.*?)</h1>", content, re.DOTALL)
                desc_m = re.search(r'name="description"\s+content="(.*?)"', content)
                h2s = re.findall(r"<h2>(.*?)</h2>", content)

                title = title_m.group(1) if title_m else f
                h1_text = re.sub(r"<[^>]+>", "", h1_m.group(1)) if h1_m else title
                desc = desc_m.group(1) if desc_m else ""
                h2_text = " | ".join([re.sub(r"<[^>]+>", "", h) for h in h2s[:5]])

                # Determine category
                cat = "General"
                if "/" in rel:
                    brand_id = rel.split("/")[0]
                    for b in BRANDS:
                        if b["id"] == brand_id:
                            cat = b["name"]
                            break
                elif "poker-" in rel or "ontario-" in rel:
                    cat = "Guides"
                elif rel in ["compare.html", "best-poker-sites-ontario.html"]:
                    cat = "Rankings"

                index.append({
                    "url": rel,
                    "title": title.split(" | ")[0],
                    "h1": h1_text,
                    "desc": desc[:120],
                    "h2s": h2_text,
                    "cat": cat
                })
    with open(os.path.join(OUT, "search-index.json"), "w") as f:
        json.dump(index, f)
    print(f"  Built: search-index.json ({len(index)} pages)")

build_sitemap()
build_robots()
build_search_index()

print("=" * 60)
total = sum(1 for root, dirs, files in os.walk(OUT) for f in files if f.endswith(".html"))
print(f"Build complete: {total} HTML pages generated")
