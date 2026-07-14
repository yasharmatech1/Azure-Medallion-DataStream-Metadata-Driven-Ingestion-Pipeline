-- Track last processed timestamps for multiple tables
CREATE TABLE watermark_table (
    table_name VARCHAR(255),
    last_watermark_value DATETIME
);

-- Sample setup data
INSERT INTO watermark_table VALUES ('sales_transactions', '2026-01-01 00:00:00');