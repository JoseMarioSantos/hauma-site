# Dados da curva de juros exibida no artigo. Para atualizar, troque a data e os pontos.
CURVA = {
    'data': '19/11/2026',
    'fonte': 'ETTJ PRE – ANBIMA',
    # 1 e 3 meses vêm da tabela PREFIXADOS (Circular 3.361) da mesma página da ANBIMA
    'nota': 'Prazos de 1 e 3 meses: tabela de prefixados (Circular 3.361) da mesma publicação.',
    # prazos cujo valor é estimado (não oficial). Ao obter os valores oficiais, troque os números e esvazie esta lista.
    'estimados': [],
    'pontos': [
        ('1 mês', 13.6239), ('3 meses', 13.8305), ('6 meses', 14.1392),
        ('1 ano', 14.6636), ('2 anos', 15.2958), ('3 anos', 15.5826),
        ('4 anos', 15.7016), ('5 anos', 15.7362), ('7,5 anos', 15.6785),
        ('10 anos', 15.5733),
    ],
}
