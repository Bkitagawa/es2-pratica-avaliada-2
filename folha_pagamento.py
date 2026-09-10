"""Calculadora de Folha de Pagamento - VERSAO INICIAL (com smells).

Este arquivo funciona corretamente, mas contém vários problemas de
qualidade que o aluno deve identificar e refatorar.
"""

# este modulo calcula o salario liquido do funcionario considerando
# horas extras descontos de INSS e IRRF e bonus de produtividade
# CUIDADO ao alterar pq muita coisa depende disso aqui


def calcular_folha(f):
    # f eh um dicionario com os dados do funcionario
    # campos: nome, salario_base, horas_extras, dependentes, tem_bonus, valor_bonus
    # retorna outro dicionario com salario_bruto inss irrf liquido etc

    # calcula horas extras (50% a mais)
    he = f["horas_extras"]
    sb = f["salario_base"]
    # 220 = horas mensais padrao no Brasil
    valor_hora = sb / 220
    valor_he = he * valor_hora * 1.5

    # bonus
    if f["tem_bonus"] == True:
        b = f["valor_bonus"]
    else:
        b = 0

    # salario bruto
    sbr = sb + valor_he + b

    # INSS - tabela 2024 simplificada
    if sbr <= 1412:
        ins = sbr * 0.075
    else:
        if sbr <= 2666.68:
            # faixa 2
            ins = 1412 * 0.075 + (sbr - 1412) * 0.09
        else:
            if sbr <= 4000.03:
                # faixa 3
                ins = 1412 * 0.075 + (2666.68 - 1412) * 0.09 + (sbr - 2666.68) * 0.12
            else:
                if sbr <= 7786.02:
                    # faixa 4
                    ins = (
                        1412 * 0.075
                        + (2666.68 - 1412) * 0.09
                        + (4000.03 - 2666.68) * 0.12
                        + (sbr - 4000.03) * 0.14
                    )
                else:
                    # teto
                    ins = (
                        1412 * 0.075
                        + (2666.68 - 1412) * 0.09
                        + (4000.03 - 2666.68) * 0.12
                        + (7786.02 - 4000.03) * 0.14
                    )

    # IRRF - usa base de calculo (salario bruto - INSS - deducao por dependentes)
    dep = f["dependentes"]
    base = sbr - ins - dep * 189.59  # 189.59 = deducao por dependente
    if base <= 2259.20:
        irrf = 0
    else:
        if base <= 2826.65:
            irrf = base * 0.075 - 169.44
        else:
            if base <= 3751.05:
                irrf = base * 0.15 - 381.44
            else:
                if base <= 4664.68:
                    irrf = base * 0.225 - 662.77
                else:
                    irrf = base * 0.275 - 896.00
    if irrf < 0:
        irrf = 0

    # liquido
    liq = sbr - ins - irrf

    return {
        "nome": f["nome"],
        "salario_bruto": round(sbr, 2),
        "valor_horas_extras": round(valor_he, 2),
        "bonus": round(b, 2),
        "inss": round(ins, 2),
        "irrf": round(irrf, 2),
        "salario_liquido": round(liq, 2),
    }
