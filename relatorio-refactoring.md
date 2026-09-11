# Relatorio de Refactoring - Pratica Avaliada 2 (ES2)

**Aluno:** Bruno Tavares Kitagawa
**Modulo/Semana:** 7 - Unidades 3, 4, 5 e 6
**Repositorio:** https://github.com/Bkitagawa/es2-pratica-avaliada-2

Todas as referencias de linha sao do commit `964a330`, o codigo original antes da refatoracao.

---

## Contexto e metodo

A PayrollFlex mantinha uma calculadora de folha de pagamento correta e intocavel: 92 linhas,
uma unica funcao de 81 linhas, cinco niveis de `if` aninhado, e um comentario no topo que
resumia o estado da coisa - `# CUIDADO ao alterar pq muita coisa depende disso aqui`.

A restricao do exercicio e refatorar sem alterar uma casa decimal: `calcular_folha(funcionario: dict) -> dict`
e contrato, com a mesma assinatura e os mesmos sete campos de retorno.

Os 16 testes do professor cobrem 16 situacoes. Antes de tocar em uma linha, construi um
**golden master**: um script que executou `calcular_folha` em 222.384 combinacoes de salario
base, horas extras, dependentes e bonus, gravou os resultados em JSON, e comparou o codigo
refatorado contra esse retrato apos cada commit. A rede de seguranca se pagou: ao simular a
armadilha mais provavel do exercicio - arredondar dentro das funcoes extraidas em vez de
apenas na saida - o golden master acusou 17.249 divergencias que os 16 testes deixam passar
em silencio.

---

## a) Smells identificados

### 1. Long Function
- **Localizacao:** `calcular_folha`, linhas 12-92 (81 linhas em uma unica funcao).
- **Por que e um smell:** para entender o calculo do salario liquido era preciso ler as 81
  linhas seguidas, porque seis responsabilidades diferentes estavam intercaladas - Tínhamos um problema que 6 decisões diferentes moravam no mesmo lugar.
  Mexendo no INSS, rolei 20 linhas para cima para descobrir que 'sbr' = salário base + horas extras + bônus. Não havia uma documentação me dizendo isso. Tive que reconstruir tudo dentro da minha cabeça.
  Numa função de responsabilidade única, essa informação estaria no nome do parâmetro. Consequencia: Qualquer alteração exigia entender o arquivo inteiro, e por isso ninguém se arriscava.

### 2. Magic Numbers
- **Localizacao:** linhas 21 (`220`), 22 (`1.5`), 64 (`189.59`), e as faixas nas linhas 34-60 e 65-77.
- **Por que e um smell:** `1412` aparece oito vezes no arquivo original, sem nenhuma indicacao
  do que representa - 1412 aparece oito vezes. Não é um número, é o teto da primeira faixa do INSS de 2024.
  O código não dizia isso em lugar algum. 
  Caso a tabela mudasse em 2025, eu precisaria achar as oito, decidir uma por uma se aquela ocorrência é o teto da faixa 1 ou o piso da faixa 2, e não errar nenhuma. 
  Um erro silencioso nessa situação produziria holerite errado sem quebrar teste nenhum. Com FAIXAS_INSS, é uma linha.

### 3. Mysterious Name
- **Localizacao:** linhas 12, 18-31, 63-64, 82 - os identificadores `f`, `sb`, `he`, `valor_he`,
  `b`, `sbr`, `ins`, `dep`, `base` e `liq`.
- **Por que e um smell:** `ins` era INSS e `liq` era liquido, mas isso so era obvio para quem
  escreveu.
  ins e liq eram legíveis para quem escreveu naquele dia. 
  Seis meses depois, nem para ele. 
  O caso pior era b e base: um era bônus, o outro era base de cálculo do IRRF, e visualmente são a mesma coisa numa leitura rápida. 
  Nome ruim não é questão de estética — ele transfere para o leitor um trabalho de decodificação que o autor podia ter feito uma vez.

### 4. Nested Conditional
- **Localizacao:** linhas 34-60 (INSS, cinco niveis de `if` aninhado) e 65-77 (IRRF, quatro niveis).
- **Por que e um smell:** para chegar ao ultimo ramo era necessario manter quatro condicoes
  simultaneas na cabeca - Cinco níveis. 
Para entender o ramo do teto, precisei segurar simultaneamente: não é ≤1412, não é ≤2666,68, não é ≤4000,03, não é ≤7786,02. 
Quatro negações na memória de trabalho antes de ler a linha que importa. É aí que erro entra: eu acreditei que estava no ramo certo e estava um nível acima.

### 5. Duplicated Code
- **Localizacao:** linhas 43, 47-52 e 55-60 - a soma `1412*0.075 + (2666.68-1412)*0.09 + ...`
  escrita por extenso em tres ramos diferentes.
- **Por que e um smell:** a mesma regra de calculo existia em tres lugares -
  A soma 1412*0.075 + (2666.68-1412)*0.09 + ... estava escrita por extenso em três ramos. 
  Se o governo mudar a alíquota de 9% para 9,5%, eu preciso acertar os três. 
  Acertar dois e esquecer um dá um bug que só aparece numa faixa salarial específica — o tipo que passa em produção por meses.

### 6. Comments
- **Localizacao:** linhas 7-9, 13-15, 17, 20, 24, 30, 33, 38, 42, 54, 62 e 64.
- **Por que e um smell:** `# faixa 2` estava em cima de um `if` que ja dizia `<= 2666.68`, e
  `# 220 = horas mensais padrao no Brasil` tapava a ausencia de um nome - # faixa 2 em cima de if sbr <= 2666.68: não acrescenta nada — o if já diz. 
  E # 220 = horas mensais padrao no Brasil estava tapando a falta de um nome: se a constante se chamasse HORAS_MENSAIS, o comentário não teria razão de existir. 
  Comentário que repete o código é ruído; comentário que explica um nome ruim é sintoma.

---

## b) Refactorings aplicados

### 1. Rename Variable - commit `5963e93`
- **Smell que resolve:** Mysterious Name
- **Antes -> Depois:** `f` -> `funcionario`, `sb` -> `salario_base`, `he` -> `horas_extras`,
  `valor_he` -> `valor_horas_extras`, `valor_hora` -> `valor_da_hora`, `b` -> `bonus`,
  `sbr` -> `salario_bruto`, `ins` -> `inss`, `dep` -> `dependentes`, `base` -> `base_irrf`,
  `liq` -> `salario_liquido`. Onze identificadores; 38 insercoes e 38 delecoes, ou seja,
  nenhuma linha de logica mudou.
- **Efeito:** 38 inserções, 38 deleções — nenhuma linha de lógica mudou, e mesmo assim o arquivo ficou outro. 
Depois disso consegui ler salario_bruto = salario_base + valor_horas_extras + bonus e entender sem rastrear nada. 
Foi o passo mais barato e o que mais abriu os seguintes: os passos 2, 3 e 4 ficaram óbvios porque o código passou a dizer o que fazia.

### 2. Replace Magic Number with Symbolic Constant - commit `a54d4aa`
- **Smell que resolve:** Magic Numbers
- **Antes -> Depois:** `220` -> `HORAS_MENSAIS`, `1.5` -> `ADICIONAL_HORA_EXTRA`,
  `189.59` -> `DEDUCAO_POR_DEPENDENTE`. As faixas viraram as tabelas `FAIXAS_INSS` e
  `FAIXAS_IRRF`, declaradas uma unica vez no topo do modulo.
- **Efeito:** a tabela do INSS passou a existir em um lugar só, no topo, no formato em que o RH a enxerga: teto e alíquota, linha por linha. Mudança de ano virou edição de cinco números numa tupla, sem tocar em nenhuma linha de cálculo. E foi possível conferir a tabela contra o documento oficial batendo o olho — antes, estava dissolvida dentro de vinte e sete linhas de if.

### 3. Decompose Conditional + Replace Conditional with Table Lookup - commit `2e84290`
- **Smell que resolve:** Nested Conditional e Duplicated Code
- **Antes -> Depois:** os dois blocos de `if` aninhado foram substituidos por lacos sobre
  `FAIXAS_INSS` e `FAIXAS_IRRF`. Saldo: 41 linhas removidas, 13 adicionadas. O clamp
  `if irrf < 0: irrf = 0` virou `max(..., 0)` e foi preservado de proposito, porque a parcela
  a deduzir de 169,44 e exatamente 7,5% de 2.259,20 - na fronteira da faixa a conta da zero e
  o ponto flutuante pode devolver um valor negativo minusculo.
- **Efeito:**  Tirei 41 linhas, e inseri outras 13. Mais importante que o saldo: a regra deixou de estar escondida na estrutura do código e passou a estar nos dados. O laço não sabe quantas faixas existem — se o governo criar uma sexta, acrescentamos uma linha na tupla e nada mais muda. Sobre o max(..., 0): a parcela a deduzir de 169,44 é exatamente 7,5% de 2.259,20, então na fronteira exata da faixa a conta dá zero — e o ponto flutuante pode devolver algo como −0,0000001. Apagar aquele clamp pareceria limpeza, mas seria remover uma protecao que eu ainda nao tinha entendido - por isso ele foi preservado como max(..., 0).

### 4. Extract Function - commit `ab84c4a`
- **Smell que resolve:** Long Function
- **Antes -> Depois:** `calcular_folha` foi decomposta em `calcular_valor_horas_extras`,
  `calcular_bonus`, `calcular_inss`, `calcular_base_irrf` e `calcular_irrf`. A funcao publica
  passou de 81 para 9 linhas de orquestracao mais o dicionario de retorno.
- **Efeito:** calcular_folha passou de 81 linhas para 9. Hoje ela não calcula nada — só chama, na ordem, e devolve. Quem lê essas 9 linhas entende a folha de pagamento inteira: horas extras, bônus, bruto, INSS, base, IRRF, líquido. É a sequência de um contracheque. Quem precisa saber como o INSS é calculado entra em calcular_inss, que cabe em uma tela e não tem mais nada dentro.

### 5. Remove Comments - commit `524f461`
- **Smell que resolve:** Comments
- **Antes -> Depois:** doze comentarios band-aid removidos. Restaram dois, que descrevem o
  formato das tuplas das tabelas de faixa.
- **Criterio adotado:** comentario que responde o QUE virou nome e foi apagado; comentario que responde POR QUE ficou. Os dois que sobraram — # (limite_superior_da_faixa, aliquota) — eles explicam a ordem dos elementos dentro da tupla, que é uma convenção arbitrária que nome nenhum carrega. Se dessemos nome, seria uma dataclass, e aí o comentário sumiria também.

---

## Decisoes conscientes

**Comparacao redundante com booleano.** `if funcionario["tem_bonus"] == True` virou
`if tem_bonus` dentro de `calcular_bonus`. Foi uma comparação redundante: o valor já era booleano. Trocar por if tem_bonus muda o comportamento para valores truthy não-booleanos — se alguém passasse a string "sim", o antigo daria falso e o novo daria verdadeiro. Verifiquei que os testes e o contrato do dicionário só usam True/False, então a mudança é segura. O ponto que vale nota é ter percebido e avaliado, não ter trocado.

**float mantido, Decimal recusado.** Trocar `float` por `Decimal` e a decisao correta para
dinheiro em producao e errada aqui: `round(2.675, 2)` devolve `2.67` no Python, enquanto
`Decimal("2.675")` com `ROUND_HALF_UP` devolve `2.68`. Seria mudanca de comportamento
observavel disfarcada de melhoria, e o enunciado proibe. Pela mesma razao nao foram feitas
atualizacao da tabela de INSS para o ano vigente, validacao de entrada nem hierarquia de
classes para as faixas. Refatoracao e mudanca de estrutura com comportamento constante.

---

## c) Reflexao sobre legibilidade

O fio condutor foi o # CUIDADO ao alterar pq muita coisa depende disso aqui. Aquele comentário não transmitia informação, transmitia medo. Ele existia porque as 81 linhas eram opacas e o autor sabia disso — era um pedido de desculpas, não uma instrução. Não foi preciso apagá-lo por decisão editorial: quando cada função passou a ter um nome que diz o que faz, um tamanho que cabe na tela, e um nível de abstração consistente — calcular_folha só orquestra, as outras só calculam — o aviso deixou de ter objeto. Não há mais "muita coisa dependendo disso aqui" de forma invisível: as dependências estão nos parâmetros das funções, explícitas.

É isso que os princípios da Unidade 6 querem dizer na prática. Nome significativo não é capricho: é o que permite apagar um comentário. Função pequena não é métrica: é o que faz caber na cabeça. Abstração consistente é o que faz calcular_folha ser legível para quem não sabe nada de INSS.

---

## Verificacao de equivalencia (Q3)

Os 16 testes do professor passam no estado final de `main`:
`pytest tests_professor_pratica2.py -v` -> 16 passed.

Alem disso, o golden master descrito no inicio foi executado apos cada um dos cinco commits de
refatoracao, comparando 222.384 casos contra o retrato do codigo original. Divergencias: 0 em
todos os passos.

| Commit | Tecnica | Efeito |
|---|---|---|
| `964a330` | - | codigo base, antes da refatoracao |
| `5963e93` | Rename Variable | 11 identificadores renomeados |
| `a54d4aa` | Replace Magic Number with Symbolic Constant | constantes e tabelas extraidas |
| `2e84290` | Decompose Conditional + Table Lookup | 41 linhas de `if` aninhado -> 13 de laco |
| `ab84c4a` | Extract Function | 1 funcao de 81 linhas -> 5 funcoes + 9 de orquestracao |
| `524f461` | Remove Comments | 12 comentarios removidos, 2 mantidos |