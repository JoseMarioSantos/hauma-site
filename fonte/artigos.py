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
GRAFICO = ('<figure class="flex flex-col gap-2 my-space-xs">'
           '<img class="w-full h-auto rounded-xl shadow-sm bg-white" src="/img/curva-juros-anbima.webp" width="886" height="483" loading="lazy" '
           'alt="Gráfico da curva de juros prefixada no Brasil (ETTJ PRE, ANBIMA), fechamento de 02/09/2026: taxa de 13,64% a.a. em 1 mês, mínima de 13,35% em 6 meses e alta até 14,55% a.a. em 7,5 anos."/>'
           '<figcaption class="font-body-sm text-body-sm text-on-surface-variant">Curva prefixada (ETTJ PRE, ANBIMA), fechamento de 02/09/2026.</figcaption></figure>')
REFS = ('<p class="font-body-sm text-body-sm text-outline border-t border-outline-variant pt-space-sm">'
        'Esse tema é discutido tanto em referências clássicas de economia monetária e renda fixa, como Mishkin e Fabozzi, quanto em trabalhos como '
        'Campbell &amp; Shiller (1991), Diebold &amp; Li (2006), Tabak &amp; Tabata (2004), Shousha (2008) e estudos do Banco Central sobre a estrutura a termo das taxas de juros.</p>')

T_ECON = 'Sua empresa precisa de um economista?'
T_CURVA = 'Além da Selic: o que a curva de juros mostra'

art_econ = artigo('artigo', T_ECON, paras(ECONOMISTA))
art_curva = artigo('artigo', T_CURVA, paras(CURVA_A) + '\n' + GRAFICO + '\n' + paras(CURVA_B), REFS)

def card(href, titulo, resumo, icon):
    return ('<a class="group bg-surface-container p-space-md rounded-xl shadow-sm flex flex-col gap-2 hover:shadow-md transition-shadow" href="%s">'
            '<span class="material-symbols-outlined text-[26px] text-secondary">%s</span>'
            '<span class="font-label-badge text-label-badge uppercase tracking-widest text-secondary">Artigo</span>'
            '<h2 class="font-headline-sm text-headline-sm text-on-surface group-hover:text-secondary">%s</h2>'
            '<p class="font-body-md text-body-md text-on-surface-variant">%s</p>'
            '<span class="mt-auto inline-flex items-center gap-1 font-label-executive text-label-executive uppercase tracking-wider text-secondary">Ler artigo'
            '<span class="material-symbols-outlined text-[16px]">arrow_forward</span></span></a>') % (href, icon, titulo, resumo)

lista = ('<!-- ==================== LISTA DE ARTIGOS ==================== -->\n'
         '<section id="artigos" class="px-margin-mobile py-space-xl flex flex-col gap-space-md">'
         '<div class="flex flex-col gap-space-xs">'
         '<span class="font-label-badge text-label-badge uppercase tracking-widest text-secondary">Conteúdo</span>'
         '<h1 class="font-headline-lg text-headline-lg text-on-surface">Notícias e Artigos</h1></div>'
         '<div class="grid sm:grid-cols-2 gap-space-md">'
         + card('/noticias/economista-na-empresa', T_ECON, 'Economia de empresas vai muito além de câmbio, juros e inflação, e é a empresa familiar de médio porte que mais perde sem essa leitura.', 'domain')
         + card('/noticias/curva-de-juros', T_CURVA, 'A diferença entre o juro de hoje e os juros que o mercado negocia para o futuro, e o que isso muda para a sua empresa.', 'show_chart')
         + '</div></section>\n')

for name, frag in [('art_econ.html', art_econ), ('art_curva.html', art_curva), ('noticias_lista.html', lista)]:
    open(os.path.join(D, name), 'w', encoding='utf-8').write(frag)
print('ok')
