import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv
from src.database import execute_query
from src.llm_engine import generate_sql, interpret_results
from src.visualization import render_chart, parse_chart_config

load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="Dealer AI Assistant - Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "temp_prompt" not in st.session_state:
    st.session_state.temp_prompt = None

# --- SESSION STATE INITIALIZATION FOR DUAL-PANE ---
if "current_df" not in st.session_state: st.session_state.current_df = None
if "current_chart_config" not in st.session_state: st.session_state.current_chart_config = None
if "current_sql" not in st.session_state: st.session_state.current_sql = None
if "current_text" not in st.session_state: st.session_state.current_text = None
if "current_question" not in st.session_state: st.session_state.current_question = None

# Custom CSS for Premium Experience (White Background)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;500;600;700&display=swap');
    
    html, body, .stMarkdown, .stText, p, h1, h2, h3 {
        font-family: 'Rubik', sans-serif !important;
    }

    .stApp {
        background-color: #ffffff;
    }

    /* Dual-Pane Column Styling */
    [data-testid="column"]:nth-of-type(1) {
        border-right: 1px solid #f1f5f9;
        padding-right: 2rem !important;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        min-height: 85vh;
        padding-bottom: 1rem !important;
    }
    
    /* Highlighted Canvas Border for Right Column */
    [data-testid="column"]:nth-of-type(2) {
        padding: 2.5rem !important;
        background-color: #ffffff;
        border: 2px solid #4f46e5; /* Highlighted indigo border */
        border-radius: 24px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
        min-height: 85vh;
        margin-left: 1rem !important;
    }

    /* Hide the default Streamlit sidebar navigation */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }


    /* Gradient Title */
    .gradient-title {
        background: linear-gradient(90deg, #4f46e5, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.2rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 20px;
    }
    
    .welcome-text {
        font-size: 1.2rem;
        font-weight: 500;
        color: #64748b;
        text-align: center;
        margin-top: -10px;
        margin-bottom: 20px;
    }

    /* Chat Message Bubbles */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
    }

    [data-testid="stChatMessageContent"] {
        border-radius: 12px !important;
        padding: 1rem !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
    }

    [data-testid="stChatMessage"]:nth-child(odd) [data-testid="stChatMessageContent"] {
        background-color: #f1f5f9 !important;
        color: #1e293b !important;
    }
    
    [data-testid="stChatMessage"]:nth-child(even) [data-testid="stChatMessageContent"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        color: #1e293b !important;
    }

    /* Sidebar Section Headers */
    .sidebar-header {
        font-size: 0.85rem;
        text-transform: uppercase;
        color: #94a3b8;
        font-weight: 700;
        letter-spacing: 1.2px;
        margin-bottom: 12px;
        margin-top: 20px;
    }

    /* ── Canvas KPI Card ─────────────────────────────── */
    .canvas-kpi-card {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        border-radius: 16px;
        padding: 1.4rem 2rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 1.5rem;
        box-shadow: 0 8px 24px rgba(79, 70, 229, 0.25);
    }
    .canvas-kpi-icon {
        font-size: 2.4rem;
        line-height: 1;
    }
    .canvas-kpi-label {
        color: rgba(255,255,255,0.75);
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.1px;
        margin-bottom: 2px;
    }
    .canvas-kpi-value {
        color: #ffffff;
        font-size: 2rem;
        font-weight: 700;
        line-height: 1.1;
    }
    .canvas-kpi-sub {
        color: rgba(255,255,255,0.6);
        font-size: 0.78rem;
        margin-top: 3px;
    }
    /* ── Canvas Section Header ───────────────────────── */
    .canvas-section-title {
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.1px;
        color: #94a3b8;
        margin-bottom: 8px;
        padding-bottom: 6px;
        border-bottom: 1px solid #e2e8f0;
    }
    </style>
    """, unsafe_allow_html=True)

# Column Display Mapping
COLUMN_DISPLAY_MAP = {
    "Stock_No": "Stock #", "Deal_No": "Deal #", "Invoice_No": "Invoice #",
    "Is_Current_Month": "Current Month?", "Is_Current_Year": "Current Year?",
    "Trade_In_Income": "Trade-In Profit", "Date_In_Stock": "History Date",
    "Stock_Value": "Value", "Days_In_Stock": "Days Aged"
}

def clean_column_names(df):
    new_columns = {col: get_friendly_name(col) for col in df.columns}
    return df.rename(columns=new_columns)

def get_friendly_name(col):
    if col in COLUMN_DISPLAY_MAP: return COLUMN_DISPLAY_MAP[col]
    return col.replace("_", " ").strip()

_CHART_KEYWORDS = ["stacked column", "stacked bar", "stacked area", "horizontal bar", "grouped bar", "grouped column", "column chart", "column graph", "bar chart", "bar graph", "line chart", "line graph", "pie chart", "donut chart", "doughnut chart", "area chart", "scatter chart", "scatter plot", "histogram", "box chart", "box plot", "violin chart", "violin plot", "treemap", "tree map", "funnel chart", "column", "bar", "line", "pie", "donut", "doughnut", "area", "scatter", "box", "violin", "funnel"]

def extract_chart_preference(question: str) -> str:
    q = question.lower()
    for kw in _CHART_KEYWORDS:
        if kw in q: return kw
    return "Not specified"

def get_cached_dictionary():
    with open("data/Database_Dictionary.md", "r") as f: return f.read()

# Sidebar
with st.sidebar:
    # 1. Centered Logo using Base64 for consistent alignment
    import base64
    with open("assets/logo.png", "rb") as f:
        sb_logo_base64 = base64.b64encode(f.read()).decode()
    
    st.markdown(f"""
        <div style='display: flex; justify-content: center; margin-top: 10px; margin-bottom: 5px;'>
            <img src='data:image/png;base64,{sb_logo_base64}' width='80'>
        </div>
        <div style='text-align: center; margin-bottom: 25px;'>
            <span style='background: linear-gradient(90deg, #4f46e5, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 700; font-size: 1.2rem; font-family: "Rubik", sans-serif;'>
                Dealer AI Assistant
            </span>
        </div>
    """, unsafe_allow_html=True)
    
    # 2. System Status Section
    st.markdown("<div class='sidebar-header'>SYSTEM STATUS</div>", unsafe_allow_html=True)
    db_exists = os.path.exists("data/Database_Data.duckdb")
    api_key_exists = os.getenv("GEMINI_API_KEY") is not None
    
    status_db = "Active" if db_exists else "Failed"
    status_api = "Google Gemini" if api_key_exists else "Failed"
    
    st.markdown(f"""
        <div style='margin-left: 5px; font-size: 0.9rem; color: #475569;'>
            <p style='margin-bottom: 5px;'>🟢 <span style='margin-left: 8px;'>Database Status: {status_db}</span></p>
            <p>🟢 <span style='margin-left: 8px;'>LLM Model: {status_api}</span></p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    
    # 3. Dealer Information Section
    st.markdown("<div class='sidebar-header'>DEALER INFORMATION</div>", unsafe_allow_html=True)
    # Placeholder for dealer info as in original
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)


# --- MAIN RENDER LOGIC ---
col_chat, col_canvas = st.columns([1, 2], gap="medium")

# Left Pane: Control (Chat)
with col_chat:
    if len(st.session_state.messages) == 0:
        # Perfectly Center Logo using Base64/HTML for alignment
        import base64
        with open("assets/logo.png", "rb") as f:
            logo_base64 = base64.b64encode(f.read()).decode()
        
        st.markdown(f"""
            <div style='display: flex; justify-content: center; margin-bottom: 10px;'>
                <img src='data:image/png;base64,{logo_base64}' width='100'>
            </div>
        """, unsafe_allow_html=True)
            
        st.markdown("<div class='welcome-text' style='margin-bottom: -15px;'>Hi there,</div>", unsafe_allow_html=True)
        st.markdown("<div class='gradient-title'>Let's get insights into your data!</div>", unsafe_allow_html=True)
    else:
        chat_container = st.container(height=650, border=False)
        with chat_container:
            for i, message in enumerate(st.session_state.messages):
                with st.chat_message(message["role"]):
                    if "sql" in message and message["sql"]:
                        with st.expander("🔍 SQL Query", expanded=False):
                            st.code(message["sql"], language="sql")
                    if message.get("content"):
                        st.markdown(message["content"])

    user_input = st.chat_input("How can I help you today?")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Process AI Response
        with st.chat_message("assistant"):
            with st.status("Analyzing Data...", expanded=True) as status:
                try:
                    data_dict = get_cached_dictionary()
                    sql = generate_sql(user_input, data_dict)
                    df = execute_query(sql)
                    
                    if df.empty:
                        response_text = "I couldn't find any data for that request."
                        st.markdown(response_text)
                        st.session_state.messages.append({"role": "assistant", "content": response_text})
                    else:
                        df_display = clean_column_names(df.copy())
                        chart_pref = extract_chart_preference(user_input)
                        response_text = interpret_results(user_input, df_display.head(20).to_string(), user_chart_preference=chart_pref)
                        chart_config = parse_chart_config(response_text)
                        clean_response = response_text.split("---")[0].strip()

                        st.markdown(clean_response)
                        
                        st.session_state.current_df = df_display
                        st.session_state.current_chart_config = chart_config
                        st.session_state.current_question = user_input
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": clean_response,
                            "sql": sql,
                        })
                    status.update(label="Complete!", state="complete", expanded=False)
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
                    status.update(label="Error Occurred", state="error")

# Right Pane: Canvas
with col_canvas:
    @st.fragment
    def render_canvas_fragment():
        if st.session_state.current_df is not None:
            df = st.session_state.current_df
            chart_config = st.session_state.current_chart_config
            question = st.session_state.get("current_question", "")

            # ── 1. KPI SUMMARY CARD ─────────────────────────────────────────────
            # Determine numeric metric column (prefer Y_AXIS from chart_config)
            metric_col = None
            metric_label = "Total Records"
            metric_value = len(df)
            metric_fmt = f"{metric_value:,}"
            metric_icon = "📊"

            if chart_config:
                y_col = chart_config.get("Y_AXIS", "")
                if y_col and y_col in df.columns and pd.api.types.is_numeric_dtype(df[y_col]):
                    metric_col = y_col

            if metric_col is None:
                # Fallback: pick first numeric column
                num_cols = df.select_dtypes(include="number").columns.tolist()
                if num_cols:
                    metric_col = num_cols[0]

            if metric_col:
                total = df[metric_col].sum()
                metric_label = metric_col
                # Smart formatting: large numbers with K / M suffix
                if total >= 1_000_000:
                    metric_fmt = f"{total / 1_000_000:,.2f}M"
                elif total >= 1_000:
                    metric_fmt = f"{total / 1_000:,.1f}K"
                else:
                    metric_fmt = f"{total:,.0f}"
                metric_icon = "💰" if any(k in metric_col.lower() for k in ["profit", "income", "revenue", "value", "price", "cost", "amount"]) else "🔢"

            row_count = len(df)
            sub_text = f"{row_count:,} record{'s' if row_count != 1 else ''} returned"

            st.markdown(f"""
                <div class="canvas-kpi-card">
                    <div class="canvas-kpi-icon">{metric_icon}</div>
                    <div>
                        <div class="canvas-kpi-label">{metric_label}</div>
                        <div class="canvas-kpi-value">{metric_fmt}</div>
                        <div class="canvas-kpi-sub">{sub_text}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # ── 2. TABLE (left) + CHART (right) ─────────────────────────────────
            col_table, col_chart = st.columns([1, 1], gap="medium")

            with col_table:
                st.markdown("<div class='canvas-section-title'>📋 Detail Data</div>", unsafe_allow_html=True)
                st.dataframe(df, width="stretch", height=380)

            with col_chart:
                if chart_config:
                    st.markdown("<div class='canvas-section-title'>📈 Chart Visualization</div>", unsafe_allow_html=True)
                    render_chart(df, chart_config)
                else:
                    st.markdown("<div class='canvas-section-title'>📈 Chart Visualization</div>", unsafe_allow_html=True)
                    st.info("No chart configuration was generated for this query.")

        else:
            # ── 1. SAMPLE DATA FOR WELCOME STATE ──────────────────────────
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            sample_df = pd.DataFrame({
                "Month": months,
                "Brand": ["Toyota"] * 12,
                "Units Sold": [42, 55, 48, 70, 66, 80, 75, 90, 85, 110, 102, 120],
                "Revenue": [126000, 165000, 144000, 210000, 198000, 240000, 225000, 270000, 255000, 330000, 306000, 360000]
            })
            
            sample_chart_config = {
                "CHART_TYPE": "line",
                "X_AXIS": "Month",
                "Y_AXIS": "Units Sold",
                "COLOR": "Brand"
            }

            # ── 2. KPI SUMMARY CARD (Sample) ──────────────────────────────────
            total_revenue = sample_df["Revenue"].sum()
            metric_fmt = f"${total_revenue / 1_000_000:,.1f}M"
            sub_text = "Total illustrative revenue for the current year"

            st.markdown(f"""
                <div style='text-align:center; margin-bottom: 1.5rem;'>
                    <h2 style='color:#1e293b; font-size:1.6rem; font-weight:700; margin-bottom:4px;'>
                        📊 Your Analytics Workspace
                    </h2>
                    <p style='color:#94a3b8; font-size:0.9rem;'>
                        Ask a question on the left — live charts &amp; tables will appear here instantly.
                    </p>
                </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
                <div class="canvas-kpi-card">
                    <div class="canvas-kpi-icon">💰</div>
                    <div>
                        <div class="canvas-kpi-label">TOTAL REvenue (Sample)</div>
                        <div class="canvas-kpi-value">{metric_fmt}</div>
                        <div class="canvas-kpi-sub">{sub_text}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # ── 3. TABLE (left) + CHART (right) ─────────────────────────────────
            col_table, col_chart = st.columns([1, 1], gap="medium")

            with col_table:
                st.markdown("<div class='canvas-section-title'>📋 Detail Data</div>", unsafe_allow_html=True)
                st.dataframe(sample_df, width="stretch", height=380)

            with col_chart:
                st.markdown("<div class='canvas-section-title'>📈 Chart Visualization</div>", unsafe_allow_html=True)
                render_chart(sample_df, sample_chart_config)


    render_canvas_fragment()
