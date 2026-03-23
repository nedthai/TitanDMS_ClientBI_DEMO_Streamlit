import pyodbc
import pandas as pd
import duckdb
import os
import time

# SQL Server Connection Configuration
SERVER = r'TITAN-VN-P-91\MSSQLSERVER2019'
DATABASE = 'DemoDealerBI'
PORT = '1433'
USERNAME = 'sa'
PASSWORD = 'Thanhlong@00'

# DuckDB Connection Configuration
# We place the duckdb file in the ../data/ directory relative to this script
DUCKDB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'Database_Data.duckdb')

# List of tables to extract based on Database Building.sql
TABLES = [
    'DimCompany',
    'DimLocation',
    'DimMake',
    'DimModelType',
    'DimModel',
    'DimDate',
    'DimVehicleClass',
    'DimVehicleType',
    'DimVehicleSalesGroup',
    'DimVehicleStockcardStatus',
    'DimDaysInStockCategory',
    'DimVehicle',
    'DimVehicleAcquisition',
    'FactVehicleStockCurrent',
    'FactVehicleStockMovement',
    'FactVehicleSales'
]

def get_sql_server_connection():
    # Construct connection string for pyodbc
    conn_str = (
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={SERVER},{PORT};'
        f'DATABASE={DATABASE};'
        f'UID={USERNAME};'
        f'PWD={PASSWORD};'
    )
    # Note: If ODBC Driver 17 is not available, try 'SQL Server'
    try:
        conn = pyodbc.connect(conn_str)
        return conn
    except pyodbc.Error as e:
        print(f"Error connecting using ODBC Driver 17: {e}")
        print("Falling back to 'SQL Server' driver...")
        conn_str_fallback = (
            f'DRIVER={{SQL Server}};'
            f'SERVER={SERVER},{PORT};'
            f'DATABASE={DATABASE};'
            f'UID={USERNAME};'
            f'PWD={PASSWORD};'
        )
        return pyodbc.connect(conn_str_fallback)

def create_views(duck_conn):
    print("Creating flattened views for LLM...", end=" ", flush=True)
    
    # 1. Sales View
    duck_conn.execute("""
    CREATE OR REPLACE VIEW vw_FactVehicleSales AS
    SELECT 
        f.Invoice_Date,
        d.Year AS Invoice_Year,
        d.Month_Name AS Invoice_Month_Name,
        d.Quarter_Name AS Invoice_Quarter_Name,
        -- Date Helpers
        CAST((date_part('year', CURRENT_DATE) - date_part('year', f.Invoice_Date)) * 12 + 
             (date_part('month', CURRENT_DATE) - date_part('month', f.Invoice_Date)) AS INT) AS Months_Ago,
        CAST(date_part('year', CURRENT_DATE) - date_part('year', f.Invoice_Date) AS INT) AS Years_Ago,
        CASE WHEN date_trunc('month', f.Invoice_Date) = date_trunc('month', CURRENT_DATE) THEN 1 ELSE 0 END AS Is_Current_Month,
        CASE WHEN date_trunc('year', f.Invoice_Date) = date_trunc('year', CURRENT_DATE) THEN 1 ELSE 0 END AS Is_Current_Year,
        c.Company_Name,
        l.Location_Name,
        mk.Make_Name,
        md.Model_Name,
        vt.Vehicle_Type_Description,
        vc.Vehicle_Class_Description,
        vsg.Vehicle_Sales_Group_Description,
        va.Vehicle_Acquisition_Description,
        f.Stock_No,
        f.Deal_No,
        f.Invoice_No,
        f.Deal_Profit,
        f.Holdback_Amount,
        f.Trade_In_Income,
        f.Aftermarket_Profit,
        f.Vehicle_Gross,
        f.Total_Gross
    FROM FactVehicleSales f
    LEFT JOIN DimDate d ON f.Invoice_Date = d.Date_Full
    LEFT JOIN DimLocation l ON f.Location_ID = l.Location_ID
    LEFT JOIN DimCompany c ON l.Company_Key = c.Company_Key
    LEFT JOIN DimVehicle v ON f.Vehicle_Key = v.Vehicle_Key
    LEFT JOIN DimModel md ON v.Model_Key = md.Model_Key
    LEFT JOIN DimModelType mt ON md.Model_Type_Key = mt.Model_Type_Key
    LEFT JOIN DimMake mk ON mt.Make_Key = mk.Make_Key
    LEFT JOIN DimVehicleType vt ON f.Vehicle_Type_ID = vt.Vehicle_Type_ID
    LEFT JOIN DimVehicleClass vc ON f.Vehicle_Class_ID = vc.Vehicle_Class_ID
    LEFT JOIN DimVehicleSalesGroup vsg ON f.Vehicle_Sales_Group_ID = vsg.Vehicle_Sales_Group_ID
    LEFT JOIN DimVehicleAcquisition va ON f.Vehicle_Acquisition_Type = va.Vehicle_Acquisition_Type
    """)

    # 2. Stock Current View
    duck_conn.execute("""
    CREATE OR REPLACE VIEW vw_FactVehicleStockCurrent AS
    SELECT 
        c.Company_Name,
        l.Location_Name,
        mk.Make_Name,
        md.Model_Name,
        vt.Vehicle_Type_Description,
        vc.Vehicle_Class_Description,
        vss.Vehicle_Stockcard_Status_Description,
        dsc.Days_In_Stock_Category_Description,
        f.Stock_No,
        f.Stocked_Date,
        f.Stock_Value,
        f.Days_In_Stock
    FROM FactVehicleStockCurrent f
    LEFT JOIN DimLocation l ON f.Location_ID = l.Location_ID
    LEFT JOIN DimCompany c ON l.Company_Key = c.Company_Key
    LEFT JOIN DimVehicle v ON f.Vehicle_Key = v.Vehicle_Key
    LEFT JOIN DimModel md ON v.Model_Key = md.Model_Key
    LEFT JOIN DimModelType mt ON md.Model_Type_Key = mt.Model_Type_Key
    LEFT JOIN DimMake mk ON mt.Make_Key = mk.Make_Key
    LEFT JOIN DimVehicleType vt ON f.Vehicle_Type_ID = vt.Vehicle_Type_ID
    LEFT JOIN DimVehicleClass vc ON f.Vehicle_Class_ID = vc.Vehicle_Class_ID
    LEFT JOIN DimVehicleStockcardStatus vss ON f.Vehicle_Stockcard_Status_Code = vss.Vehicle_Stockcard_Status_Code
    LEFT JOIN DimDaysInStockCategory dsc ON f.Days_In_Stock_Category_ID = dsc.Days_In_Stock_Category_ID
    """)

    # 3. Stock Movement View
    duck_conn.execute("""
    CREATE OR REPLACE VIEW vw_FactVehicleStockMovement AS
    SELECT 
        f.Date_In_Stock,
        d.Year AS Stock_Year,
        d.Month_Name AS Stock_Month_Name,
        -- Date Helpers
        CAST((date_part('year', CURRENT_DATE) - date_part('year', f.Date_In_Stock)) * 12 + 
             (date_part('month', CURRENT_DATE) - date_part('month', f.Date_In_Stock)) AS INT) AS Months_Ago,
        CAST(date_part('year', CURRENT_DATE) - date_part('year', f.Date_In_Stock) AS INT) AS Years_Ago,
        CASE WHEN date_trunc('month', f.Date_In_Stock) = date_trunc('month', CURRENT_DATE) THEN 1 ELSE 0 END AS Is_Current_Month,
        CASE WHEN date_trunc('year', f.Date_In_Stock) = date_trunc('year', CURRENT_DATE) THEN 1 ELSE 0 END AS Is_Current_Year,
        c.Company_Name,
        l.Location_Name,
        mk.Make_Name,
        md.Model_Name,
        vt.Vehicle_Type_Description,
        vc.Vehicle_Class_Description,
        vss.Vehicle_Stockcard_Status_Description,
        dsc.Days_In_Stock_Category_Description,
        f.Stock_No,
        f.Stocked_Date,
        f.Stock_Value,
        f.Days_In_Stock
    FROM FactVehicleStockMovement f
    LEFT JOIN DimDate d ON f.Date_In_Stock = d.Date_Full
    LEFT JOIN DimLocation l ON f.Location_ID = l.Location_ID
    LEFT JOIN DimCompany c ON l.Company_Key = c.Company_Key
    LEFT JOIN DimVehicle v ON f.Vehicle_Key = v.Vehicle_Key
    LEFT JOIN DimModel md ON v.Model_Key = md.Model_Key
    LEFT JOIN DimModelType mt ON md.Model_Type_Key = mt.Model_Type_Key
    LEFT JOIN DimMake mk ON mt.Make_Key = mk.Make_Key
    LEFT JOIN DimVehicleType vt ON f.Vehicle_Type_ID = vt.Vehicle_Type_ID
    LEFT JOIN DimVehicleClass vc ON f.Vehicle_Class_ID = vc.Vehicle_Class_ID
    LEFT JOIN DimVehicleStockcardStatus vss ON f.Vehicle_Stockcard_Status_Code = vss.Vehicle_Stockcard_Status_Code
    LEFT JOIN DimDaysInStockCategory dsc ON f.Days_In_Stock_Category_ID = dsc.Days_In_Stock_Category_ID
    """)
    print("Done")

def update_data_dictionary(duck_conn):
    print("Updating Data Dictionary with metadata...", end=" ", flush=True)
    dict_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'Database_Dictionary.md')
    
    # Columns to extract samples for
    metadata_cols = {
        'vw_FactVehicleSales': ['Company_Name', 'Location_Name', 'Make_Name', 'Vehicle_Class_Description', 'Vehicle_Type_Description'],
        'vw_FactVehicleStockCurrent': ['Vehicle_Stockcard_Status_Description', 'Days_In_Stock_Category_Description']
    }
    
    metadata_text = "\n## Categorical Data Reference (Sample Values)\n\n"
    metadata_text += "Use these values for filtering in your WHERE clauses:\n\n"
    
    for view, cols in metadata_cols.items():
        metadata_text += f"### {view}\n"
        for col in cols:
            try:
                res = duck_conn.execute(f"SELECT DISTINCT {col} FROM {view} WHERE {col} IS NOT NULL LIMIT 10").fetchall()
                values = ", ".join([f"'{r[0]}'" for r in res])
                metadata_text += f"* **{col}**: {values}\n"
            except:
                continue
        metadata_text += "\n"

    # Read existing content
    with open(dict_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split and Reconstruct (keep existing descriptions, update examples and metadata)
    # We look for the "Few-Shot SQL Examples" header as the anchor
    if "## Categorical Data Reference" in content:
        parts = content.split("## Categorical Data Reference")
        base_content = parts[0]
    elif "## Few-Shot SQL Examples" in content:
        parts = content.split("## Few-Shot SQL Examples")
        base_content = parts[0]
    else:
        base_content = content

    new_examples = """
## Few-Shot SQL Examples (Advanced)

**Question:** "What is our total gross profit this month compared to the same month last year?"
**SQL:**
```sql
SELECT 
    Invoice_Year, 
    SUM(Total_Gross) AS Total_Profit 
FROM vw_FactVehicleSales 
WHERE (Months_Ago = 0) OR (Months_Ago = 12)
GROUP BY Invoice_Year;
```

**Question:** "Top 5 makes by sales volume in the last 6 months"
**SQL:**
```sql
SELECT Make_Name, COUNT(Invoice_No) AS Sales_Count 
FROM vw_FactVehicleSales 
WHERE Months_Ago <= 6
GROUP BY Make_Name 
ORDER BY Sales_Count DESC 
LIMIT 5;
```

**Question:** "Current inventory value of New vs Used passenger vehicles"
**SQL:**
```sql
SELECT Vehicle_Class_Description, SUM(Stock_Value) AS Value 
FROM vw_FactVehicleStockCurrent 
WHERE Vehicle_Type_Description = 'Passenger'
GROUP BY Vehicle_Class_Description;
```

**Question:** "Monthly sales trend for the last 12 months"
**SQL:**
```sql
SELECT Invoice_Year, Invoice_Month_Name, SUM(Total_Gross) AS Profit
FROM vw_FactVehicleSales
WHERE Months_Ago <= 12
GROUP BY Invoice_Year, Invoice_Month_Name, Months_Ago
ORDER BY Months_Ago DESC;
```
"""

    final_content = base_content + metadata_text + new_examples
    
    with open(dict_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print("Done")

def main():
    print(f"Starting ETL process from SQL Server ({SERVER}) to DuckDB ({DUCKDB_PATH})")
    start_time = time.time()
    
    # Establish connections
    try:
        sql_conn = get_sql_server_connection()
        print("Successfully connected to SQL Server.")
    except Exception as e:
        print(f"Failed to connect to SQL Server: {e}")
        return

    try:
        duck_conn = duckdb.connect(DUCKDB_PATH)
        print("Successfully connected to DuckDB.")
    except Exception as e:
        print(f"Failed to connect to DuckDB: {e}")
        sql_conn.close()
        return

    total_rows = 0

    for table in TABLES:
        print(f"Extracting table: {table} ...", end=" ", flush=True)
        query = f"SELECT * FROM dbo.{table}"
        try:
            # Read from SQL Server into pandas DataFrame
            df = pd.read_sql(query, sql_conn)
            row_count = len(df)
            
            # Save into DuckDB safely
            # Note: duckdb can directly read the 'df' variable from the local scope
            duck_conn.execute(f"CREATE OR REPLACE TABLE {table} AS SELECT * FROM df")
            
            print(f"Done. ({row_count} rows)")
            total_rows += row_count
        except Exception as e:
            print(f"Error processing table {table}: {e}")

    # Create views to flatten schema for the AI
    create_views(duck_conn)

    # Update the Data Dictionary with sample values and advanced examples
    update_data_dictionary(duck_conn)

    # Close connections
    duck_conn.close()
    sql_conn.close()

    end_time = time.time()
    duration = end_time - start_time
    print(f"\nETL process completed in {duration:.2f} seconds.")
    print(f"Total rows extracted: {total_rows}")

if __name__ == "__main__":
    main()
