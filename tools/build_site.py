#!/usr/bin/env python3
"""Gera as páginas HTML do site Giquira Group (mesmo método do site DA-KA)."""
import json, os

OUT = "/home/claude/giquira-site"
DOMAIN = "https://giquiragroup.com"   # trocar se o domínio for outro
WA = "258844266127"
WA_TXT = "Ol%C3%A1%20Giquira%20Group!%20Gostaria%20de%20falar%20com%20a%20vossa%20equipa."

NAV = [("index.html", "Início"), ("procurement.html", "Procurement"), ("produtos.html", "Produtos"),
       ("sobre.html", "Sobre nós"), ("contactos.html", "Contactos")]

def ph(src, alt, label=None, cls="", eager=False):
    lab = label or src.split("/")[-1]
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<div class="ph {cls}" data-label="Foto: {lab}"><img src="{src}" alt="{alt}" {load} decoding="async"></div>'

WA_SVG = '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" focusable="false"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1-.7-.3-1.5-.8-2.1-1.4-.6-.6-1-1.2-1.4-1.9-.1-.2 0-.4.1-.5l.4-.5.2-.4c.1-.2 0-.3 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.5.1-.7.3-.7.7-1 1.6-.9 2.5.2 1 .7 1.9 1.3 2.7 1.3 1.7 2.9 2.9 4.9 3.5.9.3 1.7.2 2.3-.1.7-.4 1.1-1 1.3-1.7.1-.3 0-.5-.1-.6z"/></svg>'

ORG = {
    "@context": "https://schema.org", "@type": "Organization",
    "name": "Giquira Group", "url": DOMAIN + "/", "logo": DOMAIN + "/media/giquira-logo.png",
    "slogan": "Committed to quality. Committed to you.",
    "description": "Procurement internacional: compramos na China e noutros mercados e entregamos em Moçambique, com logística integrada.",
    "foundingDate": "2021", "email": "geral@giquiragroup.com",
    "telephone": ["+258844266127", "+258874266125"],
    "address": {"@type": "PostalAddress", "streetAddress": "Av. Emília Dause, N.º 948, R/C", "addressLocality": "Maputo", "addressCountry": "MZ"},
    "areaServed": {"@type": "Country", "name": "Moçambique"},
    "employee": [{"@type": "Person", "name": "Danilo", "jobTitle": "CEO"}],
    "sameAs": ["https://instagram.com/giquira_group"],
    "knowsAbout": ["Procurement", "Sourcing na China", "Importação", "Logística", "Desalfandegamento"],
}

def page(fname, title, desc, body, schema=False):
    cur = fname
    AC = ' aria-current="page"'
    nav = "\n      ".join(f'<a href="{h}"{AC if h == cur else ""}>{t}</a>' for h, t in NAV)
    mnav = "".join(f'<a href="{h}"{AC if h == cur else ""}>{t}</a>' for h, t in NAV)
    canon = DOMAIN + "/" + ("" if fname == "index.html" else fname)
    ld = f'<script type="application/ld+json">{json.dumps(ORG, ensure_ascii=False)}</script>\n' if schema else ""
    html = f'''<!doctype html>
<html lang="pt-MZ">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#3A7D2A">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Giquira Group">
<meta property="og:locale" content="pt_MZ">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{DOMAIN}/media/og-giquira.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.png" type="image/png">
<link rel="apple-touch-icon" href="favicon.png">
<link rel="preload" href="assets/fonts/big-shoulders-display-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/archivo-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/site.css">
<script>try{{if(sessionStorage.getItem('wp')){{document.documentElement.className='wp'}}}}catch(e){{}}</script>
{ld}</head>
<body>
<div class="bar" id="bar"></div>
<div class="wipe" id="wipe" aria-hidden="true">Giquira</div>
<a class="skip" href="#conteudo">Saltar para o conteúdo</a>

<header>
  <div class="w hbar">
    <a class="wm" href="index.html" aria-label="Giquira Group, página inicial"><img src="media/giquira-logo.png" alt="" width="42" height="42"><span><b>Giquira <i>Group</i></b><small>Procurement · China → Moçambique</small></span></a>
    <nav aria-label="Principal">
      {nav}
    </nav>
    <a class="btn" href="index.html#pedido">Pedir cotação</a>
  </div>
  <nav class="mnav" aria-label="Principal, telemóvel">{mnav}</nav>
</header>

<main id="conteudo" tabindex="-1">
{body}
</main>

<footer><div class="w fw">
  <div>
    <a class="wm" href="index.html"><img src="media/giquira-logo.png" alt="" width="42" height="42"><span><b>Giquira Group</b><small>Committed to quality. Committed to you.</small></span></a>
    <p style="margin:18px 0 0;max-width:36ch">Procurement internacional para empresas, ONGs, instituições e particulares em Moçambique.</p>
  </div>
  <div><h4>Páginas</h4><ul>{"".join(f'<li><a href="{h}">{t}</a></li>' for h, t in NAV)}</ul></div>
  <div><h4>Contacto</h4><ul>
    <li><a href="https://wa.me/258844266127" target="_blank" rel="noopener">+258 84 426 6127</a></li>
    <li><a href="https://wa.me/258874266125" target="_blank" rel="noopener">+258 87 426 6125</a></li>
    <li><a href="mailto:geral@giquiragroup.com">geral@giquiragroup.com</a></li>
    <li><a href="https://instagram.com/giquira_group" target="_blank" rel="noopener">@giquira_group</a></li>
    <li>Av. Emília Dause, N.º 948, R/C, Maputo</li>
  </ul></div>
  <div class="legal"><span>© <span data-year>2026</span> Giquira Group · Maputo, Moçambique</span><span>China → Moçambique</span></div>
</div></footer>
<a class="btn wa fab" href="https://wa.me/{WA}?text={WA_TXT}" target="_blank" rel="noopener" aria-label="Falar com o Giquira Group no WhatsApp">{WA_SVG}<span>WhatsApp</span></a>
<script src="assets/site.js" defer></script>
</body>
</html>
'''
    with open(os.path.join(OUT, fname), "w") as f:
        f.write(html)

# ───────────────────────── blocos partilhados ─────────────────────────
STEPS = [
    ("Envie o pedido", "Uma lista, um link ou uma foto. Diga quantidades, especificações e o prazo que precisa.", False),
    ("Encontramos o fornecedor", "Identificamos e qualificamos fábricas e fornecedores, e comparamos propostas por si.", False),
    ("Receba a cotação", "Produto, frete e taxas no mesmo documento — o custo total, sem surpresas à chegada.", False),
    ("Produção e inspeção", "Só compramos com a sua confirmação. Acompanhamos a produção e inspecionamos antes do embarque.", False),
    ("Embarque e alfândega", "Consolidamos a carga e tratamos da documentação e do desalfandegamento.", True),
    ("Entrega em Moçambique", "Levamos até ao seu armazém, loja ou escritório e confirmamos a receção.", True),
]
LG = ' <span class="lg">Logística incluída</span>'
def steps_html():
    s = "".join(
        f'<div class="st"><span class="n" aria-hidden="true">{i+1}</span><h3>{t}</h3><p>{d}{LG if lg else ""}</p></div>'
        for i, (t, d, lg) in enumerate(STEPS))
    return f'<div class="steps" id="steps"><div class="rail"><b id="fill"></b></div>{s}</div>'

CATS = [("Mobiliário", "Escritório, hotelaria, escolas e residências."),
        ("Eletrodomésticos", "Linha branca e equipamento de cozinha."),
        ("Equipamento de TI", "Computadores, redes, sistemas e periféricos."),
        ("Peças automotivas", "Peças e acessórios para frotas e oficinas."),
        ("Peças industriais", "Peças de reposição e equipamento industrial."),
        ("Tecnologia", "Áudio, carregadores, wearables e gadgets.")]
def cats_html():
    return '<ul class="cats">' + "".join(
        f'<li class="rv" style="--i:{i%3}"><small>{i+1:02d}</small><b>{t}</b><span>{d}</span></li>' for i, (t, d) in enumerate(CATS)) + "</ul>"

def china_html(videos=True):
    vids = ""
    if videos:
        vids = '<div class="vids">' + "".join(
            f'<figure><video src="media/factory-visit-video-{n}.mp4" poster="media/factory-visit-video-{n}-poster.jpg" controls playsinline preload="none" aria-label="{l}"></video><figcaption>▶ {l}</figcaption></figure>'
            for n, l in [(1, "Visita à fábrica parceira"), (2, "Linha de produção"), (3, "Acompanhamento da produção")]) + "</div>"
    return f'''<section class="sec dark" id="china"><div class="w">
  <div class="g2" style="align-items:end">
    <div><p class="eyebrow rv">No terreno · China</p><h2 class="ttl">Não compramos por catálogo. <em>Vamos à fábrica.</em></h2></div>
    <p class="lead rv" style="--i:1;max-width:48ch;margin-bottom:24px">O nosso CEO, Danilo, acompanha pessoalmente fornecedores e fábricas na China — das reuniões de negociação à linha de produção e ao contentor pronto a partir. É assim que a qualidade prometida passa a ser a qualidade entregue.</p>
  </div>
  <div class="mosaic">
    <figure class="big zoom">{ph("media/factory-visit-group.jpg", "Danilo com parceiros dentro da fábrica, com capacetes de segurança")}<figcaption>Visita técnica à fábrica</figcaption></figure>
    <figure class="zoom">{ph("media/ceo-office.jpg", "Danilo em reunião de negócios na China")}<figcaption>Reunião com fornecedor</figcaption></figure>
    <figure class="zoom">{ph("media/ceo-tea-meeting.jpg", "Reunião com parceiros na China")}<figcaption>Negociação</figcaption></figure>
    <figure class="zoom">{ph("media/ceo-container.jpg", "Danilo a acompanhar o carregamento de um contentor")}<figcaption>Carregamento</figcaption></figure>
    <figure class="zoom">{ph("media/ceo-dinner.jpg", "Danilo com parceiros comerciais na China")}<figcaption>Parceiros</figcaption></figure>
  </div>
  {vids}
</div></section>'''

PARTNERS = [("Mozambique Terramar Trading Lda", "terramar"), ("Transcargo Haulage Contractors", "transcargo-haulage"),
            ("Micaia Fundação", "micaia"), ("MozFert Lda", "mozfert"), ("EDM EP", "edm")]
def partners_html(title="Trabalham connosco"):
    li = "".join(f'<li>{ph(f"media/logos/{s}-logo.png", "Logótipo " + n, n)}<span>{n}</span></li>' for n, s in PARTNERS)
    return f'<section class="sec"><div class="w"><p class="eyebrow rv">{title}</p><h2 class="ttl">Parceiros que partilham o nosso rigor.</h2><ul class="logos">{li}</ul></div></section>'

def cta_dark(title, text, b1=("index.html#pedido", "Pedir cotação"), b2=("sobre.html", "Conhecer a empresa")):
    return f'''<section class="sec dark"><div class="w">
  <h2 class="big rv">{title}</h2>
  <p class="lead rv" style="--i:1;max-width:52ch">{text}</p>
  <div class="cta rv" style="--i:2"><a class="btn" href="{b1[0]}">{b1[1]}</a><a class="btn light" href="{b2[0]}">{b2[1]}</a></div>
</div></section>'''

# ───────────────────────── INÍCIO ─────────────────────────
TRACK = ["Fábrica", "Negociação", "Produção", "Inspeção", "Embarque", "Entrega"]
home = f'''<section class="hero"><div class="w hgrid">
  <div>
    <p class="eyebrow">Procurement internacional · desde 2021</p>
    <h1><span class="ln" style="--i:0"><span>Compramos</span></span><span class="ln" style="--i:1"><span>na <em>origem.</em></span></span><span class="ln" style="--i:2"><span>Entregamos</span></span><span class="ln" style="--i:3"><span>em Moçambique.</span></span></h1>
    <p class="lead">Encontramos o fornecedor certo na China, negociamos por si, acompanhamos a produção na fábrica — e tratamos do transporte até à sua porta. Um só parceiro, do pedido à entrega.</p>
    <div class="cta"><a class="btn" href="#pedido">Pedir cotação</a><a class="btn o" href="#como">Ver como funciona</a></div>
    <div class="facts-row"><div><b>4</b><span>Países</span></div><div><b>5</b><span>Parceiros</span></div><div><b>8</b><span>Colaboradores</span></div></div>
  </div>
  <figure class="shot">
    {ph("media/ceo-factory-enhanced.jpg", "Danilo, CEO do Giquira Group, em visita a uma fábrica parceira na China", eager=True)}
    <div class="track" id="track" aria-hidden="true">
      <div class="top"><span class="ref">GQ-<i>0421</i></span><span class="st8" id="trst">Em sourcing</span></div>
      <ol>{"".join(f"<li>{t}<small>agora</small></li>" for t in TRACK)}</ol>
      <div class="prog"><b id="prog"></b></div>
    </div>
  </figure>
</div></section>

<section class="tick" aria-label="Exemplos do que compramos">
  <div class="tk" id="t1" aria-hidden="true"></div><div class="tk" id="t2" aria-hidden="true"></div>
  <div class="w"><p class="tick-note">Se é fabricado, encontramos quem o faça bem. Não encontra a sua categoria? Envie a especificação — procuramos por si.</p></div>
</section>

<section class="sec" id="como"><div class="w g2">
  <div class="sticky"><p class="eyebrow rv">Como funciona</p><h2 class="ttl">Do pedido à sua porta</h2><p class="lead rv" style="--i:1">Seis passos e um só responsável. A logística existe para fechar o ciclo: garantir que o que compramos chega — inteiro, documentado e no prazo.</p><a class="btn o rv" style="--i:2" href="procurement.html">O serviço em detalhe</a></div>
  {steps_html()}
</div></section>

<section class="sec order" id="pedido"><div class="w g2">
  <div>
    <p class="eyebrow">Pedido de cotação</p><h2>Diga-nos o que precisa</h2>
    <p class="lead" style="max-width:none">Leva um minuto. Abrimos o WhatsApp com o pedido já escrito para o Giquira Group.</p>
    <div class="tabs" role="group" aria-label="Como quer enviar o pedido"><button type="button" aria-pressed="true" data-t="lista">Tenho uma lista</button><button type="button" aria-pressed="false" data-t="link">Tenho o link</button><button type="button" aria-pressed="false" data-t="foto">Tenho uma foto</button></div>
    <form id="fm" novalidate>
      <div class="f" id="bl" hidden><label for="lk">Link do produto</label><input id="lk" placeholder="Cole aqui o link (Alibaba, 1688, site do fabricante…)" inputmode="url" autocomplete="off"></div>
      <div class="f" id="bf" hidden><label for="ph">Foto do produto</label><label class="drop" for="ph" id="dz">Toque para escolher uma foto</label><input id="ph" type="file" accept="image/*" class="sr"></div>
      <div class="f"><label for="ds" id="dsl">Descreva o que precisa</label><textarea id="ds" rows="5" placeholder="Ex.: 200 cadeiras de escritório ergonómicas, pretas, com braços. Entrega em Maputo até março."></textarea></div>
      <div class="two">
        <div class="f"><label for="qt">Quantidade total</label><input id="qt" type="number" min="1" placeholder="Ex.: 200" inputmode="numeric"></div>
        <div class="f"><label for="dt">Para quando?</label><select id="dt"><option value="">Sem prazo definido</option><option value="1">Até 1 mês</option><option value="2">1 a 3 meses</option><option value="3">Mais de 3 meses</option></select></div>
      </div>
      <div class="two">
        <div class="f"><label for="nm">Nome ou empresa</label><input id="nm" autocomplete="organization"></div>
        <div class="f"><label for="wp">WhatsApp ou telefone</label><input id="wp" type="tel" placeholder="+258 ..." autocomplete="tel"></div>
      </div>
      <div class="f"><label for="em">Email <span style="font-weight:400;color:var(--mut)">(opcional, para a proposta formal)</span></label><input id="em" type="email" autocomplete="email"></div>
      <p class="err" id="er" role="alert"></p>
      <a class="btn wa" id="send" href="#pedido" target="_blank" rel="noopener">{WA_SVG} Enviar pedido por WhatsApp</a>
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
  <div><p class="eyebrow rv">Para quem trabalhamos</p><h2 class="ttl">Quem precisa de comprar fora, sem correr riscos.</h2></div>
  <div class="mv">
    <div class="rv"><h3>PMEs</h3><p>Equipamento, stock e reposição sem ter de viajar nem arriscar com fornecedores desconhecidos.</p></div>
    <div class="rv"><h3>ONGs</h3><p>Compras com especificação clara, documentação completa e prazos cumpridos.</p></div>
    <div class="rv"><h3>Instituições</h3><p>Processos transparentes e rastreáveis, do pedido à entrega.</p></div>
    <div class="rv"><h3>Particulares</h3><p>Mobiliário, eletrodomésticos e equipamentos trazidos diretamente da origem.</p></div>
  </div>
</div></section>

<section class="sec alt"><div class="w">
  <p class="eyebrow rv">Além do procurement</p><h2 class="ttl">Dois serviços que nasceram das nossas compras.</h2>
  <div class="pair">
    <a href="procurement.html#logistica" class="rv">{ph("media/container-full.jpg", "Contentor carregado pelo Giquira Group")}<div class="t"><span class="mono" style="color:var(--g)">Serviço de apoio</span><b>Logística</b><span>Embarque, desalfandegamento e entrega — a mesma operação que usamos nas nossas compras.</span></div></a>
    <a href="produtos.html" class="rv" style="--i:1">{ph("media/produtos-diversos.jpg", "Acessórios de tecnologia vendidos pelo Giquira Group")}<div class="t"><span class="mono" style="color:var(--g)">Serviço de apoio</span><b>Produtos em stock</b><span>Acessórios de tecnologia e produtos selecionados, prontos a vender em Moçambique.</span></div></a>
  </div>
</div></section>

{partners_html()}

{cta_dark("Committed to quality. <em>Committed to you.</em>", "Desde 2021, com experiência de comércio construída na África do Sul, nos Emirados Árabes Unidos, na China e na Tanzânia.")}
'''
page("index.html", "Giquira Group | Procurement na China para Moçambique",
     "Encontramos fornecedores, negociamos e acompanhamos a produção na China — e entregamos em Moçambique. Procurement com logística incluída.", home, schema=True)

# ───────────────────────── PROCUREMENT ─────────────────────────
INCL = ["Identificação e qualificação de fornecedores locais e internacionais", "Negociação comercial e contratação",
        "Acompanhamento da produção e inspeção pré-embarque", "Controlo de prazos e follow-up operacional",
        "Análise de custo total — produto, frete, taxas e entrega", "Transporte, desalfandegamento e entrega no destino"]
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
proc = f'''<section class="pghero"><div class="w hgrid">
  <div>
    <p class="eyebrow">Serviço principal</p>
    <h1><span class="ln" style="--i:0"><span>O seu</span></span><span class="ln" style="--i:1"><span>departamento</span></span><span class="ln" style="--i:2"><span>de compras</span></span><span class="ln" style="--i:3"><span><em>na China.</em></span></span></h1>
  </div>
  <div class="rv"><p class="lead" style="margin-top:0">Gerimos toda a cadeia de aquisição — da procura do fornecedor à entrega final em Moçambique — com foco em qualidade, custo total e prazo. Fala com uma só equipa; nós tratamos do resto.</p><div class="cta"><a class="btn" href="index.html#pedido">Pedir cotação</a><a class="btn o" href="#processo">Ver o processo</a></div></div>
</div></section>

<section class="w zoom" style="padding-bottom:clamp(56px,8vw,100px)">{ph("media/factory-visit-portrait.jpg", "Danilo, CEO do Giquira Group, em visita a fábrica parceira na China", cls="", eager=True).replace('class="ph "', 'class="ph" style="aspect-ratio:21/9"')}</section>

<section class="sec"><div class="w g2">
  <div class="sticky"><p class="eyebrow rv">O que está incluído</p><h2 class="ttl">Tudo o que uma compra internacional exige.</h2><p class="lead rv">Não vendemos um passo isolado. Assumimos a compra inteira — e a logística vem incluída, porque uma compra só está feita quando chega.</p></div>
  <ul class="rows">{"".join(f'<li class="rv"><small>{i+1:02d}</small>{t}</li>' for i, t in enumerate(INCL))}</ul>
</div></section>

<section class="sec alt" id="processo"><div class="w g2">
  <div class="sticky"><p class="eyebrow rv">O processo</p><h2 class="ttl">Da especificação à entrega</h2><p class="lead rv">Só compramos depois da sua confirmação. Em cada passo sabe o que está a acontecer.</p></div>
  {steps_html()}
</div></section>

<section class="sec dark"><div class="w">
  <p class="eyebrow rv">Porquê com o Giquira Group</p><h2 class="ttl" style="max-width:16ch">Comprar fora tem riscos. <em>O nosso trabalho é retirá-los.</em></h2>
  <div class="risk" style="margin-top:40px"><div class="h">O risco</div><div class="h">O que fazemos</div>
  {"".join(f'<div class="rv"><b>{r}</b></div><div class="rv"><p>{a}</p></div>' for r, a in RISKS)}
  </div>
</div></section>

<section class="sec"><div class="w">
  <p class="eyebrow rv">Categorias</p><h2 class="ttl">Onde já compramos com frequência.</h2>
  {cats_html()}
</div></section>

<section class="sec alt" id="logistica"><div class="w g2">
  <div class="sticky"><p class="eyebrow rv">Logística incluída</p><h2 class="ttl">A logística que fecha cada compra.</h2><p class="lead rv">A nossa operação logística existe por causa do procurement. Nas compras feitas connosco já está incluída — e também aceitamos cargas que já tenha comprado por conta própria.</p>
  <figure class="rv" style="margin:0">{ph("media/logistica-operacao.jpg", "Operação de carregamento de carga do Giquira Group").replace('class="ph "','class="ph" style="aspect-ratio:4/3"')}</figure></div>
  <ul class="rows">{"".join(f'<li class="rv"><small>{i+1:02d}</small><span><b style="display:block">{t}</b><span style="font-weight:400;color:var(--mut);font-size:16px">{d}</span></span></li>' for i, (t, d) in enumerate(LOG))}</ul>
</div></section>

{china_html(videos=False)}

{cta_dark("Diga-nos o que <em>precisa de comprar.</em>", "Envie a lista ou a especificação. Respondemos com uma proposta clara — produto, preço, prazo e entrega incluídos.", b2=("contactos.html", "Outros contactos"))}
'''
page("procurement.html", "Procurement | Giquira Group",
     "Sourcing de fornecedores na China, negociação, inspeção de qualidade e entrega em Moçambique, com logística incluída.", proc)

# ───────────────────────── PRODUTOS ─────────────────────────
LINES = [("Acessórios para smartphones", "Capas, cabos e carregadores."), ("Áudio", "Auriculares, colunas Bluetooth e headphones."),
         ("Wearables", "Smartwatches e acessórios."), ("Periféricos e gadgets", "Para escritório e uso pessoal."),
         ("Produtos de consumo", "Seleção que vai mudando."), ("Revenda B2B", "Condições para lojas e distribuidores.")]
PRODUCT_PHOTOS = [("media/produtos-diversos.jpg", "Acessórios de tecnologia")]  # acrescentar aqui as novas fotografias
gal = "".join(f'<figure class="rv" style="--i:{i%4}">{ph(s, c)}<figcaption>{c}</figcaption></figure>' for i, (s, c) in enumerate(PRODUCT_PHOTOS))
prod = f'''<section class="pghero"><div class="w hgrid">
  <div>
    <p class="eyebrow">Serviço de apoio · Produtos</p>
    <h1><span class="ln" style="--i:0"><span>Escolhidos</span></span><span class="ln" style="--i:1"><span><em>na origem.</em></span></span></h1>
    <p class="lead" style="margin-top:28px">Com a mesma rede de fornecedores que usamos no procurement, importamos uma seleção de produtos — com destaque para acessórios de tecnologia — que vendemos em Moçambique, a particulares e a revendedores.</p>
    <div class="cta"><a class="btn wa" href="https://wa.me/{WA}?text=Ol%C3%A1%20Giquira%20Group!%20Que%20produtos%20t%C3%AAm%20dispon%C3%ADveis%3F" target="_blank" rel="noopener">{WA_SVG} Ver disponibilidade</a><a class="btn o" href="procurement.html">Procura outra coisa?</a></div>
  </div>
  <figure class="shot rv" style="margin:0">{ph("media/produtos-diversos.jpg", "Acessórios de tecnologia vendidos pelo Giquira Group", eager=True)}</figure>
</div></section>

<section class="sec"><div class="w">
  <p class="eyebrow rv">Linhas de produto</p><h2 class="ttl">O que costumamos ter.</h2>
  <ul class="cats">{"".join(f'<li class="rv" style="--i:{i%3}"><small>{i+1:02d}</small><b>{t}</b><span>{d}</span></li>' for i, (t, d) in enumerate(LINES))}</ul>
</div></section>

<section class="sec alt"><div class="w">
  <p class="eyebrow rv">Galeria</p><h2 class="ttl">Alguns dos nossos produtos.</h2>
  <div class="gal">{gal}</div>
  <p class="note" style="margin-top:20px">O stock muda com frequência. Peça a lista atualizada pelo WhatsApp.</p>
</div></section>

{cta_dark("Não está aqui? <em>Encontramos.</em>", "É para isso que existe o nosso procurement. Diga-nos o que procura e compramos na origem.", b2=("procurement.html", "Ver procurement"))}
'''
page("produtos.html", "Produtos | Giquira Group",
     "Acessórios de tecnologia e produtos selecionados, importados pelo Giquira Group e disponíveis em Moçambique.", prod)

# ───────────────────────── SOBRE ─────────────────────────
sobre = f'''<section class="pghero"><div class="w">
  <p class="eyebrow">Sobre nós</p>
  <h1 style="max-width:15ch"><span class="ln" style="--i:0"><span>Nascemos do</span></span><span class="ln" style="--i:1"><span>comércio</span></span><span class="ln" style="--i:2"><span><em>internacional.</em></span></span></h1>
  <div class="facts-row" style="opacity:1;animation:none"><div><b>2021</b><span>Fundação</span></div><div><b>4</b><span>Países</span></div><div><b>5</b><span>Parceiros</span></div><div><b>8</b><span>Colaboradores</span></div></div>
</div></section>

<section class="sec"><div class="w g2">
  <figure class="sticky rv" style="margin:0">{ph("media/ceo-container.jpg", "Danilo, CEO do Giquira Group, a acompanhar operação de carga na China").replace('class="ph "','class="ph" style="aspect-ratio:4/5"')}<figcaption class="mono" style="padding-top:10px;color:var(--mut)">Danilo · Fundador e CEO</figcaption></figure>
  <div class="prose">
    <p class="eyebrow rv">A nossa história</p>
    <h2 class="ttl">Experiência construída nos mercados de onde as coisas vêm.</h2>
    <p class="rv">O Giquira Group foi fundado em 2021 com base em experiência profissional em comércio nacional e internacional, construída em mercados como a África do Sul, os Emirados Árabes Unidos, a China e a Tanzânia. Dessa vivência nasceu a convicção de que qualidade e proximidade não são opostas — são as duas faces da mesma moeda.</p>
    <p class="rv">Hoje o nosso centro é o procurement: compramos mobiliário, eletrodomésticos, equipamentos e sistemas de TI, peças automotivas e peças de reposição industriais para pequenas e médias empresas, ONGs, instituições públicas e particulares.</p>
    <p class="rv">Somos uma equipa de 8 colaboradores, orientada por processos e guiada por pessoas.</p>
    <ul class="chips rv"><li>África do Sul</li><li>Emirados Árabes Unidos</li><li>China</li><li>Tanzânia</li></ul>
    <p class="quote rv">Committed to quality. Committed to you.</p>
  </div>
</div></section>

<section class="sec alt"><div class="w">
  <div class="mv">
    <div class="rv"><h3>Missão</h3><p>Atender com excelência, agilidade e responsabilidade, desenvolvendo talentos e soluções eficazes.</p></div>
    <div class="rv"><h3>Visão</h3><p>Ser referência em consultoria, vendas e gestão de negócios, contribuindo para o crescimento dos clientes.</p></div>
    <div class="rv"><h3>Valores</h3><p>Ética, compromisso com o cliente, transparência, responsabilidade, valorização das pessoas e soluções criativas.</p></div>
  </div>
</div></section>

{china_html()}

{partners_html("Parceiros")}

{cta_dark("Trabalhemos <em>juntos.</em>", "Diga-nos o que precisa de comprar e desenhamos a solução consigo — da origem à entrega.", b2=("contactos.html", "Contactos"))}
'''
page("sobre.html", "Sobre nós | Giquira Group",
     "A história, missão e valores do Giquira Group — procurement internacional sediado em Maputo, com presença na China.", sobre)

# ───────────────────────── CONTACTOS ─────────────────────────
cont = f'''<section class="pghero"><div class="w">
  <p class="eyebrow">Contactos</p>
  <h1><span class="ln" style="--i:0"><span>Fale</span></span><span class="ln" style="--i:1"><span><em>connosco.</em></span></span></h1>
</div></section>

<section class="sec" style="padding-top:0;border-top:0"><div class="w g2">
  <div>
    <dl class="ct">
      <dt>WhatsApp e telefone</dt><dd><a href="https://wa.me/258844266127" target="_blank" rel="noopener">+258 84 426 6127</a><br><a href="https://wa.me/258874266125" target="_blank" rel="noopener">+258 87 426 6125</a></dd>
      <dt>Email</dt><dd><a href="mailto:geral@giquiragroup.com">geral@giquiragroup.com</a></dd>
      <dt>Instagram</dt><dd><a href="https://instagram.com/giquira_group" target="_blank" rel="noopener">@giquira_group</a></dd>
      <dt>Escritório</dt><dd>Av. Emília Dause, N.º 948, R/C<br>Antes da Alof Palm, Cidade de Maputo</dd>
    </dl>
    <div class="map"><iframe title="Mapa do escritório do Giquira Group em Maputo" loading="lazy" src="https://www.openstreetmap.org/export/embed.html?bbox=32.5750%2C-25.9700%2C32.6150%2C-25.9450&amp;layer=mapnik&amp;marker=-25.9575%2C32.5950"></iframe></div>
  </div>
  <div class="order" style="padding:clamp(22px,4vw,40px);border:1px solid var(--line)">
    <p class="eyebrow">Mensagem rápida</p>
    <h2 style="font-size:clamp(34px,4vw,52px)">Escreva-nos</h2>
    <form id="cf" novalidate>
      <div class="f"><label for="cn">O seu nome</label><input id="cn" autocomplete="name"></div>
      <div class="f"><label for="cm">Mensagem</label><textarea id="cm" rows="5" placeholder="Como podemos ajudar?"></textarea></div>
      <a class="btn wa" id="cwa" href="https://wa.me/{WA}" target="_blank" rel="noopener">{WA_SVG} Enviar por WhatsApp</a>
      <p class="note">Para pedir uma cotação, use o <a href="index.html#pedido">formulário de pedido</a> — fica tudo organizado com uma referência.</p>
    </form>
  </div>
</div></section>
'''
page("contactos.html", "Contactos | Giquira Group",
     "Fale com o Giquira Group: WhatsApp +258 84 426 6127, geral@giquiragroup.com, Av. Emília Dause, Maputo.", cont)

# ───────────────────────── ficheiros de apoio ─────────────────────────
pages = [n for n, _ in NAV]
with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
            "".join(f'  <url><loc>{DOMAIN}/{"" if p == "index.html" else p}</loc></url>\n' for p in pages) + "</urlset>\n")
with open(os.path.join(OUT, "robots.txt"), "w") as f:
    f.write(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
with open(os.path.join(OUT, "404.html"), "w") as f:
    f.write('<!doctype html><html lang="pt-MZ"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Página não encontrada | Giquira Group</title><link rel="stylesheet" href="/assets/site.css"></head><body><main class="w" style="padding-block:120px"><p class="eyebrow">404</p><h1>Página não <em>encontrada.</em></h1><p class="lead" style="margin-top:24px">A página que procura não existe ou foi movida.</p><a class="btn" href="/">Voltar ao início</a></main></body></html>\n')
print("ok")
