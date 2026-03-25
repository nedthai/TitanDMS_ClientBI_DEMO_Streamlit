import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Dealer AI Assistant - User Guide",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], .stApp {
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stSidebar"],
[data-testid="stSidebarCollapseButton"],
header[data-testid="stHeader"],
[data-testid="stToolbar"],
#MainMenu { display: none !important; }

.stApp {
    background: #050816;
    min-height: 100vh;
    overflow-x: hidden;
}

[data-testid="stAppViewBlockContainer"] {
    padding: 0 !important;
    max-width: 100% !important;
}
[data-testid="stVerticalBlock"] { gap: 0 !important; }

/* ── Stars ── */
.stars-bg {
    position: fixed; top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none; z-index: 0; overflow: hidden;
}
.stars-bg::before, .stars-bg::after {
    content: ''; position: absolute; top: 0; left: 0;
    width: 200%; height: 200%;
    background-image:
        radial-gradient(1px 1px at 20% 30%, rgba(255,255,255,0.6) 0%, transparent 100%),
        radial-gradient(1px 1px at 50% 10%, rgba(255,255,255,0.4) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 75% 60%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(1px 1px at 40% 80%, rgba(255,255,255,0.3) 0%, transparent 100%),
        radial-gradient(1px 1px at 90% 20%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 10% 70%, rgba(255,255,255,0.4) 0%, transparent 100%),
        radial-gradient(1px 1px at 60% 45%, rgba(255,255,255,0.3) 0%, transparent 100%),
        radial-gradient(1px 1px at 30% 55%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(1px 1px at 85% 85%, rgba(255,255,255,0.4) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 5% 40%, rgba(255,255,255,0.3) 0%, transparent 100%);
    animation: twinkle 8s linear infinite;
}
.stars-bg::after {
    background-image:
        radial-gradient(1px 1px at 15% 65%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 45% 25%, rgba(255,255,255,0.3) 0%, transparent 100%),
        radial-gradient(1px 1px at 70% 75%, rgba(255,255,255,0.4) 0%, transparent 100%),
        radial-gradient(1px 1px at 95% 50%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 25% 90%, rgba(255,255,255,0.3) 0%, transparent 100%);
    animation: twinkle 12s linear infinite reverse;
}
@keyframes twinkle {
    0%   { transform: translateY(0); opacity: 0.8; }
    50%  { opacity: 1; }
    100% { transform: translateY(-50%); opacity: 0.8; }
}

/* ── Orbs ── */
.orb {
    position: fixed; border-radius: 50%; filter: blur(80px);
    pointer-events: none; z-index: 0;
    animation: floatOrb 10s ease-in-out infinite alternate;
}
.orb-1 { width:500px;height:500px;top:-100px;left:-100px;background:radial-gradient(circle,rgba(79,70,229,0.25) 0%,transparent 70%);animation-duration:13s; }
.orb-2 { width:600px;height:600px;bottom:-150px;right:-150px;background:radial-gradient(circle,rgba(236,72,153,0.2) 0%,transparent 70%);animation-duration:17s; }
.orb-3 { width:400px;height:400px;top:40%;left:50%;transform:translate(-50%,-50%);background:radial-gradient(circle,rgba(99,102,241,0.12) 0%,transparent 70%);animation-duration:20s; }
@keyframes floatOrb {
    0%   { transform: translate(0,0) scale(1); }
    100% { transform: translate(30px,40px) scale(1.07); }
}

/* ── Page wrapper ── */
.ug-page { position:relative;z-index:1;max-width:1100px;margin:0 auto;padding:0 2rem 6rem 2rem; }

/* ── Hero ── */
.hero { text-align:center;padding:5rem 0 4rem 0; }
.hero-badge {
    display:inline-flex;align-items:center;gap:8px;
    background:rgba(79,70,229,0.15);border:1px solid rgba(99,102,241,0.4);
    border-radius:100px;padding:6px 18px;font-size:0.78rem;font-weight:600;
    letter-spacing:1.5px;text-transform:uppercase;color:#a5b4fc;margin-bottom:1.5rem;
}
.hero-badge .dot { width:7px;height:7px;background:#6366f1;border-radius:50%;animation:pulse 2s ease-in-out infinite; }
@keyframes pulse { 0%,100%{opacity:1;transform:scale(1);} 50%{opacity:0.5;transform:scale(0.8);} }
.hero-title { font-size:4rem;font-weight:900;line-height:1.1;letter-spacing:-2px;color:#fff;margin-bottom:0.5rem; }
.hero-title span { background:linear-gradient(120deg,#818cf8 0%,#c084fc 50%,#f472b6 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text; }
.hero-subtitle { font-size:1.15rem;font-weight:400;color:rgba(255,255,255,0.5);max-width:600px;margin:1.2rem auto 0 auto;line-height:1.7; }

/* ── Section divider ── */
.section-divider { display:flex;align-items:center;gap:2rem;margin:6rem 0 4rem 0; }
.section-divider-line { flex:1;height:2px;background:linear-gradient(90deg,transparent,rgba(99,102,241,0.6),transparent); }
.section-label { font-size:1rem;font-weight:800;letter-spacing:6px;text-transform:uppercase;color:#a5b4fc;white-space:nowrap;text-shadow:0 0 20px rgba(165,180,252,0.4); }

/* ── Section Lead ── */
.section-lead { font-size:1.1rem;color:rgba(255,255,255,0.45);line-height:1.8;margin-bottom:3rem;text-align:center;max-width:850px;margin-left:auto;margin-right:auto; }
.section-lead strong { color:#a5b4fc;font-weight:600; }

/* ── Model Cards ── */
.model-card { background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:18px;padding:1.8rem 2rem;margin-bottom:1.4rem;transition:border-color 0.3s,box-shadow 0.3s; }
.model-card:hover { border-color:rgba(99,102,241,0.3);box-shadow:0 8px 30px rgba(79,70,229,0.08); }
.model-card-header { display:flex;align-items:center;gap:1rem;margin-bottom:1rem; }
.model-num { display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:10px;background:linear-gradient(135deg,#4f46e5,#7c3aed);color:#fff;font-size:0.85rem;font-weight:700;flex-shrink:0; }
.model-name { font-size:1.05rem;font-weight:700;color:#e0e7ff; }
.model-body { padding-left:3rem; }
.model-summary { font-size:0.88rem;color:rgba(255,255,255,0.55);margin-bottom:1.4rem;line-height:1.7; }

/* ── Schema sub-section ── */
.schema-label {
    font-size:0.68rem;font-weight:700;letter-spacing:2.5px;
    text-transform:uppercase;color:rgba(165,180,252,0.5);
    margin-bottom:0.6rem;
}
.schema-diagram {
    background:rgba(0,0,0,0.25);
    border:1px solid rgba(99,102,241,0.15);
    border-radius:14px;
    overflow:hidden;
    margin-bottom:1.4rem;
    padding: 0.6rem;
}

/* ── Tag groups ── */
.tag-group { margin-top:1rem; }
.tag-group-label {
    display:flex;align-items:center;gap:8px;
    font-size:0.7rem;font-weight:700;letter-spacing:2px;
    text-transform:uppercase;margin-bottom:0.5rem;
}
.tag-group-label.metrics { color:#6ee7b7; }
.tag-group-label.metrics::before { content:'';display:inline-block;width:8px;height:8px;border-radius:2px;background:#6ee7b7;flex-shrink:0; }
.tag-group-label.dimensions { color:#a5b4fc; }
.tag-group-label.dimensions::before { content:'';display:inline-block;width:8px;height:8px;border-radius:2px;background:#a5b4fc;flex-shrink:0; }
.tag-row { display:flex;flex-wrap:wrap;gap:8px; }
.tag { padding:4px 12px;border-radius:100px;font-size:0.78rem;font-weight:500;border:1px solid; }
.tag-metric    { background:rgba(52,211,153,0.12);border-color:rgba(52,211,153,0.3);color:#6ee7b7; }
.tag-dimension { background:rgba(99,102,241,0.15);border-color:rgba(99,102,241,0.3);color:#a5b4fc; }
.tag-blue   { background:rgba(99,102,241,0.15);border-color:rgba(99,102,241,0.3);color:#a5b4fc; }
.tag-purple { background:rgba(168,85,247,0.15);border-color:rgba(168,85,247,0.3);color:#d8b4fe; }
.tag-pink   { background:rgba(236,72,153,0.15);border-color:rgba(236,72,153,0.3);color:#f9a8d4; }
.tag-teal   { background:rgba(20,184,166,0.15);border-color:rgba(20,184,166,0.3);color:#99f6e4; }

/* ── Tip cards ── */
.tip-grid { display:grid;grid-template-columns:1fr 1fr;gap:1rem; }
.tip-card { background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:16px;padding:1.4rem 1.6rem;transition:border-color 0.3s,transform 0.3s; }
.tip-card:hover { border-color:rgba(168,85,247,0.35);transform:translateY(-2px); }
.tip-icon { font-size:1.4rem;margin-bottom:0.7rem; }
.tip-title { font-size:0.92rem;font-weight:700;color:#e0e7ff;margin-bottom:0.35rem; }
.tip-text { font-size:0.85rem;color:rgba(255,255,255,0.45);line-height:1.6; }
.tip-example { margin-top:0.6rem;padding:0.5rem 0.8rem;background:rgba(99,102,241,0.1);border-left:2px solid rgba(99,102,241,0.5);border-radius:0 8px 8px 0;font-size:0.8rem;color:#a5b4fc;font-style:italic; }

/* ── Chart grid ── */
.chart-grid { display:grid;grid-template-columns:1fr 1fr;gap:1rem; }
.chart-card { background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:16px;padding:1.4rem 1.6rem;display:flex;align-items:flex-start;gap:1rem;transition:border-color 0.3s,transform 0.3s; }
.chart-card:hover { border-color:rgba(236,72,153,0.35);transform:translateY(-2px); }
.chart-emoji { font-size:1.6rem;flex-shrink:0;margin-top:2px; }
.chart-name { font-size:0.92rem;font-weight:700;color:#fce7f3;margin-bottom:0.3rem; }
.chart-desc { font-size:0.82rem;color:rgba(255,255,255,0.4);line-height:1.5; }

/* ── Info banner ── */
.info-banner { display:flex;align-items:flex-start;gap:1rem;background:rgba(99,102,241,0.08);border:1px solid rgba(99,102,241,0.25);border-radius:16px;padding:1.4rem 1.8rem;margin-top:2.5rem; }
.info-banner-icon { font-size:1.4rem;flex-shrink:0;margin-top:2px; }
.info-banner-text { font-size:0.9rem;color:rgba(255,255,255,0.55);line-height:1.7; }
.info-banner-text strong { color:#a5b4fc; }

/* ── Footer ── */
.ug-footer { text-align:center;padding:3rem 0 1rem 0;font-size:0.8rem;color:rgba(255,255,255,0.18);letter-spacing:0.5px; }
</style>

<div class="stars-bg"></div>
<div class="orb orb-1"></div>
<div class="orb orb-2"></div>
<div class="orb orb-3"></div>
""", unsafe_allow_html=True)


# ── SVG schema diagrams ───────────────────────────────────────────────────────

_LINE = 'stroke="rgba(99,102,241,0.38)" stroke-width="1.5" stroke-dasharray="5 3"'
_DIM_RECT = 'fill="rgba(79,70,229,0.1)" stroke="rgba(99,102,241,0.28)" stroke-width="1.2"'
_FACT_RECT = 'fill="rgba(79,70,229,0.32)" stroke="#6366f1" stroke-width="2"'
_LBL = 'text-anchor="middle" font-family="Inter,sans-serif" font-size="10" font-weight="700" fill="#a5b4fc" letter-spacing="1.5"'
_TXT = 'text-anchor="middle" font-family="Inter,sans-serif" font-size="10" fill="rgba(255,255,255,0.55)"'
_TXT2 = 'text-anchor="middle" font-family="Inter,sans-serif" font-size="10" fill="rgba(255,255,255,0.40)"'
_FACT_TXT = 'text-anchor="middle" font-family="Inter,sans-serif" font-size="13" font-weight="800" fill="#fff"'
_FACT_SUB = 'text-anchor="middle" font-family="Inter,sans-serif" font-size="10" fill="rgba(255,255,255,0.48)"'

SVG_VEHICLE_SALES = f"""
<svg viewBox="0 0 760 312" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;display:block;">
  <!-- Connection lines -->
  <line x1="380" y1="70" x2="380" y2="120" {_LINE}/>
  <line x1="575" y1="125" x2="480" y2="148" {_LINE}/>
  <line x1="380" y1="244" x2="380" y2="186" {_LINE}/>
  <line x1="178" y1="148" x2="280" y2="152" {_LINE}/>

  <!-- TOP: Time dimension -->
  <rect x="255" y="8" width="250" height="62" rx="10" {_DIM_RECT}/>
  <text x="380" y="27" {_LBL}>TIME</text>
  <text x="380" y="44" {_TXT}>Sold Date · Sold Year · Sold Month · Sold Quarter</text>
  <text x="380" y="59" {_TXT2}>Months Ago · Years Ago</text>

  <!-- CENTER: Vehicle Sales Fact -->
  <rect x="280" y="120" width="200" height="66" rx="13" {_FACT_RECT}/>
  <text x="380" y="147" {_FACT_TXT}>Vehicle Sales</text>
  <text x="380" y="166" {_FACT_SUB}>Sales Transaction Fact</text>

  <!-- RIGHT: Product dimension -->
  <rect x="575" y="70" width="175" height="120" rx="10" {_DIM_RECT}/>
  <text x="662" y="90" {_LBL}>PRODUCT</text>
  <text x="662" y="108" {_TXT}>Make</text>
  <text x="662" y="123" {_TXT}>Model</text>
  <text x="662" y="138" {_TXT}>Vehicle Type</text>
  <text x="662" y="153" {_TXT2}>Vehicle Class</text>
  <text x="662" y="168" {_TXT2}>Sales Group · Acquisition</text>

  <!-- BOTTOM: Location dimension -->
  <rect x="255" y="244" width="250" height="58" rx="10" {_DIM_RECT}/>
  <text x="380" y="264" {_LBL}>LOCATION</text>
  <text x="380" y="281" {_TXT}>Company</text>
  <text x="380" y="296" {_TXT2}>Location</text>

  <!-- LEFT: Transaction dimension -->
  <rect x="10" y="70" width="168" height="120" rx="10" {_DIM_RECT}/>
  <text x="94" y="90" {_LBL}>TRANSACTION</text>
  <text x="94" y="108" {_TXT}>Deal #</text>
  <text x="94" y="123" {_TXT}>Stock #</text>
  <text x="94" y="138" {_TXT}>Invoice #</text>
  <text x="94" y="153" {_TXT2}>Acquisition Type</text>
</svg>"""

SVG_CURRENT_INVENTORY = f"""
<svg viewBox="0 0 760 298" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;display:block;">
  <!-- Connection lines -->
  <line x1="380" y1="78" x2="380" y2="118" {_LINE}/>
  <line x1="575" y1="120" x2="480" y2="142" {_LINE}/>
  <line x1="380" y1="238" x2="380" y2="182" {_LINE}/>
  <line x1="178" y1="128" x2="280" y2="140" {_LINE}/>

  <!-- TOP: Status & Aging dimension -->
  <rect x="215" y="8" width="330" height="70" rx="10" {_DIM_RECT}/>
  <text x="380" y="28" {_LBL}>STATUS &amp; AGING</text>
  <text x="380" y="45" {_TXT}>Stock Status (In Stock · Reserved)</text>
  <text x="380" y="60" {_TXT2}>Aging Bucket: &lt;30 · 30-59 · 60-89 · 90-119 · 120-179 · 180+</text>

  <!-- CENTER: Current Inventory Fact -->
  <rect x="280" y="118" width="200" height="64" rx="13" {_FACT_RECT}/>
  <text x="380" y="146" {_FACT_TXT}>Current Inventory</text>
  <text x="380" y="163" {_FACT_SUB}>Real-time Stock Snapshot</text>

  <!-- RIGHT: Product dimension -->
  <rect x="575" y="72" width="175" height="105" rx="10" {_DIM_RECT}/>
  <text x="662" y="92" {_LBL}>PRODUCT</text>
  <text x="662" y="110" {_TXT}>Make</text>
  <text x="662" y="125" {_TXT}>Model</text>
  <text x="662" y="140" {_TXT}>Vehicle Type</text>
  <text x="662" y="155" {_TXT2}>Vehicle Class</text>

  <!-- BOTTOM: Location dimension -->
  <rect x="255" y="238" width="250" height="52" rx="10" {_DIM_RECT}/>
  <text x="380" y="258" {_LBL}>LOCATION</text>
  <text x="380" y="275" {_TXT}>Company</text>
  <text x="380" y="284" {_TXT2}>Location</text>

  <!-- LEFT: Stock reference dimension -->
  <rect x="10" y="80" width="168" height="94" rx="10" {_DIM_RECT}/>
  <text x="94" y="100" {_LBL}>STOCK</text>
  <text x="94" y="118" {_TXT}>Stock #</text>
  <text x="94" y="133" {_TXT}>Stocked Date</text>
  <text x="94" y="156" {_TXT2}>Days on Lot</text>
</svg>"""

SVG_HISTORICAL_INVENTORY = f"""
<svg viewBox="0 0 760 338" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;display:block;">
  <!-- Connection lines -->
  <!-- Time (top) → Center -->
  <line x1="380" y1="82" x2="380" y2="132" {_LINE}/>
  <!-- Product (top-right) → Center -->
  <line x1="565" y1="90" x2="480" y2="148" {_LINE}/>
  <!-- Location (bottom-right) → Center -->
  <line x1="565" y1="228" x2="480" y2="184" {_LINE}/>
  <!-- Status (bottom) → Center -->
  <line x1="380" y1="264" x2="380" y2="196" {_LINE}/>
  <!-- Stock (left) → Center -->
  <line x1="178" y1="148" x2="280" y2="156" {_LINE}/>

  <!-- TOP: Time dimension -->
  <rect x="240" y="8" width="280" height="74" rx="10" {_DIM_RECT}/>
  <text x="380" y="28" {_LBL}>TIME</text>
  <text x="380" y="45" {_TXT}>History Date · Stock Year · Stock Month</text>
  <text x="380" y="60" {_TXT2}>Months Ago · Years Ago</text>

  <!-- TOP-RIGHT: Product dimension -->
  <rect x="565" y="8" width="185" height="105" rx="10" {_DIM_RECT}/>
  <text x="657" y="28" {_LBL}>PRODUCT</text>
  <text x="657" y="46" {_TXT}>Make</text>
  <text x="657" y="61" {_TXT}>Model</text>
  <text x="657" y="76" {_TXT}>Vehicle Type</text>
  <text x="657" y="91" {_TXT2}>Vehicle Class</text>

  <!-- CENTER: Historical Inventory Fact -->
  <rect x="280" y="132" width="200" height="64" rx="13" {_FACT_RECT}/>
  <text x="380" y="159" {_FACT_TXT}>Historical Inventory</text>
  <text x="380" y="177" {_FACT_SUB}>Daily Stock Snapshot Fact</text>

  <!-- BOTTOM-RIGHT: Location dimension -->
  <rect x="565" y="200" width="185" height="64" rx="10" {_DIM_RECT}/>
  <text x="657" y="220" {_LBL}>LOCATION</text>
  <text x="657" y="238" {_TXT}>Company</text>
  <text x="657" y="253" {_TXT2}>Location</text>

  <!-- BOTTOM: Status & Aging dimension -->
  <rect x="220" y="264" width="320" height="64" rx="10" {_DIM_RECT}/>
  <text x="380" y="284" {_LBL}>STATUS &amp; AGING</text>
  <text x="380" y="301" {_TXT}>Stock Status</text>
  <text x="380" y="316" {_TXT2}>Aging Bucket: &lt;30 · 30-59 · 60-89 · 90-119 · 120-179 · 180+</text>

  <!-- LEFT: Stock reference dimension -->
  <rect x="10" y="100" width="168" height="90" rx="10" {_DIM_RECT}/>
  <text x="94" y="120" {_LBL}>STOCK</text>
  <text x="94" y="138" {_TXT}>Stock #</text>
  <text x="94" y="153" {_TXT}>Stocked Date</text>
  <text x="94" y="175" {_TXT2}>Days Aged</text>
</svg>"""


# ── Page render ───────────────────────────────────────────────────────────────

def render_user_guide():

    # ── Hero
    st.markdown("""
    <div class="ug-page" style="padding-bottom: 32px;">
      <div class="hero">
        <div class="hero-badge"><span class="dot"></span>Documentation</div>
        <div class="hero-title">Dealer AI Assistant<br><span>User Guide</span></div>
        <div class="hero-subtitle">
          Everything you need to know to unlock the full potential of your AI-powered
          automotive intelligence platform.
        </div>
      </div>

      <!-- Section 01 divider -->
      <div class="section-divider">
        <div class="section-divider-line"></div>
        <div class="section-label">01 · DATA &amp; SEMANTIC MODEL</div>
        <div class="section-divider-line"></div>
      </div>

      <div class="section-lead">
        The assistant is powered by a high-performance <strong>DuckDB</strong>
        data warehouse organised into three Semantic Views, each representing
        a distinct perspective on your dealership data.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Model Card 1: Vehicle Sales
    st.markdown(f"""
    <div class="ug-page" style="padding-top:0;padding-bottom:0;">
      <div class="model-card">
        <div class="model-card-header">
          <div class="model-num">1</div>
          <div class="model-name">Vehicle Sales</div>
        </div>
        <div class="model-body">
          <div class="model-summary">
            Tracks every completed vehicle sale, capturing the full financial breakdown
            of each transaction alongside time, product, and location context.
          </div>
          <div class="schema-label">SCHEMA</div>
          <div class="schema-diagram">{SVG_VEHICLE_SALES}</div>
          <div class="tag-group">
            <div class="tag-group-label dimensions">Dimensions</div>
            <div class="tag-row">
              <span class="tag tag-dimension">Sold Date</span>
              <span class="tag tag-dimension">Sold Year</span>
              <span class="tag tag-dimension">Sold Month</span>
              <span class="tag tag-dimension">Sold Quarter</span>
              <span class="tag tag-dimension">Months Ago</span>
              <span class="tag tag-dimension">Make</span>
              <span class="tag tag-dimension">Model</span>
              <span class="tag tag-dimension">Vehicle Type</span>
              <span class="tag tag-dimension">Vehicle Class</span>
              <span class="tag tag-dimension">Sales Group</span>
              <span class="tag tag-dimension">Acquisition</span>
              <span class="tag tag-dimension">Company</span>
              <span class="tag tag-dimension">Location</span>
            </div>
          </div>
          <div class="tag-group">
            <div class="tag-group-label metrics">Metrics</div>
            <div class="tag-row">
              <span class="tag tag-metric">Total Profit</span>
              <span class="tag tag-metric">Vehicle Gross</span>
              <span class="tag tag-metric">Deal Profit</span>
              <span class="tag tag-metric">Trade-In Profit</span>
              <span class="tag tag-metric">Aftermarket Profit</span>
              <span class="tag tag-metric">Holdback</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Model Card 2: Current Inventory
    st.markdown(f"""
    <div class="ug-page" style="padding-top:0;padding-bottom:0;">
      <div class="model-card">
        <div class="model-card-header">
          <div class="model-num">2</div>
          <div class="model-name">Current Inventory</div>
        </div>
        <div class="model-body">
          <div class="model-summary">
            A real-time snapshot of every vehicle currently on the lot, including
            its condition, aging category, and capital value tied up in inventory.
          </div>
          <div class="schema-label">SCHEMA</div>
          <div class="schema-diagram">{SVG_CURRENT_INVENTORY}</div>
          <div class="tag-group">
            <div class="tag-group-label dimensions">Dimensions</div>
            <div class="tag-row">
              <span class="tag tag-dimension">Make</span>
              <span class="tag tag-dimension">Model</span>
              <span class="tag tag-dimension">Vehicle Type</span>
              <span class="tag tag-dimension">Vehicle Class</span>
              <span class="tag tag-dimension">Company</span>
              <span class="tag tag-dimension">Location</span>
              <span class="tag tag-dimension">Stock Status</span>
              <span class="tag tag-dimension">Aging Bucket</span>
              <span class="tag tag-dimension">Stocked Date</span>
            </div>
          </div>
          <div class="tag-group">
            <div class="tag-group-label metrics">Metrics</div>
            <div class="tag-row">
              <span class="tag tag-metric">Stock Value</span>
              <span class="tag tag-metric">Days on Lot</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Model Card 3: Historical Inventory
    st.markdown(f"""
    <div class="ug-page" style="padding-top:0;padding-bottom:0;">
      <div class="model-card">
        <div class="model-card-header">
          <div class="model-num">3</div>
          <div class="model-name">Historical Inventory</div>
        </div>
        <div class="model-body">
          <div class="model-summary">
            Daily historical snapshots of inventory enabling trend analysis and
            point-in-time comparisons — ideal for "what was our stock 3 months ago?" questions.
          </div>
          <div class="schema-label">SCHEMA</div>
          <div class="schema-diagram">{SVG_HISTORICAL_INVENTORY}</div>
          <div class="tag-group">
            <div class="tag-group-label dimensions">Dimensions</div>
            <div class="tag-row">
              <span class="tag tag-dimension">History Date</span>
              <span class="tag tag-dimension">Stock Year</span>
              <span class="tag tag-dimension">Stock Month</span>
              <span class="tag tag-dimension">Months Ago</span>
              <span class="tag tag-dimension">Make</span>
              <span class="tag tag-dimension">Model</span>
              <span class="tag tag-dimension">Vehicle Type</span>
              <span class="tag tag-dimension">Vehicle Class</span>
              <span class="tag tag-dimension">Company</span>
              <span class="tag tag-dimension">Location</span>
              <span class="tag tag-dimension">Stock Status</span>
              <span class="tag tag-dimension">Aging Bucket</span>
            </div>
          </div>
          <div class="tag-group">
            <div class="tag-group-label metrics">Metrics</div>
            <div class="tag-row">
              <span class="tag tag-metric">Stock Value</span>
              <span class="tag tag-metric">Days Aged</span>
              <span class="tag tag-metric">Units in Stock</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Sections 02 & 03 + Footer
    st.markdown("""
    <div class="ug-page" style="padding-top:0;">

      <!-- Section 02: AI Interaction -->
      <div class="section-divider">
        <div class="section-divider-line"></div>
        <div class="section-label">02 · AI INTERACTION</div>
        <div class="section-divider-line"></div>
      </div>

      <div class="section-lead">
        The assistant is conversational — no SQL or technical column names needed.
        Follow these tips to get the best results.
      </div>

      <div class="tip-grid">
        <div class="tip-card">
          <div class="tip-icon">🕐</div>
          <div class="tip-title">Be Specific about Time</div>
          <div class="tip-text">Anchor your question to a clear time window for accurate results.</div>
          <div class="tip-example">"Show me sales this month" · "Revenue in 2023"</div>
        </div>
        <div class="tip-card">
          <div class="tip-icon">⚖️</div>
          <div class="tip-title">Ask for Comparisons</div>
          <div class="tip-text">The AI excels at side-by-side analysis across any dimension.</div>
          <div class="tip-example">"Compare New vs Used sales profit this year"</div>
        </div>
        <div class="tip-card">
          <div class="tip-icon">🔍</div>
          <div class="tip-title">Filter by Attributes</div>
          <div class="tip-text">Narrow results by make, model, location or any other attribute.</div>
          <div class="tip-example">"Show all Toyotas in stock more than 90 days"</div>
        </div>
        <div class="tip-card">
          <div class="tip-icon">📈</div>
          <div class="tip-title">Request Visuals</div>
          <div class="tip-text">Ask for any chart type or let the AI pick the most insightful one.</div>
          <div class="tip-example">"…as a pie chart" · "show a bar graph"</div>
        </div>
      </div>

      <!-- Section 03: Chart Gallery -->
      <div class="section-divider">
        <div class="section-divider-line"></div>
        <div class="section-label">03 · CHART GALLERY</div>
        <div class="section-divider-line"></div>
      </div>

      <div class="section-lead">
        Automatically select the best visualisation, or take manual control by requesting a specific chart type.
      </div>

      <div class="chart-grid">
        <div class="chart-card">
          <div class="chart-emoji">📊</div>
          <div>
            <div class="chart-name">Bar / Column Charts</div>
            <div class="chart-desc">Best for comparing categories side-by-side, e.g. Sales by Make.</div>
          </div>
        </div>
        <div class="chart-card">
          <div class="chart-emoji">📉</div>
          <div>
            <div class="chart-name">Line / Trend Charts</div>
            <div class="chart-desc">Best for time series visualisation, e.g. Monthly Profit Trend.</div>
          </div>
        </div>
        <div class="chart-card">
          <div class="chart-emoji">🥧</div>
          <div>
            <div class="chart-name">Pie / Donut Charts</div>
            <div class="chart-desc">Best for showing parts of a whole, e.g. Stock by Location.</div>
          </div>
        </div>
        <div class="chart-card">
          <div class="chart-emoji">📦</div>
          <div>
            <div class="chart-name">Stacked Charts</div>
            <div class="chart-desc">Best for sub-categories, e.g. Sales by Make stacked by Class.</div>
          </div>
        </div>
        <div class="chart-card">
          <div class="chart-emoji">🔷</div>
          <div>
            <div class="chart-name">Area Charts</div>
            <div class="chart-desc">Similar to line charts but emphasises volume over time.</div>
          </div>
        </div>
        <div class="chart-card">
          <div class="chart-emoji">🔵</div>
          <div>
            <div class="chart-name">Scatter Plots</div>
            <div class="chart-desc">Good for correlations, e.g. Days Aged vs Stock Value.</div>
          </div>
        </div>
        <div class="chart-card">
          <div class="chart-emoji">🗺️</div>
          <div>
            <div class="chart-name">Treemaps</div>
            <div class="chart-desc">Great for hierarchical data with nested proportions.</div>
          </div>
        </div>
        <div class="chart-card">
          <div class="chart-emoji">🔻</div>
          <div>
            <div class="chart-name">Funnel Charts</div>
            <div class="chart-desc">Ideal for stages or specific sequential pipelines.</div>
          </div>
        </div>
      </div>

      <!-- Info Banner -->
      <div class="info-banner">
        <div class="info-banner-icon">💡</div>
        <div class="info-banner-text">
          <strong>Pro tip:</strong> The AI automatically selects the most insightful chart type based on
          your question and data shape. You can always override this by adding phrases like
          <strong>"as a pie chart"</strong> or <strong>"show a bar graph"</strong> to your prompt.
        </div>
      </div>

      <div class="ug-footer">Dealer AI Assistant &nbsp;·&nbsp; User Guide &nbsp;·&nbsp; TitanDMS</div>

    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    render_user_guide()
