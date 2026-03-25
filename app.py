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
    initial_sidebar_state="collapsed"
)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "temp_prompt" not in st.session_state:
    st.session_state.temp_prompt = None

# Custom CSS for Premium Experience

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;500;600;700&display=swap');
    
    html, body, .stMarkdown, .stText, p, h1, h2, h3 {
        font-family: 'Rubik', sans-serif !important;
    }

    /* Centering results and unifying widths */
    .main .block-container {
        max-width: 850px !important;
        margin: 0 auto !important;
        padding-top: 3rem !important;
    }
    
    /* Ensure the input field matches the content width */
    [data-testid="stBottom"] > div {
        max-width: 850px !important;
        margin: 0 auto !important;
    }

    /* Vibrant Blurred Background - Lighter Pastel Mix */
    /* Minimalist White Background */
    .stApp {
        background-color: #ffffff;
        background-image: 
            radial-gradient(at 85% 0%, rgba(240, 244, 255, 0.6) 0px, transparent 40%),
            radial-gradient(at 0% 100%, rgba(245, 240, 255, 0.4) 0px, transparent 40%);
        background-attachment: fixed;
    }

    /* Main Container Cleanup */
    [data-testid="stVerticalBlock"] > div:has(div > .stHeader) {
        background: transparent;
        border: none;
        padding: 0 !important;
        box-shadow: none;
        backdrop-filter: none;
    }

    /* Gradient Title */
    .gradient-title {
        background: linear-gradient(90deg, #4f46e5, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 700;
        text-align: center;
        margin-top: 0px;
        margin-bottom: 15px; /* Reduced from 30px */
    }
    
    .welcome-text {
        font-size: 1.8rem;
        font-weight: 600;
        color: #0f172a;
        text-align: center;
        margin-top: -10px;    /* Pulled closer to logo */
        margin-bottom: -12px; /* Slightly more space for title */
    }

    /* Card Styling for Quick Actions */
    .action-card {
        background: rgba(255, 255, 255, 0.8);
        border: 1px solid #f1f5f9;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        transition: all 0.2s ease;
    }
    .action-card:hover {
        background: #ffffff;
        box-shadow: 0 10px 25px rgba(0,0,0,0.06);
        transform: translateY(-2px);
    }
    
    .card-title {
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 6px;
        font-size: 1rem;
    }
    .card-desc {
        font-size: 0.85rem;
        color: #64748b;
    }

    /* Chat Message Bubbles */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        margin-bottom: -30px !important;
        width: 100% !important;
        padding-right: 0px !important;
    }

    /* Target the content area within the chat message for bubble styling */
    [data-testid="stChatMessageContent"] {
        padding: 0.3rem 0.6rem !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03) !important;
        width: 100% !important;
        box-sizing: border-box !important;
        padding-top: 10px !important;
        padding-bottom: 10px !important;
    }

    /* Chat Content Styling (Force no borders/shadows) */
    [data-testid="stChatMessageContent"],
    [data-testid="stStatusWidget"],
    [data-testid="stStatusWidget"] > div {
        border: 1px solid transparent !important;
        box-shadow: none !important;
    }

    /* User Message Bubble */
    [data-testid="stChatMessage"]:nth-child(odd) [data-testid="stChatMessageContent"] {
        background-color: #f8fafc !important;
        color: #0f172a !important;
    }
    
    /* AI Message Bubble */
    [data-testid="stChatMessage"]:nth-child(even) [data-testid="stChatMessageContent"] {
        background-color: #ffffff !important;
        color: #1e293b !important;
    }

    /* Additional status widget cleanup */
    [data-testid="stStatusWidget"] {
        background-color: transparent !important;
    }

    /* Input Field Styling */
    [data-testid="stChatInput"] {
        border-radius: 12px !important;
        border: none !important;
        background: #ffffff !important;
        box-shadow: 0 8px 30px rgba(0,0,0,0.04) !important;
        padding: 0 !important;
    }
    
    [data-testid="stChatInput"] textarea {
        padding: 0.15rem 0.3rem !important; /* Ultra-compact (1/3 size) */
        min-height: unset !important;
    }

    /* Sidebar Section Headers (Enlarged & Refined) */
    .sidebar-header {
        font-size: 0.85rem; /* Increased as requested */
        text-transform: uppercase;
        color: #94a3b8;
        font-weight: 700;   /* Slightly bolder for prominence */
        letter-spacing: 1.2px;
        margin-bottom: 6px; /* Reduced from 12px as requested */
        margin-top: 18px;
    }

    /* Elegant Sidebar Menu Item (for Clear Chat) */
    .sidebar-action-item {
        display: flex;
        align-items: center;
        padding: 10px 12px;
        border-radius: 10px;
        color: #475569;
        font-size: 0.88rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
        text-decoration: none;
        margin-left: -5px;
    }
    .sidebar-action-item:hover {
        background-color: #f1f5f9;
        color: #0f172a;
        transform: translateX(3px);
    }
    .sidebar-action-icon {
        margin-right: 12px;
        font-size: 1rem;
        opacity: 0.8;
    }

    /* Hide the default Streamlit Multipage Navigation */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    
    /* Refined Sidebar Menu Item (Narrower, Left Aligned) */

    section[data-testid="stSidebar"] .stButton>button {
        background: none !important;
        background-color: transparent !important;
        color: #475569 !important;
        border-radius: 8px !important;
        border: none !important;
        outline: none !important;
        padding: 0.4rem 0.6rem !important; /* Reduced height/padding */
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        box-shadow: none !important;
        display: flex !important;
        justify-content: flex-start !important;
        transition: all 0.2s ease !important;
        width: fit-content !important; /* Narrower width */
        min-width: 160px !important;
        text-align: left !important;
    }
    section[data-testid="stSidebar"] .stButton>button:hover {
        background-color: #f1f5f9 !important;
        color: #0f172a !important;
        transform: translateX(3px) !important;
    }
    
    /* Main Area Buttons (Quick Insights) - More Refined Card Style */
    .stButton {
        margin-top: -12px !important; /* Pull buttons closer together */
    }
    .stButton>button {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border-radius: 12px !important;
        border: 1px solid #f1f5f9 !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;  /* Slightly smaller for refinement */
        padding: 0.4rem 0.8rem !important; /* Balanced padding */
        box-shadow: 0 4px 6px rgba(0,0,0,0.01) !important;
        text-align: center !important;  /* Center the text within the button */
        transition: all 0.2s ease !important;
        margin: 0 auto !important;
    }
    .stButton>button:hover {
        background-color: #ffffff !important;
        border-color: #4f46e5 !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.06) !important;
        transform: translateY(-2px);
    }

    /* Dashed Insight Box - override Streamlit's bordered container inner border */
    [data-testid="stChatMessage"] [data-testid="stVerticalBlockBorderWrapper"] > div {
        border: 1.8px dashed #a5b4fc !important;
        border-radius: 10px !important;
        background: rgba(238, 242, 255, 0.42) !important;
        padding: 5px 16px !important;
    }

    /* Sidebar Navigation Link (Mimic Sidebar Buttons) */
    .sidebar-nav-link {
        color: #475569 !important;
        text-decoration: none !important;
        padding: 0.45rem 0.6rem !important; /* Refined to match button padding */
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        display: flex !important;
        align-items: center !important;
        transition: all 0.2s ease !important;
        width: fit-content !important;
        min-width: 160px !important;
        border-radius: 8px !important;
        font-family: 'Rubik', sans-serif !important;
        line-height: 1.25 !important;
    }
    .sidebar-nav-link:hover {
        background-color: #f1f5f9 !important;
        color: #0f172a !important;
        transform: translateX(3px) !important;
    }
    .sidebar-nav-link span {
        margin-right: 12px;
        font-size: 1rem;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 18px; /* Consistent icon width */
    }
    </style>
    """, unsafe_allow_html=True)



# Column Display Mapping (Overwrites for special cases)
COLUMN_DISPLAY_MAP = {
    "Stock_No": "Stock #",
    "Deal_No": "Deal #",
    "Invoice_No": "Invoice #",
    "Is_Current_Month": "Current Month?",
    "Is_Current_Year": "Current Year?",
    "Trade_In_Income": "Trade-In Profit",
    "Date_In_Stock": "History Date",
    "Stock_Value": "Value",
    "Days_In_Stock": "Days Aged"
}

def clean_column_names(df):
    """Renames DataFrame columns to be more user-friendly."""
    new_columns = {}
    for col in df.columns:
        new_columns[col] = get_friendly_name(col)
    return df.rename(columns=new_columns)

def get_friendly_name(col):
    """Converts a technical column name to a friendly display name."""
    if col in COLUMN_DISPLAY_MAP:
        return COLUMN_DISPLAY_MAP[col]
    
    # Automated cleaning logic
    clean_name = col.replace("_", " ")
    clean_name = clean_name.replace(" Name", "")
    clean_name = clean_name.replace(" Description", "")
    clean_name = clean_name.replace(" Invoice", " Sold")
    clean_name = clean_name.replace("Invoice ", "Sold ")
    return clean_name.strip()

# ── Chart Preference Extraction ──────────────────────────────────────────────
# Keep this in sync with CHART_TYPE_ALIASES in visualization.py
_CHART_KEYWORDS = [
    "stacked column", "stacked bar", "stacked area",
    "horizontal bar", "grouped bar", "grouped column",
    "column chart", "column graph",
    "bar chart", "bar graph",
    "line chart", "line graph",
    "pie chart",
    "donut chart", "doughnut chart",
    "area chart",
    "scatter chart", "scatter plot",
    "histogram",
    "box chart", "box plot",
    "violin chart", "violin plot",
    "treemap", "tree map",
    "funnel chart",
    # Single-word fallbacks (order matters — longer phrases above)
    "column", "bar", "line", "pie", "donut", "doughnut",
    "area", "scatter", "box", "violin", "funnel",
]

def extract_chart_preference(question: str) -> str:
    """Return the chart type phrase if the user mentioned one, else 'Not specified'."""
    q = question.lower()
    for kw in _CHART_KEYWORDS:
        if kw in q:
            return kw
    return "Not specified"

# Main Layout Logic
# Minimalist Sidebar Design
with st.sidebar:
    # 0. Sidebar Branding (Always Visible)
    _, sb_logo_col, _ = st.columns([1, 1.5, 1])
    with sb_logo_col:
        st.image("assets/logo.png", width=80)
    
    st.markdown("""
        <div style='text-align: center; margin-top: -15px; margin-bottom: 20px;'>
            <span style='background: linear-gradient(90deg, #4f46e5, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 700; font-size: 1.1rem;'>
                Dealer AI Assistant
            </span>
        </div>
    """, unsafe_allow_html=True)
    
    # 1. System Status Section
    st.markdown("<div class='sidebar-header'>SYSTEM STATUS</div>", unsafe_allow_html=True)
    
    db_exists = os.path.exists("data/Database_Data.duckdb")
    api_key_exists = os.getenv("GEMINI_API_KEY") is not None
    
    st.markdown(f"<div class='status-row'>&nbsp;&nbsp;{'🟢' if db_exists else '🔴'} <span style='margin-left: 8px;'>Database Status: {'Active' if db_exists else 'Failed'}</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='status-row'>&nbsp;&nbsp;{'🟢' if api_key_exists else '🔴'} <span style='margin-left: 8px;'>LLM Model: {'Google Gemini' if api_key_exists else 'Failed'}</span></div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    
    # 2. Dealer Information Section
    st.markdown("<div class='sidebar-header'>DEALER INFORMATION</div>", unsafe_allow_html=True)
    # Intentionally blank for future use
    
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    
    # 3. Assistant Actions Section
    st.markdown("<div class='sidebar-header'>ASSISTANT ACTIONS</div>", unsafe_allow_html=True)
    
    # User Guide Link (With consistent icon container)
    st.markdown("""
        <a href="/User_Guide" target="_blank" class="sidebar-nav-link" style="margin-left: 2px; margin-top: -5px;">
            <span>📖</span>User Guide
        </a>
        <div style="height: 4px;"></div>
    """, unsafe_allow_html=True)


    # Left-aligned, narrow action link
    if st.button("🗑️&nbsp;&nbsp;Clear chat history", key="trigger_clear", help=None, use_container_width=False):
        st.session_state.messages = []
        st.session_state.temp_prompt = None
        st.rerun()


def get_cached_dictionary():
    with open("data/Database_Dictionary.md", "r") as f:
        return f.read()

if st.session_state.temp_prompt:
    st.session_state.messages.append({"role": "user", "content": st.session_state.temp_prompt})
    st.session_state.temp_prompt = None

# The Streamlit `st.chat_input` doesn't block, so it's placed anywhere but renders at bottom.
user_input = st.chat_input("How can I help you today?")


if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

# Header Section (Conditional)
if len(st.session_state.messages) == 0:
    st.markdown("<div style='height: 2vh;'></div>", unsafe_allow_html=True)
    _, logo_col, _ = st.columns([2, 0.4, 2])
    with logo_col:
        st.image("assets/logo.png", width=120)

    st.markdown("<div class='welcome-text'>Hi there,</div>", unsafe_allow_html=True)
    st.markdown("<div class='gradient-title' style='font-size: 2.2rem;'>Let's get insight into your data with an AI assistant!</div>", unsafe_allow_html=True)

    # Padding
    st.markdown("<div style='height: 2vh;'></div>", unsafe_allow_html=True)


# Display Chat History Loop
last_message_is_user = False
if len(st.session_state.messages) > 0:
    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            if "sql" in message:
                with st.expander("🔍 View Generated SQL Query", expanded=False):
                    st.code(message["sql"], language="sql")
            if message["content"]:
                with st.container(border=True):
                    st.markdown(message["content"])
            if "df" in message:
                has_chart = bool(message.get("chart_config"))
                if has_chart:
                    tbl_col, chart_col = st.columns([1, 1.4], gap="medium")
                    with tbl_col:
                        st.dataframe(
                            clean_column_names(message["df"].copy()),
                            width="stretch"
                        )
                    with chart_col:
                        render_chart(
                            clean_column_names(message["df"].copy()),
                            message["chart_config"]
                        )
                else:
                    st.dataframe(
                        clean_column_names(message["df"].copy()),
                        use_container_width=True
                    )
        
        # Check if this is the last message and it's from the user
        if i == len(st.session_state.messages) - 1 and message["role"] == "user":
            last_message_is_user = True

    # Process AI Response if the last message was from the user
    if last_message_is_user:
        user_msg = st.session_state.messages[-1]["content"]
        with st.chat_message("assistant"):
            with st.status("Analyzing Data...", expanded=True) as status:
                try:
                    # 1. Read Data Dictionary
                    data_dict = get_cached_dictionary()

                    # 2. Generate SQL
                    status.write("Generating SQL query...")
                    sql = generate_sql(user_msg, data_dict)
                    with st.expander("🔍 View Generated SQL Query", expanded=False):
                        st.code(sql, language="sql")

                    # 3. Execute Query
                    status.write("Executing query on DuckDB...")
                    df = execute_query(sql)
                    
                    if df.empty:
                        response_text = "I couldn't find any data for that request."
                        with st.container(border=True):
                            st.markdown(response_text)
                        # Add to session state
                        st.session_state.messages.append({"role": "assistant", "content": response_text})
                    else:
                        # Apply User-Friendly Renaming
                        df_display = clean_column_names(df.copy())
                        
                        status.write("Interpreting results...")
                        # 4. Interpret Results
                        data_summary = df.head(20).to_string()
                        chart_pref = extract_chart_preference(user_msg)
                        response_text = interpret_results(user_msg, data_summary,
                                                          user_chart_preference=chart_pref)
                        
                        # 5. Parse Chart Config
                        chart_config = parse_chart_config(response_text)
                        
                        # Clean the response text (strip chart config block)
                        clean_response = response_text.split("---")[0].strip()

                        # 6. Display Insight Box (Summarize & Highlight)
                        with st.container(border=True):
                            st.markdown(clean_response)
                        
                        # 7. Remap chart axis labels to friendly names
                        if chart_config:
                            for key in ["X_AXIS", "Y_AXIS", "COLOR"]:
                                if key in chart_config and chart_config[key] in df.columns:
                                    chart_config[key] = get_friendly_name(chart_config[key])

                        # 8. Display Table and Chart side-by-side
                        if chart_config:
                            tbl_col, chart_col = st.columns([1, 1.4], gap="medium")
                            with tbl_col:
                                st.dataframe(df_display, width="stretch")
                            with chart_col:
                                render_chart(df_display, chart_config)
                        else:
                            st.dataframe(df_display, width="stretch")
                        
                        # Add to session state
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": clean_response,
                            "sql": sql,
                            "df": df,
                            "chart_config": chart_config
                        })
                    
                    status.update(label="Complete!", state="complete", expanded=False)
                except Exception as e:
                    st.error(f"Error: {e}")
                    status.update(label="Error Occurred", state="error")
                    st.session_state.messages.append({"role": "assistant", "content": "I encountered an error processing your request."})

    # Reset temp prompt if used
    st.session_state.temp_prompt = None

