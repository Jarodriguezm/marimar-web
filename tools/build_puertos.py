"""Genera las páginas de puertos (ES /puertos/, EN /en/ports/) y el sitemap.
Uso: python3 tools/build_puertos.py   (desde la raíz del repo)"""
import json, os, html
from urllib.parse import quote
from puertos_data import PORTS

DIRECT = {'puerto-sucre'}  # jurisdicción propia de MARIMAR; el resto, vía agencias aliadas
PARTNER = {
 'es': dict(title='Agente naviero en {n}: coordinación con agencias aliadas | MARIMAR C.A.',
            h1='Su escala en {n}, coordinada por MARIMAR',
            lead=' Operamos con agencias aliadas habilitadas en la jurisdicción y MARIMAR es su punto único de contacto: cotizamos, coordinamos y damos seguimiento a toda la operación.',
            faq=['¿MARIMAR opera directamente en {n}?', 'La escala se tramita a través de una agencia aliada habilitada en la jurisdicción de {n}. MARIMAR es su punto único de contacto: le enviamos la PDA, coordinamos con el aliado y damos seguimiento a la operación de principio a fin.'],
            desc_pre='Escalas en {n} coordinadas por MARIMAR C.A. con agencias aliadas habilitadas. '),
 'en': dict(title='Ship Agent in {n}: Partner Agency Network | MARIMAR C.A.',
            h1='Your call at {n}, coordinated by MARIMAR',
            lead=' We work with licensed partner agencies in the port jurisdiction, and MARIMAR is your single point of contact: we quote, coordinate and follow up the whole operation.',
            faq=['Does MARIMAR operate directly in {n}?', 'The call is handled through a licensed partner agency in the {n} jurisdiction. MARIMAR is your single point of contact: we send the PDA, coordinate with our partner and follow up the operation end to end.'],
            desc_pre='Port calls in {n} coordinated by MARIMAR C.A. with licensed partner agencies. '),
}
SHORT = {'margarita': {'es': 'Margarita', 'en': 'Margarita'}}
for _p in PORTS:
    _p['direct'] = _p['slug'] in DIRECT
    if _p['direct']:
        continue
    for _l in ('es', 'en'):
        _d, _t = _p[_l], PARTNER[_l]
        _n = SHORT.get(_p['slug'], {}).get(_l, _d['name'])
        _d['title'] = _t['title'].format(n=_n)
        _d['h1'] = _t['h1'].format(n=_n)
        _d['lead'] = _d['lead'] + _t['lead']
        _d['desc'] = (_t['desc_pre'].format(n=_n) + _d['desc'].split('. ', 1)[1])[:300]
        for _f in _d['faq']:
            _f[1] = _f[1].replace('Sí. Nuestra División Aduanal gestiona la importación y la exportación, la clasificación arancelaria y el seguimiento del proceso.', 'Sí. La gestión aduanera se realiza con nuestro aliado habilitado en la jurisdicción, y MARIMAR coordina la documentación y el seguimiento del proceso.')
            _f[1] = _f[1].replace('Sí. Nuestra División Aduanal gestiona la documentación y el seguimiento del proceso ante los organismos competentes.', 'Sí. La gestión aduanera se realiza con nuestro aliado habilitado en la jurisdicción, y MARIMAR coordina la documentación y el seguimiento del proceso.')
            _f[1] = _f[1].replace('Yes. Our Customs Division handles imports and exports, tariff classification and process follow-up.', 'Yes. Customs clearance is handled with our licensed partner in the jurisdiction, while MARIMAR coordinates the documentation and follows up the process.')
            _f[1] = _f[1].replace('Yes. Our Customs Division manages the documentation and follows the process with the competent authorities.', 'Yes. Customs clearance is handled with our licensed partner in the jurisdiction, while MARIMAR coordinates the documentation and follows up the process.')
        _d['faq'] = [[_t['faq'][0].format(n=_n), _t['faq'][1].format(n=_n)]] + [f for f in _d['faq'] if 'Cumaná' not in f[0] and 'Cumaná' not in f[1]]


BASE = 'https://www.marimargroup.com'
PUB = os.path.join(os.path.dirname(__file__), '..', 'public')
WA = '584121859530'
MAIL = 'agencianaviera@marimargroup.com'
TODAY = '2026-09-29'
e = html.escape

UI = {
 'es': dict(dir='/puertos/', home='/', other='en', hub='Puertos', hub_title='Agente naviero en el oriente de Venezuela: puertos que atendemos | MARIMAR C.A.',
   hub_desc='MARIMAR C.A. opera en Puerto Sucre (Cumaná) y coordina escalas con agencias aliadas en Güiria, Carúpano, Guanta, Puerto La Cruz, Jose y Margarita. Agencia naviera y aduanal desde 1992.',
   hub_h1='Puertos que atendemos en el oriente de Venezuela', hub_lead='Operamos directamente en Puerto Sucre (Cumaná), nuestra sede desde 1992, y coordinamos escalas en los demás puertos del oriente venezolano con agencias aliadas habilitadas. En todos los casos, MARIMAR es su punto único de contacto. Elija el puerto para ver los servicios y solicitar su proforma de gastos (PDA).',
   kicker='Agencia naviera · Oriente de Venezuela', nav=[('/#servicios','Servicios'),('/puertos/','Puertos'),('/#nosotros','Nosotros'),('/#contacto','Contacto')],
   cta_wa='Solicitar PDA por WhatsApp', cta_mail='Escribir a agencia', req='Solicitar servicios', f_loc='Ubicación', f_base='Modalidad', f_base_v='Directa · sede MARIMAR', f_partner='Con agencia aliada', f_since='Experiencia', f_since_v='Desde 1992', f_pos='Posición',
   about='Sobre el puerto', svc='Servicios en', svc_p='Servicios que coordinamos en', how='Cómo trabajamos', steps=[('Envíe los datos de la escala','Nombre del buque, ETA, operación prevista y servicios requeridos.'),('Reciba su PDA','Le enviamos la proforma de gastos para que apruebe la escala con costos claros.'),('Coordinamos la escala','Nos encargamos de autoridades, terminal, proveedores y tripulación hasta el zarpe.')], steps3_p=('Coordinamos la escala','Junto a nuestra agencia aliada coordinamos autoridades, terminal, proveedores y tripulación, y le informamos hasta el zarpe.'),
   faq='Preguntas frecuentes', others='Otros puertos que atendemos', band_t='¿Tiene un buque rumbo a', band_p='Envíenos la ETA y los servicios que necesita. Le respondemos con la PDA.', view='Ver puerto',
   wa_txt='Hola, necesito una PDA para una escala en {p}. Buque: … ETA: … Servicios: …', wa_hub='Hola, necesito una PDA para una escala en el oriente de Venezuela. Buque: … Puerto: … ETA: …',
   home_l='Inicio', foot='Agencia naviera y aduanal. Cumaná, Venezuela, desde 1992.', lang_lbl='<b>ES</b> | EN', lang_aria='Ver en inglés', locale='es_VE', coords='{:.2f}°N · {:.2f}°O'),
 'en': dict(dir='/en/ports/', home='/en/', other='es', hub='Ports', hub_title='Ship Agent in Eastern Venezuela: Ports We Cover | MARIMAR C.A.',
   hub_desc='MARIMAR C.A. operates at Puerto Sucre (Cumaná) and coordinates calls with partner agencies at Güiria, Carúpano, Guanta, Puerto La Cruz, Jose and Margarita, Venezuela. Port agency since 1992.',
   hub_h1='Ports we cover in eastern Venezuela', hub_lead='We operate directly at Puerto Sucre (Cumaná), our home port since 1992, and coordinate calls at the other ports of eastern Venezuela with licensed partner agencies. Either way, MARIMAR is your single point of contact. Choose a port to see services and request your proforma disbursement account (PDA).',
   kicker='Port agency · Eastern Venezuela', nav=[('/en/#servicios','Services'),('/en/ports/','Ports'),('/en/#nosotros','About'),('/en/#contacto','Contact')],
   cta_wa='Request PDA via WhatsApp', cta_mail='Email the agency', req='Request services', f_loc='Location', f_base='Service model', f_base_v='Direct · MARIMAR base', f_partner='Via partner agency', f_since='Experience', f_since_v='Since 1992', f_pos='Position',
   about='About the port', svc='Services in', svc_p='Services we coordinate in', how='How we work', steps=[('Send the call details','Vessel name, ETA, planned operation and services required.'),('Receive your PDA','We send the proforma disbursement account so you can approve the call with clear costs.'),('We run the call','We handle authorities, terminal, suppliers and crew until departure.')], steps3_p=('We run the call','Together with our partner agency we coordinate authorities, terminal, suppliers and crew, and keep you informed until departure.'),
   faq='Frequently asked questions', others='Other ports we cover', band_t='Vessel heading to', band_p='Send us the ETA and the services you need. We reply with the PDA.', view='View port',
   wa_txt='Hello, I need a PDA for a call at {p}, Venezuela. Vessel: … ETA: … Services: …', wa_hub='Hello, I need a PDA for a call in eastern Venezuela. Vessel: … Port: … ETA: …',
   home_l='Home', foot='Port agency and customs broker. Cumaná, Venezuela, since 1992.', lang_lbl='ES | <b>EN</b>', lang_aria='Ver en español', locale='en_US', coords='{:.2f}°N · {:.2f}°W'),
}

def url(lang, slug=None):
    return UI[lang]['dir'] + (slug + '/' if slug else '')

def wa(text):
    return f'https://wa.me/{WA}?text=' + quote(text)

def head(lang, title, desc, path, alt_path, ld):
    u = UI[lang]
    es_p, en_p = (path, alt_path) if lang == 'es' else (alt_path, path)
    cur = ' aria-current="page"'
    nav_html = ''.join(f'<a href="{h}"' + (cur if h == u['dir'] else '') + f'>{l}</a>' for h, l in u['nav'])
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<link rel="canonical" href="{BASE}{path}">
<link rel="alternate" hreflang="es" href="{BASE}{es_p}">
<link rel="alternate" hreflang="en" href="{BASE}{en_p}">
<link rel="alternate" hreflang="x-default" href="{BASE}{es_p}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="MARIMAR C.A.">
<meta property="og:locale" content="{u['locale']}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{BASE}{path}">
<meta property="og:image" content="{BASE}/puerto-marimar.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1d2d3d">
<link rel="icon" type="image/png" href="/logo-icon.png">
<link rel="stylesheet" href="/assets/css/fonts.css">
<link rel="stylesheet" href="/assets/css/puertos.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#contenido">{'Saltar al contenido' if lang=='es' else 'Skip to content'}</a>
<header class="top"><div class="wrap">
  <a href="{u['home']}" aria-label="MARIMAR C.A."><img src="/logo-full.png" alt="MARIMAR C.A. Agencia Naviera y Aduanal" width="227" height="138"></a>
  <nav class="main" aria-label="{'Navegación principal' if lang=='es' else 'Main navigation'}">{nav_html}</nav>
  <div class="hdr-right"><a class="lang" href="{alt_path}" hreflang="{u['other']}" aria-label="{u['lang_aria']}">{u['lang_lbl']}</a><a class="btn btn-primary" href="{u['home']}#contacto">{u['req']}</a></div>
</div></header>
<main id="contenido">
'''

def foot(lang):
    u = UI[lang]
    links = ''.join(f'<a href="{url(lang, p["slug"])}">{e(p[lang]["name"])}</a>' for p in PORTS)
    return f'''</main>
<footer class="ft"><div class="wrap">
  <div><strong style="color:#fff">MARIMAR C.A.</strong><br>{u['foot']}<br><a href="tel:+584121859530">+58 412-185.95.30</a> · <a href="mailto:{MAIL}">{MAIL}</a></div>
  <nav aria-label="{u['hub']}">{links}</nav>
</div></footer>
<a class="btn btn-wa wa-float" href="{wa(u['wa_hub'])}" target="_blank" rel="noopener">WhatsApp</a>
</body>
</html>
'''

def org_ref():
    return {"@id": BASE + "/#org"}

def port_page(lang, p):
    u, d = UI[lang], p[lang]
    other = u['other']
    path, alt = url(lang, p['slug']), url(other, p['slug'])
    region = p['region_es'] if lang == 'es' else p['region_en']
    wa_link = wa(u['wa_txt'].format(p=d['name']))
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": u['home_l'], "item": BASE + u['home']},
            {"@type": "ListItem", "position": 2, "name": u['hub'], "item": BASE + u['dir']},
            {"@type": "ListItem", "position": 3, "name": d['name'], "item": BASE + path}]},
        {"@type": "Service", "name": d['h1'], "serviceType": "Ship agency" , "description": d['desc'],
         "provider": {"@type": "LocalBusiness", "@id": BASE + "/#org", "name": "MARIMAR C.A.", "url": BASE + "/", "telephone": "+584121859530",
                      "address": {"@type": "PostalAddress", "addressLocality": "Cumaná", "addressRegion": "Sucre", "addressCountry": "VE"}},
         "areaServed": {"@type": "Place", "name": d['name'], "geo": {"@type": "GeoCoordinates", "latitude": p['lat'], "longitude": p['lon']}},
         "url": BASE + path},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d['faq']]}]}
    others = ''.join(f'<a class="card" href="{url(lang, o["slug"])}"><h3>{e(o[lang]["name"])}</h3><span>{e(o["region_es"] if lang=="es" else o["region_en"])}</span><span class="more">{u["view"]} →</span></a>' for o in PORTS if o['slug'] != p['slug'])
    body = f'''<section class="hero"><div class="wrap">
  <p class="crumbs"><a href="{u['home']}">{u['home_l']}</a> › <a href="{u['dir']}">{u['hub']}</a> › {e(d['name'])}</p>
  <p class="kicker">{u['kicker']}</p>
  <h1>{e(d['h1'])}</h1>
  <p class="lead">{e(d['lead'])}</p>
  <div class="ctas"><a class="btn btn-wa" href="{wa_link}" target="_blank" rel="noopener">{u['cta_wa']}</a><a class="btn btn-ghost" href="mailto:{MAIL}?subject={quote('PDA – ' + d['name'])}">{u['cta_mail']}</a></div>
</div></section>
<section class="facts"><dl class="wrap">
  <div><dt>{u['f_loc']}</dt><dd>{e(region)}</dd></div>
  <div><dt>{u['f_base']}</dt><dd>{u['f_base_v'] if p['direct'] else u['f_partner']}</dd></div>
  <div><dt>{u['f_since']}</dt><dd>{u['f_since_v']}</dd></div>
  <div><dt>{u['f_pos']}</dt><dd>{u['coords'].format(p['lat'], abs(p['lon']))}</dd></div>
</dl></section>
<section class="blk"><div class="wrap grid2">
  <div><h2>{u['about']}</h2><p>{e(d['about'])}</p></div>
  <div><h2>{u['svc'] if p['direct'] else u['svc_p']} {e(d['name'])}</h2><ul class="svc">{''.join(f'<li>{e(s)}</li>' for s in d['services'])}</ul></div>
</div></section>
<section class="blk alt"><div class="wrap"><h2>{u['how']}</h2><div class="steps">{''.join(f'<div class="step"><h3>{e(t)}</h3><p>{e(x)}</p></div>' for t, x in (u['steps'] if p['direct'] else u['steps'][:2] + [u['steps3_p']]))}</div></div></section>
<section class="blk"><div class="wrap"><h2>{u['faq']}</h2>{''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in d['faq'])}</div></section>
<section class="blk alt"><div class="wrap"><h2>{u['others']}</h2><div class="cards">{others}</div></div></section>
<section class="band"><div class="wrap"><div><h2>{u['band_t']} {e(d['name'])}?</h2><p>{u['band_p']}</p></div><div class="ctas"><a class="btn btn-wa" href="{wa_link}" target="_blank" rel="noopener">{u['cta_wa']}</a><a class="btn btn-light" href="mailto:{MAIL}?subject={quote('PDA – ' + d['name'])}">{MAIL}</a></div></div></section>
'''
    return head(lang, d['title'], d['desc'], path, alt, ld) + body + foot(lang)

def hub_page(lang):
    u = UI[lang]; other = u['other']
    path, alt = u['dir'], UI[other]['dir']
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": u['home_l'], "item": BASE + u['home']},
            {"@type": "ListItem", "position": 2, "name": u['hub'], "item": BASE + path}]},
        {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": p[lang]['name'], "url": BASE + url(lang, p['slug'])} for i, p in enumerate(PORTS)]}]}
    cards = ''.join(f'<a class="card" href="{url(lang, p["slug"])}"><h3>{e(p[lang]["name"])}</h3><span>{e(p["region_es"] if lang=="es" else p["region_en"])} · <b>{u["f_base_v"] if p["direct"] else u["f_partner"]}</b></span><p style="margin-top:10px;font-size:15px">{e(p[lang]["lead"].split(". ")[0])}.</p><span class="more">{u["view"]} →</span></a>' for p in PORTS)
    body = f'''<section class="hero"><div class="wrap">
  <p class="crumbs"><a href="{u['home']}">{u['home_l']}</a> › {u['hub']}</p>
  <p class="kicker">{u['kicker']}</p>
  <h1>{u['hub_h1']}</h1>
  <p class="lead">{u['hub_lead']}</p>
  <div class="ctas"><a class="btn btn-wa" href="{wa(u['wa_hub'])}" target="_blank" rel="noopener">{u['cta_wa']}</a><a class="btn btn-ghost" href="mailto:{MAIL}">{u['cta_mail']}</a></div>
</div></section>
<section class="blk alt"><div class="wrap"><div class="cards">{cards}</div></div></section>
<section class="blk"><div class="wrap"><h2>{u['how']}</h2><div class="steps">{''.join(f'<div class="step"><h3>{e(t)}</h3><p>{e(x)}</p></div>' for t, x in u['steps'])}</div></div></section>
'''
    return head(lang, u['hub_title'], u['hub_desc'], path, alt, ld) + body + foot(lang)

def write(path, text):
    full = os.path.join(PUB, path.strip('/'), 'index.html')
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8').write(text)

pairs = [('/', '/en/')]
for lang in ('es', 'en'):
    write(UI[lang]['dir'], hub_page(lang))
    for p in PORTS:
        write(url(lang, p['slug']), port_page(lang, p))
pairs.append(('/puertos/', '/en/ports/'))
pairs += [(url('es', p['slug']), url('en', p['slug'])) for p in PORTS]

def alt_links(es, en):
    return (f'    <xhtml:link rel="alternate" hreflang="es" href="{BASE}{es}"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="en" href="{BASE}{en}"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}{es}"/>\n')
entries = ''.join(f'  <url>\n    <loc>{BASE}{loc}</loc>\n    <lastmod>{TODAY}</lastmod>\n{alt_links(es, en)}  </url>\n' for es, en in pairs for loc in (es, en))
open(os.path.join(PUB, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + entries + '</urlset>\n')
print('páginas:', 2 + 2 * len(PORTS), '| urls sitemap:', 2 * len(pairs))
