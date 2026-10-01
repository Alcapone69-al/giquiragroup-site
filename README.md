# Giquira Group — site

Site estático (HTML, CSS e JavaScript sem dependências), alojado no GitHub Pages.

- Páginas: `index.html`, `procurement.html`, `produtos.html`, `sobre.html`, `contactos.html`, `404.html`
- Estilos e animações: `assets/site.css` · comportamento: `assets/site.js`
- Tipos de letra (no próprio site): Schibsted Grotesk (títulos) e Instrument Sans (texto) — licença SIL OFL em `assets/fonts/`
- Fotografias e vídeos: `media/`

## Como editar

As páginas são geradas por `tools/build_site.py`. Editar o texto lá e correr:

    python3 tools/build_site.py

No topo desse ficheiro está a **CONFIGURAÇÃO**: domínio, logótipo, parceiros e produtos.

## Ligar o domínio

1. Em `tools/build_site.py`: `SITE_URL = "https://www.o-dominio"` e `BASE_PATH = "/"`.
2. Correr `python3 tools/build_site.py` (cria `CNAME`, `sitemap.xml` e os links canónicos) e publicar.
3. GitHub → Settings → Pages → Custom domain: o mesmo domínio; depois ativar **Enforce HTTPS**.
4. No DNS do domínio (sem mexer nos registos MX/SPF/DKIM do email):
   - `www` → CNAME → `alcapone69-al.github.io`
   - domínio raiz → registos A → 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153

## Logótipo oficial

Ficheiros em `media/brand/` (gerados a partir do logótipo oficial):
- `giquira-logo-horizontal.webp/.png` — símbolo + nome, para fundo claro (cabeçalho)
- `giquira-logo-horizontal-branco.webp/.png` — para fundo escuro (rodapé e transição entre páginas)
- `giquira-simbolo.webp/.png` — só o símbolo · `giquira-nome-escuro.png` / `giquira-nome-branco.png` — só o nome
- `favicon.png`, `apple-touch-icon.png`, `media/brand/icon-192.png` — ícones · `media/og-giquira.jpg` — pré-visualização nas redes
Configuração em `BRAND` (tools/build_site.py). Se chegar uma versão vetorial (SVG), basta substituir os caminhos.

## Parceiros

Logótipos em `media/logos/`, configurados em `PARTNERS`.

## Galeria de produtos (preparada, vazia)

Acrescentar itens a `PRODUCTS` (nome, descrição, preço opcional, categoria opcional, fotografia). A secção só aparece
quando houver produtos.
