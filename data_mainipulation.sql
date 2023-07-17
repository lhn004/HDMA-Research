SELECT TOP 10 * FROM HDMAdataset;


---Check data type
SELECT COLUMN_NAME, DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'HDMAdataset' AND TABLE_SCHEMA = 'dbo';


---Count the number of rows
SELECT COUNT(*) rownum
FROM HDMAdataset;


---Count null values in each column
DECLARE @TableName NVARCHAR(128) = 'HDMAdataset';
DECLARE @SchemaName NVARCHAR(128) = 'dbo';
DECLARE @DynamicSQL NVARCHAR(MAX) = '';

SELECT @DynamicSQL = @DynamicSQL + 
    'SELECT ''' + COLUMN_NAME + ''' AS ColumnName, COUNT(*) AS NullCount FROM ' + 
    QUOTENAME(@SchemaName) + '.' + QUOTENAME(@TableName) + ' WHERE ' +
    QUOTENAME(COLUMN_NAME) + ' IS NULL UNION ALL '
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = @TableName AND TABLE_SCHEMA = @SchemaName;

SET @DynamicSQL = LEFT(@DynamicSQL, LEN(@DynamicSQL) - LEN(' UNION ALL '));

EXEC sp_executesql @DynamicSQL;


---Filter only PA state and non-missing values 
---Filter only accepted and rejected applications (action_taken = 1 or action_taken = 3)
---Filter only loan_purpose = 1
---Save it in other table
WITH cte AS (
    SELECT * 
    FROM HDMAdataset
    WHERE county_code IS NOT NULL
        AND property_value IS NOT NULL
        AND income IS NOT NULL
        AND debt_to_income_ratio is NOT NULL
        AND state_code = 'PA'
        AND (action_taken = 1 OR action_taken = 3)
        AND loan_purpose = 1

)
SELECT *
INTO filtered_PA_data
FROM cte




---Count the number of rows
SELECT COUNT(*) rownum
FROM filtered_PA_data;


---Count null values in each column
DECLARE @TableName NVARCHAR(128) = 'filtered_PA_data';
DECLARE @SchemaName NVARCHAR(128) = 'dbo';
DECLARE @DynamicSQL NVARCHAR(MAX) = '';

SELECT @DynamicSQL = @DynamicSQL + 
    'SELECT ''' + COLUMN_NAME + ''' AS ColumnName, COUNT(*) AS NullCount FROM ' + 
    QUOTENAME(@SchemaName) + '.' + QUOTENAME(@TableName) + ' WHERE ' +
    QUOTENAME(COLUMN_NAME) + ' IS NULL UNION ALL '
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = @TableName AND TABLE_SCHEMA = @SchemaName;

SET @DynamicSQL = LEFT(@DynamicSQL, LEN(@DynamicSQL) - LEN(' UNION ALL '));

EXEC sp_executesql @DynamicSQL;


---Drop unnecessary column
ALTER TABLE filtered_PA_data
DROP COLUMN column1;


---Select distinct values for each column
SELECT DISTINCT loan_amount FROM filtered_PA_data;
SELECT DISTINCT property_value FROM filtered_PA_data;
SELECT DISTINCT income FROM filtered_PA_data;
SELECT DISTINCT debt_to_income_ratio FROM filtered_PA_data;
SELECT DISTINCT action_taken FROM filtered_PA_data;


---Manipulate property_value column
SELECT DISTINCT property_value FROM filtered_PA_data;

----Replace non-numeric values (Exempt) with 1111 value
UPDATE filtered_PA_data
SET property_value = 1111
WHERE ISNUMERIC(property_value) = 0;

----Change data type
ALTER TABLE filtered_PA_data
ALTER COLUMN property_value FLOAT;


---Manipulate income column
ALTER TABLE filtered_PA_data
ALTER COLUMN income FLOAT;


---Manipulate debt_to_income ratio
SELECT DISTINCT debt_to_income_ratio FROM filtered_PA_data;

UPDATE filtered_PA_data
SET debt_to_income_ratio = CASE
    WHEN debt_to_income_ratio ='<20%' THEN '15'
    WHEN debt_to_income_ratio ='50%-60%' THEN '55'
    WHEN debt_to_income_ratio ='20%-<30%' THEN '25'
    WHEN debt_to_income_ratio ='30%-<36%' THEN '33'
    WHEN debt_to_income_ratio ='>60%' THEN '60'
    WHEN debt_to_income_ratio ='Exempt' THEN '1111'
    ELSE debt_to_income_ratio
END;

ALTER TABLE filtered_PA_data
ALTER COLUMN debt_to_income_ratio INT;

---Check data type
SELECT COLUMN_NAME, DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'filtered_PA_data' AND TABLE_SCHEMA = 'dbo';



---Create an 'outcome' column - whether the application is rejected or accepted
ALTER TABLE filtered_PA_data
ADD outcome INT;

UPDATE filtered_PA_data
SET outcome = CASE
    WHEN action_taken = 1 THEN 1 --accepted applications
    ELSE 0 
END;


SELECT TOP 10 * FROM filtered_PA_data

