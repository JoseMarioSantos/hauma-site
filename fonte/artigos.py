# Gera os fragmentos HTML dos artigos e da listagem de Notícias e Artigos.
import os, html
D = os.path.dirname(os.path.abspath(__file__))

AUTOR = ('<p class="font-body-sm text-body-sm text-on-surface-variant">Por <strong class="text-on-surface">José Mario dos Santos</strong>, '
         'economista (Corecon/SP nº 33.092)</p>')

def paras(txt):
    out = []
    for p in [p.strip() for p in txt.strip().split('\n\n') if p.strip()]:
        out.append('<p>%s</p>' % html.escape(p, quote=False))
    return '\n'.join(out)

def artigo(slug_id, titulo, corpo, extra=''):
    return ('<!-- ==================== ARTIGO ==================== -->\n'
            '<section id="%s" class="px-margin-mobile py-space-xl flex flex-col gap-space-md">'
            '<article class="max-w-3xl flex flex-col gap-space-md">'
            '<a class="inline-flex items-center gap-1 font-body-sm text-body-sm text-secondary hover:underline" href="/noticias">'
            '<span class="material-symbols-outlined text-[18px]">arrow_back</span>Notícias e Artigos</a>'
            '<div class="flex flex-col gap-space-xs">'
            '<span class="font-label-badge text-label-badge uppercase tracking-widest text-secondary">Artigo</span>'
            '<h1 class="font-display-hero-mobile text-display-hero-mobile lg:font-display-hero lg:text-display-hero text-on-surface">%s</h1>'
            + AUTOR + '</div>'
            '<div class="flex flex-col gap-space-md font-body-lg text-body-lg text-on-surface-variant leading-relaxed">\n%s\n</div>'
            '%s'
            '<div class="mt-space-md bg-surface-container p-space-md rounded-xl shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-space-sm">'
            '<p class="font-body-md text-body-md text-on-surface">Quer aplicar essa leitura às decisões da sua empresa?</p>'
            '<a class="inline-flex items-center justify-center gap-2 h-11 px-space-md rounded-lg bg-secondary text-on-secondary font-label-executive text-label-executive uppercase tracking-wider" href="/contato#diagnostico-form">'
            '<span class="material-symbols-outlined text-[18px]">event_available</span>Agendar conversa</a></div>'
            '</article></section>\n') % (slug_id, titulo, corpo, extra)

ECONOMISTA = """
Essa pergunta costuma soar estranha para o empresário de porte médio. Existe uma crença comum de que economista é coisa de empresa grande, com departamento financeiro robusto e diretoria especializada.

Na prática, é justamente o contrário. E o engano começa numa ideia ainda mais restrita: a de que economista serve só para analisar taxa de câmbio, juros e inflação.

O campo da economia de empresas vai muito além disso. Trata da estrutura econômica do negócio: como ele gera receita, organiza custos e constrói resultados sólidos. Trata de decisões de organização: o que produzir internamente e o que contratar de terceiros, como equilibrar gestão e propriedade em empresas familiares, como desenvolver as capacitações que diferenciam um negócio do concorrente. Trata de estratégia competitiva, precificação, análise de mercado e decisão sob incerteza.

E trata também de como o mercado em que você atua está estruturado: se ele é concentrado ou pulverizado, como seus concorrentes reagem às suas decisões, que barreiras protegem ou ameaçam sua posição.

Entender essa dinâmica muda completamente a forma como uma empresa define preço, planeja expansão ou reage a um novo concorrente que chega no bairro.

É justamente a empresa familiar, de médio porte, que mais perde dinheiro por não ter esse tipo de leitura. Não apenas pela falta de previsibilidade do câmbio ou da taxa de juros, mas por decisões estruturais tomadas no improviso: preço definido por intuição, terceirização decidida por economia aparente, reação a um concorrente sem entender o jogo que está sendo jogado.

Não é sobre contratar um economista em tempo integral. A maioria das empresas desse porte não precisa disso.

É sobre ter, em algum momento do processo de decisão, alguém que traduza essas ferramentas para a realidade do seu negócio. Antes que o mercado faça essa tradução por você, da forma mais cara possível.

A pergunta não é se você precisa de um economista todos os dias. É se você tem alguém para consultar quando a decisão importa.
"""

CURVA_A = """
Muito se fala sobre a Selic. Mas existe uma diferença importante entre o juro que o Banco Central define hoje e os juros que o mercado negocia para o futuro.

É aí que entra a chamada curva de juros. De forma simples, ela mostra as taxas associadas a diferentes prazos (meses, um ano, dois anos, cinco anos) e ajuda a entender como o mercado está precificando o cenário econômico ao longo do tempo.

O ponto mais interessante é que a curva não olha apenas para a decisão atual do Banco Central. Ela incorpora expectativas sobre inflação, atividade econômica, câmbio, política monetária, risco e também as incertezas que existem em horizontes mais longos.
"""
CURVA_B = """
Por isso, é perfeitamente possível que o mercado espere uma redução da Selic no futuro e, ainda assim, determinadas taxas mais longas permaneçam elevadas. Isso acontece porque uma taxa de prazo maior não representa apenas uma expectativa sobre a próxima decisão do Copom. Ela também carrega um prêmio pelo risco de manter aquele capital comprometido por mais tempo.

É justamente por isso que acompanhar apenas a Selic pode contar uma parte pequena da história.

Para uma empresa, por exemplo, não importa somente saber quanto está a Selic hoje. Também importa entender a que taxa o mercado está disposto a financiar os próximos anos, porque isso influencia o custo dos financiamentos, a precificação dos títulos, as decisões de investimento e, de forma mais ampla, o custo de capital da economia.

A curva de juros funciona quase como uma fotografia das expectativas e dos riscos que o mercado está atribuindo aos diferentes horizontes de tempo. Mas existe um cuidado importante: ela não é uma previsão perfeita do futuro. Ler uma taxa futura como se o mercado estivesse dizendo exatamente onde estará a Selic naquela data ignora os prêmios de risco presentes nessas taxas.

E talvez seja justamente isso que torne a curva tão interessante. A Selic nos diz muito sobre a política monetária agora. A curva ajuda a entender como o mercado está precificando o caminho daqui para frente.
"""
import sys as _sys, math as _math
_sys.path.insert(0, D)
from curva_dados import CURVA

def _br(v, casas=2):
    return ('%.*f' % (casas, v)).replace('.', ',')

def grafico_curva(c):
    pts = c['pontos']; n = len(pts); est = set(c.get('estimados', []))
    W, H = 760, 360; L, R, T, B = 56, 24, 28, 44
    vals = [v for _, v in pts]
    lo = _math.floor(min(vals) * 2) / 2 - 0.5; hi = _math.ceil(max(vals) * 2) / 2
    x = lambda i: L + i * (W - L - R) / (n - 1)
    y = lambda v: T + (hi - v) / (hi - lo) * (H - T - B)
    g = []
    t = lo
    while t <= hi + 1e-9:
        g.append('<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" stroke="#e7e4dc" stroke-width="1"/>' % (L, W - R, y(t), y(t)))
        g.append('<text x="%d" y="%.1f" text-anchor="end" dominant-baseline="middle" font-size="12" fill="#4a5466">%s%%</text>' % (L - 8, y(t), _br(t, 1)))
        t += 0.5
    for i, (lab, _) in enumerate(pts):
        g.append('<text x="%.1f" y="%d" text-anchor="middle" font-size="12" fill="#4a5466">%s</text>' % (x(i), H - B + 22, lab))
    path = ' '.join(('M' if i == 0 else 'L') + '%.1f %.1f' % (x(i), y(v)) for i, (_, v) in enumerate(pts))
    g.append('<path d="%s" fill="none" stroke="#2a78d6" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>' % path)
    imax = max(range(n), key=lambda i: pts[i][1])
    for i, (lab, v) in enumerate(pts):
        if lab in est:
            g.append('<circle cx="%.1f" cy="%.1f" r="4.5" fill="#ffffff" stroke="#2a78d6" stroke-width="2"/>' % (x(i), y(v)))
        else:
            g.append('<circle cx="%.1f" cy="%.1f" r="4.5" fill="#2a78d6" stroke="#ffffff" stroke-width="2"/>' % (x(i), y(v)))
    for i in sorted({0, imax, n - 1}):
        anchor = 'start' if i == 0 else ('end' if i == n - 1 else 'middle')
        dx = 6 if i == 0 else (-6 if i == n - 1 else 0)
        g.append('<text x="%.1f" y="%.1f" text-anchor="%s" font-size="13" font-weight="600" fill="#13233a">%s%%</text>' % (x(i) + dx, y(pts[i][1]) + (22 if i == 0 else -12), anchor, _br(pts[i][1])))
    # hit targets (one column per point) for the tooltip
    colw = (W - L - R) / (n - 1)
    for i, (lab, v) in enumerate(pts):
        g.append('<rect class="cj-hit" data-i="%d" x="%.1f" y="%d" width="%.1f" height="%d" fill="transparent"/>' % (i, x(i) - colw / 2, T, colw, H - T - B))
    g.append('<line class="cj-cross" x1="0" x2="0" y1="%d" y2="%d" stroke="#6f7480" stroke-width="1" visibility="hidden"/>' % (T, H - B))
    svg = ('<svg viewBox="0 0 %d %d" class="w-full h-auto" role="img" aria-labelledby="cj-tit cj-desc" font-family="Inter, sans-serif">'
           '<title id="cj-tit">Curva de juros prefixada no Brasil, %s</title>'
           '<desc id="cj-desc">Taxa de %s%% a.a. em %s, máxima de %s%% a.a. em %s e %s%% a.a. em %s.</desc>%s</svg>') % (
               W, H, c['data'], _br(pts[0][1]), pts[0][0], _br(pts[imax][1]), pts[imax][0], _br(pts[-1][1]), pts[-1][0], ''.join(g))
    linhas = ''.join('<tr class="border-t border-outline-variant"><td class="py-1 pr-4">%s%s</td><td class="py-1 text-right tabular-nums">%s%%</td></tr>' % (lab, ' (estimado)' if lab in est else '', _br(v, 4)) for lab, v in pts)
    dados = ','.join('["%s",%s,%d]' % (lab, v, 1 if lab in est else 0) for lab, v in pts)
    js = ('(function(){var d=[' + dados + '],box=document.getElementById("cj"),tip=document.getElementById("cj-tip"),svg=box.querySelector("svg"),cross=svg.querySelector(".cj-cross");'
          'function f(v){return v.toFixed(2).replace(".",",")}'
          'svg.querySelectorAll(".cj-hit").forEach(function(r){r.addEventListener("pointerenter",function(){var i=+r.dataset.i,b=r.getBBox(),cx=b.x+b.width/2,s=box.clientWidth/' + str(W) + ';'
          'cross.setAttribute("x1",cx);cross.setAttribute("x2",cx);cross.setAttribute("visibility","visible");'
          'tip.textContent=d[i][0]+": "+f(d[i][1])+"% a.a."+(d[i][2]?" (estimado)":"");tip.classList.remove("hidden");'
          'var left=cx*s-tip.offsetWidth/2;left=Math.max(0,Math.min(box.clientWidth-tip.offsetWidth,left));tip.style.left=left+"px";tip.style.top="0px";});});'
          'svg.addEventListener("pointerleave",function(){tip.classList.add("hidden");cross.setAttribute("visibility","hidden");});})();')
    return ('<figure class="flex flex-col gap-2 my-space-xs">'
            '<div class="bg-white rounded-xl shadow-sm p-space-sm sm:p-space-md">'
            '<p class="font-body-md text-body-md font-semibold text-on-surface">Curva de juros prefixada no Brasil</p>'
            '<p class="font-body-sm text-body-sm text-on-surface-variant mb-2">% a.a., base 252, por prazo</p>'
            '<div class="relative" id="cj">' + svg +
            '<div id="cj-tip" class="pointer-events-none absolute hidden rounded-md bg-[#13233a] px-2 py-1 text-[13px] text-white shadow-md whitespace-nowrap"></div></div>'
            '<details class="mt-2 font-body-sm text-body-sm text-on-surface-variant"><summary class="cursor-pointer text-secondary">Ver dados em tabela</summary>'
            '<table class="mt-2 w-full max-w-xs"><thead><tr><th class="text-left py-1 pr-4 font-semibold">Prazo</th><th class="text-right py-1 font-semibold">Taxa</th></tr></thead><tbody>' + linhas + '</tbody></table></details>'
            '</div>'
            '<figcaption class="font-body-sm text-body-sm text-on-surface-variant">Fonte: ' + c['fonte'] + ', fechamento de ' + c['data'] + '.'
            + ((' Os prazos de ' + ' e '.join(sorted(est, key=[l for l, _ in pts].index)) + ' (pontos vazados) são estimados, não oficiais.') if est else '')
            + ((' ' + c['nota']) if c.get('nota') else '')
            + '</figcaption></figure>'
            '<script>' + js + '</script>')

GRAFICO = grafico_curva(CURVA)
REFS = ('<p class="font-body-sm text-body-sm text-outline border-t border-outline-variant pt-space-sm">'
        'Esse tema é discutido tanto em referências clássicas de economia monetária e renda fixa, como Mishkin e Fabozzi, quanto em trabalhos como '
        'Campbell &amp; Shiller (1991), Diebold &amp; Li (2006), Tabak &amp; Tabata (2004), Shousha (2008) e estudos do Banco Central sobre a estrutura a termo das taxas de juros.</p>')

T_ECON = 'Sua empresa precisa de um economista?'
T_CURVA = 'Além da Selic: o que a curva de juros mostra'

art_econ = artigo('artigo', T_ECON, paras(ECONOMISTA))
art_curva = artigo('artigo', T_CURVA, paras(CURVA_A) + '\n' + GRAFICO + '\n' + paras(CURVA_B), REFS)


CTRL_A = """
A Controladoria Estratégica vai muito além de acompanhar resultados, elaborar relatórios e garantir a conformidade dos processos. Seu verdadeiro papel é conectar informações financeiras, indicadores de desempenho e planejamento estratégico para apoiar decisões mais assertivas.

Em um mercado cada vez mais dinâmico, não basta saber quanto a empresa faturou ou gastou. É preciso compreender por que os resultados aconteceram, quais riscos estão envolvidos e quais oportunidades podem impulsionar o crescimento.

É nesse contexto que a Controladoria se torna uma parceira estratégica da gestão, contribuindo para:
"""
CTRL_LISTA = [('query_stats', 'Decisões baseadas em dados confiáveis'),
              ('track_changes', 'Planejamento orçamentário e acompanhamento de indicadores'),
              ('savings', 'Otimização de custos e melhoria da rentabilidade'),
              ('trending_up', 'Análise de cenários e antecipação de riscos'),
              ('handshake', 'Alinhamento entre estratégia, operação e resultados')]
CTRL_B = """
Quando integrada ao Business Intelligence, a Controladoria amplia sua capacidade analítica, transforma dados em informações relevantes e oferece à liderança uma visão mais clara do negócio.

Afinal, controlar é entender o presente. Planejar é preparar o futuro. E a estratégia está em conectar os dois para gerar resultados sustentáveis.
"""
CTRL_FECHO = ('<p class="font-headline-sm text-headline-sm italic text-on-surface border-l-4 border-secondary pl-space-md">'
              'Controladoria estratégica não é apenas explicar os números do passado. É contribuir para construir os resultados do futuro.</p>')
lista_ctrl = ('<ul class="flex flex-col gap-2 bg-surface-container p-space-md rounded-xl shadow-sm">' +
              ''.join('<li class="flex items-center gap-3 text-on-surface"><span class="material-symbols-outlined text-[22px] text-secondary">%s</span>%s</li>' % it for it in CTRL_LISTA) +
              '</ul>')
T_CTRL = 'Controladoria Estratégica: transformar números em decisões que geram valor'
CTRL_IMG = ('<figure><img class="w-full h-auto rounded-xl shadow-sm" src="/img/controladoria-estrategica.webp" width="800" height="784" '
            'alt="Arte Controladoria Estratégica: mais do que números, é sobre decisões melhores. Controlar hoje, para crescer amanhã."/></figure>')
art_ctrl = artigo('artigo', T_CTRL, CTRL_IMG + '\n' + paras(CTRL_A) + '\n' + lista_ctrl + '\n' + paras(CTRL_B) + '\n' + CTRL_FECHO)

def card(href, titulo, resumo, icon, img=None):
    if img:
        top = ('<div class="-mx-space-md -mt-space-md mb-1 h-44 overflow-hidden">'
               '<img class="w-full h-full object-cover object-top" src="%s" alt="" loading="lazy"/></div>' % img)
    else:
        top = '<span class="material-symbols-outlined text-[26px] text-secondary">%s</span>' % icon
    return ('<a class="group bg-surface-container p-space-md rounded-xl shadow-sm flex flex-col gap-2 hover:shadow-md transition-shadow overflow-hidden" href="%s">' % href
            + top +
            '<span class="font-label-badge text-label-badge uppercase tracking-widest text-secondary">Artigo</span>'
            '<h2 class="font-headline-sm text-headline-sm text-on-surface group-hover:text-secondary">%s</h2>'
            '<p class="font-body-md text-body-md text-on-surface-variant">%s</p>'
            '<span class="mt-auto inline-flex items-center gap-1 font-label-executive text-label-executive uppercase tracking-wider text-secondary">Ler artigo'
            '<span class="material-symbols-outlined text-[16px]">arrow_forward</span></span></a>' % (titulo, resumo))

lista = ('<!-- ==================== LISTA DE ARTIGOS ==================== -->\n'
         '<section id="artigos" class="px-margin-mobile py-space-xl flex flex-col gap-space-md">'
         '<div class="flex flex-col gap-space-xs">'
         '<span class="font-label-badge text-label-badge uppercase tracking-widest text-secondary">Conteúdo</span>'
         '<h1 class="font-headline-lg text-headline-lg text-on-surface">Notícias e Artigos</h1></div>'
         '<div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-space-md">'
         + card('/noticias/controladoria-estrategica', T_CTRL, 'Mais do que relatórios: como a controladoria conecta números, indicadores e estratégia para apoiar decisões que geram valor.', 'monitoring', '/img/controladoria-capa.webp')
         + card('/noticias/economista-na-empresa', T_ECON, 'Economia de empresas vai muito além de câmbio, juros e inflação, e é a empresa familiar de médio porte que mais perde sem essa leitura.', 'domain')
         + card('/noticias/curva-de-juros', T_CURVA, 'A diferença entre o juro de hoje e os juros que o mercado negocia para o futuro, e o que isso muda para a sua empresa.', 'show_chart')
         + '</div></section>\n')

for name, frag in [('art_ctrl.html', art_ctrl), ('art_econ.html', art_econ), ('art_curva.html', art_curva), ('noticias_lista.html', lista)]:
    open(os.path.join(D, name), 'w', encoding='utf-8').write(frag)
print('ok')
