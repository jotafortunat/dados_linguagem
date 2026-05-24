import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
from sqlalchemy import create_engine

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Mercado Imobiliário · Analytics",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS – dark premium theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  .stApp {
      background: linear-gradient(135deg, #0d1117 0%, #0f1923 50%, #0d1117 100%);
  }

  /* Sidebar */
  [data-testid="stSidebar"] {
      background: linear-gradient(180deg, #111827 0%, #0f1923 100%) !important;
      border-right: 1px solid rgba(99,179,237,0.15);
  }
  [data-testid="stSidebar"] * { color: #e2e8f0 !important; }
  [data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
      background: linear-gradient(135deg, #3b82f6, #06b6d4) !important;
      border-radius: 6px !important;
  }

  /* Hero */
  .hero-section {
      background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
      border: 1px solid rgba(99,179,237,0.2);
      border-radius: 16px;
      padding: 2rem 2.5rem;
      margin-bottom: 1.5rem;
      position: relative;
      overflow: hidden;
  }
  .hero-section::before {
      content: '';
      position: absolute;
      top: -50%; right: -20%;
      width: 400px; height: 400px;
      background: radial-gradient(circle, rgba(59,130,246,0.08) 0%, transparent 70%);
      border-radius: 50%;
  }
  .hero-title {
      font-size: 2rem; font-weight: 700;
      background: linear-gradient(135deg, #63b3ed, #06b6d4, #a78bfa);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      margin: 0 0 0.5rem 0;
  }
  .hero-subtitle {
      color: #94a3b8; font-size: 0.95rem; line-height: 1.6; margin: 0;
  }
  .hero-badge {
      display: inline-block;
      background: linear-gradient(135deg, #3b82f6, #06b6d4);
      color: white; font-size: 0.7rem; font-weight: 600;
      padding: 3px 10px; border-radius: 20px;
      margin-bottom: 0.75rem; letter-spacing: 0.05em; text-transform: uppercase;
  }

  /* KPI Cards */
  .kpi-card {
      background: linear-gradient(135deg, #1e293b 0%, #162032 100%);
      border: 1px solid rgba(99,179,237,0.15);
      border-radius: 14px; padding: 1.1rem 1rem;
      text-align: center; position: relative;
      overflow: hidden;
      transition: transform 0.2s ease, border-color 0.2s ease;
      height: 100%;
  }
  .kpi-card:hover { transform: translateY(-3px); border-color: rgba(99,179,237,0.4); }
  .kpi-card::after {
      content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
      background: linear-gradient(90deg, #3b82f6, #06b6d4);
  }
  .kpi-icon   { font-size: 1.5rem; margin-bottom: 0.3rem; display: block; }
  .kpi-label  { color: #64748b; font-size: 0.68rem; font-weight: 600;
                text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.3rem; }
  .kpi-value  { color: #e2e8f0; font-size: 1.15rem; font-weight: 700; line-height: 1.2; }
  .kpi-value.accent { color: #63b3ed; }
  .kpi-value.green  { color: #34d399; }

  /* Section headers */
  .section-header {
      display: flex; align-items: center; gap: 0.6rem;
      margin-bottom: 1.2rem; padding-bottom: 0.75rem;
      border-bottom: 1px solid rgba(99,179,237,0.1);
  }
  .section-header h3 { color: #e2e8f0; font-size: 1.1rem; font-weight: 600; margin: 0; }
  .section-dot {
      width: 8px; height: 8px;
      background: linear-gradient(135deg, #3b82f6, #06b6d4); border-radius: 50%;
  }

  /* Tabs */
  [data-testid="stTabs"] [data-baseweb="tab-list"] {
      background: #111827; border-radius: 12px; padding: 4px; gap: 4px;
      border: 1px solid rgba(99,179,237,0.1);
  }
  [data-testid="stTabs"] [data-baseweb="tab"] {
      background: transparent; color: #64748b !important;
      border-radius: 8px; font-size: 0.82rem; font-weight: 500;
      padding: 8px 16px; transition: all 0.2s;
  }
  [data-testid="stTabs"] [aria-selected="true"] {
      background: linear-gradient(135deg, #3b82f6, #0284c7) !important;
      color: #fff !important;
  }
  [data-testid="stTabs"] [data-baseweb="tab-border"] { display: none; }

  /* Misc */
  [data-testid="stDataFrame"] {
      border: 1px solid rgba(99,179,237,0.1) !important;
      border-radius: 12px !important; overflow: hidden;
  }
  [data-testid="stAlert"] { border-radius: 12px !important; border-width: 1px !important; }
  hr { border-color: rgba(99,179,237,0.1) !important; }

  .sidebar-brand {
      display: flex; align-items: center; gap: 0.5rem;
      padding: 1rem 0 1.5rem 0;
      border-bottom: 1px solid rgba(99,179,237,0.1); margin-bottom: 1.2rem;
  }
  .sidebar-brand-text { font-size: 1rem; font-weight: 700; color: #e2e8f0; }
  .sidebar-brand-sub  { font-size: 0.72rem; color: #64748b; }

  .insight-box {
      background: rgba(59,130,246,0.06);
      border: 1px solid rgba(59,130,246,0.2);
      border-left: 3px solid #3b82f6;
      border-radius: 10px; padding: 0.85rem 1.1rem;
      color: #94a3b8; font-size: 0.88rem; line-height: 1.65;
      margin-top: 0.8rem;
  }
  .insight-box strong { color: #63b3ed; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  MATPLOTLIB DARK THEME
# ─────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor":  "#1e293b",
    "axes.facecolor":    "#1e293b",
    "axes.edgecolor":    "#334155",
    "axes.labelcolor":   "#94a3b8",
    "xtick.color":       "#64748b",
    "ytick.color":       "#64748b",
    "text.color":        "#e2e8f0",
    "grid.color":        "#1e3a4a",
    "grid.linewidth":    0.6,
    "axes.grid":         True,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "font.family":       "DejaVu Sans",
    "axes.titlecolor":   "#e2e8f0",
    "axes.titlesize":    13,
    "axes.titleweight":  "bold",
    "axes.labelsize":    10,
})

ACCENT  = "#3b82f6"
ACCENT2 = "#06b6d4"
ACCENT3 = "#a78bfa"
GREEN   = "#34d399"
PALETTE_COOL = ["#06b6d4","#0ea5e9","#3b82f6","#6366f1","#8b5cf6","#a78bfa","#c084fc","#d8b4fe","#e879f9","#f0abfc"]
PALETTE_BLUE = [ACCENT, ACCENT2, "#0ea5e9", "#38bdf8", "#7dd3fc"]
PALETTE_PURP = ["#a78bfa","#8b5cf6","#7c3aed","#6d28d9","#5b21b6"]

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def fmt_brl(val):
    return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def section(title: str):
    st.markdown(f"""
    <div class="section-header">
      <div class="section-dot"></div>
      <h3>{title}</h3>
    </div>""", unsafe_allow_html=True)

def insight(text: str):
    st.markdown(f'<div class="insight-box">{text}</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PATHS & DATA
# ─────────────────────────────────────────────
BASE_DIR      = Path(__file__).parent
CAMINHO_DADOS = BASE_DIR / "dados" / "simulacao_mercado_imobiliario_brasil.csv"
CAMINHO_BANCO = BASE_DIR / "mercado_imobiliario.sqlite"

@st.cache_data
def carregar_dados_csv():
    df = pd.read_csv(CAMINHO_DADOS)
    df["data"]    = pd.to_datetime(df["data"], errors="coerce")
    df["ano"]     = df["data"].dt.year
    df["mes"]     = df["data"].dt.month
    df["ano_mes"] = df["data"].dt.to_period("M").astype(str)
    return df

def criar_banco_sqlite(df):
    engine = create_engine(f"sqlite:///{CAMINHO_BANCO}")
    df.to_sql("imoveis", engine, if_exists="replace", index=False)
    return engine

df     = carregar_dados_csv()
engine = criar_banco_sqlite(df)

# ─────────────────────────────────────────────
#  HERO HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-section">
  <span class="hero-badge">🏙️ Analytics Platform · Brasil 2015–2024</span>
  <h1 class="hero-title">Mercado Imobiliário Brasileiro</h1>
  <p class="hero-subtitle">
    Análise profunda do comportamento imobiliário no Brasil entre 2015 e 2024 —
    evolução de preços, diferenças regionais, valorização e relação renda × imóveis.<br>
    <strong style="color:#63b3ed">Pandas</strong> &nbsp;·&nbsp;
    <strong style="color:#06b6d4">Seaborn / Matplotlib</strong> &nbsp;·&nbsp;
    <strong style="color:#a78bfa">SQLite + SQLAlchemy</strong> &nbsp;·&nbsp;
    <strong style="color:#34d399">NumPy</strong>
  </p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
      <span style="font-size:1.5rem">🏙️</span>
      <div>
        <div class="sidebar-brand-text">ImobiAnalytics</div>
        <div class="sidebar-brand-sub">Dashboard · v3.0</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Filtros de Análise**")

    regioes = sorted(df["regiao"].dropna().unique())
    ufs     = sorted(df["uf"].dropna().unique())
    tipos   = sorted(df["tipo_imovel"].dropna().unique())
    niveis  = sorted(df["nivel_preco"].dropna().unique())

    regiao_sel = st.multiselect("🗺️ Região",         options=regioes, default=regioes)
    uf_sel     = st.multiselect("📍 UF",              options=ufs,     default=ufs)
    tipo_sel   = st.multiselect("🏠 Tipo de Imóvel",  options=tipos,   default=tipos)
    nivel_sel  = st.multiselect("💰 Nível de Preço",  options=niveis,  default=niveis)

    st.markdown("---")
    data_min = df["data"].min().date()
    data_max = df["data"].max().date()
    intervalo_datas = st.date_input(
        "📅 Período",
        value=(data_min, data_max),
        min_value=data_min,
        max_value=data_max,
    )

if isinstance(intervalo_datas, tuple) and len(intervalo_datas) == 2:
    inicio, fim = intervalo_datas
else:
    inicio, fim = data_min, data_max

# ─────────────────────────────────────────────
#  FILTRO DINÂMICO
# ─────────────────────────────────────────────
df_filtrado = df[
    (df["regiao"].isin(regiao_sel))     &
    (df["uf"].isin(uf_sel))             &
    (df["tipo_imovel"].isin(tipo_sel))  &
    (df["nivel_preco"].isin(nivel_sel)) &
    (df["data"].dt.date >= inicio)      &
    (df["data"].dt.date <= fim)
]

if df_filtrado.empty:
    st.warning("⚠️  Nenhum registro encontrado para os filtros selecionados.")
    st.stop()

# ─────────────────────────────────────────────
#  KPIs CALCULADOS
# ─────────────────────────────────────────────
preco_medio   = df_filtrado["preco_imovel"].mean()
m2_medio      = df_filtrado["preco_m2"].mean()
renda_media   = df_filtrado["renda_media"].mean()
juros_medio   = df_filtrado["taxa_juros"].mean()
total_imoveis = len(df_filtrado)

# Cidade mais cara
cidade_cara_row = (
    df_filtrado.groupby("cidade")["preco_imovel"].mean()
    .sort_values(ascending=False)
    .reset_index().iloc[0]
)
cidade_cara = cidade_cara_row["cidade"]

# Região mais cara
regiao_cara = (
    df_filtrado.groupby("regiao")["preco_imovel"].mean()
    .idxmax()
)

# Tipo mais valorizado
tipo_topo = (
    df_filtrado.groupby("tipo_imovel")["preco_imovel"].mean()
    .idxmax()
)

# Crescimento médio anual (CAGR preço médio)
preco_ano = (
    df_filtrado.groupby("ano")["preco_imovel"].mean()
    .sort_index()
)
if len(preco_ano) >= 2:
    anos_range = preco_ano.index[-1] - preco_ano.index[0]
    cagr = ((preco_ano.iloc[-1] / preco_ano.iloc[0]) ** (1 / max(anos_range, 1)) - 1) * 100
else:
    cagr = 0.0

# ─────────────────────────────────────────────
#  KPI CARDS — linha 1 (5 cards)
# ─────────────────────────────────────────────
kpi_row1 = [
    ("🏷️", "Preço Médio",          fmt_brl(preco_medio),                     ""),
    ("📐", "Preço / m²",            fmt_brl(m2_medio),                        ""),
    ("💵", "Renda Média Regional",  fmt_brl(renda_media),                     ""),
    ("📈", "Taxa de Juros",         f"{juros_medio:.2f}%",                    "accent"),
    ("🏘️", "Volume Analisado",     f"{total_imoveis:,.0f}".replace(",","."), "accent"),
]

cols = st.columns(5)
for col, (icon, label, value, cls) in zip(cols, kpi_row1):
    col.markdown(f"""
    <div class="kpi-card">
      <span class="kpi-icon">{icon}</span>
      <div class="kpi-label">{label}</div>
      <div class="kpi-value {cls}">{value}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# KPI linha 2 (4 cards adicionais exigidos)
kpi_row2 = [
    ("🏆", "Cidade Mais Cara",        cidade_cara,          "accent"),
    ("🗺️", "Região Mais Cara",        regiao_cara,          "accent"),
    ("🥇", "Tipo Mais Valorizado",     tipo_topo,            ""),
    ("📊", "Crescimento Médio Anual",  f"{cagr:.1f}% a.a.",  "green"),
]

cols2 = st.columns(4)
for col, (icon, label, value, cls) in zip(cols2, kpi_row2):
    col.markdown(f"""
    <div class="kpi-card">
      <span class="kpi-icon">{icon}</span>
      <div class="kpi-label">{label}</div>
      <div class="kpi-value {cls}">{value}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  TABS
# ─────────────────────────────────────────────
aba1, aba2, aba3, aba4, aba5, aba6 = st.tabs([
    "📈  Evolução Temporal",
    "🏠  Tipologia e Níveis",
    "🗺️  Análise Geográfica",
    "🔗  Correlações",
    "🗄️  Consulta SQL",
    "📋  Base de Dados",
])

# ══════════════════════════════════════════════
#  ABA 1 — EVOLUÇÃO TEMPORAL
# ══════════════════════════════════════════════
with aba1:
    # --- Gráfico 1: Linha temporal de preço médio mensal ---
    section("Evolução Mensal do Preço Médio dos Imóveis")

    serie_mensal = (
        df_filtrado.groupby("ano_mes")["preco_imovel"]
        .mean().reset_index().sort_values("ano_mes")
    )

    fig, ax = plt.subplots(figsize=(13, 4.5))
    fig.patch.set_facecolor("#1e293b")
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'R$ {x/1_000:.0f}k'))
    ax.fill_between(range(len(serie_mensal)), serie_mensal["preco_imovel"], alpha=0.12, color=ACCENT)
    ax.plot(range(len(serie_mensal)), serie_mensal["preco_imovel"],
            color=ACCENT, linewidth=2.2, marker="o", markersize=3.5,
            markerfacecolor=ACCENT2, markeredgecolor="#1e293b", markeredgewidth=1.5)
    step = max(1, len(serie_mensal) // 12)
    ticks = list(range(0, len(serie_mensal), step))
    ax.set_xticks(ticks)
    ax.set_xticklabels([serie_mensal["ano_mes"].iloc[i] for i in ticks], rotation=40, ha="right", fontsize=8)
    ax.set_title("Evolução Temporal de Preços — Visão Mensal", pad=14)
    ax.set_xlabel("Período (Ano-Mês)")
    ax.set_ylabel("Preço Médio (R$)")
    st.pyplot(fig, use_container_width=True)

    insight(
        "📊 A série temporal permite identificar <strong>ciclos de aquecimento e retração</strong> do mercado. "
        "Elevações de juros costumam pressionar os preços para baixo ao restringir o crédito imobiliário, "
        "enquanto períodos de queda da Selic estimulam a demanda e impulsionam a valorização."
    )

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # --- Gráfico 2: Evolução anual por região ---
    section("Valorização Anual por Região")

    serie_reg = (
        df_filtrado.groupby(["ano", "regiao"])["preco_imovel"]
        .mean().reset_index()
    )
    regioes_unicas = serie_reg["regiao"].unique()
    REGION_COLORS  = [ACCENT, ACCENT2, ACCENT3, GREEN, "#f59e0b", "#ef4444"]

    fig, ax = plt.subplots(figsize=(13, 4.5))
    fig.patch.set_facecolor("#1e293b")
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'R$ {x/1_000:.0f}k'))
    for reg, cor in zip(regioes_unicas, REGION_COLORS):
        subset = serie_reg[serie_reg["regiao"] == reg].sort_values("ano")
        ax.plot(subset["ano"], subset["preco_imovel"],
                color=cor, linewidth=2, marker="o", markersize=5, label=reg)
    ax.legend(framealpha=0.15, labelcolor="white", fontsize=9)
    ax.set_title("Evolução do Preço Médio Anual por Região", pad=14)
    ax.set_xlabel("Ano")
    ax.set_ylabel("Preço Médio (R$)")
    st.pyplot(fig, use_container_width=True)

    insight(
        "🗺️ O gráfico regional revela <strong>desigualdades estruturais</strong>: regiões como Sudeste e Sul "
        "historicamente lideram o ranking de preços, enquanto Norte e Nordeste apresentam valores mais acessíveis "
        "— reflexo direto da concentração de renda e infraestrutura no país."
    )

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # --- Gráfico 3: Crescimento % cidades top ---
    section("Cidades com Maior Crescimento de Preço (Primeiro vs. Último Ano)")

    anos_disp = sorted(df_filtrado["ano"].unique())
    if len(anos_disp) >= 2:
        ano_ini, ano_fim = anos_disp[0], anos_disp[-1]
        preco_ini = df_filtrado[df_filtrado["ano"] == ano_ini].groupby("cidade")["preco_imovel"].mean()
        preco_fim = df_filtrado[df_filtrado["ano"] == ano_fim].groupby("cidade")["preco_imovel"].mean()
        crescimento = ((preco_fim - preco_ini) / preco_ini * 100).dropna().sort_values(ascending=False).head(10)

        fig, ax = plt.subplots(figsize=(12, 4.5))
        fig.patch.set_facecolor("#1e293b")
        bars = ax.barh(crescimento.index[::-1], crescimento.values[::-1], color=PALETTE_COOL[:10], height=0.6, zorder=3)
        for bar in bars: bar.set_linewidth(0)
        ax.xaxis.set_major_formatter(mtick.PercentFormatter())
        ax.set_title(f"Top 10 Cidades — Crescimento de Preço ({ano_ini}→{ano_fim})", pad=12)
        ax.set_xlabel("Variação %")
        st.pyplot(fig, use_container_width=True)

        top_cidade_cres  = crescimento.index[0]
        top_perc_cres    = crescimento.iloc[0]
        insight(
            f"🚀 <strong>{top_cidade_cres}</strong> liderou a valorização no período analisado, "
            f"com crescimento de <strong>{top_perc_cres:.1f}%</strong>. "
            "Cidades com alto crescimento geralmente combinam expansão econômica local, "
            "migração populacional e oferta restrita de novos imóveis."
        )
    else:
        st.info("Selecione um intervalo de datas com ao menos dois anos para visualizar o crescimento por cidade.")

# ══════════════════════════════════════════════
#  ABA 2 — TIPOLOGIA E NÍVEIS
# ══════════════════════════════════════════════
with aba2:
    col_a, col_b = st.columns(2, gap="large")

    with col_a:
        section("Preço Médio por Tipo de Imóvel")
        preco_tipo = (
            df_filtrado.groupby("tipo_imovel")["preco_imovel"]
            .mean().sort_values(ascending=False).reset_index()
        )
        fig, ax = plt.subplots(figsize=(7, 4.5))
        fig.patch.set_facecolor("#1e293b")
        ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'R$ {x/1_000:.0f}k'))
        bars = ax.bar(preco_tipo["tipo_imovel"], preco_tipo["preco_imovel"],
                      color=PALETTE_BLUE[:len(preco_tipo)], width=0.55, zorder=3)
        for bar in bars: bar.set_linewidth(0)
        ax.set_title("Precificação por Tipologia", pad=12)
        ax.set_xlabel("Tipo de Imóvel")
        ax.set_ylabel("Valor Médio")
        ax.tick_params(axis="x", rotation=25)
        st.pyplot(fig, use_container_width=True)

    with col_b:
        section("Concentração por Nível de Preço")
        volume_nivel = (
            df_filtrado.groupby("nivel_preco")["preco_imovel"]
            .count().reset_index()
            .rename(columns={"preco_imovel": "quantidade"})
            .sort_values("quantidade", ascending=False)
        )
        fig, ax = plt.subplots(figsize=(7, 4.5))
        fig.patch.set_facecolor("#1e293b")
        bars = ax.bar(volume_nivel["nivel_preco"], volume_nivel["quantidade"],
                      color=PALETTE_PURP[:len(volume_nivel)], width=0.55, zorder=3)
        for bar in bars: bar.set_linewidth(0)
        ax.set_title("Volume de Imóveis por Categoria", pad=12)
        ax.set_xlabel("Nível de Preço")
        ax.set_ylabel("Quantidade de Imóveis")
        st.pyplot(fig, use_container_width=True)

    insight(
        f"🏠 <strong>{tipo_topo}</strong> é o tipo de imóvel com maior valor médio na seleção atual. "
        "A concentração nos níveis de preço reflete o perfil do mercado filtrado: "
        "quando o segmento 'Luxo' domina o volume, isso indica um mercado seletivo e de alta renda; "
        "predominância de 'Baixo' e 'Médio' sinaliza maior acessibilidade e liquidez."
    )

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # --- Preço médio por tipo e região (heatmap) ---
    section("Heatmap — Preço Médio por Região × Tipo de Imóvel")
    pivot_heat = (
        df_filtrado.groupby(["regiao", "tipo_imovel"])["preco_imovel"]
        .mean().unstack(fill_value=0)
    )
    fig, ax = plt.subplots(figsize=(12, max(3, len(pivot_heat) * 0.9)))
    fig.patch.set_facecolor("#1e293b")
    sns.heatmap(
        pivot_heat / 1_000, ax=ax,
        cmap="YlOrRd", linewidths=0.4, linecolor="#0f172a",
        annot=True, fmt=".0f", annot_kws={"size": 9, "color": "#1e293b"},
        cbar_kws={"label": "Preço médio (R$ mil)"},
    )
    ax.set_title("Distribuição Regional do Preço Médio por Tipologia (R$ mil)", pad=14)
    ax.set_xlabel("Tipo de Imóvel")
    ax.set_ylabel("Região")
    ax.tick_params(axis="x", rotation=30)
    ax.tick_params(axis="y", rotation=0)
    st.pyplot(fig, use_container_width=True)

    insight(
        "🔥 O heatmap revela a <strong>distribuição geográfica da valorização por tipologia</strong>. "
        "Células com tons mais escuros indicam combinações região-tipo de maior ticket médio, "
        "orientando estratégias de alocação de portfólio imobiliário por segmento e mercado regional."
    )

# ══════════════════════════════════════════════
#  ABA 3 — ANÁLISE GEOGRÁFICA
# ══════════════════════════════════════════════
with aba3:
    # --- Top 10 cidades mais caras ---
    section("Top 10 Cidades com Imóveis mais Caros")
    preco_cidade = (
        df_filtrado.groupby(["cidade", "uf"])["preco_imovel"]
        .mean().sort_values(ascending=False).head(10).reset_index()
    )
    preco_cidade["Local"] = preco_cidade["cidade"] + "  ·  " + preco_cidade["uf"]

    fig, ax = plt.subplots(figsize=(11, 4.8))
    fig.patch.set_facecolor("#1e293b")
    ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'R$ {x/1_000:.0f}k'))
    bars = ax.barh(preco_cidade["Local"][::-1], preco_cidade["preco_imovel"][::-1],
                   color=PALETTE_COOL[:10], height=0.6, zorder=3)
    for bar in bars: bar.set_linewidth(0)
    ax.set_title("Ranking de Valorização Municipal", pad=12)
    ax.set_xlabel("Preço Médio (R$)")
    ax.set_ylabel("")
    st.pyplot(fig, use_container_width=True)

    cidade_top = preco_cidade.iloc[0]["cidade"]
    preco_top  = preco_cidade.iloc[0]["preco_imovel"]
    st.success(
        f"🏆 A cidade mais cara na seleção atual é **{cidade_top}**, "
        f"com preço médio de **{fmt_brl(preco_top)}**."
    )

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # --- Comparação regional por barras ---
    col_r1, col_r2 = st.columns(2, gap="large")

    with col_r1:
        section("Preço Médio por Região")
        preco_reg = (
            df_filtrado.groupby("regiao")["preco_imovel"]
            .mean().sort_values(ascending=False).reset_index()
        )
        fig, ax = plt.subplots(figsize=(6.5, 4))
        fig.patch.set_facecolor("#1e293b")
        ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'R$ {x/1_000:.0f}k'))
        bars = ax.bar(preco_reg["regiao"], preco_reg["preco_imovel"],
                      color=PALETTE_COOL[:len(preco_reg)], width=0.55, zorder=3)
        for bar in bars: bar.set_linewidth(0)
        ax.set_title("Comparação Regional — Preço Médio", pad=12)
        ax.set_xlabel("Região")
        ax.set_ylabel("Preço Médio")
        ax.tick_params(axis="x", rotation=15)
        st.pyplot(fig, use_container_width=True)

    with col_r2:
        section("Renda Média por Região")
        renda_reg = (
            df_filtrado.groupby("regiao")["renda_media"]
            .mean().sort_values(ascending=False).reset_index()
        )
        fig, ax = plt.subplots(figsize=(6.5, 4))
        fig.patch.set_facecolor("#1e293b")
        ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'R$ {x/1_000:.1f}k'))
        bars = ax.bar(renda_reg["regiao"], renda_reg["renda_media"],
                      color=PALETTE_PURP[:len(renda_reg)], width=0.55, zorder=3)
        for bar in bars: bar.set_linewidth(0)
        ax.set_title("Comparação Regional — Renda Média", pad=12)
        ax.set_xlabel("Região")
        ax.set_ylabel("Renda Média")
        ax.tick_params(axis="x", rotation=15)
        st.pyplot(fig, use_container_width=True)

    insight(
        f"🗺️ <strong>{regiao_cara}</strong> lidera o ranking regional de preços. "
        "A comparação entre preço e renda por região expõe o <strong>índice de esforço habitacional</strong>: "
        "regiões com alto preço e baixa renda apresentam mercados mais excludentes, "
        "onde a maior parte da população depende de financiamentos de longo prazo para acessar a casa própria."
    )

# ══════════════════════════════════════════════
#  ABA 4 — CORRELAÇÕES
# ══════════════════════════════════════════════
with aba4:
    col_c1, col_c2 = st.columns(2, gap="large")

    with col_c1:
        # --- Dispersão Área × Preço ---
        section("Dispersão — Área (m²) × Preço do Imóvel")
        amostra = df_filtrado.sample(min(800, len(df_filtrado)), random_state=42)
        TIPO_CORES = {t: c for t, c in zip(sorted(amostra["tipo_imovel"].unique()), PALETTE_COOL)}

        fig, ax = plt.subplots(figsize=(7, 5))
        fig.patch.set_facecolor("#1e293b")
        for tipo, grupo in amostra.groupby("tipo_imovel"):
            ax.scatter(grupo["area_m2"], grupo["preco_imovel"],
                       label=tipo, alpha=0.55, s=22, color=TIPO_CORES.get(tipo, ACCENT),
                       edgecolors="none")
        ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'R$ {x/1_000:.0f}k'))
        ax.set_title("Relação Área × Preço por Tipo de Imóvel", pad=12)
        ax.set_xlabel("Área (m²)")
        ax.set_ylabel("Preço (R$)")
        ax.legend(framealpha=0.15, labelcolor="white", fontsize=8)
        st.pyplot(fig, use_container_width=True)

        corr_area = df_filtrado["area_m2"].corr(df_filtrado["preco_imovel"])
        insight(
            f"📐 A correlação entre área e preço é de <strong>{corr_area:.2f}</strong>. "
            "Valores próximos de 1 confirmam que a metragem é um <strong>preditor central</strong> do preço — "
            "cada metro quadrado adicional representa incremento significativo no valor do ativo."
        )

    with col_c2:
        # --- Renda × Preço por região ---
        section("Relação Renda Média × Preço por Região")
        renda_preco = (
            df_filtrado.groupby("regiao")
            .agg(renda=("renda_media", "mean"), preco=("preco_imovel", "mean"))
            .reset_index()
        )
        fig, ax = plt.subplots(figsize=(7, 5))
        fig.patch.set_facecolor("#1e293b")
        for i, row in renda_preco.iterrows():
            cor = PALETTE_COOL[i % len(PALETTE_COOL)]
            ax.scatter(row["renda"], row["preco"], s=160, color=cor, zorder=5, edgecolors="#1e293b", linewidth=1.5)
            ax.annotate(row["regiao"], (row["renda"], row["preco"]),
                        textcoords="offset points", xytext=(8, 4),
                        fontsize=9, color="#e2e8f0")
        ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'R$ {x/1_000:.1f}k'))
        ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'R$ {x/1_000:.0f}k'))
        ax.set_title("Renda Média vs. Preço Médio por Região", pad=12)
        ax.set_xlabel("Renda Média Regional")
        ax.set_ylabel("Preço Médio do Imóvel")
        st.pyplot(fig, use_container_width=True)

        corr_renda = df_filtrado["renda_media"].corr(df_filtrado["preco_imovel"])
        insight(
            f"💵 A correlação entre renda e preço é de <strong>{corr_renda:.2f}</strong>. "
            "Regiões com maior renda per capita sustentam preços imobiliários mais elevados, "
            "evidenciando que o <strong>poder aquisitivo local é o principal termômetro do mercado</strong>."
        )

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # --- Juros × Preço anual ---
    section("Impacto da Taxa de Juros no Preço Médio Anual")
    juros_preco = (
        df_filtrado.groupby("ano")
        .agg(preco=("preco_imovel", "mean"), juros=("taxa_juros", "mean"))
        .reset_index().sort_values("ano")
    )
    fig, ax1 = plt.subplots(figsize=(13, 4.5))
    fig.patch.set_facecolor("#1e293b")
    ax2 = ax1.twinx()
    ax1.plot(juros_preco["ano"], juros_preco["preco"], color=ACCENT, linewidth=2.2,
             marker="o", markersize=6, label="Preço Médio", markeredgecolor="#1e293b")
    ax2.plot(juros_preco["ano"], juros_preco["juros"], color="#ef4444", linewidth=1.8,
             linestyle="--", marker="s", markersize=5, label="Taxa de Juros (%)", markeredgecolor="#1e293b")
    ax1.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'R$ {x/1_000:.0f}k'))
    ax2.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{x:.1f}%'))
    ax2.tick_params(axis="y", colors="#ef4444")
    ax2.yaxis.label.set_color("#ef4444")
    ax1.set_title("Preço Médio Anual × Taxa de Juros (Eixo Duplo)", pad=14)
    ax1.set_xlabel("Ano")
    ax1.set_ylabel("Preço Médio (R$)")
    ax2.set_ylabel("Taxa de Juros (%)")
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, framealpha=0.15, labelcolor="white", fontsize=9)
    st.pyplot(fig, use_container_width=True)

    insight(
        "📈 O gráfico de eixo duplo permite identificar a <strong>relação inversa entre juros e preços</strong>. "
        "Quando a taxa Selic sobe, o custo do crédito imobiliário aumenta, reduzindo a demanda e "
        "pressionando os preços. Ciclos de queda de juros, por outro lado, liberam crédito e aquecem o mercado."
    )

# ══════════════════════════════════════════════
#  ABA 5 — CONSULTA SQL
# ══════════════════════════════════════════════
with aba5:
    section("Consulta SQL · SQLAlchemy &amp; SQLite")
    st.markdown(
        "<p style='color:#94a3b8;font-size:0.9rem;margin-bottom:1rem'>"
        "Todos os dados foram persistidos automaticamente em um banco local "
        "(<code>mercado_imobiliario.sqlite</code>). "
        "O quadro abaixo é gerado via consulta SQL pura, demonstrando domínio de engenharia de dados."
        "</p>",
        unsafe_allow_html=True,
    )

    consulta = """\
SELECT regiao,
       tipo_imovel,
       COUNT(*)            AS qtd_imoveis,
       ROUND(AVG(preco_imovel), 2) AS media_preco,
       ROUND(AVG(renda_media),  2) AS renda_local,
       ROUND(AVG(taxa_juros),   2) AS juros_medio
FROM imoveis
GROUP BY regiao, tipo_imovel
ORDER BY media_preco DESC
LIMIT 15"""

    resultado_sql = pd.read_sql(consulta, engine)
    resultado_sql["media_preco"] = resultado_sql["media_preco"].apply(fmt_brl)
    resultado_sql["renda_local"] = resultado_sql["renda_local"].apply(fmt_brl)
    resultado_sql["juros_medio"] = resultado_sql["juros_medio"].apply(lambda x: f"{x:.2f}%")

    st.dataframe(resultado_sql, use_container_width=True, hide_index=True)
    st.code(consulta, language="sql")

# ══════════════════════════════════════════════
#  ABA 6 — BASE DE DADOS
# ══════════════════════════════════════════════
with aba6:
    section("Base de Dados Filtrada")
    st.caption(f"Exibindo **{len(df_filtrado):,}** registros com base nos filtros aplicados.")
    st.dataframe(df_filtrado, use_container_width=True)

# ─────────────────────────────────────────────
#  CONCLUSÃO EXECUTIVA — DINÂMICA (dados reais)
# ─────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.divider()

# Cálculos para a conclusão
preco_ini_serie = preco_ano.iloc[0] if len(preco_ano) > 0 else 0
preco_fim_serie = preco_ano.iloc[-1] if len(preco_ano) > 0 else 0
var_total       = ((preco_fim_serie / preco_ini_serie) - 1) * 100 if preco_ini_serie > 0 else 0

regiao_mais_barata = (
    df_filtrado.groupby("regiao")["preco_imovel"].mean().idxmin()
)
diff_regioes = (
    df_filtrado.groupby("regiao")["preco_imovel"].mean().max() /
    df_filtrado.groupby("regiao")["preco_imovel"].mean().min()
)

st.markdown(f"""
<div style="background:linear-gradient(135deg,#1e293b,#0f172a);border:1px solid rgba(99,179,237,0.15);
            border-radius:16px;padding:1.8rem 2.2rem;">
  <h4 style="color:#e2e8f0;margin:0 0 1rem 0;font-size:1.15rem">
    📌 Conclusão Executiva
  </h4>

  <p style="color:#94a3b8;font-size:0.9rem;line-height:1.8;margin:0 0 0.9rem 0">
    A análise do mercado imobiliário brasileiro entre <strong style="color:#63b3ed">2015 e 2024</strong>
    evidencia um ciclo de valorização consistente: o preço médio nacional saiu de
    <strong style="color:#63b3ed">{fmt_brl(preco_ini_serie)}</strong> para
    <strong style="color:#34d399">{fmt_brl(preco_fim_serie)}</strong>,
    acumulando variação de <strong style="color:#34d399">{var_total:.1f}%</strong> no período —
    equivalente a um crescimento médio anual de <strong style="color:#34d399">{cagr:.1f}% a.a.</strong>
  </p>

  <p style="color:#94a3b8;font-size:0.9rem;line-height:1.8;margin:0 0 0.9rem 0">
    <strong style="color:#63b3ed">Disparidades regionais</strong> são marcantes:
    a região <strong style="color:#a78bfa">{regiao_cara}</strong> lidera o ranking de preços,
    com ticket médio <strong style="color:#a78bfa">{diff_regioes:.1f}×</strong> superior ao da região
    <strong style="color:#a78bfa">{regiao_mais_barata}</strong>.
    Essa diferença reflete a concentração histórica de renda, infraestrutura e
    oferta de emprego nas regiões mais desenvolvidas.
  </p>

  <p style="color:#94a3b8;font-size:0.9rem;line-height:1.8;margin:0 0 0.9rem 0">
    Por tipologia, o segmento <strong style="color:#06b6d4">{tipo_topo}</strong>
    apresenta o maior valor médio, confirmando que imóveis de maior porte e acabamento premium
    concentram os retornos mais expressivos. A relação entre
    <strong style="color:#06b6d4">renda regional e preço</strong>
    (correlação: <strong style="color:#06b6d4">{corr_renda:.2f}</strong>) reforça que
    o poder aquisitivo local é o principal determinante do patamar de preços em cada praça.
  </p>

  <p style="color:#94a3b8;font-size:0.9rem;line-height:1.8;margin:0">
    Do ponto de vista estratégico, o dashboard permite cruzar o impacto da
    <strong style="color:#ef4444">taxa de juros</strong> sobre a demanda com a
    evolução temporal dos preços — sinalizando <em>janelas de oportunidade</em>
    em momentos de retração do crédito e <em>riscos de sobreaquecimento</em> em
    ciclos de juros baixos. Para gestores imobiliários e investidores, os dados
    indicam que <strong style="color:#34d399">{cidade_cara}</strong> permanece como
    a praça de maior valorização absoluta, enquanto mercados emergentes nas
    regiões de menor preço oferecem potencial de crescimento acima da média nacional.
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown(
    "<p style='text-align:center;color:#334155;font-size:0.75rem;margin-top:1rem'>"
    "ImobiAnalytics · Dados simulados · Brasil 2015–2024 · Pandas · Seaborn · Matplotlib · SQLAlchemy · NumPy"
    "</p>",
    unsafe_allow_html=True,
)