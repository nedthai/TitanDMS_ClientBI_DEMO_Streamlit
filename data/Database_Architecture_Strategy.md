# Database Architecture & Semantic Strategy

This document outlines the core strategies implemented to optimize the Data Warehouse (DuckDB) and Semantic Model layers for the Dealer AI Assistant.

## 1. Architectural Foundation: "Flattened Views"
To minimize SQL generation errors, we transitioned from a complex snowflake schema (base tables) to a **Flattened View Architecture**.

*   **Views**: `vw_FactVehicleSales`, `vw_FactVehicleStockCurrent`, `vw_FactVehicleStockMovement`.
*   **Purpose**: These views pre-join facts with all relevant dimensions (Location, Company, Make, Model, Date).
*   **Strategy**: The AI is strictly forbidden from querying base tables. This eliminates join errors and ensures consistent business logic.

## 2. Semantic Layer Strategy: "Poor Man's Semantic Layer"
Instead of complex semantic modeling tools, we use a metadata-driven approach via `Database_Dictionary.md`.

*   **Mapping**: Maps technical column names to **Display Names** (Friendly Names).
*   **Context**: Provides the AI with a list of columns, data types, and human-readable descriptions.
*   **Few-Shot Examples**: Includes "Golden Queries" that show the AI how to handle common requests (grouping, filtering, and time-series).

## 3. Accuracy Optimization Strategies

### A. Relative Date Helpers (Proximity Logic)
Generating SQL for "last month" or "year-to-date" is error-prone. We solved this by adding relative date columns to the views:
*   `Months_Ago` / `Years_Ago`: 0 = Current, 1 = Previous, etc.
*   `Is_Current_Month` / `Is_Current_Year`: Boolean flags.
*   **Benefit**: The AI can now perform complex time-series analysis with simple `WHERE` clauses (e.g., `WHERE Months_Ago <= 12`).

### B. Categorical Metadata Extraction
The ETL script automatically extracts unique values (Enums) for key columns (Make, Location, Class) and injects them into the Data Dictionary.
*   **Benefit**: Prevents hallucination of values (e.g., knowing the system uses 'HYUNDAI' instead of 'Hyundai').

### C. Hybrid Column Aliasing
We implemented a bridge between the Technical Database and the User Experience:
*   **Technical Layer**: The AI generates SQL using standard database names.
*   **Python Layer (app.py)**: An automated "Column Cleaner" renames results in real-time (e.g., `Company_Name` → `Company`).
*   **Visualization Layer (visualization.py)**: Re-maps chart axes to match the user-friendly labels.

## 4. Maintenance Workflow
The system is designed to be self-healing:
1.  **ETL Execution**: `etl_build_duckdb_database.py` extracts data and rebuilds views.
2.  **Auto-Dictionary Update**: The same script updates the `Database_Dictionary.md` with fresh metadata and examples.
3.  **AI Engine**: `app.py` always reads the latest version of the consolidated dictionary.

---

### Core Principles for Future LLMs
If you are an AI assistant working on this project:
1.  **Trust the Views**: Never go around them.
2.  **Use Date Helpers**: Prefer `Months_Ago` over complex date math.
3.  **Check Sample Values**: Use the Categorical Reference in the dictionary to ensure your filters match the data.
4.  **Friendly UI**: Remember that the Python layer will handle the "beautification" of headers; you focus on accurate SQL logic.
