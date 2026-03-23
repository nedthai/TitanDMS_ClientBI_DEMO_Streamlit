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
    page_title="Dealer AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Premium Experience
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"], .stMarkdown, .stText {
        font-family: 'Outfit', sans-serif !important;
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
        margin-top: 0px;    /* Pull closer to logo */
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
        border-radius: 16px !important;
        padding: 1rem 1.2rem !important;
        margin-bottom: 1rem !important;
        border: none !important;
        max-width: 75%;
        box-shadow: none !important;
    }

    /* AI Message */
    [data-testid="stChatMessage"]:nth-child(odd) {
        background-color: transparent !important;
        color: #1e293b !important;
        align-self: flex-start !important;
    }
    
    /* User Message */
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: #f8fafc !important;
        color: #0f172a !important;
        align-self: flex-end !important;
        margin-left: auto !important;
    }

    /* Input Field Styling */
    [data-testid="stChatInput"] {
        border-radius: 24px !important;
        border: 1px solid #e2e8f0 !important;
        background: #ffffff !important;
        box-shadow: 0 8px 30px rgba(0,0,0,0.04) !important;
        padding: 6px !important;
    }

    /* Sidebar Section Headers (Enlarged & Refined) */
    .sidebar-header {
        font-size: 0.85rem; /* Increased as requested */
        text-transform: uppercase;
        color: #94a3b8;
        font-weight: 700;   /* Slightly bolder for prominence */
        letter-spacing: 1.2px;
        margin-bottom: 12px; /* Increased padding below header */
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
        padding: 0.5rem 1rem !important; /* Narrower/Less thick */
        box-shadow: 0 4px 6px rgba(0,0,0,0.01) !important;
        text-align: center !important;  /* Center the text within the button */
        transition: all 0.2s ease !important;
        margin: 0 auto !important;
        display: block !important;
    }
    .stButton>button:hover {
        background-color: #ffffff !important;
        border-color: #4f46e5 !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.06) !important;
        transform: translateY(-2px);
    }

    /* Hide default mascot */
    .mascot { display: none; }
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

# Main Layout Logic
# Minimalist Sidebar Design
with st.sidebar:
    # Sidebar Top Branding
    _, sb_logo_col, _ = st.columns([1, 1.5, 1])
    with sb_logo_col:
        st.image("assets/logo_leftslidebar.png", width=80)
    
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
    
    st.markdown(f"<div class='status-row'>&nbsp;&nbsp;{'🟢' if db_exists else '🔴'} <span style='margin-left: 8px;'>Database: {'Active' if db_exists else 'Fail'}</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='status-row'>&nbsp;&nbsp;{'🟢' if api_key_exists else '🔴'} <span style='margin-left: 8px;'>LLM Model: {'Gemini 1.5 Flash' if api_key_exists else 'Failed'}</span></div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    
    # 2. Dealer Information Section
    st.markdown("<div class='sidebar-header'>DEALER INFORMATION</div>", unsafe_allow_html=True)
    # Intentionally blank for future use
    
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    
    # 3. Assistant Actions Section
    st.markdown("<div class='sidebar-header'>ASSISTANT ACTIONS</div>", unsafe_allow_html=True)
    
    # Left-aligned, narrow action link
    if st.button("🗑️&nbsp;&nbsp;Clear chat history", key="trigger_clear", help=None, use_container_width=False):
        st.session_state.messages = []
        st.session_state.temp_prompt = None
        st.rerun()

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "temp_prompt" not in st.session_state:
    st.session_state.temp_prompt = None

def get_cached_dictionary():
    with open("data/Database_Dictionary.md", "r") as f:
        return f.read()

# Render Welcome Screen or Chat History
if len(st.session_state.messages) == 0:
    st.markdown("<div style='height: 5vh;'></div>", unsafe_allow_html=True)
    
    # Centered Logo - Using narrower column for precise alignment
    _, logo_col, _ = st.columns([2, 0.4, 2])
    with logo_col:
        st.image("assets/logo_main.png", width=120)
    
    st.markdown("<div class='welcome-text'>Hi there,</div>", unsafe_allow_html=True)
    st.markdown("<div class='gradient-title' style='font-size: 2.2rem;'>Let's get insight into your data with an AI assistant!</div>", unsafe_allow_html=True)
    st.markdown("<div style='height: 1vh;'></div>", unsafe_allow_html=True)
    
    # Suggested Questions - More Refined, Narrower Column
    _, center_col, _ = st.columns([1.5, 1, 1.5])
    
    questions = [
        ("📈 Monthly Profit Analysis", "What is our total gross profit for the current month?"),
        ("🚗 Top 5 Inventory Models", "Show me the top 5 vehicle models by stock value."),
        ("⏳ High-Risk Aged Stock", "Which locations have the highest aged stock over 90 days?"),
        ("🗺️ Sales Distribution Chart", "Show sales count by location as a bar chart."),
        ("🔄 Recent Stock Movements", "Recent vehicle movements and their status.")
    ]

    with center_col:
        for title, q_text in questions:
            if st.button(title, use_container_width=True):
                st.session_state.temp_prompt = q_text
                st.rerun()
            
    st.markdown("<div style='height: 8vh;'></div>", unsafe_allow_html=True)

else:
    # Display Chat History Loop
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "sql" in message:
                with st.expander("View SQL Query"):
                    st.code(message["sql"], language="sql")
            if "df" in message:
                st.dataframe(message["df"])
            if "chart_config" in message:
                render_chart(message["df"], message["chart_config"])


# Chat Input & Logic
user_input = st.chat_input("How can I help you today?")

# Handle Quick Question button clicks
if st.session_state.temp_prompt:
    user_input = st.session_state.temp_prompt
    st.session_state.temp_prompt = None # Reset for next run

if user_input:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Process AI Response
    with st.chat_message("assistant"):
        with st.status("Analyzing Data...", expanded=True) as status:
            try:
                # 1. Read Data Dictionary
                data_dict = get_cached_dictionary()

                # 2. Generate SQL
                status.write("Generating SQL query...")
                sql = generate_sql(user_input, data_dict)
                st.code(sql, language="sql")

                # 3. Execute Query
                status.write("Executing query on DuckDB...")
                df = execute_query(sql)
                
                if df.empty:
                    response_text = "I couldn't find any data for that request."
                    st.markdown(response_text)
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                else:
                    # Apply User-Friendly Renaming
                    df_display = clean_column_names(df.copy())
                    
                    status.write("Interpreting results...")
                    # 4. Interpret Results
                    # Use technical names for interpretation context to keep LLM consistent, 
                    # but the UI will show friendly names.
                    data_summary = df.head(20).to_string() 
                    response_text = interpret_results(user_input, data_summary)
                    
                    # 5. Parse Chart Config
                    chart_config = parse_chart_config(response_text)
                    
                    # Clean the response text of the chart config markers for display
                    clean_response = response_text.split("---")[0].strip()
                    st.markdown(clean_response)
                    
                    # 6. Display Table and Chart
                    st.dataframe(df_display)
                    if chart_config:
                        # Map chart axes to friendly names if they are technical
                        for key in ["X_AXIS", "Y_AXIS", "COLOR"]:
                            if key in chart_config and chart_config[key] in df.columns:
                                chart_config[key] = get_friendly_name(chart_config[key])
                                
                        render_chart(df_display, chart_config)
                    
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

# Floating Mascot Decoration
st.markdown("""
    <div class='mascot'>
        <img src='https://cdn-icons-png.flaticon.com/512/4712/4712035.png' width='100'>
    </div>
""", unsafe_allow_html=True)

# Alternative: If using local assets, Streamlit requires a different approach for fixed positioning.
# For now, we'll use a high-quality online icon to ensure it works immediately.
