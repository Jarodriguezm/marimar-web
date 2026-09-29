"""Genera las páginas de puertos (ES /puertos/, EN /en/ports/) y el sitemap.
Uso: python3 tools/build_puertos.py   (desde la raíz del repo)"""
import json, os, html
from urllib.parse import quote
from puertos_data import PORTS

DIRECT = {'puerto-sucre'}  # jurisdicción propia de MARIMAR; el resto, vía agencias aliadas
PARTNER = {
 'es': dict(title='Atención al buque (husbandry) y coordinación de escalas en {n} | MARIMAR C.A.',
            h1='Atención al buque y coordinación de su escala en {n}',
            lead=' Una agencia local habilitada en la jurisdicción actúa como agente de puerto, y MARIMAR presta la atención al buque y su tripulación (husbandry) y es su punto único de contacto: una sola PDA, coordinación y seguimiento de principio a fin.',
            faq=[['¿Quién es el agente de puerto en {n}?', 'Una agencia local asociada, habilitada en la jurisdicción de {n}, realiza los trámites oficiales como agente de puerto. MARIMAR presta la atención al buque y su tripulación (husbandry) y coordina toda la escala como su punto único de contacto.'],
                 ['¿Qué incluye la atención al buque (husbandry)?', 'La atención de las necesidades del buque y del armador durante la escala: cambios de tripulación, repuestos y suministros, atención médica, hoteles, transporte y reportes al armador.']],
            desc_pre='Atención al buque (husbandry) y coordinación de escalas en {n} por MARIMAR C.A., con agencia local habilitada. ',
            svc_map={'Agenciamiento y atención al buque': 'Atención al buque, tripulación y armador (husbandry)', 'Agenciamiento de buques tanqueros y de apoyo': 'Atención a buques tanqueros y de apoyo (husbandry)', 'Agenciamiento de tanqueros y gaseros': 'Atención a tanqueros y gaseros (husbandry)', 'Avisos de arribo y zarpe ante la Capitanía de Puerto': 'Coordinación de arribo y zarpe con el agente de puerto', 'Trámites aduanales de importación y exportación': 'Coordinación de trámites aduanales', 'Trámites aduanales': 'Coordinación de trámites aduanales'}),
 'en': dict(title='Husbandry & Port Call Coordination in {n}, Venezuela | MARIMAR C.A.',
            h1='Husbandry & coordination of your call at {n}',
            lead=' A licensed local agency acts as port agent, while MARIMAR provides husbandry and is your single point of contact: one PDA, coordination and follow-up end to end.',
            faq=[['Who is the port agent in {n}?', 'A licensed local partner agency in the {n} jurisdiction handles the official formalities as port agent. MARIMAR provides husbandry and coordinates the whole call as your single point of contact.'],
                 ['What does the husbandry service include?', 'Looking after the needs of the vessel and owner during the call: crew changes, spare parts and supplies, medical assistance, hotels, transport and reporting to the owner.']],
            desc_pre='Husbandry and port call coordination in {n} by MARIMAR C.A., with a licensed local agency. ',
            svc_map={'Vessel agency and attendance': 'Husbandry: vessel and owner attendance', 'Agency for tankers and support vessels': 'Husbandry for tankers and support vessels', 'Agency for tankers and gas carriers': 'Husbandry for tankers and gas carriers', 'Arrival and departure notices to the Harbour Master': 'Arrival and departure coordination with the port agent', 'Import and export customs clearance': 'Customs clearance coordination', 'Customs formalities': 'Customs clearance coordination'}),
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
        _d['services'] = [_t['svc_map'].get(x, x) for x in _d['services']]
        _d['desc'] = (_t['desc_pre'].format(n=_n) + _d['desc'].split('. ', 1)[1])[:300]
        for _f in _d['faq']:
            _f[1] = _f[1].replace('Sí. Nuestra División Aduanal gestiona la importación y la exportación, la clasificación arancelaria y el seguimiento del proceso.', 'Sí. La gestión aduanera se realiza con nuestro agencia local habilitada en la jurisdicción, y MARIMAR coordina la documentación y el seguimiento del proceso.')
            _f[1] = _f[1].replace('Sí. Nuestra División Aduanal gestiona la documentación y el seguimiento del proceso ante los organismos competentes.', 'Sí. La gestión aduanera se realiza con nuestro agencia local habilitada en la jurisdicción, y MARIMAR coordina la documentación y el seguimiento del proceso.')
            _f[1] = _f[1].replace('Yes. Our Customs Division handles imports and exports, tariff classification and process follow-up.', 'Yes. Customs clearance is handled with our licensed local agency in the jurisdiction, while MARIMAR coordinates the documentation and follows up the process.')
            _f[1] = _f[1].replace('Yes. Our Customs Division manages the documentation and follows the process with the competent authorities.', 'Yes. Customs clearance is handled with our licensed local agency in the jurisdiction, while MARIMAR coordinates the documentation and follows up the process.')
        _d['faq'] = [[q.format(n=_n), a.format(n=_n)] for q, a in _t['faq']] + [f for f in _d['faq'] if 'Cumaná' not in f[0] and 'Cumaná' not in f[1]]


BASE = 'https://www.marimargroup.com'
PUB = os.path.join(os.path.dirname(__file__), '..', 'public')
WA = '584121859530'
MAIL = 'agencianaviera@marimargroup.com'
TODAY = '2026-09-29'
e = html.escape

UI = {
 'es': dict(dir='/puertos/', home='/', other='en', hub='Puertos', hub_title='Agente naviero en el oriente de Venezuela: puertos que atendemos | MARIMAR C.A.',
   hub_desc='MARIMAR C.A. opera en Puerto Sucre (Cumaná) y presta atención al buque y coordinación de escalas en Güiria, Carúpano, Guanta, Puerto La Cruz, Jose y Margarita. Agencia naviera y aduanal desde 1992.',
   hub_h1='Puertos que atendemos en el oriente de Venezuela', hub_lead='Operamos directamente en Puerto Sucre (Cumaná), nuestra sede desde 1992, y en los demás puertos del oriente venezolano prestamos atención al buque (husbandry) y coordinación integral junto a agencias locales habilitadas. En todos los casos, MARIMAR es su punto único de contacto. Elija el puerto para ver los servicios y solicitar su proforma de gastos (PDA).',
   kicker='Agencia naviera · Oriente de Venezuela', nav=[('/#servicios','Servicios'),('/puertos/','Puertos'),('/#nosotros','Nosotros'),('/#contacto','Contacto')],
   cta_wa='Solicitar PDA por WhatsApp', cta_mail='Escribir a agencia', req='Solicitar servicios', f_loc='Ubicación', f_base='Modalidad', f_base_v='Directa · sede MARIMAR', f_partner='Atención al buque + agencia local', f_since='Experiencia', f_since_v='Desde 1992', f_pos='Posición',
   about='Sobre el puerto', svc='Servicios en', svc_p='Servicios que coordinamos en', how='Cómo trabajamos', steps=[('Envíe los datos de la escala','Nombre del buque, ETA, operación prevista y servicios requeridos.'),('Reciba su PDA','Le enviamos la proforma de gastos para que apruebe la escala con costos claros.'),('Coordinamos la escala','Nos encargamos de autoridades, terminal, proveedores y tripulación hasta el zarpe.')], steps3_p=('Coordinamos la escala','Con la agencia local habilitada coordinamos terminal, proveedores y tripulación, y le informamos hasta el zarpe.'),
   faq='Preguntas frecuentes', others='Otros puertos que atendemos', band_t='¿Tiene un buque rumbo a', band_p='Envíenos la ETA y los servicios que necesita. Le respondemos con la PDA.', view='Ver puerto',
   wa_txt='Hola, necesito una PDA para una escala en {p}. Buque: … ETA: … Servicios: …', wa_hub='Hola, necesito una PDA para una escala en el oriente de Venezuela. Buque: … Puerto: … ETA: …',
   home_l='Inicio', foot='Agencia naviera y aduanal. Cumaná, Venezuela, desde 1992.', lang_lbl='<b>ES</b> | EN', lang_aria='Ver en inglés', locale='es_VE', coords='{:.2f}°N · {:.2f}°O'),
 'en': dict(dir='/en/ports/', home='/en/', other='es', hub='Ports', hub_title='Ship Agent in Eastern Venezuela: Ports We Cover | MARIMAR C.A.',
   hub_desc='MARIMAR C.A. operates at Puerto Sucre (Cumaná) and provides husbandry and call coordination at Güiria, Carúpano, Guanta, Puerto La Cruz, Jose and Margarita, Venezuela. Port agency since 1992.',
   hub_h1='Ports we cover in eastern Venezuela', hub_lead='We operate directly at Puerto Sucre (Cumaná), our home port since 1992, and at the other ports of eastern Venezuela we provide husbandry and full coordination alongside licensed local agencies. Either way, MARIMAR is your single point of contact. Choose a port to see services and request your proforma disbursement account (PDA).',
   kicker='Port agency · Eastern Venezuela', nav=[('/en/#servicios','Services'),('/en/ports/','Ports'),('/en/#nosotros','About'),('/en/#contacto','Contact')],
   cta_wa='Request PDA via WhatsApp', cta_mail='Email the agency', req='Request services', f_loc='Location', f_base='Service model', f_base_v='Direct · MARIMAR base', f_partner='Husbandry + local agency', f_since='Experience', f_since_v='Since 1992', f_pos='Position',
   about='About the port', svc='Services in', svc_p='Services we coordinate in', how='How we work', steps=[('Send the call details','Vessel name, ETA, planned operation and services required.'),('Receive your PDA','We send the proforma disbursement account so you can approve the call with clear costs.'),('We run the call','We handle authorities, terminal, suppliers and crew until departure.')], steps3_p=('We run the call','With the licensed local agency we coordinate terminal, suppliers and crew, and keep you informed until departure.'),
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
    links = ''.join(f'<a href="{url(lang, p["slug"])}">{e(p[lang]["name"])}</a>' for p in PORTS) + f'<a href="{PROT[lang]["path"]}">{PROT[lang]["crumb"]}</a>'
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
    return head(lang, u['hub_title'], u['hub_desc'], path, alt, ld) + body + prot_band(lang) + foot(lang)


PROT = {
 'es': dict(path='/servicios/agente-protector/', title='Agente protector del armador en Venezuela | MARIMAR C.A.',
   desc='Agente protector (protecting agent) para armadores en Venezuela. Supervisamos la escala cuando el agente de puerto fue nombrado por el fletador: costos, tiempos, tripulación y estado del buque.',
   kicker='Servicio para armadores', h1='Agente protector del armador en Venezuela',
   lead='Cuando el fletador nombra al agente de puerto, sus intereses como armador necesitan a alguien de su lado. MARIMAR actúa como su agente protector: supervisa la escala, revisa los costos y le informa de forma independiente.',
   when_t='¿Cuándo necesita un agente protector?', when=['El fletador nombró al agente de puerto y usted quiere supervisión independiente.', 'Necesita control sobre la proforma (PDA) y la cuenta final de gastos (FDA).', 'Hay cambios de tripulación, reparaciones, repuestos o incidentes que requieren atención directa del armador.', 'Opera por primera vez en Venezuela y necesita a alguien de confianza en terreno.'],
   what_t='Qué hacemos por usted', what=['Revisión de la PDA y la FDA frente a los costos reales', 'Seguimiento de tiempos de fondeo, atraque y operación', 'Atención al buque (husbandry): tripulación, repuestos, suministros y atención médica', 'Visitas a bordo y reportes directos al armador', 'Apoyo en incidentes, reclamos y contacto con el club P&I', 'Inspecciones de condición y de carga (División Survey)'],
   why_t='Por qué MARIMAR', why=[('Desde 1992','Más de 30 años en operaciones marítimas y aduanales en Venezuela.'),('Independencia','Trabajamos para el armador. Nuestro reporte es suyo.'),('Survey propio','Evidencia técnica de condición y carga cuando hace falta.')],
   faq=[['¿Qué diferencia hay entre el agente de puerto y el agente protector?', 'El agente de puerto realiza los trámites oficiales de la escala y suele ser nombrado por quien paga los gastos de puerto, muchas veces el fletador. El agente protector trabaja solo para el armador: supervisa la escala y cuida sus intereses.'],
        ['¿En qué puertos presta el servicio?', 'En los puertos del oriente venezolano. Escríbanos con el buque, el puerto y la ETA y le confirmamos el alcance.'],
        ['¿Cómo se cotiza?', 'Según el puerto, la duración de la escala y los servicios requeridos. Le enviamos una propuesta al recibir los datos del buque.']],
   cta='Solicitar agente protector', wa='Hola, necesito un agente protector para una escala en Venezuela. Buque: … Puerto: … ETA: …', crumb='Agente protector', link_t='¿Su agente de puerto lo nombró el fletador?', link_p='Conozca nuestro servicio de agente protector del armador.', link_b='Ver servicio'),
 'en': dict(path='/en/services/protecting-agent/', title='Owners\' Protecting Agent in Venezuela | MARIMAR C.A.',
   desc='Owners\' protecting agent in Venezuela. We supervise the call when the port agent was nominated by charterers: costs, time, crew and vessel condition, reported independently to the owner.',
   kicker='Service for shipowners', h1='Owners\' protecting agent in Venezuela',
   lead='When charterers nominate the port agent, your interests as owner need someone on your side. MARIMAR acts as your protecting agent: we supervise the call, check the costs and report to you independently.',
   when_t='When do you need a protecting agent?', when=['Charterers nominated the port agent and you want independent supervision.', 'You need control over the PDA and the final disbursement account (FDA).', 'There are crew changes, repairs, spare parts or incidents requiring the owner\'s direct attention.', 'You are calling Venezuela for the first time and need someone you trust on the ground.'],
   what_t='What we do for you', what=['PDA and FDA review against actual costs', 'Monitoring of anchorage, berthing and operation times', 'Husbandry: crew, spare parts, supplies and medical assistance', 'On-board attendance and direct reports to the owner', 'Support with incidents, claims and P&I club liaison', 'Condition and cargo surveys (Survey Division)'],
   why_t='Why MARIMAR', why=[('Since 1992','Over 30 years in maritime and customs operations in Venezuela.'),('Independence','We work for the owner. Our reports are yours.'),('In-house surveys','Technical evidence on condition and cargo when needed.')],
   faq=[['What is the difference between a port agent and a protecting agent?', 'The port agent handles the official formalities of the call and is usually appointed by whoever pays the port costs, often the charterers. The protecting agent works only for the owner, supervising the call and safeguarding the owner\'s interests.'],
        ['Which ports do you cover?', 'Ports in eastern Venezuela. Send us the vessel, port and ETA and we will confirm the scope.'],
        ['How is it priced?', 'Depending on port, length of call and services required. We send a proposal once we receive the vessel details.']],
   cta='Request a protecting agent', wa='Hello, I need an owners\' protecting agent for a call in Venezuela. Vessel: … Port: … ETA: …', crumb='Protecting agent', link_t='Was your port agent nominated by charterers?', link_p='Learn about our owners\' protecting agent service.', link_b='View service'),
}

def protect_page(lang):
    u, d = UI[lang], PROT[lang]
    other = u['other']; path, alt = d['path'], PROT[other]['path']
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": u['home_l'], "item": BASE + u['home']},
            {"@type": "ListItem", "position": 2, "name": d['crumb'], "item": BASE + path}]},
        {"@type": "Service", "name": d['h1'], "serviceType": "Protecting agent", "description": d['desc'], "areaServed": {"@type": "Country", "name": "Venezuela"},
         "provider": {"@type": "LocalBusiness", "@id": BASE + "/#org", "name": "MARIMAR C.A.", "url": BASE + "/"}, "url": BASE + path},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d['faq']]}]}
    link = wa(d['wa'])
    body = f"""<section class="hero"><div class="wrap">
  <p class="crumbs"><a href="{u['home']}">{u['home_l']}</a> › {d['crumb']}</p>
  <p class="kicker">{d['kicker']}</p>
  <h1>{e(d['h1'])}</h1>
  <p class="lead">{e(d['lead'])}</p>
  <div class="ctas"><a class="btn btn-wa" href="{link}" target="_blank" rel="noopener">{d['cta']}</a><a class="btn btn-ghost" href="mailto:{MAIL}?subject={quote(d['crumb'])}">{u['cta_mail']}</a></div>
</div></section>
<section class="blk"><div class="wrap grid2">
  <div><h2>{d['when_t']}</h2><ul class="svc" style="grid-template-columns:1fr">{''.join(f'<li>{e(x)}</li>' for x in d['when'])}</ul></div>
  <div><h2>{d['what_t']}</h2><ul class="svc" style="grid-template-columns:1fr">{''.join(f'<li>{e(x)}</li>' for x in d['what'])}</ul></div>
</div></section>
<section class="blk alt"><div class="wrap"><h2>{d['why_t']}</h2><div class="steps">{''.join(f'<div class="step"><h3>{e(t)}</h3><p>{e(x)}</p></div>' for t, x in d['why'])}</div></div></section>
<section class="blk"><div class="wrap"><h2>{u['faq']}</h2>{''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in d['faq'])}</div></section>
<section class="band"><div class="wrap"><div><h2>{d['cta']}</h2><p>{u['band_p']}</p></div><div class="ctas"><a class="btn btn-wa" href="{link}" target="_blank" rel="noopener">WhatsApp</a><a class="btn btn-light" href="mailto:{MAIL}">{MAIL}</a></div></div></section>
"""
    return head(lang, d['title'], d['desc'], path, alt, ld) + body + foot(lang)

def prot_band(lang):
    d = PROT[lang]
    return f'<section class="band"><div class="wrap"><div><h2>{d["link_t"]}</h2><p>{d["link_p"]}</p></div><div class="ctas"><a class="btn btn-light" href="{d["path"]}">{d["link_b"]} →</a></div></div></section>\n'

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
for lang in ('es', 'en'):
    write(PROT[lang]['path'], protect_page(lang))
pairs.append((PROT['es']['path'], PROT['en']['path']))
pairs += [(url('es', p['slug']), url('en', p['slug'])) for p in PORTS]

def alt_links(es, en):
    return (f'    <xhtml:link rel="alternate" hreflang="es" href="{BASE}{es}"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="en" href="{BASE}{en}"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}{es}"/>\n')
entries = ''.join(f'  <url>\n    <loc>{BASE}{loc}</loc>\n    <lastmod>{TODAY}</lastmod>\n{alt_links(es, en)}  </url>\n' for es, en in pairs for loc in (es, en))
open(os.path.join(PUB, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + entries + '</urlset>\n')
print('páginas:', 4 + 2 * len(PORTS), '| urls sitemap:', 2 * len(pairs))
