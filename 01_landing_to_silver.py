# Databricks Notebook: Ingesting data via Auto Loader to Silver Delta layer
from pyspark.sql.functions import col, current_timestamp, input_file_name

# Storage Mounting configuration using Key Vault Secret Scope
storage_account = "adlsgen2prodde"
container_landing = "landing"
container_silver = "silver"

# Read connection secret securely
spark.conf.set(
    f"fs.azure.account.key.{storage_account}.dfs.core.windows.net",
    dbutils.secrets.get(scope="azure-key-vault", key="ADLSGen2-AccessKey")
)

# Define dynamic paths
source_landing_path = f"abfss://{container_landing}@{storage_account}.dfs.core.windows.net/sales_transactions/"
target_silver_path = f"abfss://{container_silver}@{storage_account}.dfs.core.windows.net/sales_tables/"
checkpoint_silver = f"abfss://{container_silver}@{storage_account}.dfs.core.windows.net/checkpoints/sales_silver/"

# Real-Time Ingestion Loop using Auto Loader
raw_stream_df = (spark.readStream
                 .format("cloudFiles")
                 .option("cloudFiles.format", "parquet")
                 .option("cloudFiles.useIncrementalListing", "true")
                 .option("cloudFiles.schemaLocation", f"{checkpoint_silver}/schema_evolution")
                 .load(source_landing_path))

# Data Cleaning, Transformation & Structuring 
cleaned_stream_df = (raw_stream_df
                     .filter(col("transaction_id").isNotNull())
                     .withColumn("src_file_origin", input_file_name())
                     .withColumn("silver_processed_at", current_timestamp())
                     .dropDuplicates(["transaction_id", "LastModifiedDate"]))

# Write Atomic Stream Pipeline to Delta Table
query = (cleaned_stream_df.writeStream
         .format("delta")
         .outputMode("append")
         .option("checkpointLocation", checkpoint_path)
         .trigger(availableNow=True) # Runs processing as micro-batch for optimum cost saving
         .start(target_silver_path))

query.awaitTermination()