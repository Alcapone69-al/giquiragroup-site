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
    "tagline": "Procurement · China → Moçambique",
    "slogan": "Committed to quality. Committed to you.",
    "logo": None, "logo_light": None,
}

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
    {"name": "EDM", "kind": "Empresa pública", "logo": "media/logos/edm.webp"},
]

# Galeria de produtos — preparada, ainda vazia (não inventar produtos).
# Cada produto: {"name": "...", "desc": "...", "price": None ou "1 500 MT", "category": None ou "Áudio",
#                "image": "media/produtos/xxx.webp", "alt": "..."}
PRODUCTS = []

NAV = [("index.html", "Início"), ("procurement.html", "Procurement"), ("produtos.html", "Produtos"),
       ("sobre.html", "Sobre nós"), ("contactos.html", "Contactos")]

# ═════════════════════════ AUXILIARES ═════════════════════════

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
        return (f'<a class="brand has-logo" href="index.html"><img src="{logo}" alt="" height="40">'
                f'<span class="bx"><span class="bn">{BRAND["name"]} {BRAND["name_2"]}</span></span></a>')
    return (f'<a class="brand" href="index.html" aria-label="{BRAND["name"]} {BRAND["name_2"]}, página inicial"><span class="bx">'
            f'<span class="bn">{BRAND["name"]} <span>{BRAND["name_2"]}</span></span>'
            f'<span class="bt">{BRAND["tagline"] if not dark else BRAND["slogan"]}</span></span></a>')

def url(path=""):
    return (SITE_URL.rstrip("/") + "/" + path) if SITE_URL else None

# ═════════════════════════ MOLDE DA PÁGINA ═════════════════════════

def page(fname, title, desc, body, schema=False):
    AC = ' aria-current="page"'
    nav = "".join(f'<a href="{h}"{AC if h == fname else ""}>{t}</a>' for h, t in NAV)
    mnav = "".join(f'<a href="{h}"{AC if h == fname else ""} style="--i:{i}">{t}<small>0{i+1}</small></a>' for i, (h, t) in enumerate(NAV))
    canon = url("" if fname == "index.html" else fname)
    meta_url = f'<link rel="canonical" href="{canon}">\n<meta property="og:url" content="{canon}">\n' if canon else ""
    og_img = f'<meta property="og:image" content="{url("media/og-giquira.jpg")}">\n' if SITE_URL and os.path.exists(os.path.join(OUT, "media/og-giquira.jpg")) else ""
    ld = ""
    if schema:
        org = {"@context": "https://schema.org", "@type": "Organization", "name": "Giquira Group",
               "slogan": BRAND["slogan"], "foundingDate": "2021", "email": CONTACT["email"],
               "description": "Procurement internacional: compramos na China e entregamos em Moçambique, com logística incluída.",
               "telephone": ["+" + CONTACT["wa_main"], "+" + CONTACT["wa_alt"]],
               "address": {"@type": "PostalAddress", "streetAddress": CONTACT["address_1"], "addressLocality": "Maputo", "addressCountry": "MZ"},
               "areaServed": {"@type": "Country", "name": "Moçambique"},
               "sameAs": [f"https://instagram.com/{CONTACT['instagram']}"]}
        if SITE_URL: org["url"] = url()
        if SITE_URL and BRAND["logo"]: org["logo"] = url(BRAND["logo"])
        ld = f'<script type="application/ld+json">{json.dumps(org, ensure_ascii=False)}</script>\n'
    labels = json.dumps({h: t for h, t in NAV}, ensure_ascii=False)
    wl = f'<img class="wl" src="{BRAND["logo_light"] or BRAND["logo"]}" alt="">' if (BRAND["logo_light"] or BRAND["logo"]) else ""
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
<link rel="preload" href="assets/fonts/schibsted-grotesk-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/instrument-sans-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/site.css">
<script>(function(d){{d.className+=' js';try{{if(sessionStorage.getItem('wp'))d.className+=' wp';else d.className+=' first'}}catch(e){{d.className+=' first'}}}})(document.documentElement)</script>
{ld}</head>
<body data-wa="{CONTACT["wa_main"]}">
<div class="bar" id="bar" aria-hidden="true"></div>
<div class="wipe" id="wipe" aria-hidden="true" data-labels='{labels}'><div class="wc">{wl}<div class="wn"><span>{BRAND["name"]} <em>{BRAND["name_2"]}</em></span></div><div class="wd" id="wd"></div></div></div>
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
    <p style="margin:20px 0 0;max-width:36ch">Procurement internacional para empresas, ONGs, instituições e particulares em Moçambique.</p>
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
<script src="assets/site.js" defer></script>
</body>
</html>
'''
    with open(os.path.join(OUT, fname), "w") as f:
        f.write(html)

def lines(*parts, start=0):
    """Título revelado linha a linha."""
    return "".join(f'<span class="ln" style="--i:{start+i}"><span>{p}</span></span>' for i, p in enumerate(parts))

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

CATS = [("Mobiliário", "Escritório, hotelaria, escolas e residências."),
        ("Eletrodomésticos", "Linha branca e equipamento de cozinha."),
        ("Equipamento de TI", "Computadores, redes, sistemas e periféricos."),
        ("Peças automotivas", "Peças e acessórios para frotas e oficinas."),
        ("Peças industriais", "Peças de reposição e equipamento industrial."),
        ("Acessórios de tecnologia", "Áudio, carregadores, wearables e gadgets.")]
def cats_html():
    return '<ul class="cats">' + "".join(
        f'<li data-rv style="--i:{i%3}"><span class="k">{i+1:02d}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(CATS)) + "</ul>"

VIDEOS = [("visita-fabrica", "Visita a uma fábrica parceira", "45 s"),
          ("processo-aluminio", "Tratamento de perfis de alumínio", "46 s"),
          ("linha-extrusao", "Linha de extrusão", "14 s")]
def china_html(videos=True):
    vids = ""
    if videos:
        vids = '<div class="vids">' + "".join(
            f'<figure class="vid" data-rv style="--i:{i}"><video src="media/{n}.mp4" poster="media/{n}-poster.webp" playsinline preload="none" aria-label="{l}"></video>'
            f'<button class="play" type="button" aria-label="Ver vídeo: {l}"><span class="pb">{PLAY}</span><span>{l}<small>{d}</small></span></button></figure>'
            for i, (n, l, d) in enumerate(VIDEOS)) + "</div>"
    S = "(max-width:760px) 50vw, 33vw"
    return f'''<section class="sec dark" id="china"><div class="w">
  <div class="head">
    <div data-rv><p class="eyebrow">No terreno, na China</p><h2>Não compramos por catálogo. <em>Vamos à fábrica.</em></h2></div>
    <p class="lead" data-rv style="--i:1">O nosso CEO, Danilo, acompanha pessoalmente fornecedores e fábricas na China: das reuniões de negociação à linha de produção e ao contentor pronto a partir. É assim que a qualidade prometida passa a ser a qualidade entregue.</p>
  </div>
  <div class="mosaic">
    <figure class="a" data-img>{img("fabrica-maquinaria", "Danilo com um parceiro numa fábrica de maquinaria pesada na China", "(max-width:760px) 100vw, 42vw")}<figcaption>Visita a fábrica de maquinaria pesada</figcaption></figure>
    <figure class="b" data-img style="--i:1">{img("reuniao-cha", "Danilo em reunião com uma fornecedora na China", S)}<figcaption>Reunião com fornecedora</figcaption></figure>
    <figure class="c" data-img style="--i:2">{img("reuniao-escritorio", "Danilo em reunião num escritório na China", S)}<figcaption>Negociação</figcaption></figure>
    <figure class="d" data-img style="--i:1">{img("jantar-parceiros", "Danilo num jantar com parceiros comerciais na China", S)}<figcaption>Com parceiros</figcaption></figure>
    <figure class="e" data-img style="--i:2">{img("contentor-danilo", "Danilo em frente a um contentor carregado de mobiliário", S)}<figcaption>Contentor pronto a partir</figcaption></figure>
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

TRACK = ["Fábrica", "Negociação", "Produção", "Inspeção", "Embarque", "Entrega"]
home = f'''<section class="hero"><div class="w hgrid">
  <div>
    <p class="eyebrow fade" style="--d:0">Procurement internacional, desde 2021</p>
    <h1>{lines("Compramos na <em>origem.</em>", "Entregamos em Moçambique.")}</h1>
    <p class="lead fade" style="--d:.35">Encontramos o fornecedor certo na China, negociamos por si, acompanhamos a produção na fábrica e tratamos do transporte até à sua porta. Um só parceiro, do pedido à entrega.</p>
    <div class="cta fade" style="--d:.5"><a class="btn" href="#pedido">Pedir cotação {ARROW}</a><a class="btn o" href="#como">Ver como funciona</a></div>
    <ul class="facts fade" style="--d:.65"><li><b>4</b><span>Países</span></li><li><b>5</b><span>Parceiros</span></li><li><b>8</b><span>Colaboradores</span></li></ul>
  </div>
  <figure class="shot" id="shot">
    {img("fabrica-aluminio", "Danilo, CEO do Giquira Group, com parceiros numa fábrica de perfis de alumínio na China", "(max-width:900px) 100vw, 44vw", eager=True)}
    <figcaption>Danilo, CEO, numa fábrica parceira</figcaption>
    <div class="track" id="track" aria-hidden="true">
      <div class="top"><span class="ref">GQ-<i>0421</i></span><span class="stt" id="trst">Em sourcing</span></div>
      <ol>{"".join(f"<li>{t}</li>" for t in TRACK)}</ol>
      <div class="prog"><b id="prog"></b></div>
    </div>
  </figure>
</div></section>

<section class="sec" id="como"><div class="w g2">
  <div class="sticky"><p class="eyebrow" data-rv>Como funciona</p><h2 data-rv>Do pedido à sua porta.</h2><p class="lead" data-rv style="--i:1">Seis passos e um só responsável. A logística existe para fechar o ciclo: garantir que o que compramos chega inteiro, documentado e no prazo.</p><a class="tlink" data-rv style="--i:2" href="procurement.html">O serviço em detalhe {GO}</a></div>
  {steps_html()}
</div></section>

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

{china_html()}

<section class="sec"><div class="w g2">
  <div class="sticky"><p class="eyebrow" data-rv>Para quem trabalhamos</p><h2 data-rv>Quem precisa de comprar fora, sem correr riscos.</h2></div>
  <div class="mv">
    <div data-rv><h3>PMEs</h3><p>Equipamento, stock e reposição sem ter de viajar nem arriscar com fornecedores desconhecidos.</p></div>
    <div data-rv><h3>ONGs</h3><p>Compras com especificação clara, documentação completa e prazos cumpridos.</p></div>
    <div data-rv><h3>Instituições</h3><p>Processos transparentes e rastreáveis, do pedido à entrega.</p></div>
    <div data-rv><h3>Particulares</h3><p>Mobiliário, eletrodomésticos e equipamentos trazidos diretamente da origem.</p></div>
  </div>
</div></section>

<section class="sec alt"><div class="w">
  <div class="head"><div data-rv><p class="eyebrow">Além do procurement</p><h2>Dois serviços que nasceram das nossas compras.</h2></div></div>
  <div class="pair">
    <a href="procurement.html#logistica" class="card" data-rv><div data-img>{img("carregamento-empilhador", "Carregamento de um contentor com empilhador num armazém na China", "(max-width:760px) 100vw, 50vw")}</div><div class="t"><span class="k">Serviço de apoio</span><h3>Logística</h3><p>Embarque, desalfandegamento e entrega: a mesma operação que usamos nas nossas compras.</p><span class="go">Ver a logística {GO}</span></div></a>
    <a href="produtos.html" class="card solid" data-rv style="--i:1"><div class="t"><span class="k">Serviço de apoio</span><h3>Produtos em stock</h3><p>Acessórios de tecnologia e produtos selecionados, prontos a vender em Moçambique.</p><span class="go">Ver produtos {GO}</span></div></a>
  </div>
</div></section>

{partners_html()}

{cta_dark("Committed to quality. <em>Committed to you.</em>", "Desde 2021, com experiência de comércio construída na África do Sul, nos Emirados Árabes Unidos, na China e na Tanzânia.")}
'''
page("index.html", "Giquira Group | Procurement na China para Moçambique",
     "Encontramos fornecedores, negociamos e acompanhamos a produção na China, e entregamos em Moçambique. Procurement com logística incluída.", home, schema=True)

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
    <p class="eyebrow fade" style="--d:0">Serviço principal</p>
    <h1>{lines("O seu departamento", "de compras <em>na China.</em>")}</h1>
  </div>
  <div class="fade" style="--d:.4"><p class="lead" style="margin-top:0">Gerimos toda a cadeia de aquisição, da procura do fornecedor à entrega final em Moçambique, com foco em qualidade, custo total e prazo. Fala com uma só equipa; nós tratamos do resto.</p><div class="cta"><a class="btn" href="index.html#pedido">Pedir cotação {ARROW}</a><a class="btn o" href="#processo">Ver o processo</a></div></div>
</div></section>

<section class="w" style="padding-bottom:clamp(64px,9vw,120px)"><div class="duo">
  <figure data-img>{img("fabrica-aluminio-2", "Danilo com parceiros numa fábrica de perfis de alumínio na China", "(max-width:700px) 55vw, 50vw")}<figcaption>Visita a uma fábrica de perfis de alumínio</figcaption></figure>
  <figure data-img style="--i:1">{img("fabrica-maquinaria", "Danilo com um parceiro numa fábrica de maquinaria pesada na China", "(max-width:700px) 45vw, 40vw")}<figcaption>Fábrica de maquinaria pesada</figcaption></figure>
</div></section>

<section class="sec"><div class="w g2">
  <div class="sticky"><p class="eyebrow" data-rv>O que está incluído</p><h2 data-rv>Tudo o que uma compra internacional exige.</h2><p class="lead" data-rv style="--i:1">Não vendemos um passo isolado. Assumimos a compra inteira, e a logística vem incluída, porque uma compra só está feita quando chega.</p></div>
  <ul class="rows">{"".join(f'<li data-rv><span class="k">{i+1:02d}</span><span>{t}</span></li>' for i, t in enumerate(INCL))}</ul>
</div></section>

<section class="sec alt" id="processo"><div class="w g2">
  <div class="sticky"><p class="eyebrow" data-rv>O processo</p><h2 data-rv>Da especificação à entrega.</h2><p class="lead" data-rv style="--i:1">Só compramos depois da sua confirmação. Em cada passo sabe o que está a acontecer.</p></div>
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

{china_html(videos=False)}

{cta_dark("Diga-nos o que <em>precisa de comprar.</em>", "Envie a lista ou a especificação. Respondemos com uma proposta clara, com produto, preço, prazo e entrega incluídos.", b2=("contactos.html", "Outros contactos"))}
'''
page("procurement.html", "Procurement | Giquira Group",
     "Sourcing de fornecedores na China, negociação, inspeção de qualidade e entrega em Moçambique, com logística incluída.", proc)

# ═════════════════════════ PRODUTOS ═════════════════════════

PLINES = [("Acessórios para smartphones", "Capas, cabos e carregadores."), ("Áudio", "Auriculares, colunas Bluetooth e headphones."),
          ("Wearables", "Smartwatches e acessórios."), ("Periféricos e gadgets", "Para escritório e uso pessoal."),
          ("Produtos de consumo", "Seleção que vai mudando."), ("Revenda B2B", "Condições para lojas e distribuidores.")]

def gallery_html():
    """Galeria de produtos. Só é gerada quando PRODUCTS tiver itens."""
    if not PRODUCTS:
        return ""
    items = ""
    for i, p in enumerate(PRODUCTS):
        price = f'<p><b>{H.escape(p["price"])}</b></p>' if p.get("price") else ""
        cat = f' data-cat="{H.escape(p["category"])}"' if p.get("category") else ""
        items += (f'<li data-rv style="--i:{i%4}"{cat}><div class="ph"><img src="{p["image"]}" alt="{H.escape(p.get("alt") or p["name"])}" loading="lazy"></div>'
                  f'<div class="t"><h3>{H.escape(p["name"])}</h3>{"<p>" + H.escape(p["desc"]) + "</p>" if p.get("desc") else ""}{price}</div></li>')
    return f'''<section class="sec alt" id="galeria"><div class="w">
  <div class="head"><div data-rv><p class="eyebrow">Galeria</p><h2>Alguns dos nossos produtos.</h2></div></div>
  <ul class="gal">{items}</ul>
</div></section>'''

prod = f'''<section class="pghero"><div class="w">
  <p class="eyebrow fade" style="--d:0">Serviço de apoio · Produtos</p>
  <h1>{lines("Produtos escolhidos", "<em>na origem.</em>")}</h1>
  <p class="lead fade" style="--d:.4;max-width:52ch">Com a mesma rede de fornecedores que usamos no procurement, importamos uma seleção de produtos, com destaque para acessórios de tecnologia, que vendemos em Moçambique a particulares e a revendedores.</p>
  <div class="cta fade" style="--d:.55"><a class="btn wa" href="{wa("Olá Giquira Group! Que produtos têm disponíveis?")}" target="_blank" rel="noopener">{WA_SVG} Ver disponibilidade</a><a class="btn o" href="procurement.html">Procura outra coisa?</a></div>
</div></section>

<section class="sec"><div class="w">
  <div class="head"><div data-rv><p class="eyebrow">Linhas de produto</p><h2>O que costumamos ter.</h2></div><p class="lead" data-rv style="--i:1">O stock muda com frequência. Peça a lista atualizada pelo WhatsApp.</p></div>
  <ul class="cats">{"".join(f'<li data-rv style="--i:{i%3}"><span class="k">{i+1:02d}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(PLINES))}</ul>
</div></section>

{gallery_html()}

{cta_dark("Não está aqui? <em>Encontramos.</em>", "É para isso que existe o nosso procurement. Diga-nos o que procura e compramos na origem.", b2=("procurement.html", "Ver procurement"))}
'''
page("produtos.html", "Produtos | Giquira Group",
     "Acessórios de tecnologia e produtos selecionados, importados pelo Giquira Group e disponíveis em Moçambique.", prod)

# ═════════════════════════ SOBRE ═════════════════════════

sobre = f'''<section class="pghero"><div class="w">
  <p class="eyebrow fade" style="--d:0">Sobre nós</p>
  <h1>{lines("Nascemos do comércio", "<em>internacional.</em>")}</h1>
  <ul class="facts fade" style="--d:.45"><li><b>2021</b><span>Fundação</span></li><li><b>4</b><span>Países</span></li><li><b>5</b><span>Parceiros</span></li><li><b>8</b><span>Colaboradores</span></li></ul>
</div></section>

<section class="sec"><div class="w g2">
  <figure class="portrait sticky" data-img>{img("contentor-danilo", "Danilo, CEO do Giquira Group, em frente a um contentor carregado na China", "(max-width:900px) 100vw, 42vw")}<figcaption>Danilo, fundador e CEO</figcaption></figure>
  <div class="prose">
    <p class="eyebrow" data-rv>A nossa história</p>
    <h2 data-rv>Experiência construída nos mercados de onde as coisas vêm.</h2>
    <p data-rv>O Giquira Group foi fundado em 2021 com base em experiência profissional em comércio nacional e internacional, construída em mercados como a África do Sul, os Emirados Árabes Unidos, a China e a Tanzânia. Dessa vivência nasceu a convicção de que qualidade e proximidade não são opostas: são as duas faces da mesma moeda.</p>
    <p data-rv>Hoje o nosso centro é o procurement: compramos mobiliário, eletrodomésticos, equipamentos e sistemas de TI, peças automotivas e peças de reposição industriais para pequenas e médias empresas, ONGs, instituições públicas e particulares.</p>
    <p data-rv>Somos uma equipa de 8 colaboradores, orientada por processos e guiada por pessoas.</p>
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

{china_html()}

{partners_html("Parceiros")}

{cta_dark("Trabalhemos <em>juntos.</em>", "Diga-nos o que precisa de comprar e desenhamos a solução consigo, da origem à entrega.", b2=("contactos.html", "Contactos"))}
'''
page("sobre.html", "Sobre nós | Giquira Group",
     "A história, missão e valores do Giquira Group: procurement internacional sediado em Maputo, com presença na China.", sobre)

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
      <dt>Escritório</dt><dd>{CONTACT["address_1"]}<br>{CONTACT["address_2"]}</dd>
    </dl>
    <div class="map"><iframe title="Mapa do escritório do Giquira Group em Maputo" loading="lazy" src="https://www.openstreetmap.org/export/embed.html?bbox=32.5750%2C-25.9700%2C32.6150%2C-25.9450&amp;layer=mapnik&amp;marker=-25.9575%2C32.5950"></iframe></div>
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
<link rel="stylesheet" href="assets/site.css"></head><body><main class="w pghero" style="min-height:80vh;display:grid;align-content:center">
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
