"""Calculadora de Folha de Pagamento - VERSAO INICIAL (com smells).

Este arquivo funciona corretamente, mas contém vários problemas de
qualidade que o aluno deve identificar e refatorar.
"""

HORAS_MENSAIS = 220
ADICIONAL_HORA_EXTRA = 1.5
DEDUCAO_POR_DEPENDENTE = 189.59

# (limite_superior_da_faixa, aliquota)
FAIXAS_INSS = (
    (1412.00, 0.075),
    (2666.68, 0.09),
    (4000.03, 0.12),
    (7786.02, 0.14),
)

# (limite_superior_da_faixa, aliquota, parcela_a_deduzir)
FAIXAS_IRRF = (
    (2259.20, 0.0, 0.0),
    (2826.65, 0.075, 169.44),
    (3751.05, 0.15, 381.44),
    (4664.68, 0.225, 662.77),
    (float("inf"), 0.275, 896.00),
)

# este modulo calcula o salario liquido do funcionario considerando
# horas extras descontos de INSS e IRRF e bonus de produtividade
# CUIDADO ao alterar pq muita coisa depende disso aqui


def calcular_folha(funcionario):
    # funcionario eh um dicionario com os dados do funcionario
    # campos: nome, salario_base, horas_extras, dependentes, tem_bonus, valor_bonus
    # retorna outro dicionario com salario_bruto inss irrf liquido etc

    # calcula horas extras (50% a mais)
    horas_extras = funcionario["horas_extras"]
    salario_base = funcionario["salario_base"]
    # 220 = horas mensais padrao no Brasil
    valor_da_hora = salario_base / HORAS_MENSAIS
    valor_horas_extras = horas_extras * valor_da_hora * ADICIONAL_HORA_EXTRA

    # bonus
    if funcionario["tem_bonus"] == True:
        bonus = funcionario["valor_bonus"]
    else:
        bonus = 0

    # salario bruto
    salario_bruto = salario_base + valor_horas_extras + bonus

    # INSS - tabela 2024 simplificada
    contribuicao = 0
    piso_da_faixa = 0
    for teto_da_faixa, aliquota in FAIXAS_INSS:
        if salario_bruto <= teto_da_faixa:
            inss = contribuicao + (salario_bruto - piso_da_faixa) * aliquota
            break
        contribuicao += (teto_da_faixa - piso_da_faixa) * aliquota
        piso_da_faixa = teto_da_faixa
    else:
        inss = contribuicao

    # IRRF - usa base_irrf de calculo (salario bruto - INSS - deducao por dependentes)
    dependentes = funcionario["dependentes"]
    base_irrf = salario_bruto - inss - dependentes * DEDUCAO_POR_DEPENDENTE
    for teto_da_faixa, aliquota, parcela_a_deduzir in FAIXAS_IRRF:
        if base_irrf <= teto_da_faixa:
            irrf = max(base_irrf * aliquota - parcela_a_deduzir, 0)
            break

    # liquido
    salario_liquido = salario_bruto - inss - irrf

    return {
        "nome": funcionario["nome"],
        "salario_bruto": round(salario_bruto, 2),
        "valor_horas_extras": round(valor_horas_extras, 2),
        "bonus": round(bonus, 2),
        "inss": round(inss, 2),
        "irrf": round(irrf, 2),
        "salario_liquido": round(salario_liquido, 2),
    }
