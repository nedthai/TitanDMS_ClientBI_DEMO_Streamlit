import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="User Guide - Dealer AI Assistant",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS to hide the sidebar and the toggle button
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;500;600;700&display=swap');
    
    html, body, .stMarkdown, .stText, p, h1, h2, h3 {
        font-family: 'Rubik', sans-serif !important;
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
        margin-bottom: 25px;
    }

    /* Completely hide the sidebar */
    [data-testid="stSidebar"] {
        display: none !important;
    }

    /* Hide the sidebar collapse button */
    [data-testid="stSidebarCollapseButton"] {
        display: none !important;
    }

    /* Adjust the main content to take full width */
    [data-testid="stAppViewBlockContainer"] {
        padding-top: 2rem !important;
        max-width: 1000px !important;
        margin: 0 auto !important;
    }
    
    /* Vibrant Blurred Background - Lighter Pastel Mix */
    .stApp {
        background-color: #ffffff;
        background-image: 
            radial-gradient(at 85% 0%, rgba(240, 244, 255, 0.6) 0px, transparent 40%),
            radial-gradient(at 0% 100%, rgba(245, 240, 255, 0.4) 0px, transparent 40%);
        background-attachment: fixed;
    }
    </style>
    """, unsafe_allow_html=True)

def render_user_guide():
    """Renders the User Guide page content."""
    
    # Header
    col1, col2 = st.columns([1, 8])
    with col1:
        st.link_button("← Back to Chat", url="/", help="Returns to the main assistant page")
    with col2:
        st.markdown("<div class='gradient-title' style='font-size: 2.2rem; text-align: left;'>User Guide & Documentation</div>", unsafe_allow_html=True)

    st.markdown("---")

    # Tabs for different documentation sections
    tabs = st.tabs(["📊 Data & Semantic Model", "🤖 AI Interaction", "📈 Chart Gallery"])

    with tabs[0]:
        st.header("Data Warehouse & Semantic Model")
        st.write("""
            The Dealer AI Assistant is powered by a high-performance **DuckDB** data warehouse. 
            The data is organized into three primary 'Semantic Views' that the AI uses to answer your questions.
        """)
        
        with st.expander("1. Vehicle Sales (vw_FactVehicleSales)", expanded=True):
            st.markdown("""
                **Purpose:** Tracks every vehicle sold, including financial performance.
                - **Key Metrics:** Total Profit, Deal Profit, Trade-In Profit.
                - **Time Dimensions:** Sold Date, Sold Year, Sold Month, Months Ago (0 = current).
                - **Attributes:** Make, Model, Vehicle Class (New/Used/Demo), Location.
            """)

        with st.expander("2. Current Inventory (vw_FactVehicleStockCurrent)"):
            st.markdown("""
                **Purpose:** A real-time snapshot of vehicles currently on the lot.
                - **Key Metrics:** Stock Value, Days Aged.
                - **Attributes:** Aging Bucket (<30, 30-59, etc.), Stock Status, Make, Model.
            """)

        with st.expander("3. Historical Inventory (vw_FactVehicleStockMovement)"):
            st.markdown("""
                **Purpose:** Daily historical snapshots for trend analysis.
                - **Usage:** Use this to compare inventory levels at different points in time (e.g., "What was our stock value 3 months ago?").
            """)

    with tabs[1]:
        st.header("How to Interact with the AI")
        st.write("""
            The assistant is designed to be conversational. You don't need to know SQL or technical column names.
        """)
        
        st.subheader("💡 Tips for Best Results")
        st.markdown("""
            - **Be Specific about Time:** Instead of "sales," try "sales this month" or "sales in 2023."
            - **Ask for Comparisons:** "Compare New vs Used sales profit this year."
            - **Filter by Attributes:** "Show me all Toyotas in stock for more than 90 days."
            - **Request Visuals:** End your question with "as a pie chart" or "show a bar graph."
        """)

    with tabs[2]:
        st.header("Supported Chart Types")
        st.write("The assistant can automatically generate the following visualizations:")
        
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            st.markdown("""
                - **Bar / Column Charts:** Best for comparing categories (e.g., Sales by Make).
                - **Line / Trend Charts:** Best for time series (e.g., Monthly Profit Trend).
                - **Pie / Donut Charts:** Best for showing parts of a whole (e.g., Stock by Location).
                - **Stacked Charts:** Best for sub-categories (e.g., Sales by Make stacked by Class).
            """)
        with chart_col2:
            st.markdown("""
                - **Area Charts:** Similar to line charts but showing volume.
                - **Scatter Plots:** Good for identifying correlations (e.g., Days Aged vs Value).
                - **Treemaps:** Great for hierarchical data.
                - **Funnel Charts:** Ideal for stages or specific sequences.
            """)

    st.info("Note: The AI automatically selects the best chart type if you don't specify one, but you can always override it in your prompt.")

if __name__ == "__main__":
    render_user_guide()
