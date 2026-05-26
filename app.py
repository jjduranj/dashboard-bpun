import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# CONFIGURACIÓN
# =====================================================

st.set_page_config(
    page_title="Dashboard Ejecutivo BPUN",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

.stApp {
    background-color: #f4f6f9;
}

/* ===== HEADER ===== */

.main-header {
    background: linear-gradient(
        90deg,
        #0b4f2f,
        #166534
    );
    padding: 30px;
    border-radius: 24px;
    color: white;
    margin-bottom: 30px;
    box-shadow: 0px 8px 24px rgba(0,0,0,0.15);
}

.header-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 10px;
}

.header-subtitle {
    font-size: 22px;
    opacity: 0.95;
}

.header-small {
    margin-top: 10px;
    font-size: 16px;
    opacity: 0.85;
}

/* ===== TITULOS ===== */

h1, h2, h3 {
    color: #0b4f2f;
    font-weight: 800;
}

/* ===== SIDEBAR ===== */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #0b4f2f,
        #14532d
    );
}

/* ===== KPI ===== */

.kpi-card {
    background: white;
    padding: 28px;
    border-radius: 24px;
    text-align: center;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
    margin-bottom: 20px;
    transition: 0.3s;
}

.kpi-card:hover {
    transform: translateY(-4px);
}

.kpi-icon {
    font-size: 42px;
}

.kpi-label {
    font-size: 18px;
    color: #64748b;
    margin-top: 12px;
    font-weight: 600;
}

.kpi-value {
    font-size: 34px;
    color: #0b4f2f;
    font-weight: 800;
    margin-top: 15px;
}

/* ===== BLOQUES ===== */

.real-box {
    background: white;
    padding: 28px;
    border-radius: 22px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
}

.future-box {
    background: white;
    padding: 28px;
    border-radius: 22px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
}

.compare-title {
    font-size: 26px;
    font-weight: 800;
    margin-bottom: 25px;
}

.real-title {
    color: #dc2626;
}

.future-title {
    color: #16a34a;
}

.metric-line {
    margin-bottom: 22px;
}

.metric-label {
    font-size: 16px;
    color: #64748b;
    font-weight: 600;
}

.metric-value {
    font-size: 30px;
    font-weight: 800;
    color: #0b4f2f;
}

/* ===== OBSERVACIONES ===== */

.obs-card {
    background: white;
    padding: 24px;
    border-radius: 20px;
    margin-bottom: 18px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.06);
}

/* ===== TABLAS ===== */

[data-testid="stDataFrame"] {
    background: white;
    border-radius: 18px;
    padding: 10px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.06);
}

/* ===== FOOTER ===== */

.footer {
    text-align:center;
    color:gray;
    margin-top:30px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("🌿 Dashboard BPUN")

st.sidebar.markdown("""
### Universidad Nacional de Colombia  
### Sede Amazonia
""")

st.sidebar.success("""
Seguimiento ejecutivo
de proyectos BPUN 2026-I
""")

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="main-header">

<div class="header-title">
📊 Dashboard Ejecutivo BPUN 724-60-100
</div>

<div class="header-subtitle">
Universidad Nacional de Colombia - Sede Amazonia
</div>

<div class="header-small">
Seguimiento Presupuestal Vigencia 2026-I
</div>

</div>
""", unsafe_allow_html=True)

# =====================================================
# LEER EXCEL
# =====================================================

archivo = "datos.xlsx"

df = pd.read_excel(archivo)

# =====================================================
# LIMPIAR COLUMNAS
# =====================================================

df.columns = df.columns.astype(str)
df.columns = df.columns.str.strip()

# =====================================================
# DETECTAR COLUMNAS
# =====================================================

col_quipu = [
    c for c in df.columns
    if "QUIPU" in c
][0]

col_aprop = [
    c for c in df.columns
    if "Apropiación" in c
][0]

col_comp = [
    c for c in df.columns
    if "Valor compromisos" in c
    and "+" not in c
][0]

col_comp_cdp = [
    c for c in df.columns
    if "Compromisos +" in c
][0]

col_saldo = [
    c for c in df.columns
    if "Saldo por Comprometer" in c
    and "CDP" not in c
][0]

col_saldo_cdp = [
    c for c in df.columns
    if "CDP" in c and "saldo" in c.lower()
][0]

col_porcentaje_real = [
    c for c in df.columns
    if "% Comprometido contractualmente" in c
][0]

col_porcentaje_cdp = [
    c for c in df.columns
    if "%" in c and "CDP" in c
][0]

col_observaciones = [
    c for c in df.columns
    if "Observ" in c
][0]

# =====================================================
# LIMPIAR FILAS
# =====================================================

df = df.dropna(how="all")

df = df[
    df[col_quipu].astype(str)
    != "Total general"
]

df = df.dropna(subset=[col_quipu])

# =====================================================
# NUMERICOS
# =====================================================

columnas_numericas = [
    col_aprop,
    col_comp,
    col_comp_cdp,
    col_saldo,
    col_saldo_cdp,
    col_porcentaje_real,
    col_porcentaje_cdp
]

for col in columnas_numericas:

    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

# =====================================================
# PORCENTAJES
# =====================================================

if df[col_porcentaje_real].max() <= 1:

    df[col_porcentaje_real] = (
        df[col_porcentaje_real] * 100
    )

if df[col_porcentaje_cdp].max() <= 1:

    df[col_porcentaje_cdp] = (
        df[col_porcentaje_cdp] * 100
    )

df[col_porcentaje_real] = (
    df[col_porcentaje_real]
    .round(0)
    .astype(int)
)

df[col_porcentaje_cdp] = (
    df[col_porcentaje_cdp]
    .round(0)
    .astype(int)
)

# =====================================================
# KPIS
# =====================================================

apropiacion = df[col_aprop].sum()

comprometido = df[col_comp].sum()

comprometido_cdp = df[col_comp_cdp].sum()

saldo = df[col_saldo].sum()

saldo_cdp = df[col_saldo_cdp].sum()

ejecucion = round(
    df[col_porcentaje_real].mean(),
    0
)

ejecucion_cdp = round(
    df[col_porcentaje_cdp].mean(),
    0
)

# =====================================================
# RESULTADO GENERAL
# =====================================================

st.markdown("## 📌 Resultado General")

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">💰</div>
        <div class="kpi-label">Apropiación Total</div>
        <div class="kpi-value">${apropiacion:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:

    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">✅</div>
        <div class="kpi-label">Comprometido</div>
        <div class="kpi-value">${comprometido:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:

    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">📌</div>
        <div class="kpi-label">Saldo por Comprometer</div>
        <div class="kpi-value">${saldo:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with c4:

    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">📈</div>
        <div class="kpi-label">Ejecución Real</div>
        <div class="kpi-value">{ejecucion:.0f}%</div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# COMPARACIÓN
# =====================================================

st.markdown("---")

st.markdown("## ⚖️ Comparación Estratégica")

c1, c2 = st.columns(2)

with c1:

    st.markdown(f"""
    <div class="real-box">

    <div class="compare-title real-title">
    🔴 Lado Real de Ejecución
    </div>

    <div class="metric-line">
        <div class="metric-label">Apropiación Vigencia</div>
        <div class="metric-value">${apropiacion:,.0f}</div>
    </div>

    <div class="metric-line">
        <div class="metric-label">Valor compromisos</div>
        <div class="metric-value">${comprometido:,.0f}</div>
    </div>

    <div class="metric-line">
        <div class="metric-label">Saldo por Comprometer</div>
        <div class="metric-value">${saldo:,.0f}</div>
    </div>

    <div class="metric-line">
        <div class="metric-label">% Comprometido contractualmente</div>
        <div class="metric-value">{ejecucion:.0f}%</div>
    </div>

    </div>
    """, unsafe_allow_html=True)

with c2:

    st.markdown(f"""
    <div class="future-box">

    <div class="compare-title future-title">
    🟢 Lado Esperanzador y Proyectado
    </div>

    <div class="metric-line">
        <div class="metric-label">Apropiación Vigencia</div>
        <div class="metric-value">${apropiacion:,.0f}</div>
    </div>

    <div class="metric-line">
        <div class="metric-label">Valor Compromisos + CDP</div>
        <div class="metric-value">${comprometido_cdp:,.0f}</div>
    </div>

    <div class="metric-line">
        <div class="metric-label">Saldo por comprometer con CDP</div>
        <div class="metric-value">${saldo_cdp:,.0f}</div>
    </div>

    <div class="metric-line">
        <div class="metric-label">% por comprometer con CDP</div>
        <div class="metric-value">{ejecucion_cdp:.0f}%</div>
    </div>

    </div>
    """, unsafe_allow_html=True)

# =====================================================
# GRAFICA
# =====================================================

st.markdown("---")

st.markdown("## 📊 Comparativo por Proyecto")

fig = go.Figure()

fig.add_trace(go.Bar(

    x=df[col_quipu],

    y=df[col_porcentaje_real],

    name='🔴 Real',

    marker_color='#dc2626',

    text=[
        f"{v:.0f}%"
        for v in df[col_porcentaje_real]
    ],

    textposition='inside',

    insidetextanchor='middle',

    textfont=dict(
        size=16,
        color='white'
    )

))

fig.add_trace(go.Bar(

    x=df[col_quipu],

    y=df[col_porcentaje_cdp],

    name='🟢 Con CDP',

    marker_color='#16a34a',

    text=[
        f"{v:.0f}%"
        for v in df[col_porcentaje_cdp]
    ],

    textposition='inside',

    insidetextanchor='middle',

    textfont=dict(
        size=16,
        color='white'
    )

))

fig.update_layout(

    barmode='group',

    height=700,

    plot_bgcolor="white",

    paper_bgcolor="white",

    yaxis_title="% Ejecución",

    xaxis_title="Proyecto",

    font=dict(
        size=14
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# DETALLADO
# =====================================================

st.markdown("---")

st.markdown("## 📁 Seguimiento Detallado")

df_visual = df.copy()

df_visual[col_porcentaje_real] = (
    df_visual[col_porcentaje_real]
    .astype(str) + "%"
)

df_visual[col_porcentaje_cdp] = (
    df_visual[col_porcentaje_cdp]
    .astype(str) + "%"
)

st.dataframe(
    df_visual,
    use_container_width=True,
    height=700
)

# =====================================================
# OBSERVACIONES
# =====================================================

st.markdown("---")

st.markdown("## 📝 Observaciones Estratégicas")

for i, row in df.iterrows():

    proyecto = row[col_quipu]

    porcentaje_real = row[col_porcentaje_real]

    porcentaje_cdp = row[col_porcentaje_cdp]

    observacion = str(
        row[col_observaciones]
    )

    observacion = observacion.replace("\n", " ")
    observacion = observacion.replace("\r", " ")
    observacion = observacion.replace("<", "")
    observacion = observacion.replace(">", "")

    if porcentaje_real >= 80:

        color = "#16a34a"
        emoji = "🟢"

    elif porcentaje_real >= 50:

        color = "#eab308"
        emoji = "🟡"

    else:

        color = "#dc2626"
        emoji = "🔴"

    st.markdown(f"""
    <div class="obs-card">

    <h4 style="
        color:{color};
        margin-bottom:15px;
    ">
    {emoji} {proyecto}
    </h4>

    <div style="
        font-size:17px;
        color:#334155;
        line-height:1.7;
        margin-bottom:18px;
    ">
    {observacion}
    </div>

    <div style="
        display:flex;
        gap:15px;
        flex-wrap:wrap;
    ">

    <div style="
        background:#fee2e2;
        padding:10px 18px;
        border-radius:12px;
        font-weight:700;
        color:#991b1b;
    ">
    🔴 Real: {porcentaje_real:.0f}%
    </div>

    <div style="
        background:#dcfce7;
        padding:10px 18px;
        border-radius:12px;
        font-weight:700;
        color:#166534;
    ">
    🟢 Esperado con CDP: {porcentaje_cdp:.0f}%
    </div>

    </div>

    </div>
    """, unsafe_allow_html=True)

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.markdown("""
<div class="footer">

### Elaboró:
<b>Jorhan Jhonatan Durán</b><br>
Seguimiento y acompañamiento a proyectos BPUN<br>
Universidad Nacional de Colombia - Sede Amazonia

</div>
""", unsafe_allow_html=True)