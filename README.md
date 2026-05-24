# 🏙️ ImobiAnalytics — Dashboard do Mercado Imobiliário Brasileiro

> Plataforma de análise interativa do mercado imobiliário brasileiro (2015–2024), construída com Streamlit, Pandas, Matplotlib, Seaborn, SQLAlchemy e NumPy.

---

## 📋 Descrição

O **ImobiAnalytics** é um dashboard analítico que explora o comportamento do mercado imobiliário no Brasil ao longo de uma década (2015–2024). A aplicação consome dados simulados de imóveis em diferentes regiões, estados e cidades do país, oferecendo uma visão ampla sobre:

- Evolução temporal dos preços
- Diferenças regionais e municipais
- Tipologia de imóveis e níveis de preço
- Correlações entre área, renda e taxa de juros
- Consulta direta ao banco de dados via SQL

A interface é construída com um **tema escuro premium** (glassmorphism + gradientes), tipografia moderna (Inter) e micro-animações, proporcionando uma experiência visual de alto nível.

---

## 🧱 Estrutura do Projeto

```
dados_linguagem/
├── app.py                              # Aplicação principal Streamlit
├── requirements.txt                    # Dependências Python
├── mercado_imobiliario.sqlite          # Banco SQLite (gerado automaticamente)
├── dados/
│   └── simulacao_mercado_imobiliario_brasil.csv   # Dataset principal
├── notebooks/
│   └── notebook.ipynb                  # Análise exploratória em Jupyter
└── README.md
```

---

## ⚙️ Tecnologias Utilizadas

| Biblioteca      | Versão mínima | Papel no projeto                                       |
|-----------------|---------------|--------------------------------------------------------|
| `streamlit`     | ≥ 1.32        | Framework do dashboard interativo                      |
| `pandas`        | ≥ 2.0         | Leitura, transformação e agregação dos dados           |
| `matplotlib`    | ≥ 3.8         | Renderização de gráficos customizados (tema escuro)    |
| `seaborn`       | ≥ 0.13        | Heatmap de correlação regional por tipologia           |
| `sqlalchemy`    | ≥ 2.0         | ORM e criação do banco SQLite com persistência         |
| `numpy`         | ≥ 1.26        | Cálculos numéricos (CAGR, correlações)                 |

---

## 🚀 Como Executar

### 1. Clone o repositório

```bash
git clone https://github.com/jotafortunat/dados_linguagem.git
cd dados_linguagem
```

### 2. Crie e ative o ambiente virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute o dashboard

```bash
streamlit run app.py
```

O dashboard será aberto automaticamente em `http://localhost:8501`.

---

## 📊 Funcionalidades do Dashboard

### 🔢 KPIs Automáticos (2 linhas de cards)

| Card | Descrição |
|------|-----------|
| 🏷️ Preço Médio | Valor médio dos imóveis no filtro atual |
| 📐 Preço / m² | Custo médio por metro quadrado |
| 💵 Renda Média Regional | Renda média do local dos imóveis selecionados |
| 📈 Taxa de Juros | Juros médios do período |
| 🏘️ Volume Analisado | Total de registros no filtro |
| 🏆 Cidade Mais Cara | Município de maior ticket médio |
| 🗺️ Região Mais Cara | Região geográfica de maior valorização |
| 🥇 Tipo Mais Valorizado | Tipologia de imóvel com maior valor médio |
| 📊 Crescimento Médio Anual | CAGR calculado para o período filtrado |

---

### 📑 Abas de Análise

#### 📈 Aba 1 — Evolução Temporal
- **Série mensal de preço médio**: Gráfico de linha com área preenchida, ideal para identificar tendências e sazonalidade
- **Valorização anual por região**: Multi-linha colorida por região geográfica
- **Top 10 cidades com maior crescimento**: Barras horizontais comparando o primeiro e o último ano disponível

#### 🏠 Aba 2 — Tipologia e Níveis
- **Preço médio por tipo de imóvel**: Gráfico de barras verticais (casa, apartamento, cobertura etc.)
- **Concentração por nível de preço**: Volume de imóveis por segmento (Econômico, Médio, Alto, Luxo)
- **Heatmap Região × Tipo**: Matriz de calor mostrando o preço médio para cada combinação

#### 🗺️ Aba 3 — Análise Geográfica
- **Top 10 cidades mais caras**: Ranking municipal com destaque para a cidade líder
- **Preço médio por região**: Comparação entre as 5 regiões do Brasil
- **Renda média por região**: Contextualiza o índice de esforço habitacional de cada região

#### 🔗 Aba 4 — Correlações
- **Dispersão Área × Preço**: Scatter colorido por tipo de imóvel (amostra de até 800 registros)
- **Renda × Preço por Região**: Mapa de bolhas anotado por região
- **Juros × Preço Anual**: Gráfico de eixo duplo mostrando a relação inversa entre Selic e preços

#### 🗄️ Aba 5 — Consulta SQL
- Interface de consulta direta ao banco `mercado_imobiliario.sqlite`
- Query padrão exibe: região, tipo de imóvel, quantidade, preço médio, renda local e juros médio
- Exibe também o código SQL executado para fins didáticos

#### 📋 Aba 6 — Base de Dados
- Tabela completa com todos os registros do filtro ativo
- Permite inspeção direta dos dados brutos

---

## 🎛️ Filtros Interativos (Sidebar)

| Filtro | Tipo | Descrição |
|--------|------|-----------|
| 🗺️ Região | Multiselect | Norte, Nordeste, Centro-Oeste, Sudeste, Sul |
| 📍 UF | Multiselect | Estado(s) dos imóveis |
| 🏠 Tipo de Imóvel | Multiselect | Casa, Apartamento, Cobertura, etc. |
| 💰 Nível de Preço | Multiselect | Econômico, Médio, Alto, Luxo |
| 📅 Período | Date range | Intervalo de datas da análise |

Todos os gráficos, KPIs e tabelas são recalculados dinamicamente de acordo com os filtros aplicados.

---

## 🗄️ Banco de Dados

Na inicialização, o `app.py` carrega o CSV e **persiste automaticamente** os dados em um banco SQLite local (`mercado_imobiliario.sqlite`) via SQLAlchemy:

```python
engine = create_engine("sqlite:///mercado_imobiliario.sqlite")
df.to_sql("imoveis", engine, if_exists="replace", index=False)
```

A tabela `imoveis` é recriada a cada execução, garantindo consistência com os dados do CSV. A aba **Consulta SQL** usa esta conexão para executar queries arbitrárias com `pd.read_sql()`.

---

## 📁 Dataset

**Arquivo:** `dados/simulacao_mercado_imobiliario_brasil.csv`

Dataset simulado com registros de imóveis brasileiros contendo as seguintes colunas principais:

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `data` | date | Data da transação/referência |
| `cidade` | str | Município do imóvel |
| `uf` | str | Unidade Federativa |
| `regiao` | str | Região geográfica do Brasil |
| `tipo_imovel` | str | Tipo (casa, apartamento, etc.) |
| `nivel_preco` | str | Segmento de mercado |
| `preco_imovel` | float | Valor do imóvel em R$ |
| `preco_m2` | float | Preço por metro quadrado |
| `area_m2` | float | Área em metros quadrados |
| `renda_media` | float | Renda média regional |
| `taxa_juros` | float | Taxa de juros vigente (%) |

---

## 📐 Arquitetura da Aplicação

```
app.py
│
├── Configuração da página (st.set_page_config)
├── CSS customizado (tema escuro premium)
├── Configuração do Matplotlib (dark theme)
│
├── Carregamento de dados
│   ├── carregar_dados_csv()  ← @st.cache_data
│   └── criar_banco_sqlite()  ← SQLAlchemy
│
├── Hero Header
├── Sidebar (filtros dinâmicos)
├── Filtragem do DataFrame
│
├── Cálculo de KPIs
│   ├── Preço médio, m², renda, juros, volume
│   ├── Cidade / Região mais cara
│   ├── Tipo mais valorizado
│   └── CAGR (Crescimento Médio Anual Composto)
│
├── KPI Cards (linha 1: 5 cards | linha 2: 4 cards)
│
└── Tabs de análise
    ├── Aba 1: Evolução Temporal   (3 gráficos)
    ├── Aba 2: Tipologia e Níveis  (3 gráficos)
    ├── Aba 3: Análise Geográfica  (3 gráficos)
    ├── Aba 4: Correlações         (3 gráficos)
    ├── Aba 5: Consulta SQL        (tabela + query)
    └── Aba 6: Base de Dados       (dataframe bruto)
```

---

## 🎨 Design System

- **Fonte:** Inter (Google Fonts)
- **Background:** `linear-gradient(135deg, #0d1117, #0f1923)`
- **Accent colors:** `#3b82f6` (azul), `#06b6d4` (ciano), `#a78bfa` (violeta), `#34d399` (verde)
- **Tema Matplotlib:** Totalmente customizado em dark mode (`#1e293b`)
- **Paletas de gráfico:** `PALETTE_COOL`, `PALETTE_BLUE`, `PALETTE_PURP`
- **Componentes:** KPI cards com hover, section headers com dot indicator, insight boxes com borda esquerda colorida

---

## 📓 Notebook Exploratório

O arquivo `notebooks/notebook.ipynb` contém análises complementares em Jupyter Notebook, úteis para experimentação antes de incorporar visualizações ao dashboard principal.

---

## 🤝 Contribuições

Contribuições são bem-vindas! Abra uma *issue* ou envie um *pull request* com melhorias, novos gráficos ou correções.

---

## 📄 Licença

Distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais informações.

---

<p align="center">
  <strong>ImobiAnalytics</strong> · Dados simulados · Brasil 2015–2024<br>
  Pandas · Seaborn · Matplotlib · SQLAlchemy · NumPy · Streamlit
</p>
