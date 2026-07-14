# Databricks Notebook: Aggregations for Financial Reporting (Gold Layer)
from pyspark.sql.functions import sum, count, col, window

storage_account = "adlsgen2prodde"
container_silver = "silver"
container_gold = "gold"

silver_path = f"abfss://{container_silver}@{storage_account}.dfs.core.windows.net/sales_tables/"
gold_path = f"abfss://{container_gold}@{storage_account}.dfs.core.windows.net/reports/daily_financials/"
checkpoint_gold = f"abfss://{container_gold}@{storage_account}.dfs.core.windows.net/checkpoints/sales_gold/"

# Read state from Silver Delta Lakehouse
silver_df = spark.readStream.format("delta").load(silver_path)

# Apply Business Aggregations (Total Revenue per product line per hour)
gold_aggregated_df = (silver_df
                      .groupBy(
                          col("product_category"),
                          window(col("LastModifiedDate"), "1 hour").alias("transaction_window")
                      )
                      .agg(
                          sum("total_price").alias("hourly_revenue"),
                          count("transaction_id").alias("total_transaction_count")
                      )
                      .withColumn("window_start", col("transaction_window.start"))
                      .withColumn("window_end", col("transaction_window.end"))
                      .drop("transaction_window"))

# Write directly to Gold Endpoint
gold_query = (gold_aggregated_df.writeStream
              .format("delta")
              .outputMode("complete") # Complete mode applies updates inside aggregation structures
              .option("checkpointLocation", checkpoint_gold)
              .trigger(availableNow=True)
              .start(gold_path))

gold_query.awaitTermination()

# Optimize Delta Table performance configurations
spark.sql(f"OPTIMIZE delta.`{gold_path}` ZORDER BY (product_category)")