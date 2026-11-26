# Fonte das páginas do site

As páginas em `public/` são geradas a partir destes arquivos:

- `base.html`: página original com todas as seções (cabeçalho, rodapé e seções numeradas)
- `quem.html`, `servicos.html`, `como.html`: seções reescritas
- `artigos.py`: gera `art_econ.html`, `art_curva.html` e `noticias_lista.html`

Para gerar de novo (na raiz do projeto):

    python fonte/artigos.py
    python fonte/split.py fonte/base.html public

O menu e a lista de páginas ficam em `split.py` (`MENU` e `PAGES`).

## Demonstração do Motor de Modelagem HAUMA

A página `/servicos/motor-de-modelagem-demonstracao` (modelo diferente da ferramenta Modelagem de A a Z) é gerada a partir do modelo HTML completo, que fica **fora deste repositório** (o repositório é público):

    node fonte/demo/gerar_demo.js "C:\Users\jmari\OneDrive\BUDGET TELLO\Modelo_Financeiro_Modelagem_Completa.html"

O gerador calcula os 4 cenários no computador e grava só os **resultados** na página; o motor de cálculo não vai para o site. As premissas aparecem em modo leitura. Rode de novo sempre que o modelo mudar. Nunca copie o modelo completo para dentro desta pasta.
