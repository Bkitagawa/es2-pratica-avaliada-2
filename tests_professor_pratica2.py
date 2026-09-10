"""Testes do professor — Prática Avaliada 2 ES2.

Verificam que o comportamento da função `calcular_folha` foi preservado
após a refatoração do aluno. A API pública obrigatória é:

    calcular_folha(funcionario: dict) -> dict

com os mesmos campos de entrada e saída do arquivo original
folha_pagamento.py.
"""

import pytest

from folha_pagamento import calcular_folha


def _func(salario_base, horas_extras=0, dependentes=0, tem_bonus=False, valor_bonus=0):
    return {
        "nome": "Funcionario Teste",
        "salario_base": salario_base,
        "horas_extras": horas_extras,
        "dependentes": dependentes,
        "tem_bonus": tem_bonus,
        "valor_bonus": valor_bonus,
    }


class TestCalculoBasico:
    def test_retorna_dicionario_com_campos_obrigatorios(self) -> None:
        r = calcular_folha(_func(3000))
        for campo in (
            "nome",
            "salario_bruto",
            "valor_horas_extras",
            "bonus",
            "inss",
            "irrf",
            "salario_liquido",
        ):
            assert campo in r

    def test_preserva_nome(self) -> None:
        r = calcular_folha(_func(3000))
        assert r["nome"] == "Funcionario Teste"

    def test_salario_base_simples_sem_extras_sem_bonus(self) -> None:
        # 3000 bruto, INSS faixa 3
        r = calcular_folha(_func(3000))
        assert r["salario_bruto"] == 3000
        assert r["bonus"] == 0
        assert r["valor_horas_extras"] == 0


class TestHorasExtras:
    def test_horas_extras_50_por_cento(self) -> None:
        # salario 2200 -> valor_hora = 10 -> 10h extras = 10 * 10 * 1.5 = 150
        r = calcular_folha(_func(2200, horas_extras=10))
        assert r["valor_horas_extras"] == 150.0

    def test_horas_extras_compoem_bruto(self) -> None:
        r = calcular_folha(_func(2200, horas_extras=10))
        assert r["salario_bruto"] == 2200 + 150


class TestBonus:
    def test_bonus_aplicado(self) -> None:
        r = calcular_folha(_func(3000, tem_bonus=True, valor_bonus=500))
        assert r["bonus"] == 500
        assert r["salario_bruto"] == 3500

    def test_bonus_desativado_nao_aplica(self) -> None:
        r = calcular_folha(_func(3000, tem_bonus=False, valor_bonus=500))
        assert r["bonus"] == 0


class TestINSS:
    def test_inss_faixa_1(self) -> None:
        # 1400 -> faixa 1 (7.5%)
        r = calcular_folha(_func(1400))
        assert r["inss"] == round(1400 * 0.075, 2)

    def test_inss_faixa_2(self) -> None:
        # 2000 -> faixa 2: 1412 * 0.075 + (2000 - 1412) * 0.09
        esperado = round(1412 * 0.075 + (2000 - 1412) * 0.09, 2)
        r = calcular_folha(_func(2000))
        assert r["inss"] == esperado

    def test_inss_teto(self) -> None:
        # salario alto: INSS bate no teto
        teto = round(
            1412 * 0.075
            + (2666.68 - 1412) * 0.09
            + (4000.03 - 2666.68) * 0.12
            + (7786.02 - 4000.03) * 0.14,
            2,
        )
        r = calcular_folha(_func(10000))
        assert r["inss"] == teto


class TestIRRF:
    def test_irrf_isento(self) -> None:
        # 2000 bruto, INSS ~196.92, base ~1803 -> isento
        r = calcular_folha(_func(2000))
        assert r["irrf"] == 0

    def test_irrf_aplica_em_salario_medio_alto(self) -> None:
        r = calcular_folha(_func(5000))
        assert r["irrf"] > 0

    def test_irrf_nunca_negativo(self) -> None:
        r = calcular_folha(_func(2200, dependentes=5))
        assert r["irrf"] >= 0


class TestDependentes:
    def test_dependentes_reduzem_irrf(self) -> None:
        sem = calcular_folha(_func(5000, dependentes=0))
        com = calcular_folha(_func(5000, dependentes=3))
        assert com["irrf"] < sem["irrf"]


class TestSalarioLiquido:
    def test_liquido_eh_bruto_menos_descontos(self) -> None:
        r = calcular_folha(_func(3000, horas_extras=5, tem_bonus=True, valor_bonus=200))
        esperado = round(r["salario_bruto"] - r["inss"] - r["irrf"], 2)
        assert r["salario_liquido"] == esperado

    def test_cenario_completo(self) -> None:
        # Cenário com todos os componentes ativos
        r = calcular_folha(
            _func(4000, horas_extras=10, dependentes=2, tem_bonus=True, valor_bonus=300)
        )
        assert r["salario_bruto"] > 0
        assert r["valor_horas_extras"] > 0
        assert r["bonus"] == 300
        assert r["inss"] > 0
        assert r["salario_liquido"] > 0
        assert r["salario_liquido"] < r["salario_bruto"]
