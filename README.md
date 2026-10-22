# Operação Pega-Laranja: Investigação de Redes e Fraudes com PaySim

Projeto desenvolvido para simulação e análise de **Prevenção à Fraude e Anti-Lavagem de Dinheiro (AML)**, investigando padrões de contas laranjas (*mule accounts*) em transações financeiras.

---

## Visão Geral do Projeto
No ecossistema de pagamentos digitais, criminosos frequentemente utilizam redes de contas intermediárias para pulverizar e lavar dinheiro roubado antes de efetuar o saque final. Este projeto utiliza uma base transacional de 6,3 milhões de registros do simulador **PaySim** para expor esse comportamento através de engenharia de dados, consultas SQL avançadas e análise de redes.

## Tecnologias e Ferramentas Utilizadas
* **Python 3.x** (Linguagem principal)
* **SQLite & SQL** (Armazenamento relacional e queries analíticas)
* **Pandas** (Manipulação e estruturação de dados)
* **NetworkX & Matplotlib** (Visualização e mapeamento de grafos de redes)
* **Jupyter Notebooks** (Relatório analítico interativo)

---

## Hipóteses e Metodologia
1. **Concentração de Risco:** As fraudes se concentram em operações de alta liquidez.
2. **Modus Operandi:** O uso de contas intermediárias (`TRANSFER`) seguido de esvaziamento total do saldo (`CASH_OUT` com `newbalanceOrig = 0`).

### Principais Etapas da Investigação:
1. **Engenharia de Dados:** Ingestão do dataset em lotes (*chunks*) de um arquivo CSV de 6M+ linhas para um banco SQLite otimizado com índices relacionais.
2. **Data Quality & EDA:** Auditoria de nulos (0% de valores corrompidos) e identificação de que **100% das fraudes** ocorrem exclusivamente nas categorias `TRANSFER` e `CASH_OUT`.
3. **Análise Comportamental:** Constatação de que o valor médio das fraudes é ~4x superior ao das transações legítimas, com uma taxa de esvaziamento de saldo de quase 98%.
4. **Network / Graph Analysis:** Mapeamento visual das conexões de transferência entre contas suspeitas utilizando grafos direcionados.
### Mapeamento de Redes (Graph Analytics)
![Mapa de Redes de Contas Laranjas](mapa_redes_fraude.png)
*Visualização de conexões entre contas de origem e destino em transações fraudulentas (NetworkX).*

---

## Principais Achados e Insights
* **Taxa Base de Fraude:** ~0,13% (evento altamente desbalanceado, espelhando o mundo real).
* **Assinatura de Fraude:** Transações de alto valor em `TRANSFER` que zeram o saldo da origem (`newbalanceOrig = 0`), culminando em saques rápidos.

## Recomendações de Negócio
* Implementação de travas de segurança e *hold* temporário para transferências atípicas seguidas de esvaziamento imediato.
* Adoção de monitoramento contínuo baseado em análise de redes para detecção precoce de *hubs* de contas laranjas.

---

## Estrutura do Repositório
```text
projeto_aml_paysim/
│
├── 01_ingestao_dados.py          # Script de engenharia e criação do banco SQLite
├── 02_eda_e_investigacao.ipynb   # Jupyter Notebook com a EDA, queries SQL e Grafos
├── paysim_banco.db               # Banco de dados relacional local (indexado)
└── README.md                     # Documentação oficial do projeto