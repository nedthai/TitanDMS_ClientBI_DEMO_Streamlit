---------------------------------------------------------------------------------------------------------------
-- 0. SCHEMA DESCRIPTION | + To describe the purpose of this cript and the schema of database 'DemoDealerBI' --
---------------------------------------------------------------------------------------------------------------

-- PURPOSE OF THIS SCRIPT
--
-- + This script is designed to build up the SQL Server database 'DemoDealerBI' by | * creating necessary tables
--                                                                                 | * generating data for dimensions and facts
--                                                                                 | * transforming data where needed
--                                                                                 | * and finally checking the data to ensure everything is correct.
-- + The script is structured into four main sections | 1. CREATE TABLE
--                                                    | 2. GENERATE DATA
--                                                    | 3. TRANSFORM DATA
--                                                    | 4. CHECK DATA

-- THE SCHEMA OF DATABASE 'DemoDealerBI'
-- + The entire data architecture follows Star Schema with DIM and FACT tables. In fact, it's more accurately Snowflake Schema.
-- + About DIM tables
--   - dbo.DimDate is a standard date dimension table with various date attributes
--   - dbo.DimCompany is the father of dbo.DimLocation
--   - dbo.DimMake is the father of dbo.DimModelType which is the father of dbo.DimModel and dbo.DimVehicle is the child of dbo.DimModel
--   - dbo.DimVehicleClass, dbo.DimVehicleType, dbo.DimVehicleSalesGroup, dbo.DimVehicleStockcardStatus, dbo.DimDaysInStockCategory and dbo.DimVehicleAcquisition are standalone dimension tables with only ID and Description
-- + About FACT tables
--   - dbo.FactVehicleStockCurrent and dbo.FactVehicleStockMovement have the same dimension keys and measures, but the former one is for current stock while the latter one is for stock movement with Date_In_Stock as an additional attribute
--   - dbo.FactVehicleStockCurrent
--     * Dimension keys include | Days_In_Stock_Category_ID from dbo.DimDaysInStockCategory
--                              | Location_ID from dbo.DimLocation
--                              | Vehicle_Key from dbo.DimVehicle
--                              | Vehicle_Class_ID from dbo.DimVehicleClass
--                              | Vehicle_Type_ID from dbo.DimVehicleType
--                              | Vehicle_Stockcard_Status_Code from dbo.DimVehicleStockcardStatus
--     * Some columns just be the additional information for stock, such as Vehicle_ID, Stock_No, Stocked_Date, Vehicle_Stockcard_Key
--	   * Measures include | Stock_Value is the value of the vehicle in stock, which is calculated based on the cost price and other factors
--                        | Days_In_Stock is the number of days that the vehicle has been in stock, which is calculated as the difference between the current date and the stocked date
--   - dbo.FactVehicleStockMovement
--     * Dimension keys include | Date_In_Stock will link to Date_Full in dbo.DimDate
--                              | Days_In_Stock_Category_ID from dbo.DimDaysInStockCategory
--                              | Location_ID from dbo.DimLocation
--                              | Vehicle_Key from dbo.DimVehicle
--                              | Vehicle_Class_ID from dbo.DimVehicleClass
--                              | Vehicle_Type_ID from dbo.DimVehicleType
--                              | Vehicle_Stockcard_Status_Code from dbo.DimVehicleStockcardStatus
--     * Some columns just be the additional information for stock, such as Vehicle_ID, Stock_No, Stocked_Date, Vehicle_Stockcard_Key
--	   * Measures include | Stock_Value is the value of the vehicle in stock, which is calculated based on the cost price and other factors
--                        | Days_In_Stock is the number of days that the vehicle has been in stock, which is calculated as the difference between the current date and the stocked date
--   - dbo.FactVehicleSales has more dimension keys than the other two FACT tables, and it contains sales related measures
--     * Dimension keys include | Invoice_Date will link to Date_Full in dbo.DimDate
--                              | Location_ID from dbo.DimLocation
--                              | Vehicle_Key from dbo.DimVehicle
--                              | Vehicle_Class_ID from dbo.DimVehicleClass
--                              | Vehicle_Type_ID from dbo.DimVehicleType
--                              | Vehicle_Sales_Group_ID from dbo.DimVehicleSalesGroup
--                              | Vehicle_Acquisition_Type from dbo.DimVehicleAcquisition
--     * Some columns just be the additional information for sales, such as Vehicle_ID, Stock_No, Deal_No, Invoice_No, Vehicle_Deal_Key, Vehicle_Stockcard_Key and Purchased_From_Name
--	   * Measures include | Deal_Profit is the profit from the deal of selling a vehicle, which is calculated as the difference between the selling price and the cost price of the vehicle
--                        | Holdback_Amount is the amount that the dealership receives from the manufacturer after selling a vehicle, which is usually a percentage of the selling price
--                        | Trade_In_Income is the income from trading in a used vehicle when selling a new vehicle, which is calculated as the difference between the trade-in value and the cost price of the used vehicle
--                        | Aftermarket_Profit is the profit from selling aftermarket products or services, such as extended warranty, insurance, accessories, etc.
--                        | Vehicle_Gross is the sum of Deal_Profit, Holdback_Amount and Trade_In_Income
--                        | Total_Gross is the sum of Vehicle_Gross and Aftermarket_Profit

-------------------------------------------------------------------------
-- 1. CREATE TABLE | + To create tables for dimensions and facts       --
--                 | + Check exsistence of tables before creating them --
-------------------------------------------------------------------------

-- dbo.DimDate
IF EXISTS (SELECT 1 FROM sysobjects WHERE id = object_id('dbo.DimDate'))
BEGIN
    DROP TABLE dbo.DimDate
END
CREATE TABLE dbo.DimDate (
    Date_Key               INT,
    Date_Full              DATE,
    Date_Full_Name         VARCHAR(50),
    Year                   INT,
    Quarter                INT,
    Quarter_Key            INT,
    Quarter_Name           VARCHAR(50),
    Month                  INT,
    Month_Key              INT,
    Month_Name             VARCHAR(50),
    Month_Short_Name       VARCHAR(3),
    Month_Number_Of_Days   INT,
    Week_Of_Year           INT,
    Week_Of_Year_Key       INT,
    Week_Day               INT,
    Week_Day_Name          VARCHAR(50),
    Week_Day_Short_Name    VARCHAR(3),
    Day_Of_Year            INT,
    Day_Of_Month           INT,
    ISO_Week               INT,
    ISO_Week_Key           INT,
    Fiscal_Year            INT,
    Fiscal_Quarter         INT,
    Fiscal_Quarter_Key     INT,
    Fiscal_Month           INT,
    Fiscal_Month_Key       INT,
    Is_Workday_Key         INT,
    Is_Workday_Description VARCHAR(50),
    Timeline_Type          VARCHAR(50)
)

-- dbo.DimCompany
IF EXISTS (SELECT 1 FROM sysobjects WHERE id = object_id('dbo.DimCompany'))
BEGIN
    DROP TABLE dbo.DimCompany
END
CREATE TABLE dbo.DimCompany (
    Company_Key  INT,
    Company_Name NVARCHAR(256)
)

-- dbo.DimLocation
IF EXISTS (SELECT 1 FROM sysobjects WHERE id = object_id('dbo.DimLocation'))
BEGIN
    DROP TABLE dbo.DimLocation
END
CREATE TABLE dbo.DimLocation (
    Location_ID   INT,
    Location_Name NVARCHAR(256),
    Company_Key   INT
)

-- dbo.DimMake
IF EXISTS (SELECT 1 FROM sysobjects WHERE id = object_id('dbo.DimMake'))
BEGIN
    DROP TABLE dbo.DimMake
END
CREATE TABLE dbo.DimMake (
    Make_Key  INT,
    Make_Name NVARCHAR(80)
)

-- dbo.DimModelType
IF EXISTS (SELECT 1 FROM sysobjects WHERE id = object_id('dbo.DimModelType'))
BEGIN
    DROP TABLE dbo.DimModelType
END
CREATE TABLE dbo.DimModelType (
    Model_Type_Key  INT,
    Model_Type_Name NVARCHAR(128),
    Make_Key        INT
)

-- dbo.DimModel
IF EXISTS (SELECT 1 FROM sysobjects WHERE id = object_id('dbo.DimModel'))
BEGIN
    DROP TABLE dbo.DimModel
END
CREATE TABLE dbo.DimModel (
    Model_Key      INT,
    Model_Name     NVARCHAR(80),
    Model_Type_Key INT
)

-- dbo.DimVehicle
IF EXISTS (SELECT 1 FROM sysobjects WHERE id = object_id('dbo.DimVehicle'))
BEGIN
    DROP TABLE dbo.DimVehicle
END
CREATE TABLE dbo.DimVehicle (
    Vehicle_Key         INT,
    VIN                 NVARCHAR(34),
    REGO_NO             NVARCHAR(80),
    Manufacturer_ID     NVARCHAR(80),
    Colour              NVARCHAR(256),
    Vehicle_Description NVARCHAR(2000),
    Model_Key           INT
)

-- dbo.DimVehicleClass
IF EXISTS (SELECT 1 FROM sysobjects WHERE id = object_id('dbo.DimVehicleClass'))
BEGIN
    DROP TABLE dbo.DimVehicleClass
END
CREATE TABLE dbo.DimVehicleClass (
    Vehicle_Class_ID          INT,
    Vehicle_Class_Description NVARCHAR(4000)
)

-- dbo.DimVehicleType
IF EXISTS (SELECT 1 FROM sysobjects WHERE id = object_id('dbo.DimVehicleType'))
BEGIN
    DROP TABLE dbo.DimVehicleType
END
CREATE TABLE dbo.DimVehicleType (
    Vehicle_Type_ID          INT,
    Vehicle_Type_Description NVARCHAR(4000)
)

-- dbo.DimVehicleSalesGroup
IF EXISTS (SELECT 1 FROM sysobjects WHERE id = object_id('dbo.DimVehicleSalesGroup'))
BEGIN
    DROP TABLE dbo.DimVehicleSalesGroup
END
CREATE TABLE dbo.DimVehicleSalesGroup (
    Vehicle_Sales_Group_ID          INT,
    Vehicle_Sales_Group_Description NVARCHAR(512)
)

-- dbo.DimVehicleStockcardStatus
IF EXISTS (SELECT 1 FROM sysobjects WHERE id = object_id('dbo.DimVehicleStockcardStatus'))
BEGIN
    DROP TABLE dbo.DimVehicleStockcardStatus
END
CREATE TABLE dbo.DimVehicleStockcardStatus (
    Vehicle_Stockcard_Status_Code        INT,
    Vehicle_Stockcard_Status_Description NVARCHAR(4000)
)

-- dbo.DimDaysInStockCategory
IF EXISTS (SELECT 1 FROM sysobjects WHERE id = object_id('dbo.DimDaysInStockCategory'))
BEGIN
    DROP TABLE dbo.DimDaysInStockCategory
END
CREATE TABLE dbo.DimDaysInStockCategory (
    Days_In_Stock_Category_ID          INT,
    Days_In_Stock_Category_Description NVARCHAR(200)
)

-- dbo.DimVehicleAcquisition
IF EXISTS (SELECT 1 FROM sysobjects WHERE id = object_id('dbo.DimVehicleAcquisition'))
BEGIN
    DROP TABLE dbo.DimVehicleAcquisition
END
CREATE TABLE dbo.DimVehicleAcquisition (
    Vehicle_Acquisition_Type        INT,
    Vehicle_Acquisition_Description NVARCHAR(4000)
)

-- dbo.FactVehicleStockCurrent
IF EXISTS (SELECT 1 FROM sysobjects WHERE id = object_id('dbo.FactVehicleStockCurrent'))
BEGIN
    DROP TABLE dbo.FactVehicleStockCurrent
END
CREATE TABLE dbo.FactVehicleStockCurrent (
    Days_In_Stock_Category_ID     INT,
    Location_ID                   INT,
    Vehicle_Key                   INT,
    Vehicle_Class_ID              INT,
    Vehicle_Type_ID               INT,
    Vehicle_Stockcard_Status_Code INT,
    Vehicle_ID                    NVARCHAR(80),
    Stock_No                      INT,
    Stocked_Date                  DATE,
    Vehicle_Stockcard_Key         INT,
    Stock_Value                   DECIMAL(19,4),
    Days_In_Stock                 INT
)

-- dbo.FactVehicleStockMovement
IF EXISTS (SELECT 1 FROM sysobjects WHERE id = object_id('dbo.FactVehicleStockMovement'))
BEGIN
    DROP TABLE dbo.FactVehicleStockMovement
END
CREATE TABLE dbo.FactVehicleStockMovement (
    Date_In_Stock                 DATE,
    Days_In_Stock_Category_ID     INT,
    Location_ID                   INT,
    Vehicle_Key                   INT,
    Vehicle_Class_ID              INT,
    Vehicle_Type_ID               INT,
    Vehicle_Stockcard_Status_Code INT,
    Vehicle_ID                    NVARCHAR(80),
    Stock_No                      INT,
    Stocked_Date                  DATE,
    Vehicle_Stockcard_Key         INT,
    Stock_Value                   DECIMAL(19,4),
    Days_In_Stock                 INT
)

-- dbo.FactVehicleSales
IF EXISTS (SELECT 1 FROM sysobjects WHERE id = object_id('dbo.FactVehicleSales'))
BEGIN
    DROP TABLE dbo.FactVehicleSales
END
CREATE TABLE dbo.FactVehicleSales (
    Invoice_Date             DATE,
    Location_ID              INT,
    Vehicle_Key              INT,
    Vehicle_Class_ID         INT,
    Vehicle_Type_ID          INT,
    Vehicle_Sales_Group_ID   INT,
    Vehicle_Acquisition_Type INT,
    Vehicle_ID               NVARCHAR(80),
    Stock_No                 INT,
    Deal_No                  INT,
    Invoice_No               INT,
    Vehicle_Deal_Key         INT,
    Vehicle_Stockcard_Key    INT,
    Purchased_From_Name      NVARCHAR(256),
    Deal_Profit              DECIMAL(19,4),
    Holdback_Amount          DECIMAL(19,4),
    Trade_In_Income          DECIMAL(19,4),
    Aftermarket_Profit       DECIMAL(19,4),
    Vehicle_Gross            DECIMAL(19,4),
    Total_Gross              DECIMAL(19,4)
)


--------------------------------------------------------------------
-- 2. GENERATE DATA | + To generate data for dimensions and facts --
--                  | + Truncate tables first                     --
--                  | + After that insert data to tables          --
--------------------------------------------------------------------

-- Truncate tables before inserting data to avoid duplication if you run this script multiple times
TRUNCATE TABLE dbo.DimCompany
TRUNCATE TABLE dbo.DimLocation
TRUNCATE TABLE dbo.DimMake
TRUNCATE TABLE dbo.DimModelType
TRUNCATE TABLE dbo.DimModel
TRUNCATE TABLE dbo.DimDate
TRUNCATE TABLE dbo.DimVehicleClass
TRUNCATE TABLE dbo.DimVehicleType
TRUNCATE TABLE dbo.DimVehicleSalesGroup
TRUNCATE TABLE dbo.DimVehicleStockcardStatus
TRUNCATE TABLE dbo.DimDaysInStockCategory
TRUNCATE TABLE dbo.DimVehicle
TRUNCATE TABLE dbo.FactVehicleStockCurrent
TRUNCATE TABLE dbo.FactVehicleStockMovement
TRUNCATE TABLE dbo.FactVehicleSales

-- Gen data for dbo.DimCompany
INSERT INTO dbo.DimCompany (
    Company_Key,
    Company_Name
)
SELECT COMPANY_KEY  AS Company_Key,
       COMPANY_NAME AS Company_Name
FROM Westpoint_Autos_DW.dbo.DIM_Company

-- Gen data for dbo.DimLocation
INSERT INTO dbo.DimLocation (
    Location_ID,
    Location_Name,
    Company_Key
)
SELECT LOCATION_ID   AS Location_ID,
       LOCATION_NAME AS Location_Name,
       COMPANY_KEY   AS Company_Key
FROM Westpoint_Autos_DW.dbo.DIM_Location

-- Gen data for dbo.DimMake
INSERT INTO dbo.DimMake (
    Make_Key,
    Make_Name
)
SELECT MAKE_KEY AS Make_Key,
       MAKE_ID  AS Make_Name
FROM Westpoint_Autos_DW.dbo.DIM_Make

-- Gen data for dbo.DimModelType
INSERT INTO dbo.DimModelType (
    Model_Type_Key,
    Model_Type_Name,
    Make_Key
)
SELECT MODEL_TYPE_KEY AS Model_Type_Key,
       MODEL_TYPE_ID  AS Model_Type_Name,
       MAKE_KEY       AS Make_Key
FROM Westpoint_Autos_DW.dbo.DIM_ModelType

-- Gen data for dbo.DimModel
INSERT INTO dbo.DimModel (
    Model_Key,
    Model_Name,
    Model_Type_Key
)
SELECT MODEL_KEY      AS Model_Key,
       MODEL_ID       AS Model_Name,
       MODEL_TYPE_KEY AS Model_Type_Key
FROM Westpoint_Autos_DW.dbo.DIM_Model
UNION ALL
SELECT -2             AS Model_Key,
       'USED VEH'     AS Model_Name,
       1              AS Model_Type_Key

-- Gen data for dbo.DimDate
INSERT INTO dbo.DimDate (
    Date_Key,
    Date_Full,
    Date_Full_Name,
    Year,
    Quarter,
    Quarter_Key,
    Quarter_Name,
    Month,
    Month_Key,
    Month_Name,
    Month_Short_Name,
    Month_Number_Of_Days,
    Week_Of_Year,
    Week_Of_Year_Key,
    Week_Day,
    Week_Day_Name,
    Week_Day_Short_Name,
    Day_Of_Year,
    Day_Of_Month,
    ISO_Week,
    ISO_Week_Key,
    Fiscal_Year,
    Fiscal_Quarter,
    Fiscal_Quarter_Key,
    Fiscal_Month,
    Fiscal_Month_Key,
    Is_Workday_Key,
    Is_Workday_Description,
    Timeline_Type
)
SELECT DD.DATEKEY                AS Date_Key,
       DD.DATEFULL               AS Date_Full,
       DD.DATEFULLNAME           AS Date_Full_Name,
       DD.YEAR                   AS Year,
       DD.QUARTER                AS Quarter,
       DD.QUARTERKEY             AS Quarter_Key,
       DD.QUARTERNAME            AS Quarter_Name,
       DD.MONTH                  AS Month,
       DD.MONTHKEY               AS Month_Key,
       DD.MONTHNAME              AS Month_Name,
       LEFT(DD.MONTHNAME, 3)     AS Month_Short_Name,
       DD.MONTHNUMBEROFDAYS      AS Month_Number_Of_Days,
       DD.WEEKOFYEAR             AS Week_Of_Year,
       DD.WEEKOFYEARKEY          AS Week_Of_Year_Key,
       DD.WEEKDAY                AS Week_Day,
       DD.WEEKDAYNAME            AS Week_Day_Name,
       LEFT(DD.WEEKDAYNAME, 3)   AS Week_Day_Short_Name,
       DD.DAYOFYEAR              AS Day_Of_Year,
       DD.DAYOFMONTH             AS Day_Of_Month,
       DD.ISOWEEK                AS ISO_Week,
       DD.ISOWEEKKEY             AS ISO_Week_Key,
       DD.FISCALYEAR             AS Fiscal_Year,
       DD.FISCALQUARTER          AS Fiscal_Quarter,
       DD.FISCALQUARTERKEY       AS Fiscal_Quarter_Key,
       DD.FISCALMONTH            AS Fiscal_Month,
       DD.FISCALMONTHKEY         AS Fiscal_Month_Key,
       DD.ISWORKDAYKEY           AS Is_Workday_Key,
       DD.ISWORKDAYDESCRIPTION   AS Is_Workday_Description,
       CASE WHEN DD.DATEFULL < PD.ProcessDate THEN 'Past'
            WHEN DD.DATEFULL = PD.ProcessDate THEN 'Present'
            WHEN DD.DATEFULL > PD.ProcessDate THEN 'Future' END AS Timeline_Type
FROM Westpoint_Autos_DW.dbo.DIM_Date DD
     CROSS JOIN (SELECT ProcessDate FROM Westpoint_Autos_DW.dbo.ETL_Config_Setting_Master) PD

-- Gen data for dbo.DimVehicleClass
INSERT INTO dbo.DimVehicleClass (
    Vehicle_Class_ID,
    Vehicle_Class_Description
)
SELECT VEHICLE_CLASS_ID          AS Vehicle_Class_ID,
       VEHICLE_CLASS_DESCRIPTION AS Vehicle_Class_Description
FROM Westpoint_Autos_DW.dbo.DIM_VehicleClass
WHERE IS_ACTIVE = 1

-- Gen data for dbo.DimVehicleType
INSERT INTO dbo.DimVehicleType (
    Vehicle_Type_ID,
    Vehicle_Type_Description
)
SELECT VEHICLE_TYPE_ID          AS Vehicle_Type_ID,
       VEHICLE_TYPE_DESCRIPTION AS Vehicle_Type_Description
FROM Westpoint_Autos_DW.dbo.DIM_VehicleType
WHERE IS_ACTIVE = 1

-- Gen data for dbo.DimVehicleSalesGroup
INSERT INTO dbo.DimVehicleSalesGroup (
    Vehicle_Sales_Group_ID,
    Vehicle_Sales_Group_Description
)
SELECT VEHICLE_SALES_GROUP_ID          AS Vehicle_Sales_Group_ID,
       VEHICLE_SALES_GROUP_DESCRIPTION AS Vehicle_Sales_Group_Description
FROM Westpoint_Autos_DW.dbo.DIM_VehicleSalesGroup
WHERE IS_ACTIVE = 1

-- Gen data for dbo.DimVehicleStockcardStatus
INSERT INTO dbo.DimVehicleStockcardStatus (
    Vehicle_Stockcard_Status_Code,
    Vehicle_Stockcard_Status_Description
)
SELECT VEHICLE_STOCKCARD_STATUS_CODE        AS Vehicle_Stockcard_Status_Code,
       VEHICLE_STOCKCARD_STATUS_DESCRIPTION AS Vehicle_Stockcard_Status_Description
FROM Westpoint_Autos_DW.dbo.DIM_VehicleStockcardStatus
WHERE IS_ACTIVE = 1

-- Gen data for dbo.DimDaysInStockCategory
INSERT INTO dbo.DimDaysInStockCategory (
    Days_In_Stock_Category_ID,
    Days_In_Stock_Category_Description
)
SELECT 1 AS Days_In_Stock_Category_ID, '<30'     AS Days_In_Stock_Category_Description UNION ALL
SELECT 2 AS Days_In_Stock_Category_ID, '30-59'   AS Days_In_Stock_Category_Description UNION ALL
SELECT 3 AS Days_In_Stock_Category_ID, '60-89'   AS Days_In_Stock_Category_Description UNION ALL
SELECT 4 AS Days_In_Stock_Category_ID, '90-119'  AS Days_In_Stock_Category_Description UNION ALL
SELECT 5 AS Days_In_Stock_Category_ID, '120-179' AS Days_In_Stock_Category_Description UNION ALL
SELECT 6 AS Days_In_Stock_Category_ID, '180+'    AS Days_In_Stock_Category_Description

-- Gen data for dbo.DimVehicle
INSERT INTO dbo.DimVehicle (
    Vehicle_Key,
    VIN,
    REGO_NO,
    Manufacturer_ID,
    Colour,
    Vehicle_Description,
    Model_Key
)
SELECT VEHICLE_KEY                                            AS Vehicle_Key,
       VIN                                                    AS VIN,
       REGO_NO                                                AS REGO_NO,
       MANUFACTURER_ID                                        AS Manufacturer_ID,
       COLOUR                                                 AS Colour,
       VEHICLE_DESCRIPTION                                    AS Vehicle_Description,
       CASE WHEN MODEL_KEY IS NULL THEN -2 ELSE MODEL_KEY END AS Model_Key
FROM Westpoint_Autos_DW.dbo.DIM_Vehicle

-- Gen data for dbo.DimVehicleAcquisition
INSERT INTO dbo.DimVehicleAcquisition (
    Vehicle_Acquisition_Type,
    Vehicle_Acquisition_Description
)
SELECT VEHICLE_ACQUISITION_TYPE AS Vehicle_Acquisition_Type,
       CASE WHEN VEHICLE_ACQUISITION_TYPE = -1 THEN 'Unknown' ELSE VEHICLE_ACQUISITION_DESCRIPTION END AS Vehicle_Acquisition_Description
FROM Westpoint_Autos_DW.dbo.DIM_VehicleAcquisition

-- Gen data for dbo.FactVehicleStockCurrent
INSERT INTO dbo.FactVehicleStockCurrent (
    Days_In_Stock_Category_ID,
    Location_ID,
    Vehicle_Key,
    Vehicle_Class_ID,
    Vehicle_Type_ID,
    Vehicle_Stockcard_Status_Code,
    Vehicle_ID,
    Stock_No,
    Stocked_Date,
    Vehicle_Stockcard_Key,
    Stock_Value,
    Days_In_Stock
)
SELECT CASE WHEN DATEDIFF(DAY, FVS.STOCKED_DATE, DDS.MAX_DATEFULL) < 30  THEN 1
            WHEN DATEDIFF(DAY, FVS.STOCKED_DATE, DDS.MAX_DATEFULL) < 60  THEN 2
            WHEN DATEDIFF(DAY, FVS.STOCKED_DATE, DDS.MAX_DATEFULL) < 90  THEN 3
            WHEN DATEDIFF(DAY, FVS.STOCKED_DATE, DDS.MAX_DATEFULL) < 120 THEN 4
            WHEN DATEDIFF(DAY, FVS.STOCKED_DATE, DDS.MAX_DATEFULL) < 180 THEN 5
            ELSE 6 END                                   AS Days_In_Stock_Category_ID,
       FVS.LOCATION_ID                                   AS Location_ID,
       FVS.VEHICLE_KEY                                   AS Vehicle_Key,
       FVS.VEHICLE_CLASS_ID                              AS Vehicle_Class_ID,
       FVS.VEHICLE_TYPE_ID                               AS Vehicle_Type_ID,
       FVS.VEHICLE_STOCKCARD_STATUS_CODE                 AS Vehicle_Stockcard_Status_Code,
       FVS.VEHICLE_ID                                    AS Vehicle_ID,
       FVS.STOCK_NO                                      AS Stock_No,
       FVS.STOCKED_DATE                                  AS Stocked_Date,
       FVS.VEHICLE_STOCKCARD_KEY                         AS Vehicle_Stockcard_Key,
       FVS.STOCK_VALUE                                   AS Stock_Value,
       DATEDIFF(DAY, FVS.STOCKED_DATE, DDS.MAX_DATEFULL) AS Days_In_Stock
FROM Westpoint_Autos_DW.dbo.FCT_VehicleStock FVS
     CROSS JOIN (SELECT MAX(Date_Full) AS MAX_DATEFULL FROM dbo.DimDate WHERE Timeline_Type <> 'Future') DDS
WHERE FVS.VEHICLE_STOCKCARD_STATUS_CODE IN (2,4)

-- Gen data for dbo.FactVehicleStockMovement
INSERT INTO dbo.FactVehicleStockMovement (
    Date_In_Stock,
    Days_In_Stock_Category_ID,
    Location_ID,
    Vehicle_Key,
    Vehicle_Class_ID,
    Vehicle_Type_ID,
    Vehicle_Stockcard_Status_Code,
    Vehicle_ID,
    Stock_No,
    Stocked_Date,
    Vehicle_Stockcard_Key,
    Stock_Value,
    Days_In_Stock
)
SELECT FVS.DATE_IN_STOCK                                  AS Date_In_Stock,
       CASE WHEN DATEDIFF(DAY, FVS.STOCKED_DATE, FVS.DATE_IN_STOCK) < 30  THEN 1
            WHEN DATEDIFF(DAY, FVS.STOCKED_DATE, FVS.DATE_IN_STOCK) < 60  THEN 2
            WHEN DATEDIFF(DAY, FVS.STOCKED_DATE, FVS.DATE_IN_STOCK) < 90  THEN 3
            WHEN DATEDIFF(DAY, FVS.STOCKED_DATE, FVS.DATE_IN_STOCK) < 120 THEN 4
            WHEN DATEDIFF(DAY, FVS.STOCKED_DATE, FVS.DATE_IN_STOCK) < 180 THEN 5
            ELSE 6 END                                    AS Days_In_Stock_Category_ID,
       FVS.LOCATION_ID                                    AS Location_ID,
       FVS.VEHICLE_KEY                                    AS Vehicle_Key,
       FVS.VEHICLE_CLASS_ID                               AS Vehicle_Class_ID,
       FVS.VEHICLE_TYPE_ID                                AS Vehicle_Type_ID,
       FVS.VEHICLE_STOCKCARD_STATUS_CODE                  AS Vehicle_Stockcard_Status_Code,
       FVS.VEHICLE_ID                                     AS Vehicle_ID,
       FVS.STOCK_NO                                       AS Stock_No,
       FVS.STOCKED_DATE                                   AS Stocked_Date,
       FVS.VEHICLE_STOCKCARD_KEY                          AS Vehicle_Stockcard_Key,
       FVS.STOCK_VALUE                                    AS Stock_Value,
       DATEDIFF(DAY, FVS.STOCKED_DATE, FVS.DATE_IN_STOCK) AS Days_In_Stock
FROM Westpoint_Autos_DW.dbo.FCT_VehicleStock_Movement FVS

-- Gen data for dbo.FactVehicleSales
INSERT INTO dbo.FactVehicleSales (
    Invoice_Date,
    Location_ID,
    Vehicle_Key,
    Vehicle_Class_ID,
    Vehicle_Type_ID,
    Vehicle_Sales_Group_ID,
    Vehicle_Acquisition_Type,
    Vehicle_ID,
    Stock_No,
    Deal_No,
    Invoice_No,
    Vehicle_Deal_Key,
    Vehicle_Stockcard_Key,
    Purchased_From_Name,
    Deal_Profit,
    Holdback_Amount,
    Trade_In_Income,
    Aftermarket_Profit,
    Vehicle_Gross,
    Total_Gross
)
SELECT INVOICE_DATE                                                        AS Invoice_Date,
       LOCATION_ID                                                         AS Location_ID,
       VEHICLE_KEY                                                         AS Vehicle_Key,
       VEHICLE_CLASS_ID                                                    AS Vehicle_Class_ID,
       VEHICLE_TYPE_ID                                                     AS Vehicle_Type_ID,
       VEHICLE_SALES_GROUP_ID                                              AS Vehicle_Sales_Group_ID,
       VEHICLE_ACQUISITION_TYPE                                            AS Vehicle_Acquisition_Type,
       VEHICLE_ID                                                          AS Vehicle_ID,
       STOCK_NO                                                            AS Stock_No,
       DEAL_NO                                                             AS Deal_No,
       INVOICE_NO                                                          AS Invoice_No,
       VEHICLE_DEAL_KEY                                                    AS Vehicle_Deal_Key,
       VEHICLE_STOCKCARD_KEY                                               AS Vehicle_Stockcard_Key,
       PURCHASED_FROM_NAME                                                 AS Purchased_From_Name,
       DEAL_PROFIT                                                         AS Deal_Profit,
       HOLDBACK_AMT                                                        AS Holdback_Amount,
       TRADE_IN_INCOME                                                     AS Trade_In_Income,
       AFTERMARKET_PROFIT                                                  AS Aftermarket_Profit,
       (DEAL_PROFIT + HOLDBACK_AMT + TRADE_IN_INCOME)                      AS Vehicle_Gross,
       (DEAL_PROFIT + HOLDBACK_AMT + TRADE_IN_INCOME + AFTERMARKET_PROFIT) AS Total_Gross
FROM Westpoint_Autos_DW.dbo.FCT_VehicleSales


------------------------------------------------------------
-- 3. TRANSFORM DATA | + To transform data on some tables --
------------------------------------------------------------

UPDATE c
SET c.Company_Name = 'Co ' + CAST(Company_Key AS VARCHAR(10))
FROM dbo.DimCompany c

UPDATE l
SET l.Location_Name = 'Lo ' + CAST(Location_ID AS VARCHAR(10))
FROM dbo.DimLocation l

UPDATE v
SET v.VIN     = REPLACE(VIN,     RIGHT(VIN,     CAST(ROUND(LEN(VIN)*0.75,0) AS INT)),     'xxxxxxxxxxxxxxx'),
    v.REGO_NO = REPLACE(REGO_NO, RIGHT(REGO_NO, CAST(ROUND(LEN(REGO_NO)*0.75,0) AS INT)), 'xxxxx')
FROM dbo.DimVehicle v


--------------------------------------------------------------
-- 4. CHECK DATA | + To check data to sure everything is ok --
--------------------------------------------------------------

;WITH CTE_DATA AS (
    SELECT 'VW_RPT_DIM_Company'                TableName, COUNT(1) CountRow FROM dbo.DimCompany                UNION ALL
    SELECT 'VW_RPT_DIM_Location'               TableName, COUNT(1) CountRow FROM dbo.DimLocation               UNION ALL
    SELECT 'VW_RPT_DIM_Make'                   TableName, COUNT(1) CountRow FROM dbo.DimMake                   UNION ALL
    SELECT 'VW_RPT_DIM_ModelType'              TableName, COUNT(1) CountRow FROM dbo.DimModelType              UNION ALL
    SELECT 'VW_RPT_DIM_Model'                  TableName, COUNT(1) CountRow FROM dbo.DimModel                  UNION ALL
    SELECT 'VW_RPT_DIM_Date'                   TableName, COUNT(1) CountRow FROM dbo.DimDate                   UNION ALL
    SELECT 'VW_RPT_DIM_VehicleClass'           TableName, COUNT(1) CountRow FROM dbo.DimVehicleClass           UNION ALL
    SELECT 'VW_RPT_DIM_VehicleType'            TableName, COUNT(1) CountRow FROM dbo.DimVehicleType            UNION ALL
    SELECT 'VW_RPT_DIM_VehicleSalesGroup'      TableName, COUNT(1) CountRow FROM dbo.DimVehicleSalesGroup      UNION ALL
    SELECT 'VW_RPT_DIM_VehicleStockcardStatus' TableName, COUNT(1) CountRow FROM dbo.DimVehicleStockcardStatus UNION ALL
    SELECT 'VW_RPT_DIM_DaysInStockCategory'    TableName, COUNT(1) CountRow FROM dbo.DimDaysInStockCategory    UNION ALL
    SELECT 'VW_RPT_DIM_Vehicle'                TableName, COUNT(1) CountRow FROM dbo.DimVehicle                UNION ALL
    SELECT 'VW_RPT_FCT_VehicleStock_Current'   TableName, COUNT(1) CountRow FROM dbo.FactVehicleStockCurrent   UNION ALL
    SELECT 'VW_RPT_FCT_VehicleStock_Movement'  TableName, COUNT(1) CountRow FROM dbo.FactVehicleStockMovement  UNION ALL
    SELECT 'VW_RPT_FCT_VehicleSales'           TableName, COUNT(1) CountRow FROM dbo.FactVehicleSales
)
SELECT TableName, CountRow FROM CTE_DATA

SELECT TOP(100) * FROM dbo.DimCompany
SELECT TOP(100) * FROM dbo.DimLocation