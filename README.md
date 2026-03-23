# Dealer AI Assistant 🤖

A premium Streamlit-based chatbot powered by Google Gemini API to query and visualize vehicle dealership data from a DuckDB database.

## Features

- **Natural Language to SQL**: Ask questions in plain English and get data directly from the `.duckdb` file.
- **Smart Insights**: Get interpreted summaries of the data results.
- **Dynamic Charts**: Interactive Plotly charts (Bar, Line, Pie, etc.) generated based on your questions.
- **Premium UI**: Modern light-themed interface designed for optimal user experience.

## Project Structure

```
TitanDMS_ClientBI_DEMO_Streamlit/
├── data/                    # Database and Data Dictionary
│   ├── Database_Data.duckdb
│   └── Database_Dictionary.md
├── src/                     # Source code
│   ├── database.py         # DuckDB logic
│   ├── llm_engine.py       # Gemini integration
│   ├── visualization.py    # Plotly rendering
│   └── prompts.py          # AI Prompts
├── app.py                   # Main Application (Chatbot)
├── requirements.txt         # Dependencies
└── .env                     # Environment variables (API Keys)
```

## Setup & Run

1. **Environment Setup**:
   Create a `.env` file with your Gemini API Key:

   ```env
   GEMINI_API_KEY=your_api_key_here
   DUCKDB_PATH=data/Database_Data.duckdb
   ```

2. **Run ETL (Optional)**:
   If you need to rebuild the database from SQL Server:

   ```bash
   python data/etl_build_duckdb_database.py
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the App**:
   ```bash
   streamlit run app.py
   ```

## Example Questions

- "What is our total gross profit?"
- "Show me a bar chart of sales count by location."
- "Top 5 models by stock value."
- "What are the recent vehicle movements?"
