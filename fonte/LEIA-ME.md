# Fonte das páginas do site

As páginas em `public/` são geradas a partir destes arquivos:

- `base.html`: página original com todas as seções (cabeçalho, rodapé e seções numeradas)
- `quem.html`, `servicos.html`, `como.html`: seções reescritas
- `artigos.py`: gera `art_econ.html`, `art_curva.html` e `noticias_lista.html`

Para gerar de novo (na raiz do projeto):

    python fonte/artigos.py
    python fonte/split.py fonte/base.html public

O menu e a lista de páginas ficam em `split.py` (`MENU` e `PAGES`).
