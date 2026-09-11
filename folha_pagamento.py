"""Calculo da folha de pagamento mensal: horas extras, bonus, INSS e IRRF."""

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

def calcular_valor_horas_extras(salario_base, horas_extras):
    valor_da_hora = salario_base / HORAS_MENSAIS
    return horas_extras * valor_da_hora * ADICIONAL_HORA_EXTRA


def calcular_bonus(tem_bonus, valor_bonus):
    return valor_bonus if tem_bonus else 0


def calcular_inss(salario_bruto):
    contribuicao = 0
    piso_da_faixa = 0
    for teto_da_faixa, aliquota in FAIXAS_INSS:
        if salario_bruto <= teto_da_faixa:
            return contribuicao + (salario_bruto - piso_da_faixa) * aliquota
        contribuicao += (teto_da_faixa - piso_da_faixa) * aliquota
        piso_da_faixa = teto_da_faixa
    return contribuicao


def calcular_base_irrf(salario_bruto, inss, dependentes):
    return salario_bruto - inss - dependentes * DEDUCAO_POR_DEPENDENTE


def calcular_irrf(base_de_calculo):
    for teto_da_faixa, aliquota, parcela_a_deduzir in FAIXAS_IRRF:
        if base_de_calculo <= teto_da_faixa:
            return max(base_de_calculo * aliquota - parcela_a_deduzir, 0)
    return 0
    
def calcular_folha(funcionario):
    salario_base = funcionario["salario_base"]
    valor_horas_extras = calcular_valor_horas_extras(salario_base, funcionario["horas_extras"])
    bonus = calcular_bonus(funcionario["tem_bonus"], funcionario["valor_bonus"])
    salario_bruto = salario_base + valor_horas_extras + bonus

    inss = calcular_inss(salario_bruto)
    base_irrf = calcular_base_irrf(salario_bruto, inss, funcionario["dependentes"])
    irrf = calcular_irrf(base_irrf)
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
