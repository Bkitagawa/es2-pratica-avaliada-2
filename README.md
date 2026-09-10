# PRÁTICA AVALIADA 2 - ES2 (10 pontos)

**Módulo/Semana:** 7

**Conteúdo avaliado:** Módulos 4, 5 e 6 (Unidades 4, 5 e 6, com retomada de fundamentos da Unidade 3)

**Duração sugerida:** 2 horas

**Tipo:** Prática integradora avaliativa

**Linguagem:** Python 3.10+ com pytest

---

## CONTEXTUALIZAÇÃO

A **"PayrollFlex"** mantém uma calculadora de folha de pagamento legada
escrita por um estagiário. O código **funciona corretamente** — todos
os cálculos batem com a tabela de INSS/IRRF — mas a equipe acumulou
queixas: ninguém quer encostar no arquivo, qualquer ajuste exige horas
para entender o que cada trecho faz, e novos colegas ficam perdidos
nos `if` aninhados.

Você foi contratado como engenheiro de software para **refatorar** esse
módulo: melhorar a estrutura, a legibilidade e a manutenibilidade do
código **sem alterar o comportamento observável**. A função pública
`calcular_folha(funcionario: dict) -> dict` deve continuar produzindo
exatamente os mesmos resultados — verificados pelos testes
automatizados do professor.

---

## CÓDIGO BASE

O arquivo `folha_pagamento.py` contém a função `calcular_folha` que:

- Recebe um dicionário com `nome`, `salario_base`, `horas_extras`,
  `dependentes`, `tem_bonus` e `valor_bonus`.
- Retorna um dicionário com `nome`, `salario_bruto`,
  `valor_horas_extras`, `bonus`, `inss`, `irrf` e `salario_liquido`.

O código apresenta vários *code smells* (Unidade 4) e problemas de
legibilidade (Unidade 6) — sua tarefa é identificá-los e corrigi-los
aplicando as técnicas de refactoring vistas na Unidade 3 e formalizadas
na Unidade 4.

> 💡 A Unidade 5 (Compreensão, Manutenção e Evolução) entra como pano
> de fundo conceitual: refatorar é um exercício de manutenção
> preventiva — você está pagando dívida técnica para preparar o
> sistema para evoluir com segurança.

---

## QUESTÃO 1: Refatoração do Código (5,5 pontos)

Refatore `folha_pagamento.py` mantendo a **mesma API pública**:

- A função `calcular_folha(funcionario: dict) -> dict` deve continuar
  existindo no módulo `folha_pagamento`, com a mesma assinatura e
  mesmos campos no dicionário de saída.
- Os valores numéricos retornados devem ser **idênticos** aos da versão
  original (verificado pelos testes do professor).

### Refatorações esperadas (aplicar pelo menos 4 das listadas)

| Refatoração (Fowler) | Onde aplicar |
|---|---|
| **Extract Method** | Quebrar a função monolítica em funções menores com responsabilidade única (cálculo de horas extras, INSS, IRRF, etc.). |
| **Replace Magic Number with Symbolic Constant** | Substituir `220`, `1412`, `2666.68`, `0.075`, `189.59` etc. por constantes nomeadas. |
| **Decompose Conditional** | Achatar os `if`/`else` aninhados das faixas de INSS e IRRF. |
| **Rename Variable** / **Rename Function** | Renomear identificadores curtos (`f`, `sb`, `he`, `b`, `ins`, `liq`) para nomes descritivos. |
| **Replace Temp with Query** | Substituir variáveis temporárias por funções, quando útil. |
| **Introduce Parameter Object** | Substituir o `dict` solto por um dataclass (opcional, mas vale ponto extra de legibilidade). |

### Critérios de Avaliação

| Critério | Pontuação |
|---|---:|
| Função monolítica decomposta em funções pequenas e coesas | 1,8 |
| Magic numbers substituídos por constantes nomeadas | 1,0 |
| Renomeação consistente (sem identificadores abreviados não óbvios) | 1,0 |
| Estrutura condicional achatada (sem `if` profundamente aninhados) | 0,8 |
| Comentários "band-aid" removidos (código autoexplicativo) | 0,9 |

---

## QUESTÃO 2: Relatório de Refactoring (3,5 pontos)

Crie o arquivo `relatorio-refactoring.md` documentando seu trabalho.

### Conteúdo obrigatório

**a) (1,5 pontos) Smells identificados.** Liste os code smells
presentes no código original, nomeados conforme o catálogo de Fowler
(*Long Method*, *Magic Numbers*, *Bad Names*, *Long Function*,
*Comments*, *Primitive Obsession*, etc.). Para cada smell:

- **Localização:** trecho ou linha aproximada.
- **Por que é um smell:** 1–2 frases.

Mínimo: **4 smells distintos**.

**b) (1,5 pontos) Refactorings aplicados.** Liste as técnicas de
refactoring que você usou (também nomeadas conforme catálogo). Para
cada uma:

- **Smell que ela resolve.**
- **Trecho antes / depois** (citar nomes de função/variável envolvidos
  — não precisa colar o código inteiro).

Mínimo: **4 refactorings distintos**.

**c) (0,5 pontos) Reflexão sobre legibilidade.** Em 1 parágrafo,
descreva como suas decisões de nomenclatura e estrutura tornaram o
código mais legível (referencie princípios da Unidade 6: nomes
significativos, funções pequenas, abstração consistente).

### Critérios de Avaliação

| Critério | Pontuação |
|---|---:|
| ≥4 smells nomeados corretamente e localizados | 1,5 |
| ≥4 refactorings nomeados, com smell associado e antes/depois | 1,5 |
| Reflexão coerente referenciando princípios de código legível | 0,5 |

---

## QUESTÃO 3: Verificação de Equivalência (1,0 ponto)

Garanta que sua refatoração não quebrou o comportamento:

```bash
pytest tests_professor_pratica2.py -v
```

Resultado esperado: **todos os 16 testes passam**.

### Critérios de Avaliação

| Critério | Pontuação |
|---|---:|
| Todos os 16 testes do professor passam após refatoração | 1,0 |

---

## ESTRUTURA DE ARQUIVOS ESPERADA

```
es2-pratica-avaliada-2/
├── README.md
├── folha_pagamento.py         (refatorado por você, mesma API)
├── relatorio-refactoring.md   (criado por você)
├── tests_professor_pratica2.py
└── requirements.txt
```

---

## INSTRUÇÕES DE EXECUÇÃO

```bash
pip install -r requirements.txt
pytest tests_professor_pratica2.py -v
```

---

## ENTREGA

1. **Repositório GitHub** com todos os arquivos da prática.
2. **Link do repositório** submetido na plataforma de ensino.
3. Garanta que os testes do professor passam antes de submeter.

### Prazos

- **Início:** Módulo/Semana 7
- **Entrega:** Final do Módulo/Semana 7
- **Feedback:** Módulo/Semana 8

---

## IMPORTANTE

- Esta é uma **avaliação individual**.
- **Você NÃO escreve novos testes** — o trabalho é refatorar mantendo
  o comportamento, validado pelos testes do professor.
- A API pública é o **contrato**: nome da função, assinatura e campos
  do dicionário de retorno devem permanecer estáveis.
- Plágio será **penalizado com nota zero**.

---

## OBSERVAÇÕES SOBRE CORREÇÃO

- A correção do código refatorado é **automática** (testes do
  professor) + **manual** (qualidade da refatoração, leitura do
  código).
- O relatório (`relatorio-refactoring.md`) é avaliado manualmente.
- A Q3 é a única âncora de avaliação de "testes passando": se a
  refatoração quebrar o comportamento, a perda se concentra em Q3
  (1,0 ponto). Os critérios qualitativos da Q1 avaliam a refatoração
  pelo que foi feito, não pelo resultado dos testes.

---

## MATERIAL DIDÁTICO

- Plano de Estudos das Unidades 3, 4, 5 e 6.
- Learning Check das Unidades 3, 4 e 6.
- Catálogo de refactorings: livro *Refactoring* (Martin Fowler).
- Princípios de código legível: livro *Clean Code* (Robert Martin) e
  livro-texto da disciplina (Valente, *Fundamentos de Manutenção de
  Software*).