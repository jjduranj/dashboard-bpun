import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io

st.set_page_config(
    page_title="Dashboard BPUN 724-60-100",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=DM+Mono:wght@400;500&display=swap');

* { font-family: 'Sora', sans-serif; }
.stApp { background-color: #f0f4f0; }

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #052e16 0%, #064e24 60%, #0b4f2f 100%);
    border-right: 3px solid #16a34a;
}
section[data-testid="stSidebar"] * { color: #d1fae5 !important; }
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 { color: #a7f3d0 !important; }

.main-header {
    background: linear-gradient(135deg, #052e16 0%, #064e24 40%, #0b4f2f 100%);
    padding: 36px 40px;
    border-radius: 20px;
    color: white;
    margin-bottom: 28px;
    box-shadow: 0 8px 32px rgba(5,46,22,0.35);
    position: relative;
    overflow: hidden;
}
.main-header::before {
    content: '';
    position: absolute;
    top: -50%; right: -10%;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(22,163,74,0.15) 0%, transparent 70%);
    border-radius: 50%;
}
.header-badge {
    display: inline-block;
    background: rgba(134,239,172,0.2);
    border: 1px solid rgba(134,239,172,0.4);
    color: #86efac;
    font-size: 12px; font-weight: 600;
    letter-spacing: 2px; text-transform: uppercase;
    padding: 6px 14px; border-radius: 20px;
    margin-bottom: 14px; font-family: 'DM Mono', monospace;
}
.header-title { font-size: 38px; font-weight: 800; margin: 0 0 8px 0; line-height: 1.1; color: #fff; }
.header-sub { font-size: 18px; color: #86efac; font-weight: 400; margin: 0; }
.header-meta { margin-top: 16px; font-size: 13px; color: #6ee7b7; font-family: 'DM Mono', monospace; opacity: 0.8; }

.semaforo-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 28px; }
.semaforo-card {
    border-radius: 18px; padding: 24px 20px;
    text-align: center; position: relative; overflow: hidden;
    box-shadow: 0 4px 20px rgba(0,0,0,0.10);
    transition: transform 0.2s;
}
.semaforo-card:hover { transform: translateY(-3px); }
.semaforo-card.verde { background: linear-gradient(135deg, #15803d, #16a34a); color: white; }
.semaforo-card.amarillo { background: linear-gradient(135deg, #b45309, #d97706); color: white; }
.semaforo-card.rojo { background: linear-gradient(135deg, #b91c1c, #dc2626); color: white; }
.semaforo-num { font-size: 64px; font-weight: 800; line-height: 1; font-family: 'DM Mono', monospace; }
.semaforo-label { font-size: 14px; opacity: 0.9; margin-top: 6px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; }
.semaforo-sub { font-size: 12px; opacity: 0.75; margin-top: 4px; font-family: 'DM Mono', monospace; }
.semaforo-dot {
    position: absolute; width: 120px; height: 120px;
    border-radius: 50%; top: -30px; right: -30px;
    background: rgba(255,255,255,0.08);
}

.kpi-card {
    background: white; border-radius: 16px; padding: 22px 18px;
    box-shadow: 0 2px 16px rgba(5,46,22,0.08); border-left: 4px solid #16a34a;
    position: relative; overflow: hidden; transition: transform 0.2s, box-shadow 0.2s;
    margin-bottom: 4px;
}
.kpi-card:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(5,46,22,0.14); }
.kpi-card.danger { border-left-color: #dc2626; }
.kpi-card.warning { border-left-color: #d97706; }
.kpi-card.info { border-left-color: #0891b2; }
.kpi-card.success { border-left-color: #16a34a; }
.kpi-icon { font-size: 26px; margin-bottom: 8px; display: block; }
.kpi-label { font-size: 11px; color: #64748b; font-weight: 600; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 6px; }
.kpi-value { font-size: 24px; font-weight: 800; color: #0b4f2f; line-height: 1; font-family: 'DM Mono', monospace; }
.kpi-sub { font-size: 11px; color: #94a3b8; margin-top: 5px; font-family: 'DM Mono', monospace; }
.spark { height: 36px; margin-top: 10px; }

.section-title {
    font-size: 20px; font-weight: 800; color: #0b4f2f;
    margin: 28px 0 14px 0; padding-bottom: 10px;
    border-bottom: 2px solid #bbf7d0;
}

.cmp-box { background: white; border-radius: 18px; padding: 28px; box-shadow: 0 2px 16px rgba(5,46,22,0.07); height: 100%; }
.cmp-tag { display: inline-block; padding: 5px 14px; border-radius: 20px; font-size: 12px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 16px; }
.cmp-tag.real { background: #fee2e2; color: #991b1b; }
.cmp-tag.cdp { background: #dcfce7; color: #166534; }
.cmp-row { display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #f1f5f1; }
.cmp-row:last-child { border-bottom: none; }
.cmp-row-label { font-size: 13px; color: #64748b; font-weight: 500; }
.cmp-row-value { font-size: 17px; font-weight: 800; color: #0b4f2f; font-family: 'DM Mono', monospace; }
.cmp-big { font-size: 32px !important; color: #16a34a !important; }
.cmp-big.red { color: #dc2626 !important; }

.rank-row {
    display: flex; align-items: center; gap: 14px;
    background: white; border-radius: 14px; padding: 14px 18px;
    margin-bottom: 10px; box-shadow: 0 2px 10px rgba(5,46,22,0.06);
    transition: transform 0.15s;
}
.rank-row:hover { transform: translateX(4px); }
.rank-medal { font-size: 24px; min-width: 32px; text-align: center; }
.rank-name { flex: 1; font-size: 14px; font-weight: 700; color: #0b4f2f; }
.rank-bar-wrap { flex: 2; background: #f1f5f1; border-radius: 8px; height: 10px; overflow: hidden; }
.rank-bar-inner { height: 100%; border-radius: 8px; }
.rank-pct { font-size: 14px; font-weight: 800; min-width: 48px; text-align: right; font-family: 'DM Mono', monospace; }

.obs-box { background: white; border-radius: 18px; padding: 28px; box-shadow: 0 2px 16px rgba(5,46,22,0.07); margin-bottom: 20px; }
.obs-text { font-size: 15px; color: #334155; line-height: 1.8; white-space: pre-wrap; }
.status-pill { display: inline-flex; align-items: center; gap: 6px; padding: 6px 16px; border-radius: 20px; font-size: 13px; font-weight: 700; margin-right: 10px; margin-top: 12px; }
.pill-real { background: #fee2e2; color: #991b1b; }
.pill-cdp { background: #dcfce7; color: #166534; }

.alert-banner { border-radius: 12px; padding: 14px 18px; margin-bottom: 12px; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 10px; }
.alert-danger { background: #fee2e2; color: #991b1b; border-left: 4px solid #dc2626; }
.alert-success { background: #dcfce7; color: #166534; border-left: 4px solid #16a34a; }

.proj-header { background: white; border-radius: 18px; padding: 30px; box-shadow: 0 2px 16px rgba(5,46,22,0.08); margin-bottom: 20px; border-top: 5px solid #16a34a; }
.proj-name { font-size: 26px; font-weight: 800; color: #0b4f2f; margin-bottom: 6px; }
.proj-sub { font-size: 14px; color: #64748b; font-family: 'DM Mono', monospace; }
.progress-container { background: #f1f5f1; border-radius: 12px; height: 14px; overflow: hidden; margin: 8px 0; }
.progress-bar-real { height: 100%; background: linear-gradient(90deg, #dc2626, #ef4444); border-radius: 12px; }
.progress-bar-cdp { height: 100%; background: linear-gradient(90deg, #16a34a, #22c55e); border-radius: 12px; }
.prog-label { display: flex; justify-content: space-between; font-size: 12px; color: #64748b; margin-top: 4px; }

[data-testid="stDataFrame"] { background: white; border-radius: 14px; overflow: hidden; box-shadow: 0 2px 12px rgba(5,46,22,0.07); }

.footer { text-align: center; color: #94a3b8; margin-top: 40px; font-size: 13px; padding: 20px; border-top: 1px solid #e2e8f0; }
</style>
""", unsafe_allow_html=True)

# ── DATOS ──────────────────────────────────────────────

@st.cache_data
def load_data():
    df = pd.read_excel("datos.xlsx")
    df.columns = df.columns.astype(str).str.strip()

    col_quipu    = [c for c in df.columns if "QUIPU" in c][0]
    col_aprop    = [c for c in df.columns if "Apropiación" in c][0]
    col_comp     = [c for c in df.columns if "Valor compromisos" in c and "+" not in c][0]
    col_comp_cdp = [c for c in df.columns if "Compromisos +" in c][0]
    col_saldo    = [c for c in df.columns if "Saldo por Comprometer" in c and "CDP" not in c][0]
    col_saldo_cdp= [c for c in df.columns if "CDP" in c and "saldo" in c.lower()][0]
    col_pct_real = [c for c in df.columns if "% Comprometido contractualmente" in c][0]
    col_pct_cdp  = [c for c in df.columns if "%" in c and "CDP" in c][0]
    col_obs      = [c for c in df.columns if "Observ" in c][0]

    df = df.dropna(how="all")
    df = df[df[col_quipu].astype(str) != "Total general"]
    df = df.dropna(subset=[col_quipu])

    for col in [col_aprop, col_comp, col_comp_cdp, col_saldo, col_saldo_cdp, col_pct_real, col_pct_cdp]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    if df[col_pct_real].max() <= 1: df[col_pct_real] *= 100
    if df[col_pct_cdp].max()  <= 1: df[col_pct_cdp]  *= 100

    df[col_pct_real] = df[col_pct_real].round(1)
    df[col_pct_cdp]  = df[col_pct_cdp].round(1)

    return df, {"quipu": col_quipu, "aprop": col_aprop, "comp": col_comp,
                "comp_cdp": col_comp_cdp, "saldo": col_saldo, "saldo_cdp": col_saldo_cdp,
                "pct_real": col_pct_real, "pct_cdp": col_pct_cdp, "obs": col_obs}

df, C = load_data()

def fmt(v): return f"${v:,.0f}" if not pd.isna(v) else "$0"
def fmt_m(v): return f"${v/1_000_000:.1f}M" if not pd.isna(v) else "$0"

def status(pct):
    if pct >= 80: return "success", "🟢", "#16a34a", "Ejecución alta"
    if pct >= 50: return "warning", "🟡", "#d97706", "Ejecución media"
    return "danger", "🔴", "#dc2626", "Ejecución baja"

def short(name):
    parts = str(name).split(" ", 1)
    return parts[1] if len(parts) > 1 else name

# ── EXPORTAR EXCEL ─────────────────────────────────────

def export_excel(df_exp):
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="xlsxwriter") as writer:
        df_exp.to_excel(writer, index=False, sheet_name="BPUN")
        wb = writer.book
        ws = writer.sheets["BPUN"]
        hdr = wb.add_format({"bold": True, "bg_color": "#0b4f2f", "font_color": "white", "border": 1})
        for col_num, val in enumerate(df_exp.columns):
            ws.write(0, col_num, val, hdr)
            ws.set_column(col_num, col_num, 22)
    buf.seek(0)
    return buf

# ── SIDEBAR ────────────────────────────────────────────

st.sidebar.markdown("""
<div style="padding:10px 0 20px 0;">
  <div style="font-size:11px;letter-spacing:2px;text-transform:uppercase;color:#6ee7b7;margin-bottom:6px;font-family:'DM Mono',monospace;">Universidad Nacional</div>
  <div style="font-size:18px;font-weight:800;color:#d1fae5;">Sede Amazonia</div>
  <div style="font-size:13px;color:#6ee7b7;margin-top:4px;">BPUN 724-60-100 · 2026-I</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🗂️ Navegación")
vista = st.sidebar.radio("Vista:", ["📊 Resumen General", "🔍 Por Proyecto"], label_visibility="collapsed")

if vista == "🔍 Por Proyecto":
    st.sidebar.markdown("### 📁 Proyecto")
    proyecto_sel = st.sidebar.selectbox("Proyecto:", df[C["quipu"]].tolist(), label_visibility="collapsed")

st.sidebar.markdown("---")
total_aprop  = df[C["aprop"]].sum()
pct_media    = df[C["pct_real"]].mean()
st.sidebar.markdown(f"""
<div style="padding:12px;background:rgba(134,239,172,0.1);border-radius:12px;">
  <div style="font-size:11px;color:#6ee7b7;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;">Resumen rápido</div>
  <div style="font-size:13px;color:#d1fae5;margin-bottom:4px;">💰 Apropiación total</div>
  <div style="font-size:16px;font-weight:700;color:#86efac;font-family:'DM Mono',monospace;">{fmt(total_aprop)}</div>
  <div style="font-size:13px;color:#d1fae5;margin-top:10px;margin-bottom:4px;">📈 Ejecución promedio</div>
  <div style="font-size:16px;font-weight:700;color:#86efac;font-family:'DM Mono',monospace;">{pct_media:.1f}%</div>
  <div style="font-size:12px;color:#6ee7b7;margin-top:8px;">{len(df)} proyectos activos</div>
</div>
""", unsafe_allow_html=True)

# ── HEADER ─────────────────────────────────────────────

st.markdown("""
<div class="main-header">
  <div class="header-badge">Seguimiento Presupuestal · Vigencia 2026-I</div>
  <div class="header-title">📊 Dashboard Ejecutivo BPUN 724-60-100</div>
  <div class="header-sub">Universidad Nacional de Colombia — Sede Amazonia</div>
  <div class="header-meta">Elaborado por: Jorhan Jhonatan Durán · Seguimiento y acompañamiento a proyectos BPUN</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# VISTA GENERAL
# ══════════════════════════════════════════════════════

if vista == "📊 Resumen General":

    apropiacion     = df[C["aprop"]].sum()
    comprometido    = df[C["comp"]].sum()
    comprometido_cdp= df[C["comp_cdp"]].sum()
    saldo           = df[C["saldo"]].sum()
    saldo_cdp       = df[C["saldo_cdp"]].sum()
    ejecucion       = df[C["pct_real"]].mean()
    ejecucion_cdp   = df[C["pct_cdp"]].mean()

    n_verde   = int((df[C["pct_real"]] >= 80).sum())
    n_amarillo= int(((df[C["pct_real"]] >= 50) & (df[C["pct_real"]] < 80)).sum())
    n_rojo    = int((df[C["pct_real"]] < 50).sum())

    # ── ALERTAS ──────────────────────────────────────
    bajos  = df[df[C["pct_real"]] < 50]
    altos  = df[df[C["pct_real"]] >= 80]
    if len(bajos):
        st.markdown(f'<div class="alert-banner alert-danger">⚠️ <strong>{len(bajos)} proyecto(s) con ejecución real menor al 50%:</strong> {", ".join(bajos[C["quipu"]].tolist())}</div>', unsafe_allow_html=True)
    if len(altos):
        st.markdown(f'<div class="alert-banner alert-success">✅ <strong>{len(altos)} proyecto(s) con ejecución real mayor al 80%:</strong> {", ".join(altos[C["quipu"]].tolist())}</div>', unsafe_allow_html=True)

    # ── SEMÁFORO ─────────────────────────────────────
    st.markdown('<div class="section-title">🚦 Semáforo Ejecutivo</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="semaforo-grid">
      <div class="semaforo-card verde">
        <div class="semaforo-dot"></div>
        <div class="semaforo-num">{n_verde}</div>
        <div class="semaforo-label">En meta</div>
        <div class="semaforo-sub">Ejecución ≥ 80%</div>
      </div>
      <div class="semaforo-card amarillo">
        <div class="semaforo-dot"></div>
        <div class="semaforo-num">{n_amarillo}</div>
        <div class="semaforo-label">En proceso</div>
        <div class="semaforo-sub">Ejecución 50–79%</div>
      </div>
      <div class="semaforo-card rojo">
        <div class="semaforo-dot"></div>
        <div class="semaforo-num">{n_rojo}</div>
        <div class="semaforo-label">Crítico</div>
        <div class="semaforo-sub">Ejecución &lt; 50%</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPIs CON SPARKLINES ───────────────────────────
    st.markdown('<div class="section-title">📌 Indicadores Generales</div>', unsafe_allow_html=True)

    vals_aprop = df[C["aprop"]].tolist()
    vals_comp  = df[C["comp"]].tolist()
    vals_saldo = df[C["saldo"]].tolist()
    vals_pct   = df[C["pct_real"]].tolist()

    def make_spark(values, color):
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        fill = f"rgba({r},{g},{b},0.15)"
        fig = go.Figure(go.Scatter(
            y=values, mode="lines", fill="tozeroy",
            line=dict(color=color, width=2),
            fillcolor=fill
        ))
        fig.update_layout(
            margin=dict(l=0,r=0,t=0,b=0), height=48,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(visible=False), yaxis=dict(visible=False),
            showlegend=False
        )
        return fig

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""<div class="kpi-card info">
          <span class="kpi-icon">💰</span>
          <div class="kpi-label">Apropiación Total</div>
          <div class="kpi-value">{fmt(apropiacion)}</div>
          <div class="kpi-sub">Vigencia 2026-I</div>
        </div>""", unsafe_allow_html=True)
        st.plotly_chart(make_spark(vals_aprop, "#0891b2"), use_container_width=True, config={"displayModeBar": False}, key="spark1")

    with c2:
        st.markdown(f"""<div class="kpi-card success">
          <span class="kpi-icon">✅</span>
          <div class="kpi-label">Comprometido Real</div>
          <div class="kpi-value">{fmt(comprometido)}</div>
          <div class="kpi-sub">{ejecucion:.1f}% del total</div>
        </div>""", unsafe_allow_html=True)
        st.plotly_chart(make_spark(vals_comp, "#16a34a"), use_container_width=True, config={"displayModeBar": False}, key="spark2")

    with c3:
        st.markdown(f"""<div class="kpi-card warning">
          <span class="kpi-icon">📌</span>
          <div class="kpi-label">Saldo por Comprometer</div>
          <div class="kpi-value">{fmt(saldo)}</div>
          <div class="kpi-sub">Sin considerar CDP</div>
        </div>""", unsafe_allow_html=True)
        st.plotly_chart(make_spark(vals_saldo, "#d97706"), use_container_width=True, config={"displayModeBar": False}, key="spark3")

    with c4:
        st.markdown(f"""<div class="kpi-card danger">
          <span class="kpi-icon">📈</span>
          <div class="kpi-label">Ejecución Promedio</div>
          <div class="kpi-value">{ejecucion:.1f}%</div>
          <div class="kpi-sub">Con CDP: {ejecucion_cdp:.1f}%</div>
        </div>""", unsafe_allow_html=True)
        st.plotly_chart(make_spark(vals_pct, "#dc2626"), use_container_width=True, config={"displayModeBar": False}, key="spark4")

    # ── COMPARACIÓN ESTRATÉGICA ───────────────────────
    st.markdown('<div class="section-title">⚖️ Comparación Estratégica</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""<div class="cmp-box">
          <span class="cmp-tag real">🔴 Ejecución Real</span>
          <div class="cmp-row"><span class="cmp-row-label">Apropiación vigencia</span><span class="cmp-row-value">{fmt(apropiacion)}</span></div>
          <div class="cmp-row"><span class="cmp-row-label">Valor compromisos</span><span class="cmp-row-value">{fmt(comprometido)}</span></div>
          <div class="cmp-row"><span class="cmp-row-label">Saldo por comprometer</span><span class="cmp-row-value">{fmt(saldo)}</span></div>
          <div class="cmp-row"><span class="cmp-row-label">% Comprometido</span><span class="cmp-row-value cmp-big red">{ejecucion:.1f}%</span></div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="cmp-box">
          <span class="cmp-tag cdp">🟢 Proyección con CDP</span>
          <div class="cmp-row"><span class="cmp-row-label">Apropiación vigencia</span><span class="cmp-row-value">{fmt(apropiacion)}</span></div>
          <div class="cmp-row"><span class="cmp-row-label">Compromisos + CDP</span><span class="cmp-row-value">{fmt(comprometido_cdp)}</span></div>
          <div class="cmp-row"><span class="cmp-row-label">Saldo con CDP</span><span class="cmp-row-value">{fmt(saldo_cdp)}</span></div>
          <div class="cmp-row"><span class="cmp-row-label">% con CDP</span><span class="cmp-row-value cmp-big">{ejecucion_cdp:.1f}%</span></div>
        </div>""", unsafe_allow_html=True)

    # ── GRÁFICAS ─────────────────────────────────────
    st.markdown('<div class="section-title">📊 Análisis Visual</div>', unsafe_allow_html=True)
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Ejecución %", "💵 Montos $", "📉 Saldos $", "🍩 Distribución", "🎯 Real vs CDP"])

    proj_short = [short(p) for p in df[C["quipu"]].tolist()]
    VERDE, ROJO = "#16a34a", "#dc2626"
    AZUL, NARANJA = "#0891b2", "#d97706"

    with tab1:
        fig = go.Figure()
        fig.add_trace(go.Bar(x=proj_short, y=df[C["pct_real"]], name="🔴 Real",
            marker_color=ROJO, text=[f"{v:.0f}%" for v in df[C["pct_real"]]],
            textposition="inside", insidetextanchor="middle", textfont=dict(size=13, color="white")))
        fig.add_trace(go.Bar(x=proj_short, y=df[C["pct_cdp"]], name="🟢 Con CDP",
            marker_color=VERDE, text=[f"{v:.0f}%" for v in df[C["pct_cdp"]]],
            textposition="inside", insidetextanchor="middle", textfont=dict(size=13, color="white")))
        fig.add_hline(y=80, line_dash="dash", line_color="#f59e0b",
            annotation_text="Meta 80%", annotation_position="right", line_width=2)
        fig.update_layout(barmode="group", height=460, plot_bgcolor="white", paper_bgcolor="white",
            yaxis=dict(title="% Ejecución", range=[0,115], gridcolor="#f1f5f1"),
            xaxis=dict(tickangle=-25), legend=dict(orientation="h", y=1.1, x=1, xanchor="right"),
            margin=dict(l=20,r=20,t=40,b=60), font=dict(family="Sora"))
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=proj_short, y=df[C["aprop"]]/1e6, name="Apropiación", marker_color=AZUL,
            text=[fmt_m(v) for v in df[C["aprop"]]], textposition="inside", textfont=dict(color="white", size=11)))
        fig2.add_trace(go.Bar(x=proj_short, y=df[C["comp"]]/1e6, name="Comprometido Real", marker_color=ROJO,
            text=[fmt_m(v) for v in df[C["comp"]]], textposition="inside", textfont=dict(color="white", size=11)))
        fig2.add_trace(go.Bar(x=proj_short, y=df[C["comp_cdp"]]/1e6, name="Con CDP", marker_color=VERDE,
            text=[fmt_m(v) for v in df[C["comp_cdp"]]], textposition="inside", textfont=dict(color="white", size=11)))
        fig2.update_layout(barmode="group", height=460, plot_bgcolor="white", paper_bgcolor="white",
            yaxis=dict(title="Millones COP", gridcolor="#f1f5f1"),
            xaxis=dict(tickangle=-25), legend=dict(orientation="h", y=1.1, x=1, xanchor="right"),
            margin=dict(l=20,r=20,t=40,b=60), font=dict(family="Sora"))
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        # Waterfall de saldos
        measure = ["relative"] * len(proj_short) + ["total"]
        x_wf = proj_short + ["TOTAL"]
        y_wf = list(df[C["saldo"]]/1e6) + [df[C["saldo"]].sum()/1e6]
        text_wf = [fmt_m(v) for v in df[C["saldo"]].tolist()] + [fmt_m(df[C["saldo"]].sum())]
        fig3 = go.Figure(go.Waterfall(
            orientation="v", measure=measure,
            x=x_wf, y=y_wf,
            text=text_wf, textposition="outside",
            connector={"line": {"color": "#cbd5e1", "width": 1}},
            increasing={"marker": {"color": NARANJA}},
            totals={"marker": {"color": AZUL}},
            decreasing={"marker": {"color": ROJO}},
        ))
        fig3.update_layout(
            title="Cascada de saldos por comprometer (Millones COP)",
            title_font=dict(size=15, family="Sora"), height=460,
            plot_bgcolor="white", paper_bgcolor="white",
            yaxis=dict(title="Millones COP", gridcolor="#f1f5f1"),
            xaxis=dict(tickangle=-25),
            margin=dict(l=20,r=20,t=60,b=60), font=dict(family="Sora"))
        st.plotly_chart(fig3, use_container_width=True)

    with tab4:
        # Donut de distribución de apropiación
        fig4 = go.Figure(go.Pie(
            labels=proj_short,
            values=df[C["aprop"]].tolist(),
            hole=0.55,
            textinfo="label+percent",
            textfont=dict(size=12, family="Sora"),
            marker=dict(colors=[
                "#0b4f2f","#15803d","#16a34a","#22c55e","#4ade80",
                "#0891b2","#0e7490","#155e75","#164e63"
            ], line=dict(color="white", width=2)),
            hovertemplate="<b>%{label}</b><br>%{value:,.0f} COP<br>%{percent}<extra></extra>"
        ))
        fig4.update_layout(
            annotations=[dict(text=f"<b>{fmt_m(total_aprop)}</b><br>Total", x=0.5, y=0.5,
                font_size=16, showarrow=False, font=dict(family="DM Mono"))],
            height=500, paper_bgcolor="white",
            legend=dict(orientation="v", x=1.0, y=0.5),
            margin=dict(l=20,r=120,t=40,b=40), font=dict(family="Sora"))
        st.plotly_chart(fig4, use_container_width=True)

    with tab5:
        # Scatter real vs CDP
        df_sc = df.copy()
        df_sc["short"] = proj_short
        _, _, colors_sc, _ = zip(*[status(p) for p in df_sc[C["pct_real"]]])

        fig5 = go.Figure()
        # línea diagonal referencia
        fig5.add_trace(go.Scatter(x=[0,100], y=[0,100], mode="lines",
            line=dict(color="#94a3b8", dash="dash", width=1),
            name="Igualdad Real=CDP", showlegend=True))
        # puntos
        fig5.add_trace(go.Scatter(
            x=df_sc[C["pct_real"]], y=df_sc[C["pct_cdp"]],
            mode="markers+text",
            text=df_sc["short"], textposition="top center",
            textfont=dict(size=11, family="Sora"),
            marker=dict(size=18, color=list(colors_sc),
                line=dict(color="white", width=2), opacity=0.9),
            hovertemplate="<b>%{text}</b><br>Real: %{x:.1f}%<br>Con CDP: %{y:.1f}%<extra></extra>",
            name="Proyectos"
        ))
        fig5.add_hline(y=80, line_dash="dot", line_color="#f59e0b", line_width=1.5,
            annotation_text="Meta CDP 80%", annotation_position="right")
        fig5.add_vline(x=80, line_dash="dot", line_color="#f59e0b", line_width=1.5,
            annotation_text="Meta Real 80%", annotation_position="top")
        fig5.update_layout(
            height=480, plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(title="% Ejecución Real", range=[-5,110], gridcolor="#f1f5f1"),
            yaxis=dict(title="% Ejecución con CDP", range=[-5,110], gridcolor="#f1f5f1"),
            legend=dict(orientation="h", y=1.1, x=0),
            margin=dict(l=40,r=20,t=40,b=60), font=dict(family="Sora"))
        st.plotly_chart(fig5, use_container_width=True)
        st.caption("Puntos sobre la diagonal: el CDP agrega valor. Puntos en el cuadrante verde (derecha-arriba): en o cerca de la meta.")

    # ── RANKING ──────────────────────────────────────
    st.markdown('<div class="section-title">🏆 Ranking de Proyectos por Ejecución Real</div>', unsafe_allow_html=True)

    df_rank = df.sort_values(C["pct_real"], ascending=False).reset_index(drop=True)
    medals = ["🥇", "🥈", "🥉"] + ["·"] * (len(df_rank) - 3)

    for i, row in df_rank.iterrows():
        pct = row[C["pct_real"]]
        pct_c = row[C["pct_cdp"]]
        _, _, color, _ = status(pct)
        bar_color = color
        st.markdown(f"""
        <div class="rank-row">
          <div class="rank-medal">{medals[i]}</div>
          <div class="rank-name">{row[C["quipu"]]}</div>
          <div style="flex:3;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
              <div class="rank-bar-wrap" style="flex:1;">
                <div class="rank-bar-inner" style="width:{min(pct,100):.1f}%;background:{bar_color};"></div>
              </div>
              <span class="rank-pct" style="color:{bar_color};">{pct:.0f}%</span>
            </div>
            <div style="display:flex;align-items:center;gap:8px;">
              <div class="rank-bar-wrap" style="flex:1;">
                <div class="rank-bar-inner" style="width:{min(pct_c,100):.1f}%;background:#16a34a;opacity:0.5;"></div>
              </div>
              <span class="rank-pct" style="color:#16a34a;opacity:0.7;">{pct_c:.0f}%</span>
            </div>
          </div>
          <div style="font-size:12px;color:#94a3b8;min-width:80px;text-align:right;font-family:'DM Mono',monospace;">{fmt_m(row[C["aprop"]])}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── TABLA DETALLADA ───────────────────────────────
    st.markdown('<div class="section-title">📁 Seguimiento Detallado</div>', unsafe_allow_html=True)

    df_vis = df[[C["quipu"], C["aprop"], C["comp"], C["comp_cdp"],
                  C["saldo"], C["saldo_cdp"], C["pct_real"], C["pct_cdp"]]].copy()
    df_vis.columns = ["Proyecto", "Apropiación", "Comprometido Real",
                       "Comprometido+CDP", "Saldo Real", "Saldo con CDP", "% Real", "% con CDP"]
    df_vis["% Real"]    = df_vis["% Real"].map(lambda x: f"{x:.1f}%")
    df_vis["% con CDP"] = df_vis["% con CDP"].map(lambda x: f"{x:.1f}%")
    for col in ["Apropiación","Comprometido Real","Comprometido+CDP","Saldo Real","Saldo con CDP"]:
        df_vis[col] = df_vis[col].map(fmt)

    st.dataframe(df_vis, use_container_width=True, hide_index=True, height=360)

    # ── EXPORTAR ──────────────────────────────────────
    st.markdown('<div class="section-title">⬇️ Exportar Datos</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        buf = export_excel(df_vis)
        st.download_button(
            label="📥 Descargar Excel — Resumen General",
            data=buf,
            file_name="BPUN_resumen_2026I.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    with c2:
        csv = df_vis.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📄 Descargar CSV — Resumen General",
            data=csv,
            file_name="BPUN_resumen_2026I.csv",
            mime="text/csv",
            use_container_width=True
        )

    # ── OBSERVACIONES ─────────────────────────────────
    st.markdown('<div class="section-title">📝 Observaciones por Proyecto</div>', unsafe_allow_html=True)
    for _, row in df.iterrows():
        obs = str(row[C["obs"]]).strip().replace("<","").replace(">","")
        pct  = row[C["pct_real"]]
        pctc = row[C["pct_cdp"]]
        _, emoji, color, label = status(pct)
        st.markdown(f"""
        <div class="obs-box">
          <div style="display:flex;align-items:center;gap:12px;margin-bottom:14px;">
            <span style="font-size:20px;">{emoji}</span>
            <div>
              <div style="font-size:17px;font-weight:800;color:{color};">{row[C["quipu"]]}</div>
              <div style="font-size:12px;color:#94a3b8;font-family:'DM Mono',monospace;">{label}</div>
            </div>
          </div>
          <div class="obs-text">{obs if obs != "nan" else "Sin observaciones registradas."}</div>
          <div>
            <span class="status-pill pill-real">🔴 Real: {pct:.1f}%</span>
            <span class="status-pill pill-cdp">🟢 Con CDP: {pctc:.1f}%</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# VISTA POR PROYECTO
# ══════════════════════════════════════════════════════

else:
    row = df[df[C["quipu"]] == proyecto_sel].iloc[0]
    pct_real = row[C["pct_real"]]
    pct_cdp  = row[C["pct_cdp"]]
    aprop    = row[C["aprop"]]
    comp     = row[C["comp"]]
    comp_cdp = row[C["comp_cdp"]]
    sal      = row[C["saldo"]]
    sal_cdp  = row[C["saldo_cdp"]]
    obs      = str(row[C["obs"]]).strip().replace("<","").replace(">","")

    _, emoji_s, color, label_s = status(pct_real)

    # Cabecera proyecto
    st.markdown(f"""
    <div class="proj-header" style="border-top-color:{color};">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:16px;">
        <div>
          <div class="proj-name">{emoji_s} {proyecto_sel}</div>
          <div class="proj-sub">{label_s} · Corte 2026-I</div>
        </div>
        <div style="text-align:right;">
          <div style="font-size:56px;font-weight:800;color:{color};font-family:'DM Mono',monospace;line-height:1;">{pct_real:.0f}%</div>
          <div style="font-size:13px;color:#94a3b8;">ejecución real</div>
        </div>
      </div>
      <div style="margin-top:20px;">
        <div style="font-size:12px;color:#64748b;margin-bottom:6px;">🔴 Ejecución contractual real</div>
        <div class="progress-container"><div class="progress-bar-real" style="width:{min(pct_real,100):.1f}%;"></div></div>
        <div class="prog-label"><span>{pct_real:.1f}% comprometido</span><span>100% meta</span></div>
        <div style="font-size:12px;color:#64748b;margin-top:14px;margin-bottom:6px;">🟢 Proyección con CDP en trámite</div>
        <div class="progress-container"><div class="progress-bar-cdp" style="width:{min(pct_cdp,100):.1f}%;"></div></div>
        <div class="prog-label"><span>{pct_cdp:.1f}% proyectado</span><span>100% meta</span></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # KPIs del proyecto
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="kpi-card info"><span class="kpi-icon">💰</span>
          <div class="kpi-label">Apropiación</div><div class="kpi-value">{fmt(aprop)}</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="kpi-card danger"><span class="kpi-icon">✅</span>
          <div class="kpi-label">Comprometido Real</div><div class="kpi-value">{fmt(comp)}</div>
          <div class="kpi-sub">{pct_real:.1f}% del total</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="kpi-card success"><span class="kpi-icon">📋</span>
          <div class="kpi-label">Proyectado con CDP</div><div class="kpi-value">{fmt(comp_cdp)}</div>
          <div class="kpi-sub">{pct_cdp:.1f}% proyectado</div></div>""", unsafe_allow_html=True)

    st.markdown("&nbsp;", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""<div class="kpi-card warning"><span class="kpi-icon">📌</span>
          <div class="kpi-label">Saldo por Comprometer (Real)</div><div class="kpi-value">{fmt(sal)}</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="kpi-card success"><span class="kpi-icon">📌</span>
          <div class="kpi-label">Saldo con CDP en Trámite</div><div class="kpi-value">{fmt(sal_cdp)}</div></div>""", unsafe_allow_html=True)

    # Velocímetros
    st.markdown('<div class="section-title">📊 Posición vs. Promedio General</div>', unsafe_allow_html=True)
    media_real = df[C["pct_real"]].mean()
    media_cdp  = df[C["pct_cdp"]].mean()
    col_g1, col_g2 = st.columns(2)

    for col_g, val, ref, label_g, bar_color in [
        (col_g1, pct_real, media_real, "Ejecución Real", "#dc2626"),
        (col_g2, pct_cdp,  media_cdp,  "Proyectado con CDP", "#16a34a"),
    ]:
        with col_g:
            fig_g = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=val,
                title={"text": label_g, "font": {"size": 16, "family": "Sora"}},
                delta={"reference": ref, "suffix": "%", "valueformat": ".1f"},
                gauge={
                    "axis": {"range": [0,100], "ticksuffix": "%"},
                    "bar": {"color": bar_color},
                    "steps": [
                        {"range": [0,50],  "color": "#fee2e2"},
                        {"range": [50,80], "color": "#fef3c7"},
                        {"range": [80,100],"color": "#dcfce7"},
                    ],
                    "threshold": {"line": {"color": "#d97706","width":4}, "thickness":0.75, "value": ref}
                },
                number={"suffix":"%","valueformat":".1f","font":{"size":34,"family":"DM Mono"}}
            ))
            fig_g.update_layout(height=270, margin=dict(l=20,r=20,t=60,b=10), paper_bgcolor="white", font=dict(family="Sora"))
            st.plotly_chart(fig_g, use_container_width=True)
            st.markdown(f'<div style="text-align:center;font-size:12px;color:#94a3b8;margin-top:-14px;">Promedio general: <b>{ref:.1f}%</b></div>', unsafe_allow_html=True)

    # Comparativo con todos los proyectos (resaltado)
    st.markdown('<div class="section-title">📈 Este Proyecto vs. Todos los Demás</div>', unsafe_allow_html=True)
    proj_labels_all = [short(p) for p in df[C["quipu"]].tolist()]
    colores_real = ["#dc2626" if p == proyecto_sel else "#fca5a5" for p in df[C["quipu"]].tolist()]
    colores_cdp  = ["#16a34a" if p == proyecto_sel else "#86efac" for p in df[C["quipu"]].tolist()]

    fig_cmp = go.Figure()
    fig_cmp.add_trace(go.Bar(x=proj_labels_all, y=df[C["pct_real"]], name="🔴 Real",
        marker_color=colores_real,
        text=[f"{v:.0f}%" for v in df[C["pct_real"]]],
        textposition="inside", textfont=dict(size=12, color="white")))
    fig_cmp.add_trace(go.Bar(x=proj_labels_all, y=df[C["pct_cdp"]], name="🟢 Con CDP",
        marker_color=colores_cdp,
        text=[f"{v:.0f}%" for v in df[C["pct_cdp"]]],
        textposition="inside", textfont=dict(size=12, color="white")))
    fig_cmp.add_hline(y=80, line_dash="dash", line_color="#f59e0b",
        annotation_text="Meta 80%", annotation_position="right", line_width=2)
    fig_cmp.update_layout(barmode="group", height=400, plot_bgcolor="white", paper_bgcolor="white",
        yaxis=dict(title="% Ejecución", range=[0,115], gridcolor="#f1f5f1"),
        xaxis=dict(tickangle=-25), legend=dict(orientation="h", y=1.1, x=1, xanchor="right"),
        margin=dict(l=20,r=20,t=40,b=60), font=dict(family="Sora"))
    st.plotly_chart(fig_cmp, use_container_width=True)
    st.caption("El proyecto seleccionado aparece con color más intenso.")

    # Donut individual del proyecto
    st.markdown('<div class="section-title">🍩 Composición del Presupuesto</div>', unsafe_allow_html=True)
    comp_restante = max(aprop - comp, 0)
    cdp_adicional = max(comp_cdp - comp, 0)
    fig_donut = go.Figure(go.Pie(
        labels=["Comprometido Real", "CDP Adicional", "Saldo libre"],
        values=[comp, cdp_adicional, comp_restante - cdp_adicional],
        hole=0.60,
        marker=dict(colors=["#dc2626","#f59e0b","#e2e8f0"], line=dict(color="white", width=2)),
        textinfo="label+percent",
        textfont=dict(size=12, family="Sora"),
        hovertemplate="<b>%{label}</b><br>%{value:,.0f} COP<br>%{percent}<extra></extra>"
    ))
    fig_donut.update_layout(
        annotations=[dict(text=f"<b>{pct_real:.0f}%</b><br>real", x=0.5, y=0.5,
            font_size=18, showarrow=False, font=dict(family="DM Mono"))],
        height=400, paper_bgcolor="white",
        margin=dict(l=20,r=20,t=20,b=20), font=dict(family="Sora"))
    st.plotly_chart(fig_donut, use_container_width=True)

    # Observaciones
    st.markdown('<div class="section-title">📝 Observaciones del Proyecto</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="obs-box">
      <div class="obs-text">{obs if obs != "nan" else "Sin observaciones registradas."}</div>
      <div style="margin-top:16px;">
        <span class="status-pill pill-real">🔴 Real: {pct_real:.1f}%</span>
        <span class="status-pill pill-cdp">🟢 Con CDP: {pct_cdp:.1f}%</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Exportar proyecto individual
    st.markdown('<div class="section-title">⬇️ Exportar Este Proyecto</div>', unsafe_allow_html=True)
    df_proj = df[df[C["quipu"]] == proyecto_sel][[
        C["quipu"], C["aprop"], C["comp"], C["comp_cdp"],
        C["saldo"], C["saldo_cdp"], C["pct_real"], C["pct_cdp"], C["obs"]
    ]].copy()
    df_proj.columns = ["Proyecto","Apropiación","Comprometido Real","Comprometido+CDP",
                        "Saldo Real","Saldo con CDP","% Real","% con CDP","Observaciones"]

    c1, c2 = st.columns(2)
    with c1:
        buf_p = export_excel(df_proj)
        st.download_button(
            label=f"📥 Descargar Excel — {short(proyecto_sel)}",
            data=buf_p,
            file_name=f"BPUN_{short(proyecto_sel).replace(' ','_')}_2026I.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    with c2:
        csv_p = df_proj.to_csv(index=False).encode("utf-8")
        st.download_button(
            label=f"📄 Descargar CSV — {short(proyecto_sel)}",
            data=csv_p,
            file_name=f"BPUN_{short(proyecto_sel).replace(' ','_')}_2026I.csv",
            mime="text/csv",
            use_container_width=True
        )

# ── FOOTER ─────────────────────────────────────────────

st.markdown("""
<div class="footer">
  <b>Elaboró:</b> Jorhan Jhonatan Durán · Seguimiento y acompañamiento a proyectos BPUN<br>
  Universidad Nacional de Colombia — Sede Amazonia · Vigencia 2026-I
</div>
""", unsafe_allow_html=True)