#!/usr/bin/env python3
"""Gera as páginas HTML do site Giquira Group.

Uso:  python3 tools/build_site.py      (a partir da pasta do site)

Tudo o que muda com frequência está na secção CONFIGURAÇÃO, logo abaixo:
  • SITE_URL / BASE_PATH  → domínio (ver README, "Ligar o domínio")
  • BRAND                 → logótipo oficial (cabeçalho, rodapé e transição entre páginas)
  • PARTNERS              → parceiros e respetivos logótipos
  • PRODUCTS              → galeria de produtos (vazia até haver fotografias e aprovação)
"""
import json, os, html as H

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ═════════════════════════ CONFIGURAÇÃO ═════════════════════════

# Domínio: None enquanto não estiver ligado. Exemplo depois de ligar: "https://www.exemplo.com"
SITE_URL = None
# Caminho base onde o site está publicado. GitHub Pages sem domínio: "/giquiragroup-site/". Com domínio: "/".
BASE_PATH = "/giquiragroup-site/"

# Logótipo oficial. Enquanto for None, o site usa o nome "Giquira Group" em texto.
# Quando chegar: copiar os ficheiros para media/brand/ e preencher, por exemplo:
#   "logo": "media/brand/giquira-logo.svg",        (versão para fundo claro: cabeçalho)
#   "logo_light": "media/brand/giquira-logo-branco.svg",  (versão para fundo escuro: rodapé e transição)
BRAND = {
    "name": "Giquira", "name_2": "Group",
    "tagline": "Procurement · Logística · Produtos",
    "slogan": "Committed to quality. Committed to you.",
    "logo": "media/brand/giquira-logo-horizontal.webp",          # cabeçalho (fundo claro)
    "logo_light": "media/brand/giquira-logo-horizontal-branco.webp",  # rodapé e transição (fundo escuro)
    "mark": "media/brand/giquira-simbolo.webp",                   # símbolo sozinho
}

# Loja física (localização enviada pelo cliente, 12/11/2026)
STORE = {"lat": -25.962473, "lng": 32.579533}
def store_maps():
    return f"https://maps.google.com/?q={STORE['lat']},{STORE['lng']}"
def store_iframe(title):
    la, lo = STORE["lat"], STORE["lng"]
    bbox = f"{lo-0.008:.4f}%2C{la-0.006:.4f}%2C{lo+0.008:.4f}%2C{la+0.006:.4f}"
    return (f'<iframe title="{title}" loading="lazy" src="https://www.openstreetmap.org/export/embed.html?bbox={bbox}'
            f'&amp;layer=mapnik&amp;marker={la}%2C{lo}"></iframe>')

# Empresa do grupo que faz o procurement (carta de apresentação, nov. 2026)
COMPAN = {"name": "Compan Services, Lda", "founded": "novembro de 2021", "team": 13}
# Empresas do grupo (notas do Danilo, 18/11/2026)
GROUP_COMPANIES = ["Compan Services, Lda", "RA Solution", "FA Electronics"]

CONTACT = {
    "wa_main": "258844266127", "wa_main_label": "+258 84 426 6127",
    "wa_alt": "258874266125", "wa_alt_label": "+258 87 426 6125",
    "email": "geral@giquiragroup.com", "instagram": "giquira_group",
    "address_1": "Av. Emília Dause, N.º 948, R/C", "address_2": "Antes da Alof Palm, Cidade de Maputo",
}

# Parceiros: quando os logótipos chegarem, colocar em media/logos/ e preencher "logo".
PARTNERS = [
    {"name": "Mozambique Terramar Trading", "kind": "Lda", "logo": "media/logos/terramar.webp"},
    {"name": "Transcargo Haulage Contractors", "kind": "Lda", "logo": "media/logos/transcargo.webp"},
    {"name": "Micaia", "kind": "Fundação", "logo": "media/logos/micaia.webp"},
    {"name": "MozFert", "kind": "Lda", "logo": "media/logos/mozfert.webp"},
]

# Produtos da loja — tirados dos posts da loja (novembro de 2026). Preços em MT.
# Cada produto: name, brand, tag (texto grande do cartão enquanto não há foto), category (igual a um nome de PLINES),
#               desc (opcional), variants [(opção, preço)], image (None até haver foto quadrada em media/produtos/).
PRICES_DATE = "novembro de 2026"
_B = lambda *v: list(zip(("9 000 BTU", "12 000 BTU", "18 000 BTU", "24 000 BTU", "30 000 BTU", "36 000 BTU"), v))
PRODUCTS = [
    # Telemóveis
    {"name": "iPhone 18 Pro Max 256 GB · só eSIM", "brand": "Apple", "tag": "18 Pro Max", "category": "Telemóveis",
     "variants": [("Burgundy", 125000), ("Glacier", 123000), ("Black", 123000), ("Silver", 123000)], "image": "media/produtos/iphone-18-pro-max.webp"},
    {"name": "iPhone 18 Pro Max 256 GB · 1 SIM + eSIM", "brand": "Apple", "tag": "18 Pro Max", "category": "Telemóveis",
     "variants": [("Burgundy", 127000), ("Glacier", 125000), ("Black", 125000), ("Silver", 123000)], "image": "media/produtos/iphone-18-pro-max.webp"},
    {"name": "iPhone 18 Pro Max 512 GB · 1 SIM + eSIM", "brand": "Apple", "tag": "18 Pro Max", "category": "Telemóveis",
     "variants": [("Burgundy", 142000), ("Glacier", 140000), ("Black", 140000), ("Silver", 137000)], "image": "media/produtos/iphone-18-pro-max.webp"},
    {"name": "iPhone 17 Pro Max", "brand": "Apple", "tag": "17 Pro Max", "category": "Telemóveis", "desc": "Cores: Blue, Orange e Silver.",
     "variants": [("256 GB · só eSIM", 108000), ("256 GB · 1 SIM + eSIM", 118000), ("512 GB · 1 SIM + eSIM", 136000), ("1 TB · 1 SIM + eSIM", 152000)], "image": "media/produtos/iphone-17-pro-max.webp"},
    {"name": "iPhone 17 Pro · 1 SIM + eSIM", "brand": "Apple", "tag": "17 Pro", "category": "Telemóveis",
     "variants": [("256 GB", 108000), ("512 GB", 125000), ("1 TB", 135000)], "image": "media/produtos/iphone-17-pro.webp"},
    {"name": "iPhone 17 Air 256 GB · só eSIM", "brand": "Apple", "tag": "17 Air", "category": "Telemóveis",
     "variants": [("256 GB", 79000)], "image": "media/produtos/iphone-17-air.webp"},
    {"name": "iPhone 17 256 GB · 1 SIM + eSIM", "brand": "Apple", "tag": "17", "category": "Telemóveis",
     "variants": [("256 GB", 70000)], "image": "media/produtos/iphone-17.webp"},
    # Televisores
    {"name": "Samsung Crystal UHD 4K U8000F (2025)", "brand": "Samsung", "tag": "Crystal UHD", "category": "Televisores",
     "variants": [('43"', 30500), ('55"', 36500), ('65"', 48000), ('75"', 73500), ('85"', 99500)], "image": "media/produtos/samsung-crystal-uhd.webp"},
    {"name": "Samsung QLED 4K (2025)", "brand": "Samsung", "tag": "QLED", "category": "Televisores",
     "variants": [('Q70F 55"', 50500), ('Q70F 65"', 60500), ('Q60F 75"', 98500), ('Q70F 85"', 125500)], "image": "media/produtos/samsung-qled.webp"},
    {"name": "Xiaomi TV A", "brand": "Xiaomi", "tag": "TV A", "category": "Televisores",
     "variants": [('43" Full HD', 18500), ('43" 4K Ultra HD', 20500), ('50" 4K Ultra HD', 27000), ('55" 4K Ultra HD', 31000), ('65" 4K Ultra HD', 43000)], "image": "media/produtos/xiaomi-tv-a.webp"},
    {"name": "Xiaomi TV A Pro QLED", "brand": "Xiaomi", "tag": "A Pro QLED", "category": "Televisores",
     "variants": [('43"', 22500), ('55"', 32000), ('65"', 45000), ('75"', 63000)], "image": "media/produtos/xiaomi-tv-a-pro.webp"},
    # Ar condicionado
    {"name": "Gree R410 Inverter · Frio", "brand": "Gree", "tag": "Inverter", "category": "Ar condicionado", "variants": _B(29500, 32500, 42500, 51500, 65500, 75500), "image": "media/produtos/gree.webp"},
    {"name": "Gree R410 · Quente e frio", "brand": "Gree", "tag": "Quente e frio", "category": "Ar condicionado", "variants": _B(27500, 30500, 41500, 51500), "image": "media/produtos/gree.webp"},
    {"name": "Gree R410 · Frio", "brand": "Gree", "tag": "Frio", "category": "Ar condicionado", "variants": _B(23500, 23500, 33500, 39500), "image": "media/produtos/gree.webp"},
    {"name": "Midea Inverter R32", "brand": "Midea", "tag": "Inverter", "category": "Ar condicionado", "variants": _B(23000, 27500, 37500, 46500), "image": "media/produtos/midea.webp"},
    {"name": "Super General", "brand": "Super General", "tag": "Split", "category": "Ar condicionado", "variants": _B(22000, 23500, 33500, 41500), "image": "media/produtos/super-general.webp"},
    {"name": "DePoint R410", "brand": "DePoint", "tag": "R410", "category": "Ar condicionado", "variants": _B(19500, 20500, 28500, 37500, 54500), "image": "media/produtos/depoint.webp"},
    {"name": "Mozpoint", "brand": "Mozpoint", "tag": "Split", "category": "Ar condicionado", "variants": _B(18500, 19500, 26500, 36500), "image": "media/produtos/mozpoint.webp"},
    {"name": "AUX Inverter", "brand": "AUX", "tag": "Inverter", "category": "Ar condicionado", "variants": [("9 000 BTU", 20500), ("12 000 BTU", 21500)], "image": "media/produtos/aux.webp"},
    {"name": "SPJ · Frio", "brand": "SPJ", "tag": "Frio", "category": "Ar condicionado", "variants": [("9 000 BTU", 18500), ("24 000 BTU", 36500)], "image": "media/produtos/spj.webp"},
    {"name": "Syinix", "brand": "Syinix", "tag": "Split", "category": "Ar condicionado", "variants": [("9 000 BTU", 18500), ("12 000 BTU", 19500)], "image": "media/produtos/syinix.webp"},
    {"name": "Chigo", "brand": "Chigo", "tag": "Split", "category": "Ar condicionado", "variants": [("9 000 BTU", 17500), ("12 000 BTU", 18500)], "image": "media/produtos/chigo.webp"},
    # Internet via satélite (lista de 19/11/2026)
    {"name": "Kit Starlink", "brand": "Starlink", "tag": "Internet", "category": "Internet Starlink", "desc": "Internet via satélite, em qualquer ponto do país.",
     "variants": [("Starlink Standard (V4)", 22000), ("Starlink Mini", 12800)], "image": "media/produtos/starlink.webp"},
    # Vídeo e microfones
    {"name": "DJI Osmo Mobile (estabilizador para telemóvel)", "brand": "DJI", "tag": "Osmo Mobile", "category": "Vídeo e microfones",
     "variants": [("Osmo Mobile 7P", 11000), ("Osmo Mobile 8", 12000), ("Osmo Mobile 8P", 15500)], "image": "media/produtos/dji-osmo-mobile.webp"},
    {"name": "DJI Mic Mini (microfone sem fios)", "brand": "DJI", "tag": "Mic Mini", "category": "Vídeo e microfones",
     "variants": [("DJI Mic Mini 2", 16000), ("DJI Mic Mini 2S", 21000), ("Capas magnéticas (várias cores)", 2500)], "image": "media/produtos/dji-mic-mini.webp"},
    {"name": "Hollyland Lark (microfone sem fios)", "brand": "Hollyland", "tag": "Lark M2", "category": "Vídeo e microfones",
     "variants": [("Lark M2", 11000), ("Lark M2S", 12500)], "image": "media/produtos/hollyland-lark-m2.webp"},
    # Consolas e jogos
    {"name": "GTA 6 (PS5)", "brand": "PlayStation 5", "tag": "GTA 6", "category": "Consolas e jogos", "variants": [("Jogo para PS5", 7500)], "image": "media/produtos/gta-6.webp"},
    {"name": "Consola portátil SJGAM M18", "brand": "SJGAM", "tag": "M18", "category": "Consolas e jogos", "variants": [("SJGAM M18", 8000)], "image": "media/produtos/sjgam-m18.webp"},
    # Acessórios e equipamentos
    {"name": "Sunmi V2s (POS com impressora)", "brand": "Sunmi", "tag": "V2s", "category": "Acessórios e equipamentos", "desc": "Terminal de vendas portátil com impressora de talões.",
     "variants": [("Sunmi V2s", 14500)], "image": "media/produtos/sunmi-v2s.webp"},
    {"name": "Localizador GPS (tracker)", "brand": "GPS", "tag": "Tracker", "category": "Acessórios e equipamentos", "variants": [("Tracker GPS", 3500)], "image": None},
]
# Gree R410 Frio: 9 000 e 12 000 BTU têm o mesmo preço (23.500 MT) — confirmado pela loja.

def mt(v):
    return f"{v:,}".replace(",", ".") + " MT"

NAV = [("index.html", "Início"), ("procurement.html", "Procurement"), ("produtos.html", "Produtos"),
       ("sobre.html", "Sobre nós"), ("contactos.html", "Contactos")]

# ═════════════════════════ AUXILIARES ═════════════════════════

import hashlib
def ver(path):
    """Versão do ficheiro (muda sempre que o conteúdo muda), para o browser não usar uma cópia antiga."""
    with open(os.path.join(OUT, path), "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()[:8]
CSS_V, JS_V = ver("assets/site.css"), ver("assets/site.js")

ARROW = '<svg class="ar" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h9M8.5 4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
WA_SVG = '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" focusable="false"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1-.7-.3-1.5-.8-2.1-1.4-.6-.6-1-1.2-1.4-1.9-.1-.2 0-.4.1-.5l.4-.5.2-.4c.1-.2 0-.3 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.5.1-.7.3-.7.7-1 1.6-.9 2.5.2 1 .7 1.9 1.3 2.7 1.3 1.7 2.9 2.9 4.9 3.5.9.3 1.7.2 2.3-.1.7-.4 1.1-1 1.3-1.7.1-.3 0-.5-.1-.6z"/></svg>'
PLAY = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 1.8v12.4L14 8z"/></svg>'

def wa(text=None, num=None):
    n = num or CONTACT["wa_main"]
    from urllib.parse import quote
    return f"https://wa.me/{n}" + (f"?text={quote(text)}" if text else "")

def img(name, alt, sizes="(max-width:760px) 100vw, 50vw", eager=False):
    """Fotografia otimizada (media/<name>.webp 960px + media/<name>-480.webp)."""
    load = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    return (f'<div class="ph"><img src="media/{name}.webp" srcset="media/{name}-480.webp 480w, media/{name}.webp 960w" '
            f'sizes="{sizes}" width="960" height="1280" alt="{H.escape(alt)}" {load}></div>')

def brand(dark=False):
    logo = BRAND["logo_light"] if dark and BRAND["logo_light"] else BRAND["logo"]
    if logo:
        return (f'<a class="brand has-logo" href="index.html" aria-label="{BRAND["name"]} {BRAND["name_2"]}, página inicial"><img src="{logo}" alt="" width="195" height="40">'
                f'<span class="bx"><span class="bn">{BRAND["name"]} {BRAND["name_2"]}</span></span></a>')
    return (f'<a class="brand" href="index.html" aria-label="{BRAND["name"]} {BRAND["name_2"]}, página inicial"><span class="bx">'
            f'<span class="bn">{BRAND["name"]} <span>{BRAND["name_2"]}</span></span>'
            f'<span class="bt">{BRAND["tagline"] if not dark else BRAND["slogan"]}</span></span></a>')

# Endereço público atual (enquanto o domínio não estiver ligado, usa o do GitHub Pages)
PUBLIC_URL = SITE_URL or "https://alcapone69-al.github.io/giquiragroup-site"
def url(path=""):
    return PUBLIC_URL.rstrip("/") + "/" + path

# ═════════════════════════ MOLDE DA PÁGINA ═════════════════════════

def page(fname, title, desc, body, schema=False):
    AC = ' aria-current="page"'
    nav = "".join(f'<a href="{h}"{AC if h == fname else ""}>{t}</a>' for h, t in NAV)
    mnav = "".join(f'<a href="{h}"{AC if h == fname else ""} style="--i:{i}">{t}<small>0{i+1}</small></a>' for i, (h, t) in enumerate(NAV))
    canon = url("" if fname == "index.html" else fname)
    meta_url = f'<link rel="canonical" href="{canon}">\n<meta property="og:url" content="{canon}">\n' if canon else ""
    og_img = f'<meta property="og:image" content="{url("media/og-giquira.jpg")}">\n' if os.path.exists(os.path.join(OUT, "media/og-giquira.jpg")) else ""
    ld = ""
    if schema:
        org = {"@context": "https://schema.org", "@type": "Organization", "name": "Giquira Group",
               "slogan": BRAND["slogan"], "email": CONTACT["email"],
               "description": "Grupo familiar em Maputo: procurement internacional, logística, venda de produtos eletrónicos, consultoria e construção civil.",
               "subOrganization": {"@type": "Organization", "name": COMPAN["name"], "foundingDate": "2021-11",
                                   "description": "Empresa do Giquira Group dedicada ao procurement."},
               "telephone": ["+" + CONTACT["wa_main"], "+" + CONTACT["wa_alt"]],
               "address": {"@type": "PostalAddress", "streetAddress": CONTACT["address_1"], "addressLocality": "Maputo", "addressCountry": "MZ"},
               "areaServed": {"@type": "Country", "name": "Moçambique"},
               "sameAs": [f"https://instagram.com/{CONTACT['instagram']}"]}
        org["url"] = url()
        if BRAND["logo"]: org["logo"] = url(BRAND["logo"])
        ld = f'<script type="application/ld+json">{json.dumps(org, ensure_ascii=False)}</script>\n'
    labels = json.dumps({h: t for h, t in NAV}, ensure_ascii=False)
    wl = f'<img class="wl" src="{BRAND["logo_light"] or BRAND["logo"]}" alt="" width="973" height="200">' if (BRAND["logo_light"] or BRAND["logo"]) else ""
    wn = "" if wl else f'<div class="wn"><span>{BRAND["name"]} <em>{BRAND["name_2"]}</em></span></div>'
    html = f'''<!doctype html>
<html lang="pt-MZ">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
{meta_url}<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#24561A">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Giquira Group">
<meta property="og:locale" content="pt_MZ">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
{og_img}<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.png" type="image/png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="preload" href="assets/fonts/schibsted-grotesk-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/instrument-sans-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/site.css?v={CSS_V}">
<script>(function(d){{d.className+=' js';try{{if(sessionStorage.getItem('wp'))d.className+=' wp';else d.className+=' first'}}catch(e){{d.className+=' first'}}}})(document.documentElement)</script>
{ld}</head>
<body data-wa="{CONTACT["wa_main"]}">
<div class="bar" id="bar" aria-hidden="true"></div>
<div class="wipe" id="wipe" aria-hidden="true" data-labels='{labels}'><div class="wc">{wl}{wn}<div class="wd" id="wd"></div></div></div>
<a class="skip" href="#conteudo">Saltar para o conteúdo</a>

<header>
  <div class="w hbar">
    {brand()}
    <nav class="mainnav" aria-label="Principal">{nav}</nav>
    <div class="hact">
      <a class="btn" href="index.html#pedido">Pedir cotação {ARROW}</a>
      <button class="mtog" id="mtog" type="button" aria-expanded="false" aria-controls="mpanel" aria-label="Abrir menu"><i></i></button>
    </div>
  </div>
</header>
<div class="mpanel" id="mpanel">
  <nav aria-label="Principal, telemóvel">{mnav}</nav>
  <div class="mfoot">
    <a class="btn" href="index.html#pedido">Pedir cotação {ARROW}</a>
    <a class="btn wa" href="{wa("Olá Giquira Group! Gostaria de falar com a vossa equipa.")}" target="_blank" rel="noopener">{WA_SVG} WhatsApp</a>
    <p>{CONTACT["wa_main_label"]} · {CONTACT["email"]}</p>
  </div>
</div>

<main id="conteudo" tabindex="-1">
{body}
</main>

<footer><div class="w fw">
  <div>
    {brand(dark=True)}
    <p style="margin:20px 0 0;max-width:36ch">Grupo familiar em Maputo: procurement, logística e venda de produtos.</p>
  </div>
  <div><h4>Páginas</h4><ul>{"".join(f'<li><a href="{h}">{t}</a></li>' for h, t in NAV)}</ul></div>
  <div><h4>Contacto</h4><ul>
    <li><a href="{wa(num=CONTACT["wa_main"])}" target="_blank" rel="noopener">{CONTACT["wa_main_label"]}</a></li>
    <li><a href="{wa(num=CONTACT["wa_alt"])}" target="_blank" rel="noopener">{CONTACT["wa_alt_label"]}</a></li>
    <li><a href="mailto:{CONTACT["email"]}">{CONTACT["email"]}</a></li>
    <li><a href="https://instagram.com/{CONTACT["instagram"]}" target="_blank" rel="noopener">@{CONTACT["instagram"]}</a></li>
    <li>{CONTACT["address_1"]}, Maputo</li>
  </ul></div>
  <div class="legal"><span>© <span data-year>2026</span> Giquira Group · Maputo, Moçambique</span><span>{BRAND["slogan"]}</span></div>
</div></footer>
<a class="btn wa fab" href="{wa("Olá Giquira Group! Gostaria de falar com a vossa equipa.")}" target="_blank" rel="noopener" aria-label="Falar com o Giquira Group no WhatsApp">{WA_SVG}<span>WhatsApp</span></a>
<script src="assets/site.js?v={JS_V}" defer></script>
</body>
</html>
'''
    with open(os.path.join(OUT, fname), "w") as f:
        f.write(html)

def lines(*parts, start=0):
    """Título revelado linha a linha."""
    return " ".join(f'<span class="ln" style="--i:{start+i}"><span>{p}</span></span>' for i, p in enumerate(parts))

# ═════════════════════════ BLOCOS PARTILHADOS ═════════════════════════

STEPS = [
    ("Envie o pedido", "Uma lista, um link ou uma foto. Diga quantidades, especificações e o prazo de que precisa.", False),
    ("Encontramos o fornecedor", "Identificamos e qualificamos fábricas e fornecedores, e comparamos propostas por si.", False),
    ("Receba a cotação", "Produto, frete e taxas no mesmo documento: o custo total, sem surpresas à chegada.", False),
    ("Produção e inspeção", "Só compramos com a sua confirmação. Acompanhamos a produção e inspecionamos antes do embarque.", False),
    ("Embarque e alfândega", "Consolidamos a carga e tratamos da documentação e do desalfandegamento.", True),
    ("Entrega em Moçambique", "Levamos até ao seu armazém, loja ou escritório e confirmamos a receção.", True),
]
def steps_html():
    lg = '<br><span class="lg">Logística incluída</span>'
    s = "".join(f'<li class="st"><span class="n" aria-hidden="true">{i+1}</span><h3>{t}</h3><p>{d}{lg if l else ""}</p></li>'
                for i, (t, d, l) in enumerate(STEPS))
    return f'<div class="steps" id="steps"><span class="rail" aria-hidden="true"><b id="fill"></b></span><ol class="stl">{s}</ol></div>'

CATS = [("Material industrial", "Peças, ferramentas e equipamento para a indústria."),
        ("Equipamentos de construção", "Máquinas e materiais para construção civil."),
        ("Mobiliário", "Para escritórios e residências."),
        ("Segurança e proteção individual", "EPI: fardamento, calçado, capacetes e mais."),
        ("Energias renováveis", "Painéis solares, baterias e sistemas de energia."),
        ("Material hospitalar", "Equipamento e consumíveis para unidades de saúde.")]
def cats_html():
    return '<ul class="cats">' + "".join(
        f'<li data-rv style="--i:{i%3}"><span class="k">{i+1:02d}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(CATS)) + "</ul>"

VIDEOS = [("visita-dubai", "Visita a um parceiro no Dubai", "13 s"),
          ("visita-fabrica", "Visita a uma fábrica parceira", "45 s"),
          ("processo-aluminio", "Tratamento de perfis de alumínio", "46 s"),
          ("linha-extrusao", "Linha de extrusão", "14 s")]
def china_html(videos=True):
    vids = ""
    if videos:
        vids = '<div class="vids">' + "".join(
            f'<figure class="vid" data-rv style="--i:{i}"><video src="media/{n}.mp4" poster="media/{n}-poster.webp" playsinline preload="none" aria-label="{l}"></video>'
            f'<button class="play" type="button" aria-label="Ver vídeo: {l}"><span class="pb">{PLAY}</span><span>{l} <small>{d}</small></span></button></figure>'
            for i, (n, l, d) in enumerate(VIDEOS)) + "</div>"
    S = "(max-width:760px) 50vw, 33vw"
    return f'''<section class="sec dark" id="china"><div class="w">
  <div class="head">
    <div data-rv><p class="eyebrow">No terreno</p><h2>Não compramos por catálogo. <em>Vamos à fábrica.</em></h2></div>
    <p class="lead" data-rv style="--i:1">A nossa equipa visita fornecedores, fábricas e parceiros, na China, no Dubai e na Tanzânia: das reuniões de negociação à linha de produção e ao contentor pronto a partir. É assim que a qualidade prometida passa a ser a qualidade entregue.</p>
  </div>
  <div class="mosaic">
    <figure class="a" data-img>{img("parceiro-tanzania", "Aperto de mão com um parceiro na Tanzânia, em frente a empilhadores", "(max-width:760px) 100vw, 34vw")}<figcaption>Com um parceiro na Tanzânia</figcaption></figure>
    <figure class="b" data-img style="--i:1">{img("reuniao-cha", "Reunião com uma fornecedora na China", S)}<figcaption>Reunião com fornecedora</figcaption></figure>
    <figure class="c" data-img style="--i:2">{img("reuniao-escritorio", "Reunião de negociação num escritório na China", S)}<figcaption>Negociação</figcaption></figure>
    <figure class="d" data-img style="--i:1">{img("jantar-parceiros", "Jantar com parceiros comerciais na China", S)}<figcaption>Com parceiros</figcaption></figure>
    <figure class="e" data-img style="--i:2">{img("contentor-danilo", "Contentor carregado de mobiliário, pronto a partir", S)}<figcaption>Contentor pronto a partir</figcaption></figure>
    <figure class="f" data-img style="--i:3">{img("fabrica-maquinaria", "Visita a uma fábrica de maquinaria pesada na China", S)}<figcaption>Fábrica de maquinaria pesada</figcaption></figure>
  </div>
  {vids}
</div></section>'''

def partners_html(title="Trabalham connosco"):
    li = ""
    for i, p in enumerate(PARTNERS):
        top = f'<img src="{p["logo"]}" alt="Logótipo {H.escape(p["name"])}" loading="lazy">' if p["logo"] else f'<span class="k">{i+1:02d}</span>'
        li += f'<li data-rv style="--i:{i}">{top}<div><b>{p["name"]}</b><span>{p["kind"]}</span></div></li>'
    return f'''<section class="sec"><div class="w">
  <div class="head"><div data-rv><p class="eyebrow">{title}</p><h2>Parceiros que partilham o nosso rigor.</h2></div></div>
  <ul class="partners">{li}</ul>
</div></section>'''

def cta_dark(title, text, b1=("index.html#pedido", "Pedir cotação"), b2=("sobre.html", "Conhecer a empresa")):
    return f'''<section class="sec dark"><div class="w">
  <h2 class="big" data-rv>{title}</h2>
  <p class="lead" data-rv style="--i:1;max-width:52ch">{text}</p>
  <div class="cta" data-rv style="--i:2"><a class="btn" href="{b1[0]}">{b1[1]} {ARROW}</a><a class="btn light" href="{b2[0]}">{b2[1]}</a></div>
</div></section>'''

GO = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h9M8.5 4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'

# ═════════════════════════ INÍCIO ═════════════════════════

# Fotos a deslizar no topo do Início. O Danilo vai mandar fotos do armazém, dos contentores e da Praça dos Heróis:
# quando chegarem, guardar em media/ (versões <nome>.webp 960×1280 e <nome>-480.webp) e acrescentar aqui.
HERO_SLIDES = [
    ("fabrica-aluminio", "Luís, CEO do Giquira Group, numa fábrica de alumínio na China", "Luís, CEO, numa fábrica de alumínio na China"),
    ("contentor-carregado", "Contentor carregado com mobiliário à saída de um armazém", "Contentor carregado à saída do armazém"),
    ("carregamento-empilhador", "Carregamento de um contentor com empilhador num armazém", "Carregamento no armazém"),
]
def hero_slides():
    S = "(max-width:900px) 100vw, 44vw"
    sl = "".join(f'<div class="sl{" on" if i == 0 else ""}" role="group" aria-roledescription="foto" aria-label="{i+1} de {len(HERO_SLIDES)}">'
                 f'{img(n, a, S, eager=(i == 0))}<span class="cap">{c}</span></div>' for i, (n, a, c) in enumerate(HERO_SLIDES))
    dots = "".join(f'<button type="button" aria-label="Ver foto {i+1}"{" aria-current=\"true\"" if i == 0 else ""}></button>' for i in range(len(HERO_SLIDES)))
    return f'<div class="slides" data-slides aria-roledescription="carrossel" aria-label="Fotografias do Giquira Group">{sl}<div class="sdots">{dots}</div></div>' if len(HERO_SLIDES) > 1 else sl

TRACK = ["Fábrica", "Negociação", "Produção", "Inspeção", "Embarque", "Entrega"]
home = f'''<section class="hero"><div class="w hgrid">
  <div>
    <p class="eyebrow fade" style="--d:0">Procurement · Logística · Produtos</p>
    <h1>{lines("Um grupo de família.", "Um só <em>parceiro.</em>")}</h1>
    <p class="lead fade" style="--d:.35">O Giquira Group encontra o fornecedor certo, onde quer que ele esteja, e trata do transporte até Moçambique.</p>
    <div class="cta fade" style="--d:.5"><a class="btn" href="#pedido">Pedir cotação {ARROW}</a><a class="btn o" href="#servicos">Ver os serviços</a></div>
    <ul class="facts fade" style="--d:.65"><li><b>5</b><span>Áreas de negócio</span></li><li><b>4</b><span>Países</span></li><li><b>{COMPAN["team"]}</b><span>Colaboradores</span></li></ul>
  </div>
  <figure class="shot" id="shot">
    {hero_slides()}
    <div class="track" id="track" aria-hidden="true">
      <div class="top"><span class="ref">GQ-<i>0421</i></span><span class="stt" id="trst">Em sourcing</span></div>
      <ol>{"".join(f"<li>{t}</li>" for t in TRACK)}</ol>
      <div class="prog"><b id="prog"></b></div>
    </div>
  </figure>
</div></section>

<section class="sec" id="empresa"><div class="w g2">
  <div class="sticky"><p class="eyebrow" data-rv>Quem somos</p><h2 data-rv>Uma empresa de família, feita de comércio.</h2></div>
  <div class="prose">
    <p data-rv>O Giquira Group é um grupo familiar sediado em Maputo. Nasceu da experiência da família nas áreas de produção alimentar, construção civil e produtos, construída em mercados como a África do Sul, os Emirados Árabes Unidos, a China e a Tanzânia.</p>
    <p data-rv>Hoje o grupo expandiu para mais três áreas: procurement, logística e venda de produtos eletrónicos. Atua também em consultoria e construção civil.</p>
    <p data-rv>Empresas do grupo: {", ".join(GROUP_COMPANIES[:-1])} e {GROUP_COMPANIES[-1]}.</p>
    <p data-rv>Mais do que um nome, somos uma família e uma equipa com o mesmo compromisso em cada pedido.</p>
    <ul class="chips" data-rv><li>África do Sul</li><li>Emirados Árabes Unidos</li><li>China</li><li>Tanzânia</li></ul>
    <a class="tlink" data-rv href="sobre.html" style="margin-top:28px">A nossa história {GO}</a>
  </div>
</div></section>

<section class="sec alt" id="servicos"><div class="w">
  <div class="head"><div data-rv><p class="eyebrow">O que fazemos</p><h2>Cinco áreas, <em>um só parceiro.</em></h2></div><p class="lead" data-rv style="--i:1">O procurement é o coração do grupo. A logística e a loja nasceram dele, e o grupo atua também em consultoria e construção civil.</p></div>
  <div class="svc">
    <a href="procurement.html" class="card main" data-rv><div data-img>{img("fabrica-aluminio-2", "Visita a uma fábrica de perfis de alumínio", "(max-width:760px) 100vw, 56vw")}</div><div class="t"><span class="badge">Mais procurado</span><span class="k">Serviço principal · {COMPAN["name"]}</span><h3>Procurement</h3><p>Encontramos o fornecedor certo, negociamos por si, acompanhamos a produção e entregamos em Moçambique. Um só responsável, do pedido à entrega.</p><span class="go">Ver o procurement {GO}</span></div></a>
    <a href="procurement.html#logistica" class="card" data-rv style="--i:1"><div data-img>{img("carregamento-empilhador", "Carregamento de um contentor com empilhador num armazém", "(max-width:760px) 100vw, 40vw")}</div><div class="t"><span class="k">Serviço de apoio</span><h3>Logística</h3><p>Embarque, desalfandegamento e entrega até à sua porta.</p><span class="go">Ver a logística {GO}</span></div></a>
    <a href="produtos.html" class="card solid" data-rv style="--i:2"><div class="t"><span class="k">Serviço de apoio</span><h3>Venda de produtos</h3><p>Loja física com stock de eletrónica: telemóveis, televisores, colunas, consolas e auriculares.</p><span class="go">Ver produtos {GO}</span></div></a>
  </div>
  <div class="svc2">
    <div class="card" data-rv><div class="t"><span class="k">Também atuamos em</span><h3>Consultoria</h3><p>Apoio a empresas e organizações nas suas decisões de compra e de negócio.</p><a class="go" href="{wa("Olá Giquira Group! Gostaria de saber mais sobre os vossos serviços de consultoria.")}" target="_blank" rel="noopener">Falar connosco {GO}</a></div></div>
    <div class="card" data-rv style="--i:1"><div class="t"><span class="k">Também atuamos em</span><h3>Construção civil</h3><p>Obras e projetos de construção, com materiais e equipamentos da nossa rede de fornecedores.</p><a class="go" href="{wa("Olá Giquira Group! Gostaria de saber mais sobre os vossos serviços de construção civil.")}" target="_blank" rel="noopener">Falar connosco {GO}</a></div></div>
</div>
</div></section>

<section class="sec"><div class="w g2">
  <div class="sticky"><p class="eyebrow" data-rv>Clientes</p><h2 data-rv>Para quem trabalhamos.</h2><p class="lead" data-rv style="--i:1">Quem precisa de comprar fora sem correr riscos, ou de produto em stock já em Moçambique.</p></div>
  <div class="mv">
    <div data-rv><h3>PMEs</h3><p>Equipamento, stock e reposição sem ter de viajar nem arriscar com fornecedores desconhecidos.</p></div>
    <div data-rv><h3>ONGs</h3><p>Compras com especificação clara, documentação completa e prazos cumpridos.</p></div>
    <div data-rv><h3>Particulares</h3><p>Mobiliário, eletrodomésticos e eletrónica, por encomenda ou na nossa loja.</p></div>
  </div>
</div></section>

{china_html()}

{partners_html()}

<section class="sec order" id="pedido"><div class="w g2">
  <div>
    <p class="eyebrow">Pedido de cotação</p><h2>Diga-nos o que precisa.</h2>
    <p class="lead" style="max-width:none">Leva um minuto. Abrimos o WhatsApp com o pedido já escrito para o Giquira Group.</p>
    <div class="tabs" role="group" aria-label="Como quer enviar o pedido"><span class="ind" aria-hidden="true"></span><button type="button" aria-pressed="true" data-t="lista">Tenho uma lista</button><button type="button" aria-pressed="false" data-t="link">Tenho o link</button><button type="button" aria-pressed="false" data-t="foto">Tenho uma foto</button></div>
    <form id="fm" novalidate>
      <div class="f" id="bl" hidden><label for="lk">Link do produto</label><input id="lk" placeholder="Cole aqui o link (Alibaba, 1688, site do fabricante…)" inputmode="url" autocomplete="off"></div>
      <div class="f" id="bf" hidden><label for="ph">Foto do produto</label><label class="drop" for="ph" id="dz">Toque para escolher uma foto</label><input id="ph" type="file" accept="image/*" class="sr"></div>
      <div class="f"><label for="ds" id="dsl">Descreva o que precisa</label><textarea id="ds" rows="5" placeholder="Ex.: 200 cadeiras de escritório ergonómicas, pretas, com braços. Entrega em Maputo até março."></textarea></div>
      <div class="two">
        <div class="f"><label for="qt">Quantidade total <span class="opt">(opcional)</span></label><input id="qt" type="number" min="1" placeholder="Ex.: 200" inputmode="numeric"></div>
        <div class="f"><label for="dt">Para quando?</label><select id="dt"><option value="">Sem prazo definido</option><option value="1">Até 1 mês</option><option value="2">1 a 3 meses</option><option value="3">Mais de 3 meses</option></select></div>
      </div>
      <div class="two">
        <div class="f"><label for="nm">Nome ou empresa</label><input id="nm" autocomplete="organization"></div>
        <div class="f"><label for="wp">WhatsApp ou telefone</label><input id="wp" type="tel" placeholder="+258 …" autocomplete="tel"></div>
      </div>
      <div class="f"><label for="em">Email <span class="opt">(opcional, para a proposta formal)</span></label><input id="em" type="email" autocomplete="email"></div>
      <p class="err" id="er" role="alert"></p>
      <a class="btn wa" id="send" href="{wa()}" target="_blank" rel="noopener">{WA_SVG} Enviar pedido por WhatsApp</a>
      <p class="note">Se escolheu uma foto ou tem uma lista em ficheiro, anexe-a na conversa do WhatsApp. Respondemos em até 24 horas úteis.</p>
    </form>
  </div>
  <div class="pv" aria-live="polite">
    <p class="pvlabel">O seu pedido</p><p class="pvref">GQ-<i id="ref">0000</i></p>
    <div id="tags"></div>
    <div class="pic" id="pic">A sua lista aparece aqui</div>
    <p class="pvdesc" id="pd">Comece a escrever e veja o pedido a ganhar forma.</p>
    <p class="ready" id="rd" hidden>Pedido preparado. Falta carregar em enviar no WhatsApp.</p>
  </div>
</div></section>

{cta_dark("Committed to quality. <em>Committed to you.</em>", "Um grupo de família, com experiência de comércio construída na África do Sul, nos Emirados Árabes Unidos, na China e na Tanzânia.")}
'''
page("index.html", "Giquira Group | Procurement, logística e produtos em Moçambique",
     "Grupo familiar em Maputo: procurement com a Compan Services, logística até Moçambique e loja com stock de eletrónica.", home, schema=True)

# ═════════════════════════ PROCUREMENT ═════════════════════════

INCL = ["Identificação e qualificação de fornecedores locais e internacionais", "Negociação comercial e contratação",
        "Acompanhamento da produção e inspeção pré-embarque", "Controlo de prazos e acompanhamento operacional",
        "Análise de custo total: produto, frete, taxas e entrega", "Transporte, desalfandegamento e entrega no destino"]
RISKS = [("Fornecedor que não entrega", "Visitamos e qualificamos os fornecedores antes de qualquer pagamento."),
         ("Mercadoria diferente da amostra", "Acompanhamos a produção e inspecionamos antes do embarque."),
         ("Custos escondidos", "A proposta mostra o custo total, já com transporte e taxas."),
         ("Carga parada sem responsável", "Um só interlocutor do pedido à entrega, com ponto de situação regular.")]
LOG = [("Consolidação na origem", "Juntamos a mercadoria de vários fornecedores numa só carga."),
       ("Transporte internacional", "Marítimo, aéreo ou rodoviário, conforme o volume e o prazo."),
       ("Desalfandegamento", "Documentação e desembaraço aduaneiro tratados por nós."),
       ("Armazenagem", "Receção e guarda temporária da carga, quando necessário."),
       ("Distribuição", "Transporte até ao seu armazém, loja ou escritório."),
       ("Ponto de situação", "Informação regular sobre onde está a sua carga.")]
proc = f'''<section class="pghero"><div class="w hgrid" style="align-items:end">
  <div>
    <p class="eyebrow fade" style="--d:0">Serviço principal · o mais procurado</p>
    <h1>{lines("O seu departamento", "de compras <em>lá fora.</em>")}</h1>
  </div>
  <div class="fade" style="--d:.4"><p class="lead" style="margin-top:0">Gerimos toda a cadeia de aquisição: encontramos o fornecedor certo, onde quer que esteja, negociamos, acompanhamos a produção e entregamos em Moçambique. Fala com uma só equipa; nós tratamos do resto.</p><div class="cta"><a class="btn" href="index.html#pedido">Pedir cotação {ARROW}</a><a class="btn o" href="#processo">Ver o processo</a></div></div>
</div></section>

<section class="w" style="padding-bottom:clamp(64px,9vw,120px)"><div class="duo">
  <figure data-img>{img("fabrica-aluminio-2", "Visita a uma fábrica de perfis de alumínio na China", "(max-width:700px) 55vw, 50vw")}<figcaption>Visita a uma fábrica de perfis de alumínio</figcaption></figure>
  <figure data-img style="--i:1">{img("fabrica-maquinaria", "Visita a uma fábrica de maquinaria pesada na China", "(max-width:700px) 45vw, 40vw")}<figcaption>Fábrica de maquinaria pesada</figcaption></figure>
</div></section>

<section class="sec"><div class="w g2">
  <div class="sticky"><p class="eyebrow" data-rv>Quem faz</p><h2 data-rv>{COMPAN["name"]}</h2><p class="lead" data-rv style="--i:1">A empresa do Giquira Group dedicada ao procurement.</p></div>
  <div class="prose">
    <p data-rv>A Compan Services foi criada em {COMPAN["founded"]} por representantes com muita experiência no comércio nacional e internacional, em especial na África do Sul, nos Emirados Árabes Unidos, na China e na Tanzânia.</p>
    <p data-rv>Fornece mobiliário, eletrodomésticos, equipamentos e sistemas de tecnologia da informação, peças automotivas e peças de reposição industriais a pequenas e médias empresas, ONGs e particulares.</p>
    <p data-rv>Conta com {COMPAN["team"]} colaboradores experientes e com o compromisso de um serviço de qualidade, com bons resultados e a máxima satisfação de cada cliente.</p>
    <ul class="chips" data-rv><li>África do Sul</li><li>Emirados Árabes Unidos</li><li>China</li><li>Tanzânia</li></ul>
  </div>
</div></section>

<section class="sec"><div class="w g2">
  <div class="sticky"><p class="eyebrow" data-rv>O que está incluído</p><h2 data-rv>Tudo o que uma compra internacional exige.</h2><p class="lead" data-rv style="--i:1">Não vendemos um passo isolado. Assumimos a compra inteira, e a logística vem incluída, porque uma compra só está feita quando chega.</p></div>
  <ul class="rows">{"".join(f'<li data-rv><span class="k">{i+1:02d}</span><span>{t}</span></li>' for i, t in enumerate(INCL))}</ul>
</div></section>

<section class="sec alt" id="processo"><div class="w g2">
  <div class="sticky"><p class="eyebrow" data-rv>Como funciona</p><h2 data-rv>Do pedido à sua porta.</h2><p class="lead" data-rv style="--i:1">Só compramos depois da sua confirmação. Em cada passo sabe o que está a acontecer.</p></div>
  {steps_html()}
</div></section>

<section class="sec dark"><div class="w">
  <div class="head"><div data-rv><p class="eyebrow">Porquê com o Giquira Group</p><h2>Comprar fora tem riscos. <em>O nosso trabalho é retirá-los.</em></h2></div></div>
  <div class="risk"><div class="h">O risco</div><div class="h">O que fazemos</div>
  {"".join(f'<div data-rv><h3>{r}</h3></div><div data-rv style="--i:1"><p>{a}</p></div>' for r, a in RISKS)}
  </div>
</div></section>

<section class="sec"><div class="w">
  <div class="head"><div data-rv><p class="eyebrow">Categorias</p><h2>Onde já compramos com frequência.</h2></div><p class="lead" data-rv style="--i:1">Não encontra a sua categoria? Envie a especificação e procuramos por si.</p></div>
  {cats_html()}
</div></section>

<section class="sec alt" id="logistica"><div class="w g2">
  <div class="sticky"><p class="eyebrow" data-rv>Logística incluída</p><h2 data-rv>A logística que fecha cada compra.</h2><p class="lead" data-rv style="--i:1">A nossa operação logística existe por causa do procurement. Nas compras feitas connosco já está incluída, e também aceitamos cargas que já tenha comprado por conta própria.</p>
  <figure class="portrait" data-img style="margin-top:8px">{img("contentor-carregado", "Contentor carregado com mobiliário à saída de um armazém na China", "(max-width:900px) 100vw, 40vw")}<figcaption>Contentor carregado à saída do armazém</figcaption></figure></div>
  <ul class="rows">{"".join(f'<li data-rv><span class="k">{i+1:02d}</span><span>{t}<span class="d">{d}</span></span></li>' for i, (t, d) in enumerate(LOG))}</ul>
</div></section>

{china_html()}

{cta_dark("Diga-nos o que <em>precisa de comprar.</em>", "Envie a lista ou a especificação. Respondemos com uma proposta clara, com produto, preço, prazo e entrega incluídos.", b2=("contactos.html", "Outros contactos"))}
'''
page("procurement.html", "Procurement | Giquira Group",
     "Procurement com a Compan Services, Lda: fornecedores qualificados, negociação, inspeção de qualidade e entrega em Moçambique, com logística incluída.", proc)

# ═════════════════════════ PRODUTOS ═════════════════════════

PLINES = [("telemoveis", "Telemóveis", "iPhone 17 e 18, em várias versões."), ("televisores", "Televisores", "Samsung e Xiaomi, de 43 a 85 polegadas."),
          ("ar-condicionado", "Ar condicionado", "Gree, Midea e outras marcas, de 9 000 a 36 000 BTU."),
          ("starlink", "Internet Starlink", "Kits Starlink Standard e Mini."),
          ("video", "Vídeo e microfones", "Estabilizadores DJI e microfones sem fios."),
          ("consolas", "Consolas e jogos", "Consolas portáteis e jogos para PS5."),
          ("acessorios", "Acessórios e equipamentos", "POS com impressora, localizadores GPS e mais."),
          ("colunas", "Colunas", "Colunas Bluetooth e sistemas de som."),
          ("auriculares", "Auriculares", "Com e sem fios, para o dia a dia.")]
# Cada produto de PRODUCTS deve ter "category" igual a um destes nomes (ex.: "Telemóveis") para aparecer na lista certa.

def prods_of(cat):
    return [p for p in PRODUCTS if (p.get("category") or "").strip().lower() == cat.lower()]

def product_card(p):
    vs = p["variants"]
    lo = min(v for _, v in vs)
    if p.get("image"):
        top = f'<div class="pt ph"><img src="{p["image"]}" alt="{H.escape(p["name"])}" loading="lazy" width="600" height="600"></div>'
    else:
        top = f'<div class="pt" aria-hidden="true"><span class="br">{H.escape(p["brand"])}</span><b>{H.escape(p["tag"])}</b></div>'
    if len(vs) > 1:
        price = f'<p class="from">desde <b>{mt(lo)}</b></p><ul class="var">' + "".join(
            f'<li><span>{H.escape(l)}</span><b>{mt(v)}</b></li>' for l, v in vs) + "</ul>"
    else:
        price = f'<p class="from"><b>{mt(lo)}</b></p>'
    desc = f'<p class="pd">{H.escape(p["desc"])}</p>' if p.get("desc") else ""
    msg = f'Olá Giquira Group! Tenho interesse no {p["name"]}. Está disponível?'
    return (f'<li class="pc">{top}<div class="t"><h4>{H.escape(p["name"])}</h4>{desc}{price}'
            f'<a class="btn wa sm" href="{wa(msg)}" target="_blank" rel="noopener">{WA_SVG} Fazer pedido</a></div></li>')

def carousel_html():
    """Carrossel infinito das categorias da loja. Clicar numa categoria abre a lista dessa secção logo abaixo."""
    items = "".join(
        f'<li class="it"><button type="button" class="tile" data-open="{sl}" aria-expanded="false" aria-controls="cat-{sl}">'
        f'<span class="k">{i+1:02d}{(" · " + str(n) + (" modelos" if n > 1 else " modelo")) if (n := len(prods_of(t))) else ""}</span>'
        f'<h3>{t}</h3><p>{d}</p><span class="more">Ver produtos {GO}</span></button></li>'
        for i, (sl, t, d) in enumerate(PLINES))
    L = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M10 3 5 8l5 5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    R = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="m6 3 5 5-5 5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    return f'''<div class="pcar" data-car role="region" aria-roledescription="carrossel" aria-label="Categorias da loja">
    <div class="cnav"><span class="hint">Deslize para ver todas as categorias</span><button type="button" data-prev aria-label="Categoria anterior">{L}</button><button type="button" data-next aria-label="Categoria seguinte">{R}</button></div>
    <div class="vp" tabindex="0"><ul class="tr">{items}</ul></div>
  </div>'''

def cat_panels_html():
    """Uma lista por categoria, escondida até se clicar na categoria."""
    out = ""
    for sl, t, d in PLINES:
        prods = prods_of(t)
        if prods:
            body = ('<ul class="prods">' + "".join(product_card(p) for p in prods) + "</ul>"
                    f'<p class="pnote">Preços de {PRICES_DATE}, sujeitos a alteração. Confirme o preço e a disponibilidade pelo WhatsApp antes de vir à loja.</p>')
        else:
            body = (f'<div class="empty"><p>A lista de {t.lower()} em stock vai estar aqui em breve. Até lá, pergunte-nos o que temos neste momento.</p>'
                    f'<a class="btn wa" href="{wa("Olá Giquira Group! Que " + t.lower() + " têm em stock?")}" target="_blank" rel="noopener">{WA_SVG} Perguntar por {t.lower()}</a></div>')
        out += (f'<div class="cpanel" id="cat-{sl}" hidden tabindex="-1" aria-label="{t}">'
                f'<div class="cph"><div><p class="eyebrow">Na loja</p><h3>{t}</h3></div>'
                f'<button type="button" class="cclose" data-close aria-label="Fechar a lista de {t.lower()}">Fechar ✕</button></div>{body}</div>')
    return f'<div class="cpanels" id="lista">{out}</div>'

prod = f'''<section class="pghero"><div class="w">
  <p class="eyebrow fade" style="--d:0">Serviço de apoio · Produtos</p>
  <h1>{lines("Loja com stock,", "<em>pronta a levar.</em>")}</h1>
  <p class="lead fade" style="--d:.4;max-width:52ch">Temos loja física com stock de eletrónica e climatização: telemóveis, televisores, ar condicionado, Starlink, equipamento de vídeo e microfones, consolas e jogos, e acessórios. Vendemos a particulares e a revendedores, com a mesma rede de fornecedores que usamos no procurement.</p>
  <div class="cta fade" style="--d:.55"><a class="btn wa" href="{wa("Olá Giquira Group! Que produtos têm disponíveis?")}" target="_blank" rel="noopener">{WA_SVG} Ver disponibilidade</a><a class="btn o" href="#loja">Onde fica a loja</a></div>
</div></section>

<section class="sec"><div class="w">
  <div class="head"><div data-rv><p class="eyebrow">Na loja</p><h2>O que temos em stock.</h2></div><p class="lead" data-rv style="--i:1">Toque numa categoria para ver os produtos dessa secção.</p></div>
  {carousel_html()}
  {cat_panels_html()}
</div></section>

<section class="sec alt" id="loja"><div class="w g2">
  <div class="sticky"><p class="eyebrow" data-rv>A loja</p><h2 data-rv>Venha ver o stock.</h2><p class="lead" data-rv style="--i:1">Fica ao lado do nosso escritório, na {CONTACT["address_1"]}, antes da Alof Palm, em Maputo. Antes de vir, confirme pelo WhatsApp se o produto que procura está disponível.</p>
    <div class="cta" data-rv style="--i:2"><a class="btn" href="{store_maps()}" target="_blank" rel="noopener">Abrir no Google Maps {ARROW}</a><a class="btn wa" href="{wa("Olá Giquira Group! Gostaria de saber se têm este produto na loja.")}" target="_blank" rel="noopener">{WA_SVG} Confirmar stock</a></div></div>
  <div class="map" data-rv style="margin-top:0">{store_iframe("Mapa da loja do Giquira Group em Maputo")}</div>
</div></section>

{cta_dark("Não está aqui? <em>Encontramos.</em>", "É para isso que existe o nosso procurement. Diga-nos o que procura e compramos na origem.", b2=("procurement.html", "Ver procurement"))}
'''
page("produtos.html", "Produtos | Giquira Group",
     "Loja Giquira Group em Maputo: iPhone, televisores Samsung e Xiaomi, ar condicionado e mais, com preços.", prod)

# ═════════════════════════ SOBRE ═════════════════════════

sobre = f'''<section class="pghero"><div class="w">
  <p class="eyebrow fade" style="--d:0">Sobre nós</p>
  <h1>{lines("Uma família feita", "de <em>comércio.</em>")}</h1>
  <ul class="facts fade" style="--d:.45"><li><b>2021</b><span>Compan Services</span></li><li><b>4</b><span>Países</span></li><li><b>{len(PARTNERS)}</b><span>Parceiros</span></li><li><b>{COMPAN["team"]}</b><span>Colaboradores</span></li></ul>
</div></section>

<section class="sec"><div class="w g2">
  <figure class="portrait sticky" data-img>{img("contentor-carregado", "Contentor carregado com mobiliário à saída de um armazém", "(max-width:900px) 100vw, 42vw")}<figcaption>Uma compra pronta a partir</figcaption></figure>
  <div class="prose">
    <p class="eyebrow" data-rv>A nossa história</p>
    <h2 data-rv>Experiência construída nos mercados de onde as coisas vêm.</h2>
    <p data-rv>O Giquira Group é uma empresa de família sediada em Maputo. Nasceu da experiência da família nas áreas de produção alimentar, construção civil e produtos, construída em mercados como a África do Sul, os Emirados Árabes Unidos, a China e a Tanzânia. Dessa vivência nasceu a convicção de que qualidade e proximidade não são opostas: são as duas faces da mesma moeda.</p>
    <p data-rv>Em {COMPAN["founded"]} nasceu a {COMPAN["name"]}, o ramo do grupo que faz o procurement: compramos material industrial, equipamentos de construção, mobiliário para escritórios e residências, equipamento de segurança e proteção individual, energias renováveis e material hospitalar para pequenas e médias empresas, ONGs e particulares.</p>
    <p data-rv>Hoje o grupo expandiu para mais três áreas: procurement, logística e venda de produtos eletrónicos, e atua também em consultoria e construção civil. À volta do procurement cresceram a logística, que leva cada compra até ao destino, e a loja, com stock de eletrónica pronto a vender.</p>
    <p data-rv>Empresas do grupo: {", ".join(GROUP_COMPANIES[:-1])} e {GROUP_COMPANIES[-1]}.</p>
    <p data-rv>Somos uma equipa de {COMPAN["team"]} colaboradores, orientada por processos e guiada por pessoas.</p>
    <ul class="chips" data-rv><li>África do Sul</li><li>Emirados Árabes Unidos</li><li>China</li><li>Tanzânia</li></ul>
    <p class="quote" data-rv>{BRAND["slogan"]}</p>
  </div>
</div></section>

<section class="sec alt"><div class="w g2">
  <div class="sticky"><p class="eyebrow" data-rv>O que nos orienta</p><h2 data-rv>Missão, visão e valores.</h2></div>
  <div class="mv">
    <div data-rv><h3>Missão</h3><p>Atender com excelência, agilidade e responsabilidade, desenvolvendo talentos e soluções eficazes.</p></div>
    <div data-rv><h3>Visão</h3><p>Ser referência em consultoria, vendas e gestão de negócios, contribuindo para o crescimento dos clientes.</p></div>
    <div data-rv><h3>Valores</h3><p>Ética, compromisso com o cliente, transparência, responsabilidade, valorização das pessoas e soluções criativas.</p></div>
  </div>
</div></section>

{partners_html("Parceiros")}

{cta_dark("Trabalhemos <em>juntos.</em>", "Diga-nos o que precisa de comprar e desenhamos a solução consigo, da origem à entrega.", b2=("contactos.html", "Contactos"))}
'''
page("sobre.html", "Sobre nós | Giquira Group",
     "A história, missão e valores do Giquira Group: empresa de família em Maputo, com procurement, logística e venda de produtos.", sobre)

# ═════════════════════════ CONTACTOS ═════════════════════════

cont = f'''<section class="pghero"><div class="w">
  <p class="eyebrow fade" style="--d:0">Contactos</p>
  <h1>{lines("Fale <em>connosco.</em>")}</h1>
  <p class="lead fade" style="--d:.35">Para pedir uma cotação, o mais rápido é o <a class="tlink" href="index.html#pedido">formulário de pedido</a>. Para tudo o resto, estamos aqui.</p>
</div></section>

<section class="sec" style="padding-top:0;border-top:0"><div class="w g2">
  <div data-rv>
    <dl class="ct">
      <dt>WhatsApp e telefone</dt><dd><a href="{wa(num=CONTACT["wa_main"])}" target="_blank" rel="noopener">{CONTACT["wa_main_label"]}</a><br><a href="{wa(num=CONTACT["wa_alt"])}" target="_blank" rel="noopener">{CONTACT["wa_alt_label"]}</a></dd>
      <dt>Email</dt><dd><a href="mailto:{CONTACT["email"]}">{CONTACT["email"]}</a></dd>
      <dt>Instagram</dt><dd><a href="https://instagram.com/{CONTACT["instagram"]}" target="_blank" rel="noopener">@{CONTACT["instagram"]}</a></dd>
      <dt>Escritório e loja</dt><dd>{CONTACT["address_1"]}<br>{CONTACT["address_2"]}<br><a href="{store_maps()}" target="_blank" rel="noopener">Abrir no Google Maps</a></dd>
    </dl>
    <div class="map">{store_iframe("Mapa do escritório e da loja do Giquira Group em Maputo")}</div>
  </div>
  <div class="boxed" data-rv style="--i:1">
    <p class="eyebrow">Mensagem rápida</p>
    <h2 style="font-size:clamp(28px,3vw,40px)">Escreva-nos.</h2>
    <form id="cf" novalidate>
      <div class="f"><label for="cn">O seu nome</label><input id="cn" autocomplete="name"></div>
      <div class="f"><label for="cm">Mensagem</label><textarea id="cm" rows="5" placeholder="Como podemos ajudar?"></textarea></div>
      <a class="btn wa" id="cwa" href="{wa()}" target="_blank" rel="noopener">{WA_SVG} Enviar por WhatsApp</a>
    </form>
  </div>
</div></section>
'''
page("contactos.html", "Contactos | Giquira Group",
     "Fale com o Giquira Group: WhatsApp +258 84 426 6127, geral@giquiragroup.com, Av. Emília Dause, Maputo.", cont)

# ═════════════════════════ FICHEIROS DE APOIO ═════════════════════════

B = BASE_PATH if BASE_PATH.endswith("/") else BASE_PATH + "/"
with open(os.path.join(OUT, "404.html"), "w") as f:
    f.write(f'''<!doctype html><html lang="pt-MZ"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Página não encontrada | Giquira Group</title><meta name="robots" content="noindex"><base href="{B}"><link rel="icon" href="favicon.png">
<link rel="stylesheet" href="assets/site.css?v={CSS_V}"></head><body><main class="w pghero" style="min-height:80vh;display:grid;align-content:center">
<p class="eyebrow">Erro 404</p><h1>Esta página <em>não existe.</em></h1><p class="lead" style="margin-top:24px">O endereço pode estar errado ou a página foi movida.</p>
<div class="cta"><a class="btn" href="index.html">Voltar ao início</a><a class="btn o" href="contactos.html">Contactos</a></div></main></body></html>
''')

if SITE_URL:
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
                "".join(f'  <url><loc>{url("" if p == "index.html" else p)}</loc></url>\n' for p, _ in NAV) + "</urlset>\n")
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {url('sitemap.xml')}\n")
    host = SITE_URL.split("://", 1)[-1].strip("/")
    with open(os.path.join(OUT, "CNAME"), "w") as f:
        f.write(host + "\n")
else:
    for n in ("sitemap.xml", "CNAME"):
        p = os.path.join(OUT, n)
        if os.path.exists(p): os.remove(p)
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write("User-agent: *\nAllow: /\n")
print("ok · domínio:", SITE_URL or "por ligar", "· base:", BASE_PATH, "· logótipo:", BRAND["logo"] or "por receber", "· produtos:", len(PRODUCTS))
