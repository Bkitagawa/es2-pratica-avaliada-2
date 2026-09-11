# Relatorio de Refactoring - Pratica Avaliada 2 (ES2)

**Aluno:** Bruno Tavares Kitagawa
**Modulo:** 7 - Unidades 3, 4, 5 e 6
**Repositorio:** https://github.com/Bkitagawa/es2-pratica-avaliada-2

Todas as referencias de linha sao do commit `964a330` (codigo original, antes da refatoracao).

---

## a) Smells identificados

### 1. Long Function
- **Localizacao:** `calcular_folha`, linhas 12-92 (81 linhas em uma unica funcao).
- **Por que e um smell:** [ESCREVA: 1-2 frases suas sobre por que uma funcao desse tamanho e um problema]

### 2. Magic Numbers
- **Localizacao:** linhas 21 (`220`), 22 (`1.5`), 64 (`189.59`), 34-60 e 65-77 (faixas de INSS e IRRF).
- **Por que e um smell:** [ESCREVA: por que numero solto no meio do codigo e problema de manutencao]

### 3. Mysterious Name
- **Localizacao:** linhas 12, 18-31, 63-64, 82 - identificadores `f`, `sb`, `he`, `valor_he`, `b`, `sbr`, `ins`, `dep`, `base`, `liq`.
- **Por que e um smell:** [ESCREVA: por que abreviacao nao obvia custa tempo de leitura]

### 4. Nested Conditional
- **Localizacao:** linhas 34-60 (INSS, 5 niveis de `if` aninhado) e 65-77 (IRRF, 4 niveis).
- **Por que e um smell:** [ESCREVA: por que o aninhamento profundo dificulta o entendimento]

### 5. Duplicated Code
- **Localizacao:** linhas 43, 47-52 e 55-60 - a soma `1412*0.075 + (2666.68-1412)*0.09 + ...` repetida em tres ramos.
- **Por que e um smell:** [ESCREVA: qual o risco de manter a mesma conta em tres lugares]

### 6. Comments
- **Localizacao:** linhas 7-9, 13-15, 17, 20, 24, 30, 33, 38, 42, 54, 62, 64 - incluindo `# CUIDADO ao alterar pq muita coisa depende disso aqui`.
- **Por que e um smell:** [ESCREVA: quando o comentario esta tapando um nome ruim em vez de informar]

---

## b) Refactorings aplicados

### 1. Rename Variable - commit `5963e93`
- **Smell que resolve:** Mysterious Name
- **Antes -> Depois:** `f` -> `funcionario`, `sb` -> `salario_base`, `he` -> `horas_extras`, `valor_he` -> `valor_horas_extras`, `valor_hora` -> `valor_da_hora`, `b` -> `bonus`, `sbr` -> `salario_bruto`, `ins` -> `inss`, `dep` -> `dependentes`, `base` -> `base_irrf`, `liq` -> `salario_liquido` (11 identificadores; 38 insercoes, 38 delecoes).
- **Observacao:** [ESCREVA: o que mudou na leitura do codigo depois disso]

### 2. Replace Magic Number with Symbolic Constant - commit `a54d4aa`
- **Smell que resolve:** Magic Numbers
- **Antes -> Depois:** `220` -> `HORAS_MENSAIS`, `1.5` -> `ADICIONAL_HORA_EXTRA`, `189.59` -> `DEDUCAO_POR_DEPENDENTE`; as faixas viraram as tabelas `FAIXAS_INSS` e `FAIXAS_IRRF`, declaradas uma unica vez no topo do modulo.
- **Observacao:** [ESCREVA: o que acontece agora se a tabela do INSS mudar de ano]

### 3. Decompose Conditional + Replace Conditional with Table Lookup - commit `2e84290`
- **Smell que resolve:** Nested Conditional e Duplicated Code
- **Antes -> Depois:** os dois blocos de `if` aninhado foram substituidos por lacos sobre `FAIXAS_INSS` e `FAIXAS_IRRF`. 41 linhas removidas, 13 adicionadas. O clamp `if irrf < 0: irrf = 0` virou `max(..., 0)`.
- **Observacao:** [ESCREVA: por que voce manteve o clamp em vez de apagar - a explicacao da fronteira de 2.259,20]

### 4. Extract Function - commit `ab84c4a`
- **Smell que resolve:** Long Function
- **Antes -> Depois:** `calcular_folha` (81 linhas) foi decomposta em `calcular_valor_horas_extras`, `calcular_bonus`, `calcular_inss`, `calcular_base_irrf` e `calcular_irrf`. `calcular_folha` passou a ter 9 linhas de orquestracao mais o dicionario de retorno.
- **Observacao:** [ESCREVA: o que a funcao calcular_folha comunica agora que antes nao comunicava]

### 5. Remove Comments - commit `524f461`
- **Smell que resolve:** Comments
- **Antes -> Depois:** 12 comentarios band-aid removidos. Sobraram 2, que descrevem o formato das tuplas das tabelas de faixa - informacao que nome nenhum carrega.
- **Observacao:** [ESCREVA: qual o criterio que voce usou para decidir o que apagar e o que manter]

---

## Decisoes conscientes

[ESCREVA: comente a troca de `if funcionario["tem_bonus"] == True` por `if tem_bonus` - comparacao redundante com booleano]

[ESCREVA: comente por que voce NAO trocou float por Decimal, mesmo sendo a escolha correta em producao - seria mudanca de comportamento observavel, que o enunciado proibe]

---

## c) Reflexao sobre legibilidade

[ESCREVA: 1 paragrafo. Ganchos possiveis - nomes significativos (Unidade 6 / Clean Code), funcoes pequenas com responsabilidade unica, nivel de abstracao consistente em calcular_folha. O melhor exemplo concreto que voce tem e o comentario "CUIDADO ao alterar pq muita coisa depende disso aqui": era um aviso de medo, escrito porque ninguem entendia o codigo. Voce nao o apagou por capricho - ele deixou de ter objeto quando o codigo passou a se explicar sozinho.]

---

## Verificacao de equivalencia (Q3)

Os 16 testes do professor passam no estado final: `pytest tests_professor_pratica2.py -v` -> 16 passed.

Alem disso, foi usado um golden master como rede de seguranca durante toda a refatoracao: um script de conferencia executou `calcular_folha` em 222.384 combinacoes de salario base, horas extras, dependentes e bonus antes da primeira alteracao, gravou os resultados, e comparou apos cada commit. Divergencias: 0 em todos os passos.
