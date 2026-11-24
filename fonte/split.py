import re, sys, os
src_path, pub = sys.argv[1], sys.argv[2]
src = open(src_path, encoding='utf-8').read()
BASE = 'https://haumaconsultoria.com.br'

# ---------- slice sections ----------
marks = [(m.start(), m.group(1)) for m in re.finditer(r'<!-- =+ ([^\n]*?) =+ -->', src)]
def key(label):
    m = re.match(r'(\d+)\.', label)
    return m.group(1) if m else 'artigos'
sec_start = marks[0][0]
e = src.index('<!-- Vanilla JS for FAQ')
sec_end = src.rfind('</div>', 0, e)
S = {}
for i, (pos, label) in enumerate(marks):
    end = marks[i + 1][0] if i + 1 < len(marks) else sec_end
    S[key(label)] = src[pos:end]
assert set(S) == set(['1','2','3','4','5','6','7','8','9','10','11','12','13','artigos']), S.keys()
QUEM = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'quem.html'), encoding='utf-8').read()
_q = QUEM.index('<!-- ==================== NOSSA VISÃO')
QUEM, VISAO = QUEM[:_q], QUEM[_q:]
SERVICOS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'servicos.html'), encoding='utf-8').read()
COMO = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'como.html'), encoding='utf-8').read()
_rd = lambda n: open(os.path.join(os.path.dirname(os.path.abspath(__file__)), n), encoding='utf-8').read()
MODELAGEM = _rd('modelagem.html')
ART_ECON, ART_CURVA, NOT_LISTA, ART_CTRL, ART_CRESCER = _rd('art_econ.html'), _rd('art_curva.html'), _rd('noticias_lista.html'), _rd('art_ctrl.html'), _rd('art_crescer.html')
EXTRA_TITLES = {'/noticias/crescer-com-retorno': 'Crescer não basta: retorno, caixa e ciclos', '/noticias/controladoria-estrategica': 'Controladoria Estratégica', '/noticias/economista-na-empresa': 'Sua empresa precisa de um economista?', '/noticias/curva-de-juros': 'Além da Selic: o que a curva de juros mostra'}
prefix = src[:sec_start]
suffix = src[sec_end:]

# ---------- absolute asset paths (pages live in subfolders) ----------
def absassets(h):
    return h.replace('src="logo-hauma.png"', 'src="/logo-hauma.png"').replace('href="favicon.png"', 'href="/favicon.png"')

# ---------- remove contact dialog + its script ----------
d0 = suffix.index('<dialog id="contato-dialog"')
d1 = suffix.index('</script>', d0) + len('</script>')
suffix = suffix[:d0] + suffix[d1:]
assert suffix.count("form.addEventListener('submit'") == 1
suffix = suffix.replace("form.addEventListener('submit'", "if (form) form.addEventListener('submit'")
suffix = suffix.replace("dd.querySelector('button').addEventListener", "dd.firstElementChild.addEventListener")
suffix = suffix.replace("dd.querySelectorAll('a').forEach", "dd.querySelectorAll('.dd-panel a').forEach")

# ---------- menu structure ----------
MENU = [
    ('sobre', 'Sobre', [('/sobre', 'Quem somos'), ('/sobre/nossa-visao', 'Nossa visão'), ('/sobre/para-quem', 'Para quem é')]),
    ('servicos', 'Serviços', [('/servicos', 'Nossos serviços'), ('/servicos/modelagem-de-a-a-z', 'Modelagem de A a Z'), ('/servicos/como-trabalhamos', 'Como trabalhamos'),
                              ('/servicos/contratacao', 'Modelos de contratação'), ('/servicos/duvidas', 'Dúvidas')]),
    ('noticias', 'Notícias e Artigos', [('/noticias', 'Notícias e Artigos')]),
    ('contato', 'Contato', [('/contato', 'Contato')]),
]
LINK = {
    '#inicio': '/', '#problema': '/#problema', '#comparativo': '/#comparativo',
    '#sobre': '/sobre', '#diferencial': '/servicos/como-trabalhamos#diferencial', '#visao': '/sobre/nossa-visao', '#para-quem': '/sobre/para-quem',
    '#servicos': '/servicos', '#como-trabalhamos': '/servicos/como-trabalhamos', '#metodologia': '/servicos/como-trabalhamos#metodologia',
    '#contratacao': '/servicos/contratacao', '#faq': '/servicos/duvidas',
    '#artigos': '/noticias', '#contato': '/contato', '#diagnostico-form': '/contato#diagnostico-form',
}
def relink(html):
    return re.sub(r'href="(#[a-z\-]+)"', lambda m: 'href="%s"' % LINK.get(m.group(1), m.group(1)), html)

# ---------- header ----------
logo = re.search(r'<a href="#inicio" aria-label="HAUMA[^"]*">.*?</a>', prefix).group(0)
agendar = re.search(r'<a class="inline-flex items-center justify-center h-11 px-space-md rounded-lg bg-secondary[^>]*data-path="agendamento"[^>]*>.*?</span></span></a>', prefix).group(0)
menubtn = re.search(r'<button aria-label="Abrir Menu".*?</button>', prefix).group(0)
topbar = re.search(r'<div class="hidden lg:block bg-\[#13233a\].*?</div></div>', prefix).group(0)

def dropdown(label, items, active):
    href = items[0][0]
    cls = 'text-secondary' if active else 'text-on-surface hover:text-secondary'
    if len(items) == 1:
        return '<a href="%s"%s class="py-2 text-[16px] font-medium %s transition-colors">%s</a>' % (href, ' aria-current="page"' if active else '', cls, label)
    links = ''.join('<a class="block px-4 py-2.5 text-[15px] text-on-surface hover:bg-surface-container-low hover:text-secondary" href="%s">%s</a>' % it for it in items)
    return ('<div class="relative group dd">'
            '<a href="%s"%s class="flex items-center gap-1 py-2 text-[16px] font-medium %s transition-colors">%s'
            '<span class="material-symbols-outlined text-[20px] transition-transform group-hover:rotate-180">expand_more</span></a>'
            '<div class="dd-panel absolute left-0 top-full pt-2 invisible opacity-0 group-hover:visible group-hover:opacity-100 group-focus-within:visible group-focus-within:opacity-100 transition-opacity">'
            '<div class="min-w-[240px] rounded-lg bg-surface-container-lowest shadow-xl border border-outline-variant py-2">%s</div></div></div>') % (
                href, ' aria-current="page"' if active else '', cls, label, links)

def mgroup(label, items):
    if len(items) == 1:
        return '<a class="py-3 font-body-lg text-body-lg text-on-surface hover:text-secondary border-b border-outline-variant" href="%s">%s</a>' % (items[0][0], label)
    return ('<span class="pt-3 pb-1 font-label-badge text-label-badge uppercase tracking-widest text-secondary">%s</span>' % label +
            ''.join('<a class="py-2.5 pl-3 font-body-lg text-body-lg text-on-surface hover:text-secondary border-b border-outline-variant" href="%s">%s</a>' % it for it in items))

def header(group):
    return ('<header class="fixed top-0 w-full z-50 pt-safe">' + topbar +
            '<div class="bg-surface/95 backdrop-blur-xl shadow-[0_1px_8px_rgba(19,35,58,0.08)]">'
            '<div class="max-w-6xl mx-auto h-16 lg:h-20 px-margin-mobile lg:px-margin flex items-center justify-between gap-space-sm">'
            '<div class="flex items-center gap-space-sm">' + menubtn + relink(logo) + '</div>'
            '<nav class="hidden lg:flex items-center gap-9" aria-label="Menu principal">'
            + ''.join(dropdown(label, items, g == group) for g, label, items in MENU) +
            '</nav>'
            '<div class="flex items-center gap-space-xs">' + relink(agendar) + '</div>'
            '</div>'
            '<nav id="menu-panel" class="hidden lg:hidden border-t border-outline-variant bg-surface px-margin-mobile pb-space-sm flex flex-col max-h-[75vh] overflow-y-auto" aria-label="Menu">'
            '<a class="py-3 font-body-lg text-body-lg text-on-surface hover:text-secondary border-b border-outline-variant" href="/">Início</a>'
            + ''.join(mgroup(label, items) for g, label, items in MENU) +
            '</nav></div></header>')

h0 = prefix.index('<header'); h1 = prefix.index('</header>') + len('</header>')

# ---------- bottom nav (mobile) ----------
BOTTOM = [('home', '/', 'corporate_fare', 'Início'), ('sobre', '/sobre', 'info', 'Sobre'),
          ('servicos', '/servicos', 'query_stats', 'Serviços'), ('agendar', '/contato#diagnostico-form', 'event_available', 'Agendar'),
          ('contato', '/contato', 'mail', 'Contato')]
def bottom(active):
    items = ''
    for k, href, icon, label in BOTTOM:
        act = (k == active)
        items += ('<a%s class="flex flex-col items-center justify-center gap-1 w-14 h-11 transition-colors %s" href="%s">'
                  '<span class="material-symbols-outlined text-[20px]">%s</span><span class="font-label-badge text-label-badge">%s</span></a>') % (
                      ' aria-current="page"' if act else '', 'text-secondary' if act else 'text-on-surface-variant', href, icon, label)
    return '<div class="flex justify-around items-center h-16 px-space-xs">' + items + '</div>'
b0 = suffix.index('<nav class="lg:hidden fixed bottom-0')
b0 = suffix.index('>', b0) + 1
b1 = suffix.index('</nav>', b0)

# ---------- banner with breadcrumb + sibling tabs ----------
def banner(group, path):
    g = [m for m in MENU if m[0] == group][0]
    title = [t for h, t in g[2] if h == path][0]
    crumb = ('<nav aria-label="Você está em" class="font-body-sm text-body-sm text-white/70">'
             '<a class="hover:text-[#f5d565]" href="/">Início</a> <span class="mx-1">/</span> '
             '<a class="hover:text-[#f5d565]" href="%s">%s</a> <span class="mx-1">/</span> '
             '<span class="text-[#f5d565]">%s</span></nav>') % (g[2][0][0], g[1], title)
    tabs = ''.join(
        ('<a aria-current="page" class="shrink-0 px-4 py-2 rounded-full bg-[#e9c349] text-[#13233a] font-semibold" href="%s">%s</a>' if h == path else
         '<a class="shrink-0 px-4 py-2 rounded-full bg-white/10 text-white hover:bg-white/20" href="%s">%s</a>') % (h, t)
        for h, t in g[2])
    return ('<!-- ==================== BANNER ==================== -->\n'
            '<section class="bg-[#13233a] px-margin-mobile pt-space-xl pb-space-lg lg:pt-14 flex flex-col gap-space-md">'
            '<div class="flex flex-col gap-space-sm">' + crumb +
            '<h1 class="font-display-hero-mobile text-display-hero-mobile lg:font-display-hero lg:text-display-hero text-white">%s</h1></div>'
            '<div class="flex gap-2 overflow-x-auto pb-1 font-body-sm text-body-sm">%s</div>'
            '</section>\n') % (title, tabs)

CTA = ('<!-- ==================== CTA ==================== -->\n'
       '<section class="bg-[#13233a] px-margin-mobile py-space-xl flex flex-col gap-space-md items-center text-center">'
       '<h2 class="font-headline-lg text-headline-lg text-white">Descubra com precisão onde está o caixa da sua empresa</h2>'
       '<p class="font-body-md text-body-md text-white/80 max-w-xl">Agende uma conversa inicial confidencial e sem compromisso.</p>'
       '<a class="inline-flex items-center justify-center gap-2 h-12 px-space-lg rounded-lg bg-[#e9c349] text-[#13233a] font-label-executive text-label-executive uppercase tracking-wider hover:brightness-105" href="/contato#diagnostico-form">'
       '<span class="material-symbols-outlined text-[18px]">event_available</span>Agendar diagnóstico</a>'
       '</section>\n')

def placeholder(icon, text, title):
    return ('<section class="px-margin-mobile py-space-xl flex flex-col gap-space-md">'
            '<h2 class="font-headline-lg text-headline-lg text-on-surface">' + title + '</h2>'
            '<div class="bg-surface-container p-space-md rounded-xl shadow-sm flex items-start gap-space-sm max-w-2xl">'
            '<span class="material-symbols-outlined text-[24px] text-secondary">%s</span>'
            '<p class="font-body-md text-body-md text-on-surface-variant">%s</p></div></section>\n') % (icon, text)

CONTACT = ('<!-- ==================== DADOS DE CONTATO ==================== -->\n'
    '<section class="px-margin-mobile py-space-xl flex flex-col gap-space-md">'
    '<div class="bg-surface-container p-space-lg rounded-2xl shadow-sm flex flex-col gap-space-sm max-w-xl">'
    '<span class="font-label-badge text-label-badge uppercase tracking-widest text-secondary">Fale diretamente</span>'
    '<h2 class="font-headline-md text-headline-md text-on-surface">José Mario dos Santos</h2>'
    '<p class="font-body-sm text-body-sm text-on-surface-variant -mt-1">Economista · Corecon/SP nº 33.092</p>'
    '<div class="flex flex-col">'
    '<a class="flex items-center gap-3 py-3 border-b border-outline-variant text-on-surface hover:text-secondary" href="mailto:jmario.hauma@outlook.com"><span class="material-symbols-outlined text-[20px] text-secondary">mail</span><span class="font-body-md text-body-md">jmario.hauma@outlook.com</span></a>'
    '<a class="flex items-center gap-3 py-3 border-b border-outline-variant text-on-surface hover:text-secondary" href="tel:+5517997115321"><span class="material-symbols-outlined text-[20px] text-secondary">call</span><span class="font-body-md text-body-md">+55 (17) 9 99711-5321</span></a>'
    '<div class="flex items-center gap-3 py-3 text-on-surface-variant"><span class="material-symbols-outlined text-[20px] text-secondary">pin_drop</span><span class="font-body-md text-body-md">Sede em Bebedouro – SP · atendimento nacional (eixo SP e capitais)</span></div>'
    '<a class="flex items-center gap-3 py-3 text-on-surface hover:text-secondary" href="https://www.ohub.com.br/empresa/hauma-solucoes-empresariais-ltda-bebedouro-sp-742652" target="_blank" rel="noopener noreferrer"><span class="material-symbols-outlined text-[20px] text-[#1f8a3b]">verified</span><span class="font-body-md text-body-md">Documentos verificados no OHUB</span></a>'
    '</div>'
    '<div class="mt-space-xs flex flex-col sm:flex-row gap-space-sm">'
    '<a class="flex-1 inline-flex items-center justify-center gap-2 h-12 px-space-md rounded-lg bg-secondary text-on-secondary font-label-executive text-label-executive uppercase tracking-wider" href="https://wa.me/5517997115321" target="_blank" rel="noopener noreferrer"><span class="material-symbols-outlined text-[18px]">chat</span>WhatsApp</a>'
    '<a class="flex-1 inline-flex items-center justify-center gap-2 h-12 px-space-md rounded-lg bg-surface-container-high text-secondary font-label-executive text-label-executive uppercase tracking-wider" href="/contato#diagnostico-form"><span class="material-symbols-outlined text-[18px]">event_available</span>Agendar diagnóstico</a>'
    '</div></div></section>\n')

# (file, group, path, body)
PAGES = [
    ('index', 'home', '/', [S['1'], S['2'], S['7'], CTA]),
    ('sobre', 'sobre', '/sobre', [QUEM]),
    ('sobre/nossa-visao', 'sobre', '/sobre/nossa-visao', [VISAO]),
    ('sobre/para-quem', 'sobre', '/sobre/para-quem', [S['6']]),
    ('servicos', 'servicos', '/servicos', [SERVICOS]),
    ('servicos/modelagem-de-a-a-z', 'servicos', '/servicos/modelagem-de-a-a-z', [MODELAGEM]),
    ('servicos/como-trabalhamos', 'servicos', '/servicos/como-trabalhamos', [COMO]),
    ('servicos/contratacao', 'servicos', '/servicos/contratacao', [S['10']]),
    ('servicos/duvidas', 'servicos', '/servicos/duvidas', [S['11']]),
    ('noticias', 'noticias', '/noticias', [NOT_LISTA]),
    ('noticias/crescer-com-retorno', 'noticias', '/noticias/crescer-com-retorno', [ART_CRESCER]),
    ('noticias/controladoria-estrategica', 'noticias', '/noticias/controladoria-estrategica', [ART_CTRL]),
    ('noticias/economista-na-empresa', 'noticias', '/noticias/economista-na-empresa', [ART_ECON]),
    ('noticias/curva-de-juros', 'noticias', '/noticias/curva-de-juros', [ART_CURVA]),
    ('contato', 'contato', '/contato', [CONTACT, S['12']]),
]


DESCRICOES = {
    '/': 'Consultoria em finanças corporativas, FP&A e governança para empresas de médio e grande porte. Modelagem integrada de DRE, Fluxo de Caixa e Balanço.',
    '/sobre': 'Conheça a HAUMA: consultoria conduzida pelo economista José Mario dos Santos, com mais de 30 anos em gestão estratégica e finanças corporativas.',
    '/sobre/nossa-visao': 'Lucro não é o mesmo que rentabilidade. Por que o EBITDA não é caixa e como o EVA mostra se a sua empresa realmente cria valor.',
    '/sobre/para-quem': 'Para empresários, sócios, investidores e empresas em preparação para M&A, com faturamento acima de R$ 10 milhões por ano.',
    '/servicos': 'FP&A, controladoria, DRE gerencial, painéis em Power BI, modelagem financeira, valuation, estudos de viabilidade, gestão de caixa e governança para empresas de médio e grande porte.',
    '/servicos/modelagem-de-a-a-z': 'Modelagem de A a Z: modelo de project finance online, com 180 meses, 7 cenários, DRE, DFC e Balanço integrados e valuation por FCFF, FCFE e DDM. Assinatura HAUMA.',
    '/servicos/como-trabalhamos': 'Do alinhamento com NDA ao acompanhamento mensal: as 6 etapas do trabalho da HAUMA e o diagnóstico financeiro em 3 a 5 semanas.',
    '/servicos/contratacao': 'Projeto pontual de modelagem e valuation, FP&A contínuo ou advisory para M&A e sócios: escolha o formato ideal para a sua empresa.',
    '/servicos/duvidas': 'Perguntas frequentes sobre FP&A, faturamento mínimo, atendimento remoto, sigilo das informações e prazo do diagnóstico financeiro.',
    '/noticias': 'Artigos da HAUMA sobre economia de empresas, gestão financeira, juros e decisões estratégicas para empresas de médio e grande porte.',
    '/noticias/crescer-com-retorno': 'Crescer não basta: por que ROIC, WACC, capital de giro e geração de caixa definem se a empresa cria valor de verdade.',
    '/noticias/controladoria-estrategica': 'Controladoria estratégica vai além de relatórios: conecta números, indicadores e planejamento para decisões que geram valor.',
    '/noticias/economista-na-empresa': 'Economia de empresas vai muito além de câmbio, juros e inflação. Por que a empresa familiar de médio porte é a que mais perde sem essa leitura.',
    '/noticias/curva-de-juros': 'A diferença entre a Selic e a curva de juros, por que as taxas longas podem seguir altas e o que isso muda no custo de capital da sua empresa.',
    '/contato': 'Fale com a HAUMA por WhatsApp, telefone ou e-mail, ou solicite um diagnóstico financeiro confidencial para a sua empresa.',
}
OLD_DESC = '<meta name="description" content="Pare de andar no escuro na gestão financeira da sua empresa. Consultoria financeira HAUMA."/>'

WIDTH_CSS = ('@media (min-width:1024px){main section,footer{padding-left:max(2rem,calc((100% - 72rem)/2))!important;'
             'padding-right:max(2rem,calc((100% - 72rem)/2))!important;}}')

for fname, group, path, body in PAGES:
    if group == 'home':
        title = 'HAUMA Consultoria'
    else:
        g = [m for m in MENU if m[0] == group][0]
        title = ([t for h, t in g[2] if h == path] or [EXTRA_TITLES.get(path)])[0] + ' | HAUMA Consultoria'
    pre = prefix[:h0] + header(group) + prefix[h1:]
    pre = pre.replace('.dd.dd-closed', WIDTH_CSS + '.dd.dd-closed', 1)
    pre = pre.replace('<title>HAUMA Consultoria</title>', '<title>%s</title>' % title, 1)
    pre = pre.replace('content="HAUMA Consultoria"/>', 'content="%s"/>' % title, 1)
    pre = pre.replace('<link rel="canonical" href="%s/"/>' % BASE, '<link rel="canonical" href="%s%s"/>' % (BASE, path), 1)
    pre = pre.replace('<meta property="og:url" content="%s/"/>' % BASE, '<meta property="og:url" content="%s%s"/>' % (BASE, path), 1)
    d = DESCRICOES[path].replace('&', '&amp;')
    assert pre.count(OLD_DESC) == 1
    pre = pre.replace(OLD_DESC, '<meta name="description" content="%s"/><meta property="og:description" content="%s"/>' % (d, d), 1)
    active_bottom = {'home': 'home', 'sobre': 'sobre', 'servicos': 'servicos', 'noticias': None, 'contato': 'contato'}[group]
    if path == '/contato#diagnostico-form':
        active_bottom = 'agendar'
    suf = suffix[:b0] + bottom(active_bottom) + suffix[b1:]
    html = absassets(pre + relink(''.join(body)) + relink(suf))
    out = os.path.join(pub, fname + '.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8', newline='').write(html)
    print(fname, len(html), 'anchors-left:', len(re.findall(r'href="#[a-z]', html)))

# ---------- sitemap.xml e robots.txt ----------
import datetime
hoje = datetime.date.today().isoformat()
urls = ''.join('  <url><loc>%s%s</loc><lastmod>%s</lastmod></url>\n' % (BASE, path, hoje) for _, _, path, _ in PAGES)
open(os.path.join(pub, 'sitemap.xml'), 'w', encoding='utf-8', newline='\n').write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '</urlset>\n')
open(os.path.join(pub, 'robots.txt'), 'w', encoding='utf-8', newline='\n').write(
    'User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n' % BASE)
print('sitemap:', len(PAGES), 'paginas')
