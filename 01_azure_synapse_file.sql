-- Create database container pointing to Lakehouse Layer
CREATE DATABASE synapse_serving_db;
GO

USE synapse_serving_db;
GO

-- 1. Create External Data Source linked securely to ADLS Gen2
CREATE EXTERNAL DATA SOURCE AzureGoldLakehouse
WITH (
    LOCATION = 'abs://gold@adlsgen2prodde.dfs.core.windows.net'
);
GO

-- 2. Create Format Identifier for Delta Architectures
CREATE EXTERNAL FILE FORMAT DeltaFormat
WITH (
    FORMAT_TYPE = DELTA
);
GO

-- 3. Create External View/Table inside Serverless Engine for Direct Query Access
CREATE EXTERNAL TABLE serving_daily_financials (
    product_category VARCHAR(100),
    hourly_revenue DECIMAL(18,4),
    total_transaction_count BIGINT,
    window_start DATETIME2,
    window_end DATETIME2
)
WITH (
    LOCATION = 'reports/daily_financials/',
    DATA_SOURCE = AzureGoldLakehouse,
    FILE_FORMAT = DeltaFormat
);
GO

-- End of File: Validate setup connectivity
SELECT TOP 100 * FROM serving_daily_financials ORDER BY hourly_revenue DESC;