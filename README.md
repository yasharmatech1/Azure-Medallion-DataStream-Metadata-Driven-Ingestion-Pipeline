# Azure-Medallion-DataStream-Metadata-Driven-Ingestion-Pipeline
Tech Stack: ADF, Databricks (Auto Loader, PySpark), ADLS Gen2, Synapse Analytics, Azure Key Vault

# Enterprise Azure Data Engineering Pipeline: End-to-End Medallion Architecture

This repository contains the complete production-grade source code for building an automated, metadata-driven incremental data pipeline using the Microsoft Azure Analytics stack.

## 🏗️ System Architecture

```text
[ On-Prem/Cloud SQL DB ] 
      │
      │ (Incremental Extraction: ADF Metadata Lookup -> ForEach Table)
      ▼
[ Azure Data Factory ] ─── (Secured via Azure Key Vault Secrets)
      │
      │ (Sinks raw incremental files dynamically)
      ▼
[ ADLS Gen2: /landing Zone ] 
      │
      │ (Continuous Ingestion via Databricks Auto Loader)
      ▼
[ Azure Databricks (Silver Layer) ] ─── (Schema Enforcement & Deduplication)
      │
      │ (Business Logic Aggregations)
      ▼
[ Azure Databricks (Gold Layer) ] ─── (Delta Table optimization)
      │
      │ (Serverless SQL Endpoint / Direct Query sync)
      ▼
[ Azure Synapse Analytics ] ─── (Enterprise Serving Layer)
