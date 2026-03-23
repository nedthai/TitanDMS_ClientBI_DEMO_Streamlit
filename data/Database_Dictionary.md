# Dealer AI Assistant
# Data Dictionary & Query Guide

## Overview
This database contains vehicle inventory, movements, and sales data for a dealership. 
The schema has been conceptually flattened into three wide views for ease of querying. **You must exclusively query these views.** 
Do **NOT** attempt to query the underlying base tables (e.g., `FactVehicleSales`, `DimLocation`) directly.

## 1. `vw_FactVehicleSales`
**Purpose:** Tracks completed vehicle sales, including gross profit and transaction details.

| Column Name | Display Name | Data Type | Description |
| :--- | :--- | :--- | :--- |
| `Invoice_Date` | **Sold Date** | DATE | Date the vehicle was invoiced and officially sold. |
| `Invoice_Year` | **Sold Year** | INT | Year of the invoice date. |
| `Invoice_Month_Name` | **Sold Month** | VARCHAR | Month of the invoice date (e.g., 'January'). |
| `Invoice_Quarter_Name` | **Sold Quarter** | VARCHAR | Quarter of the invoice date (e.g., 'Q1'). |
| `Months_Ago` | **Months Ago** | INT | Number of months since the invoice date (0 = current month). |
| `Years_Ago` | **Years Ago** | INT | Number of years since the invoice date (0 = current year). |
| `Is_Current_Month` | **Current Month?** | INT | Boolean flag (1 if Invoice_Date is in the current month). |
| `Is_Current_Year` | **Current Year?** | INT | Boolean flag (1 if Invoice_Date is in the current year). |
| `Company_Name` | **Company** | VARCHAR | Name of the dealership company. |
| `Location_Name` | **Location** | VARCHAR | Name of the specific dealership location. |
| `Make_Name` | **Make** | VARCHAR | Vehicle manufacturer (e.g., 'Toyota'). |
| `Model_Name` | **Model** | VARCHAR | Vehicle model name (e.g., 'Camry'). |
| `Vehicle_Type_Description` | **Vehicle Type** | VARCHAR | General type (e.g., 'Passenger', 'Commercial'). |
| `Vehicle_Class_Description` | **Vehicle Class** | VARCHAR | Class of vehicle (e.g., 'New', 'Used', 'Demo'). |
| `Vehicle_Sales_Group_Description` | **Sales Group** | VARCHAR | Sales categorization group. |
| `Vehicle_Acquisition_Description` | **Acquisition** | VARCHAR | How the vehicle was acquired (e.g., 'Trade-In', 'Factory'). |
| `Stock_No` | **Stock #** | INT | Unique inventory identifier. |
| `Deal_No` | **Deal #** | INT | Identifier for the sales agreement. |
| `Invoice_No` | **Invoice #** | INT | Invoice document number. |
| `Deal_Profit` | **Deal Profit** | DECIMAL | Profit directly from the vehicle sale. |
| `Holdback_Amount` | **Holdback** | DECIMAL | Manufacturer incentives/rebates. |
| `Trade_In_Income` | **Trade-In Profit** | DECIMAL | Profit made on traded-in vehicles. |
| `Aftermarket_Profit` | **Aftermarket Profit** | DECIMAL | Profit from warranties/accessories. |
| `Vehicle_Gross` | **Vehicle Gross** | DECIMAL | Subtotal profit (`Deal_Profit` + `Holdback_Amount` + `Trade_In_Income`). |
| `Total_Gross` | **Total Profit** | DECIMAL | Total Transaction Profit (`Vehicle_Gross` + `Aftermarket_Profit`). |

---

## 2. `vw_FactVehicleStockCurrent`
**Purpose:** Represents current physical inventory sitting on the lot today.

| Column Name | Display Name | Data Type | Description |
| :--- | :--- | :--- | :--- |
| `Company_Name` | **Company** | VARCHAR | Dealership company name. |
| `Location_Name` | **Location** | VARCHAR | Dealership location name. |
| `Make_Name` | **Make** | VARCHAR | Vehicle manufacturer. |
| `Model_Name` | **Model** | VARCHAR | Vehicle model. |
| `Vehicle_Type_Description` | **Vehicle Type** | VARCHAR | General type of vehicle. |
| `Vehicle_Class_Description` | **Vehicle Class** | VARCHAR | 'New', 'Used', etc. |
| `Vehicle_Stockcard_Status_Description` | **Stock Status** | VARCHAR | Status of the stock card (e.g., 'In Stock', 'Reserved'). |
| `Days_In_Stock_Category_Description`| **Aging Bucket** | VARCHAR | Aging bucket (e.g., '<30', '30-59', '90-119', '180+'). |
| `Stock_No` | **Stock #** | INT | Inventory identifier. |
| `Stocked_Date` | **Stocked Date** | DATE | Date the vehicle entered inventory. |
| `Stock_Value` | **Value** | DECIMAL | Capital value of the parked inventory. |
| `Days_In_Stock` | **Days Aged** | INT | Total number of days the vehicle has sat in inventory. |

---

## 3. `vw_FactVehicleStockMovement`
**Purpose:** Tracks historical daily snapshots of inventory. Useful for period-over-period comparisons.

| Column Name | Display Name | Data Type | Description |
| :--- | :--- | :--- | :--- |
| `Date_In_Stock` | **History Date** | DATE | The historical date for which stock is recorded. |
| `Stock_Year` | **Stock Year** | INT | Year of the stock date. |
| `Stock_Month_Name` | **Stock Month** | VARCHAR | Month of the stock date. |
| `Months_Ago` | **Months Ago** | INT | Number of months since the stock date (0 = current month). |
| `Years_Ago` | **Years Ago** | INT | Number of years since the stock date (0 = current year). |
| `Is_Current_Month` | **Current Month?** | INT | Boolean flag (1 if Date_In_Stock is in the current month). |
| `Is_Current_Year` | **Current Year?** | INT | Boolean flag (1 if Date_In_Stock is in the current year). |
| `Company_Name` | **Company** | VARCHAR | Dealership company name. |
| `Location_Name` | **Location** | VARCHAR | Dealership location name. |
| `Make_Name` | **Make** | VARCHAR | Vehicle manufacturer. |
| `Model_Name` | **Model** | VARCHAR | Vehicle model. |
| `Vehicle_Type_Description` | **Vehicle Type** | VARCHAR | General vehicle type. |
| `Vehicle_Class_Description` | **Vehicle Class** | VARCHAR | 'New', 'Used', etc. |
| `Vehicle_Stockcard_Status_Description` | **Stock Status** | VARCHAR | Status on that historical date. |
| `Days_In_Stock_Category_Description`| **Aging Bucket** | VARCHAR | Aging bucket on that historical date. |
| `Stock_No` | **Stock #** | INT | Inventory identifier. |
| `Stocked_Date` | **Stocked Date** | DATE | Date the vehicle originally entered inventory. |
| `Stock_Value` | **Value** | DECIMAL | Value of inventory on that date. |
| `Days_In_Stock` | **Days Aged** | INT | Days aged as of `Date_In_Stock`. |

---


## Categorical Data Reference (Sample Values)

Use these values for filtering in your WHERE clauses:

### vw_FactVehicleSales
* **Company_Name**: 'Co 4', 'Co 3', 'Co 2', 'Co 17', 'Co 18', 'Co 19', 'Co 16', 'Co 14', 'Co 6', 'Co 20'
* **Location_Name**: 'Lo 1812500', 'Lo 411008', 'Lo 201000', 'Lo 1711009', 'Lo 1711007', 'Lo 2022000', 'Lo 712500', 'Lo 121021', 'Lo 2011006', 'Lo 1911051'
* **Make_Name**: 'HYUNDAI', 'GWM', 'EVOLUTION', 'KOKODA', 'SUBARU', 'MITSUBISHI', 'ISUZU', 'CRUSADER CARAVANS', 'JAECOO', 'USED VEH'
* **Vehicle_Class_Description**: 'Demo', 'Used', 'New'
* **Vehicle_Type_Description**: 'SUV', 'Utility Vehicle', 'CARAVAN', 'Motorcycle', 'Light Truck', 'Commercial', 'Scooter', 'Tractors', 'Other', 'Adult Quad Bike'

### vw_FactVehicleStockCurrent
* **Vehicle_Stockcard_Status_Description**: 'In Stock (available)', 'Assigned (In Stock)'
* **Days_In_Stock_Category_Description**: '120-179', '<30', '30-59', '90-119', '180+', '60-89'


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
