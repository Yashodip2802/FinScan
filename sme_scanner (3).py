import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import random

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FinScan — SME Financial Health Scanner",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── DESIGN SYSTEM ──────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --bg:       #06080C;
  --bg1:      #0C1018;
  --bg2:      #111620;
  --bg3:      #161D2A;
  --border:   rgba(255,255,255,0.06);
  --border2:  rgba(255,255,255,0.1);
  --teal:     #00D4AA;
  --teal2:    #00A882;
  --red:      #FF4757;
  --amber:    #FFB830;
  --blue:     #4A9FFF;
  --text:     #E8ECF4;
  --muted:    rgba(232,236,244,0.45);
  --faint:    rgba(232,236,244,0.18);
}

html, body, [class*="css"] {
  font-family: 'Outfit', -apple-system, system-ui, sans-serif !important;
  background: var(--bg) !important;
  color: var(--text) !important;
}
.main, .block-container { background: var(--bg) !important; }
.block-container { padding: 1.5rem 2.5rem 4rem !important; max-width: 1380px !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
  background: var(--bg1) !important;
  border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] .block-container { padding: 1.5rem 1.2rem !important; }
.sidebar-logo {
  font-family: 'Outfit', sans-serif;
  font-weight: 800;
  font-size: 1.5rem;
  letter-spacing: -0.03em;
  color: var(--teal);
  margin-bottom: 0.2rem;
}
.sidebar-tagline {
  font-size: 0.72rem;
  font-weight: 500;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--faint);
  margin-bottom: 2rem;
}
.sidebar-section {
  font-size: 0.68rem;
  font-weight: 600;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--teal);
  margin: 1.5rem 0 0.6rem;
  padding-bottom: 0.4rem;
  border-bottom: 1px solid rgba(0,212,170,0.15);
}

/* ── Inputs ── */
.stSlider > div > div { background: rgba(0,212,170,0.08) !important; }
.stSlider [data-baseweb="slider"] div[role="slider"] { background: var(--teal) !important; border-color: var(--teal) !important; }
.stNumberInput input, .stTextInput input, .stSelectbox select {
  background: var(--bg2) !important;
  border: 1px solid var(--border2) !important;
  color: var(--text) !important;
  border-radius: 8px !important;
  font-family: 'Outfit', sans-serif !important;
}
label { color: var(--muted) !important; font-size: 0.78rem !important; font-weight: 500 !important; }

/* ── Header ── */
.page-header {
  position: relative;
  padding: 2.5rem 0 2rem;
  margin-bottom: 1.5rem;
  overflow: hidden;
}
.page-header::before {
  content: "";
  position: absolute;
  top: -80px; left: -100px;
  width: 500px; height: 300px;
  background: radial-gradient(ellipse, rgba(0,212,170,0.06) 0%, transparent 70%);
  pointer-events: none;
}
.eyebrow {
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--teal);
  margin-bottom: 0.5rem;
}
.page-title {
  font-family: 'Outfit', sans-serif;
  font-size: clamp(1.9rem, 3.5vw, 3rem);
  font-weight: 800;
  letter-spacing: -0.03em;
  line-height: 1.05;
  color: #FFFFFF;
  margin-bottom: 0.5rem;
}
.page-title .accent { color: var(--teal); }
.page-desc {
  font-size: 0.92rem;
  color: var(--muted);
  font-weight: 300;
  max-width: 540px;
  line-height: 1.65;
}

/* ── Score Ring ── */
.score-wrap {
  background: linear-gradient(145deg, var(--bg2), var(--bg1));
  border: 1px solid var(--border2);
  border-radius: 20px;
  padding: 2rem;
  text-align: center;
  position: relative;
  overflow: hidden;
}
.score-wrap::before {
  content: "";
  position: absolute;
  top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, transparent, var(--teal), transparent);
}
.score-grade {
  font-family: 'Outfit', sans-serif;
  font-size: 4.5rem;
  font-weight: 800;
  line-height: 1;
  margin: 0.5rem 0 0.2rem;
}
.score-label { font-size: 0.75rem; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted); }
.score-status { font-size: 0.85rem; font-weight: 500; margin-top: 0.4rem; }

/* ── KPI Cards ── */
.kpi-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 1.2rem 1.4rem;
  position: relative;
  overflow: hidden;
  transition: border-color 0.25s, transform 0.2s;
}
.kpi-card:hover { border-color: var(--border2); transform: translateY(-1px); }
.kpi-card::after {
  content: "";
  position: absolute;
  bottom: 0; left: 0; right: 0; height: 2px;
  border-radius: 0 0 14px 14px;
}
.kpi-card.teal::after  { background: linear-gradient(90deg, var(--teal), transparent); }
.kpi-card.red::after   { background: linear-gradient(90deg, var(--red), transparent); }
.kpi-card.amber::after { background: linear-gradient(90deg, var(--amber), transparent); }
.kpi-card.blue::after  { background: linear-gradient(90deg, var(--blue), transparent); }
.kpi-lbl { font-size: 0.68rem; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: var(--faint); margin-bottom: 0.4rem; }
.kpi-val { font-family: 'Outfit', sans-serif; font-size: 1.9rem; font-weight: 700; line-height: 1; color: #fff; margin-bottom: 0.25rem; }
.kpi-sub { font-size: 0.78rem; font-weight: 400; }
.kpi-sub.pos { color: #00D4AA; }
.kpi-sub.neg { color: var(--red); }
.kpi-sub.neu { color: var(--muted); }

/* ── Section headings ── */
.sec-head {
  font-family: 'Outfit', sans-serif;
  font-size: 1rem;
  font-weight: 700;
  color: #fff;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 1rem;
}
.sec-head::before {
  content: "";
  display: block;
  width: 3px; height: 16px;
  background: var(--teal);
  border-radius: 2px;
}

/* ── Anomaly chips ── */
.anomaly-list { display: flex; flex-direction: column; gap: 8px; }
.anomaly-item {
  display: flex; align-items: flex-start; gap: 10px;
  background: var(--bg3);
  border: 1px solid var(--border);
  border-left: 3px solid;
  border-radius: 10px;
  padding: 10px 14px;
  font-size: 0.82rem;
  line-height: 1.5;
}
.anomaly-item.high { border-left-color: var(--red); }
.anomaly-item.medium { border-left-color: var(--amber); }
.anomaly-item.low { border-left-color: var(--blue); }
.anomaly-dot { width: 7px; height: 7px; border-radius: 50%; margin-top: 5px; flex-shrink: 0; }
.anomaly-dot.high { background: var(--red); box-shadow: 0 0 6px var(--red); }
.anomaly-dot.medium { background: var(--amber); box-shadow: 0 0 6px var(--amber); }
.anomaly-dot.low { background: var(--blue); box-shadow: 0 0 6px var(--blue); }
.anomaly-text { color: var(--text); }
.anomaly-text strong { color: #fff; font-weight: 600; }

/* ── Compliance bars ── */
.comp-row {
  display: flex; align-items: center; gap: 12px;
  margin-bottom: 12px;
}
.comp-label { font-size: 0.78rem; font-weight: 500; color: var(--muted); min-width: 130px; }
.comp-bar-bg { flex: 1; height: 6px; background: rgba(255,255,255,0.06); border-radius: 6px; overflow: hidden; }
.comp-bar-fill { height: 100%; border-radius: 6px; transition: width 1s; }
.comp-score { font-size: 0.78rem; font-weight: 600; min-width: 36px; text-align: right; font-family: 'JetBrains Mono', monospace; }

/* ── Insight cards ── */
.insight-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.insight-card {
  background: var(--bg3);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 14px 16px;
}
.insight-icon { font-size: 1.2rem; margin-bottom: 6px; }
.insight-title { font-size: 0.82rem; font-weight: 600; color: #fff; margin-bottom: 4px; }
.insight-body { font-size: 0.75rem; color: var(--muted); line-height: 1.5; }

/* ── Footer ── */
.footer {
  margin-top: 3rem;
  padding-top: 1.2rem;
  border-top: 1px solid var(--border);
  font-size: 0.7rem;
  color: var(--faint);
  text-align: center;
  letter-spacing: 0.05em;
}

/* ── Misc ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton, div[data-testid="stToolbar"] { display: none; }
div[data-testid="stMetric"] { background: var(--bg2); border-radius: 12px; padding: 1rem; border: 1px solid var(--border); }
</style>
""", unsafe_allow_html=True)

# ─── CHART THEME ─────────────────────────────────────────────────────────────
BG    = "#0C1018"
GRID  = "rgba(255,255,255,0.04)"
TEAL  = "#00D4AA"
RED   = "#FF4757"
AMBER = "#FFB830"
BLUE  = "#4A9FFF"
MUTED = "rgba(232,236,244,0.4)"
FONT  = "Outfit, -apple-system, system-ui, sans-serif"

def chart_layout(h=320, title=""):
    return dict(
        height=h,
        paper_bgcolor=BG, plot_bgcolor=BG,
        font=dict(family=FONT, color=MUTED, size=12),
        margin=dict(l=10, r=10, t=40 if title else 20, b=10),
        title=dict(text=title, font=dict(family=FONT, size=13, color="#fff"), x=0.01, xanchor="left") if title else {},
        xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(size=11), tickcolor="rgba(0,0,0,0)"),
        yaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False, tickfont=dict(size=11)),
        hovermode="x unified",
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
    )

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">⬡ FinScan</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-tagline">SME Health Intelligence</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Company Profile</div>', unsafe_allow_html=True)
    company_name = st.text_input("Company Name", value="Acme Retail Pvt Ltd")
    industry = st.selectbox("Industry", ["E-commerce", "SaaS / Tech", "Retail", "Logistics", "Healthcare", "Manufacturing", "Consulting"])
    employees = st.slider("Employees", 5, 500, 48)
    founded_years = st.slider("Years in Operation", 1, 20, 3)

    st.markdown('<div class="sidebar-section">Revenue & Costs</div>', unsafe_allow_html=True)
    monthly_revenue = st.number_input("Monthly Revenue (₹ L)", min_value=1.0, max_value=5000.0, value=42.0, step=1.0)
    monthly_expenses = st.number_input("Monthly Expenses (₹ L)", min_value=1.0, max_value=5000.0, value=31.0, step=1.0)
    outstanding_debt = st.number_input("Outstanding Debt (₹ L)", min_value=0.0, max_value=10000.0, value=85.0, step=5.0)
    cash_reserves = st.number_input("Cash Reserves (₹ L)", min_value=0.0, max_value=5000.0, value=28.0, step=1.0)

    st.markdown('<div class="sidebar-section">Transaction Behaviour</div>', unsafe_allow_html=True)
    avg_txn_count = st.slider("Avg Monthly Transactions", 10, 2000, 340)
    large_txn_pct = st.slider("Large Txns (>₹5L) %", 0, 40, 8)
    cross_border_pct = st.slider("Cross-border Txns %", 0, 60, 12)
    late_payments = st.slider("Late Payment Incidents (6mo)", 0, 30, 4)

    st.markdown('<div class="sidebar-section">Compliance Posture</div>', unsafe_allow_html=True)
    gst_filed = st.selectbox("GST Filing Status", ["Regular & On-time", "Occasional Delays", "Frequent Delays", "Non-compliant"])
    kyc_complete = st.checkbox("KYC / KYB Complete", value=True)
    audit_done = st.checkbox("Annual Audit Done", value=True)
    aml_training = st.checkbox("AML Training Done", value=False)

    st.markdown("---")
    run = st.button("⬡  Run Financial Scan", use_container_width=True)

# ─── SCORING ENGINE ──────────────────────────────────────────────────────────
def compute_score(rev, exp, debt, cash, txn, large_pct, cross_pct, late,
                  gst, kyc, audit, aml, years, employees):
    scores = {}

    # 1. Profitability (25 pts)
    margin = (rev - exp) / rev if rev > 0 else 0
    if margin > 0.30: scores["profitability"] = 25
    elif margin > 0.20: scores["profitability"] = 22
    elif margin > 0.10: scores["profitability"] = 17
    elif margin > 0.05: scores["profitability"] = 12
    elif margin > 0: scores["profitability"] = 7
    else: scores["profitability"] = 0

    # 2. Liquidity (20 pts)
    monthly_burn = max(exp - rev, 0)
    runway = (cash / monthly_burn) if monthly_burn > 0 else 24
    runway = min(runway, 24)
    liq_score = min(20, (runway / 24) * 20)
    debt_ratio = debt / (rev * 12) if rev > 0 else 5
    if debt_ratio > 3: liq_score *= 0.5
    elif debt_ratio > 2: liq_score *= 0.7
    elif debt_ratio > 1: liq_score *= 0.85
    scores["liquidity"] = round(liq_score, 1)

    # 3. Compliance (25 pts)
    comp = 25
    if gst == "Occasional Delays": comp -= 5
    elif gst == "Frequent Delays": comp -= 12
    elif gst == "Non-compliant": comp -= 20
    if not kyc: comp -= 5
    if not audit: comp -= 4
    if not aml: comp -= 2
    scores["compliance"] = max(0, comp)

    # 4. Transaction Health (15 pts)
    txn_score = 15
    if large_pct > 20: txn_score -= 5
    elif large_pct > 12: txn_score -= 2
    if cross_pct > 35: txn_score -= 4
    elif cross_pct > 20: txn_score -= 2
    if late > 10: txn_score -= 5
    elif late > 5: txn_score -= 3
    elif late > 2: txn_score -= 1
    scores["txn_health"] = max(0, txn_score)

    # 5. Operational Maturity (15 pts)
    ops = 0
    ops += min(6, years * 1.5)
    ops += min(5, (employees / 100) * 5)
    if audit: ops += 2
    if kyc: ops += 2
    scores["ops_maturity"] = round(min(15, ops), 1)

    total = sum(scores.values())
    return round(total), scores

def get_grade(score):
    if score >= 85: return "A+", "#00D4AA", "Excellent — Low Risk"
    if score >= 75: return "A",  "#00D4AA", "Strong — Minimal Risk"
    if score >= 65: return "B+", "#4A9FFF", "Good — Manageable Risk"
    if score >= 55: return "B",  "#4A9FFF", "Moderate — Watch Key Areas"
    if score >= 45: return "C",  "#FFB830", "Below Average — Action Needed"
    if score >= 35: return "D",  "#FF4757", "Weak — High Risk Exposure"
    return "F", "#FF4757", "Critical — Immediate Attention Required"

def generate_anomalies(large_pct, cross_pct, late, gst, cash, exp, rev, debt):
    flags = []
    margin = (rev - exp) / rev if rev > 0 else 0
    monthly_burn = max(exp - rev, 0)
    runway = (cash / monthly_burn) if monthly_burn > 0 else 99

    if large_pct > 15:
        flags.append(("high", f"<strong>Unusual large-value transaction concentration</strong> — {large_pct}% of transactions exceed ₹5L threshold. Recommend enhanced due diligence and transaction purpose documentation."))
    if cross_pct > 25:
        flags.append(("high", f"<strong>Elevated cross-border payment exposure</strong> — {cross_pct}% of volume involves international transfers. FEMA compliance verification advised."))
    if late > 8:
        flags.append(("high", f"<strong>Chronic late payment pattern detected</strong> — {late} incidents in 6 months signals cash flow stress or poor receivables management."))
    if gst in ["Frequent Delays", "Non-compliant"]:
        flags.append(("high", "<strong>GST compliance breach</strong> — Irregular filing history creates regulatory liability and blocks access to input tax credits."))
    if runway < 3 and monthly_burn > 0:
        flags.append(("high", f"<strong>Critical runway risk</strong> — Cash reserves support only {runway:.1f} months of operations at current burn rate."))
    if margin < 0.05 and margin >= 0:
        flags.append(("medium", f"<strong>Thin profit margins</strong> — {margin*100:.1f}% net margin leaves no buffer for market shocks or cost spikes."))
    if debt / (rev * 12) > 1.5 if rev > 0 else False:
        flags.append(("medium", "<strong>High debt-to-revenue ratio</strong> — Outstanding debt exceeds 1.5x annual revenue. Debt servicing risk elevated."))
    if large_pct > 8 and cross_pct > 15:
        flags.append(("medium", "<strong>Potential structuring risk pattern</strong> — Combination of high cross-border volume and large transactions warrants AML review."))
    if not flags:
        flags.append(("low", "<strong>No critical anomalies detected</strong> — Transaction patterns and compliance indicators within acceptable thresholds."))
    if gst == "Occasional Delays":
        flags.append(("low", "<strong>Intermittent GST filing delays</strong> — Minor delays noted. Recommend automated filing reminders to maintain clean record."))
    return flags[:6]

def get_forecast(rev, exp, months=12):
    dates = pd.date_range(start=datetime.today(), periods=months, freq='ME')
    growth = np.random.normal(0.025, 0.012, months).cumsum()
    rev_fc = [rev * (1 + g) for g in growth]
    exp_fc = [exp * (1 + g * 0.7 + np.random.normal(0, 0.008)) for g in growth]
    profit_fc = [r - e for r, e in zip(rev_fc, exp_fc)]
    return dates, rev_fc, exp_fc, profit_fc

def generate_txn_data(avg_count, months=12):
    dates = pd.date_range(end=datetime.today(), periods=months, freq='ME')
    counts = [max(10, int(avg_count * np.random.normal(1, 0.15))) for _ in range(months)]
    flagged = [max(0, int(c * np.random.uniform(0.01, 0.05))) for c in counts]
    return dates, counts, flagged

# ─── MAIN ────────────────────────────────────────────────────────────────────
# Compute on every render (live updates)
score, sub_scores = compute_score(
    monthly_revenue, monthly_expenses, outstanding_debt, cash_reserves,
    avg_txn_count, large_txn_pct, cross_border_pct, late_payments,
    gst_filed, kyc_complete, audit_done, aml_training,
    founded_years, employees
)
grade, grade_color, status_text = get_grade(score)
margin_pct = ((monthly_revenue - monthly_expenses) / monthly_revenue * 100) if monthly_revenue > 0 else 0
monthly_burn = max(monthly_expenses - monthly_revenue, 0)
runway_months = round(cash_reserves / monthly_burn, 1) if monthly_burn > 0 else "∞"
debt_ratio = round(outstanding_debt / (monthly_revenue * 12), 2) if monthly_revenue > 0 else "N/A"

# ─── HEADER ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="page-header">
  <div class="eyebrow">⬡ FinScan · SME Financial Intelligence Platform</div>
  <div class="page-title">Financial Health<br><span class="accent">Scanner</span></div>
  <div class="page-desc">
    Real-time risk scoring, anomaly detection, and compliance monitoring for <strong style="color:#fff">{company_name}</strong>.
    Powered by multi-dimensional financial analysis.
  </div>
</div>
""", unsafe_allow_html=True)

# ─── TOP ROW: Score + KPIs ───────────────────────────────────────────────────
col_score, col_kpis = st.columns([1, 3], gap="large")

with col_score:
    st.markdown(f"""
    <div class="score-wrap">
      <div class="score-label">Health Score</div>
      <div class="score-grade" style="color:{grade_color}">{score}<span style="font-size:1.5rem;opacity:0.5">/100</span></div>
      <div class="score-label" style="font-size:1.5rem;font-weight:700;color:{grade_color};margin-bottom:0.3rem">{grade}</div>
      <div class="score-status" style="color:{grade_color}">{status_text}</div>
    </div>
    """, unsafe_allow_html=True)

with col_kpis:
    k1, k2, k3, k4 = st.columns(4, gap="small")
    with k1:
        col = "pos" if margin_pct > 0 else "neg"
        st.markdown(f"""<div class="kpi-card teal">
          <div class="kpi-lbl">Net Margin</div>
          <div class="kpi-val">{margin_pct:.1f}%</div>
          <div class="kpi-sub {col}">{'▲ Profitable' if margin_pct > 0 else '▼ Loss-making'}</div>
        </div>""", unsafe_allow_html=True)
    with k2:
        rw = f"{runway_months} mo" if runway_months != "∞" else "∞"
        rw_class = "neg" if isinstance(runway_months, float) and runway_months < 6 else "pos"
        st.markdown(f"""<div class="kpi-card {'red' if isinstance(runway_months, float) and runway_months < 6 else 'teal'}">
          <div class="kpi-lbl">Cash Runway</div>
          <div class="kpi-val">{rw}</div>
          <div class="kpi-sub {rw_class}">₹{cash_reserves:.0f}L reserves</div>
        </div>""", unsafe_allow_html=True)
    with k3:
        dr_val = f"{debt_ratio}x" if debt_ratio != "N/A" else "N/A"
        dr_class = "neg" if isinstance(debt_ratio, float) and debt_ratio > 1.5 else "neu"
        st.markdown(f"""<div class="kpi-card {'red' if isinstance(debt_ratio, float) and debt_ratio > 1.5 else 'amber'}">
          <div class="kpi-lbl">Debt / Revenue</div>
          <div class="kpi-val">{dr_val}</div>
          <div class="kpi-sub {dr_class}">{'High leverage' if isinstance(debt_ratio, float) and debt_ratio > 1.5 else 'Manageable'}</div>
        </div>""", unsafe_allow_html=True)
    with k4:
        comp_pct = round((sub_scores["compliance"] / 25) * 100)
        comp_class = "pos" if comp_pct >= 80 else ("neu" if comp_pct >= 60 else "neg")
        st.markdown(f"""<div class="kpi-card {'teal' if comp_pct >= 80 else ('amber' if comp_pct >= 60 else 'red')}">
          <div class="kpi-lbl">Compliance Score</div>
          <div class="kpi-val">{comp_pct}%</div>
          <div class="kpi-sub {comp_class}">{'Compliant' if comp_pct >= 80 else ('Partial' if comp_pct >= 60 else 'At Risk')}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── ROW 2: Score Breakdown + Forecast ───────────────────────────────────────
col_a, col_b = st.columns([1, 2], gap="large")

with col_a:
    st.markdown('<div class="sec-head">Score Breakdown</div>', unsafe_allow_html=True)
    cats = {
        "Profitability": (sub_scores["profitability"], 25, TEAL),
        "Compliance":    (sub_scores["compliance"],    25, BLUE),
        "Liquidity":     (sub_scores["liquidity"],     20, AMBER),
        "Txn Health":    (sub_scores["txn_health"],    15, TEAL),
        "Ops Maturity":  (sub_scores["ops_maturity"],  15, BLUE),
    }
    for cat, (val, maxv, color) in cats.items():
        pct = round((val / maxv) * 100)
        fill_color = TEAL if pct >= 70 else (AMBER if pct >= 45 else RED)
        st.markdown(f"""
        <div class="comp-row">
          <div class="comp-label">{cat}</div>
          <div class="comp-bar-bg">
            <div class="comp-bar-fill" style="width:{pct}%;background:{fill_color}"></div>
          </div>
          <div class="comp-score" style="color:{fill_color}">{val:.0f}/{maxv}</div>
        </div>
        """, unsafe_allow_html=True)

    # Radar chart
    cats_r = ["Profit", "Compliance", "Liquidity", "Txn Health", "Ops"]
    vals_r = [
        sub_scores["profitability"] / 25 * 100,
        sub_scores["compliance"] / 25 * 100,
        sub_scores["liquidity"] / 20 * 100,
        sub_scores["txn_health"] / 15 * 100,
        sub_scores["ops_maturity"] / 15 * 100,
    ]
    vals_r_closed = vals_r + [vals_r[0]]
    cats_r_closed = cats_r + [cats_r[0]]

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=vals_r_closed, theta=cats_r_closed,
        fill='toself',
        fillcolor='rgba(0,212,170,0.08)',
        line=dict(color=TEAL, width=2),
        hovertemplate="%{theta}: <b>%{r:.0f}%</b><extra></extra>",
    ))
    fig_radar.update_layout(
        height=260,
        paper_bgcolor=BG, plot_bgcolor=BG,
        font=dict(family=FONT, color=MUTED, size=11),
        margin=dict(l=20, r=20, t=20, b=20),
        polar=dict(
            bgcolor=BG,
            radialaxis=dict(visible=True, range=[0,100], gridcolor=GRID, tickfont=dict(size=9), tickcolor="rgba(0,0,0,0)"),
            angularaxis=dict(gridcolor=GRID, tickfont=dict(size=11, color="#fff")),
        ),
    )
    st.plotly_chart(fig_radar, use_container_width=True)

with col_b:
    st.markdown('<div class="sec-head">12-Month Financial Forecast</div>', unsafe_allow_html=True)
    dates_fc, rev_fc, exp_fc, profit_fc = get_forecast(monthly_revenue, monthly_expenses)

    fig_fc = go.Figure()
    fig_fc.add_trace(go.Scatter(
        x=dates_fc, y=rev_fc, name="Revenue",
        line=dict(color=TEAL, width=2.5),
        fill='tozeroy', fillcolor='rgba(0,212,170,0.05)',
        hovertemplate="Revenue: ₹<b>%{y:.1f}L</b><extra></extra>",
    ))
    fig_fc.add_trace(go.Scatter(
        x=dates_fc, y=exp_fc, name="Expenses",
        line=dict(color=RED, width=2, dash='dot'),
        hovertemplate="Expenses: ₹<b>%{y:.1f}L</b><extra></extra>",
    ))
    fig_fc.add_trace(go.Bar(
        x=dates_fc, y=profit_fc, name="Net Profit",
        marker=dict(color=[TEAL if p > 0 else RED for p in profit_fc], opacity=0.6),
        hovertemplate="Profit: ₹<b>%{y:.1f}L</b><extra></extra>",
        yaxis="y2",
    ))
    layout_fc = chart_layout(h=340)
    layout_fc["yaxis"]["title"] = dict(text="₹ Lakhs", font=dict(color=MUTED, size=11))
    layout_fc["yaxis2"] = dict(
        overlaying="y", side="right",
        showgrid=False, zeroline=True, zerolinecolor=GRID,
        tickfont=dict(size=10), title=dict(text="Net Profit", font=dict(color=MUTED, size=11)),
    )
    fig_fc.update_layout(**layout_fc)
    st.plotly_chart(fig_fc, use_container_width=True)

# ─── ROW 3: Anomaly Flags + Transaction Volume ────────────────────────────────
col_c, col_d = st.columns([1, 1], gap="large")

with col_c:
    st.markdown('<div class="sec-head">Anomaly & Risk Flags</div>', unsafe_allow_html=True)
    anomalies = generate_anomalies(
        large_txn_pct, cross_border_pct, late_payments,
        gst_filed, cash_reserves, monthly_expenses, monthly_revenue, outstanding_debt
    )
    st.markdown('<div class="anomaly-list">', unsafe_allow_html=True)
    for severity, text in anomalies:
        st.markdown(f"""
        <div class="anomaly-item {severity}">
          <div class="anomaly-dot {severity}"></div>
          <div class="anomaly-text">{text}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_d:
    st.markdown('<div class="sec-head">Transaction Volume — 12 Month History</div>', unsafe_allow_html=True)
    dates_t, counts_t, flagged_t = generate_txn_data(avg_txn_count)

    fig_txn = go.Figure()
    fig_txn.add_trace(go.Bar(
        x=dates_t, y=counts_t, name="Total Txns",
        marker=dict(color=BLUE, opacity=0.5, line=dict(width=0)),
        hovertemplate="<b>%{x|%b %Y}</b><br>Total: <b>%{y}</b><extra></extra>",
    ))
    fig_txn.add_trace(go.Scatter(
        x=dates_t, y=flagged_t, name="Flagged",
        mode="lines+markers",
        line=dict(color=RED, width=2),
        marker=dict(size=6, color=RED),
        hovertemplate="Flagged: <b>%{y}</b><extra></extra>",
        yaxis="y2",
    ))
    layout_txn = chart_layout(h=300)
    layout_txn["yaxis2"] = dict(
        overlaying="y", side="right",
        showgrid=False, zeroline=False,
        tickfont=dict(size=10, color=RED),
        title=dict(text="Flagged", font=dict(color=RED, size=10)),
    )
    fig_txn.update_layout(**layout_txn)
    st.plotly_chart(fig_txn, use_container_width=True)

# ─── ROW 4: Compliance Details + Insights ────────────────────────────────────
col_e, col_f = st.columns([1, 1], gap="large")

with col_e:
    st.markdown('<div class="sec-head">Compliance Checklist</div>', unsafe_allow_html=True)
    checks = [
        ("GST Filing",         gst_filed in ["Regular & On-time"],            gst_filed),
        ("KYC / KYB",          kyc_complete,                                   "Verified" if kyc_complete else "Incomplete"),
        ("Annual Audit",       audit_done,                                     "Filed" if audit_done else "Not done"),
        ("AML Training",       aml_training,                                   "Completed" if aml_training else "Not completed"),
        ("FEMA Exposure",      cross_border_pct < 25,                          f"{cross_border_pct}% cross-border"),
        ("Late Payment Risk",  late_payments < 5,                              f"{late_payments} incidents in 6mo"),
    ]
    for label, ok, detail in checks:
        icon_color = TEAL if ok else RED
        icon = "✓" if ok else "✗"
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;padding:9px 12px;
                    background:var(--bg3);border-radius:10px;margin-bottom:7px;
                    border:1px solid var(--border)">
          <span style="color:{icon_color};font-size:0.85rem;font-weight:700;min-width:16px">{icon}</span>
          <span style="font-size:0.82rem;color:#fff;font-weight:500;flex:1">{label}</span>
          <span style="font-size:0.75rem;color:var(--muted)">{detail}</span>
        </div>
        """, unsafe_allow_html=True)

with col_f:
    st.markdown('<div class="sec-head">AI-Powered Insights</div>', unsafe_allow_html=True)
    insights = []
    if margin_pct > 15:
        insights.append(("💰", "Strong Profitability", f"Your {margin_pct:.1f}% margin outperforms the {industry} industry median of ~12%. Protect this by monitoring cost creep."))
    elif margin_pct > 0:
        insights.append(("⚠️", "Margin Pressure", f"At {margin_pct:.1f}% net margin, a 5% cost increase would push you into loss territory. Review largest expense categories."))
    else:
        insights.append(("🔴", "Burning Cash", f"Operating at a loss of ₹{abs(monthly_revenue - monthly_expenses):.0f}L/month. Prioritise path to profitability or extend runway."))

    if isinstance(runway_months, float) and runway_months < 6:
        insights.append(("🚨", "Runway Critical", f"Only {runway_months} months of cash left. Immediate fundraise or cost reduction required."))
    elif isinstance(runway_months, float) and runway_months < 12:
        insights.append(("📊", "Runway Watch", f"{runway_months} months runway. Begin fundraising conversations now — don't wait for sub-3 months."))
    else:
        insights.append(("✅", "Healthy Liquidity", "Cash reserves provide adequate operational buffer. Consider deploying excess cash into growth or debt reduction."))

    if large_txn_pct > 10 and cross_border_pct > 20:
        insights.append(("🔍", "AML Pattern Risk", "High-value + cross-border transaction mix triggers AML review criteria. Document all transaction purposes proactively."))
    else:
        insights.append(("🛡️", "Transaction Profile Clean", "No significant AML risk patterns detected. Maintain current documentation standards."))

    if sub_scores["compliance"] >= 22:
        insights.append(("📋", "Compliance Leader", "Strong compliance posture reduces regulatory risk and improves access to credit. Use this as a competitive advantage."))
    else:
        insights.append(("📋", "Compliance Gaps", "Address GST filing and AML training gaps. Non-compliance fines can exceed ₹10L+ and block banking access."))

    st.markdown('<div class="insight-grid">', unsafe_allow_html=True)
    for icon, title, body in insights[:4]:
        st.markdown(f"""
        <div class="insight-card">
          <div class="insight-icon">{icon}</div>
          <div class="insight-title">{title}</div>
          <div class="insight-body">{body}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─── ROW 5: Burn Rate Waterfall ───────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="sec-head">Cost Structure & Burn Analysis</div>', unsafe_allow_html=True)

col_g, col_h = st.columns([2, 1], gap="large")

with col_g:
    # Simulated cost breakdown
    random.seed(42)
    cost_cats = ["Payroll", "Tech / Infra", "Marketing", "Operations", "Compliance", "Finance / Admin", "Other"]
    weights = [0.38, 0.18, 0.15, 0.12, 0.06, 0.07, 0.04]
    costs = [monthly_expenses * w for w in weights]
    colors_bar = [TEAL, BLUE, AMBER, "#7C6AF7", TEAL, BLUE, MUTED]

    fig_cost = go.Figure(go.Bar(
        x=cost_cats, y=costs,
        marker=dict(color=colors_bar, line=dict(width=0)),
        hovertemplate="<b>%{x}</b><br>₹%{y:.1f}L/month<extra></extra>",
        text=[f"₹{c:.1f}L" for c in costs],
        textposition="outside",
        textfont=dict(size=11, color=MUTED),
    ))
    layout_cost = chart_layout(h=280)
    layout_cost["yaxis"]["title"] = dict(text="₹ Lakhs / Month", font=dict(size=11))
    fig_cost.update_layout(**layout_cost)
    st.plotly_chart(fig_cost, use_container_width=True)

with col_h:
    # Gauges for key ratios
    debt_to_rev = (outstanding_debt / (monthly_revenue * 12) * 100) if monthly_revenue > 0 else 0

    fig_gauge = go.Figure()
    fig_gauge.add_trace(go.Indicator(
        mode="gauge+number",
        value=min(debt_to_rev, 300),
        title=dict(text="Debt/Revenue %", font=dict(size=13, color=MUTED)),
        number=dict(suffix="%", font=dict(size=26, color="#fff")),
        gauge=dict(
            axis=dict(range=[0, 300], tickcolor=MUTED, tickfont=dict(size=10)),
            bar=dict(color=TEAL if debt_to_rev < 80 else (AMBER if debt_to_rev < 150 else RED)),
            bgcolor=BG,
            borderwidth=0,
            steps=[
                dict(range=[0, 80], color="rgba(0,212,170,0.08)"),
                dict(range=[80, 150], color="rgba(255,184,48,0.08)"),
                dict(range=[150, 300], color="rgba(255,71,87,0.08)"),
            ],
            threshold=dict(line=dict(color="#fff", width=2), thickness=0.75, value=debt_to_rev),
        ),
        domain=dict(x=[0, 1], y=[0.5, 1])
    ))
    fig_gauge.add_trace(go.Indicator(
        mode="gauge+number",
        value=min(margin_pct, 50),
        title=dict(text="Net Margin %", font=dict(size=13, color=MUTED)),
        number=dict(suffix="%", font=dict(size=26, color="#fff")),
        gauge=dict(
            axis=dict(range=[0, 50], tickcolor=MUTED, tickfont=dict(size=10)),
            bar=dict(color=TEAL if margin_pct > 15 else (AMBER if margin_pct > 5 else RED)),
            bgcolor=BG,
            borderwidth=0,
            steps=[
                dict(range=[0, 5], color="rgba(255,71,87,0.08)"),
                dict(range=[5, 15], color="rgba(255,184,48,0.08)"),
                dict(range=[15, 50], color="rgba(0,212,170,0.08)"),
            ],
        ),
        domain=dict(x=[0, 1], y=[0, 0.45])
    ))
    fig_gauge.update_layout(
        height=300,
        paper_bgcolor=BG, plot_bgcolor=BG,
        font=dict(family=FONT, color=MUTED),
        margin=dict(l=20, r=20, t=20, b=20),
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

# ─── FOOTER ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
  FinScan · SME Financial Health Intelligence &nbsp;·&nbsp;
  Scan generated for <strong>{company_name}</strong> &nbsp;·&nbsp;
  {datetime.today().strftime('%d %B %Y')} &nbsp;·&nbsp;
  Built with Streamlit + Plotly &nbsp;·&nbsp;
  Scores are indicative and for analytical purposes only
</div>
""", unsafe_allow_html=True)