# Cryptocurrency Analytics Data Engineering Pipeline

This project implements a **production-grade cryptocurrency data engineering pipeline** that processes Bitcoin (BTC), Ethereum (ETH), and Dogecoin (DOGE) market data from January 2020 to present. Built on Snowflake's data cloud platform, the pipeline demonstrates advanced data engineering patterns including **medallion architecture**, **change data capture (CDC)**, **event-driven orchestration**, and **real-time analytics**.

The pipeline ingests cryptocurrency data from Yahoo Finance API, processes it through multiple transformation layers, and generates comprehensive financial analytics including technical indicators, volatility metrics, and performance benchmarks. The entire workflow is automated using Snowflake's native orchestration capabilities with intelligent resource management and error handling.

### ➡️ **For comprehensive overview and detailed walkthrough, complete this end-to-end tutorial: [Data Engineering with Notebooks](https://codelabs-preview.appspot.com/?file_id=1YSeHJtOA5iL07o71Xsk5OWpftGxDQF0aYC6Bi9oy7Ro/#0)**

---

## Data Engineering Concepts Implementation

This pipeline demonstrates comprehensive **data engineering concepts** with practical implementations:

- **ETL/ELT Pipelines**: Implemented ELT pattern with Yahoo Finance API extraction, S3 staging, and Snowflake transformation layers
- **Medallion Architecture (Bronze-Silver-Gold)**: Three-tier data architecture with RAW_CRYPTO → HARMONIZED_CRYPTO → ANALYTICS_CRYPTO schemas
- **Change Data Capture (CDC)**: Snowflake Streams monitor table changes to trigger downstream processing (`RAW_CRYPTO_STREAM_BTC`, `HARMONIZED_STREAM`)
- **Event-Driven Architecture**: Tasks execute conditionally using `SYSTEM$STREAM_HAS_DATA()` to process only when new data arrives
- **Batch Processing**: Scheduled 4-hour data extraction with incremental loading and merge operations
- **Data Quality Framework**: Schema validation, null rate monitoring, and duplicate detection across all pipeline stages
- **Workflow Orchestration**: DAG-based task dependencies with `LOAD_CRYPTO_TASK → HARMONIZE_CRYPTO_TASK → UPDATE_ANALYTICS_TASK`
- **Dynamic Resource Management**: Auto-scaling warehouse compute (XSMALL → LARGE → XSMALL) based on processing requirements
- **Stream Processing**: Real-time change tracking and incremental data processing using Snowflake Streams
- **Dimensional Modeling**: Star schema design with fact tables (`DAILY_PERFORMANCE`) and dimension tables for analytics layer
- **Custom UDFs**: Python-based user-defined functions for complex volatility calculations and statistical analysis
- **Data Lineage**: End-to-end tracking from source APIs through transformation layers to analytics consumption

---

## Architecture Overview

![Architecture Diagram](assets/Architecture_diagram.png)

The pipeline implements a **modern data engineering architecture** following the **medallion pattern** with sophisticated **stream processing** and **event-driven orchestration**:

### **Data Engineering Architecture Layers**

**Bronze Layer (Raw Data Ingestion)**
```
External APIs → Data Validation → Staging (S3) → Raw Tables
     │              │               │            │
Yahoo Finance → Quality Checks → Data Lake → RAW_CRYPTO Schema
```

**Silver Layer (Data Harmonization)**
```
Raw Data → CDC Streams → Transformations → Harmonized Tables
    │          │             │               │
  Bronze → Change Capture → Business Logic → HARMONIZED_CRYPTO Schema
```

**Gold Layer (Analytics & Aggregation)**
```
Harmonized Data → Analytics Engine → Metrics → Consumption Layer
      │               │              │           │
    Silver → Technical Indicators → KPIs → ANALYTICS_CRYPTO Schema
```

### **Core Data Engineering Components**

**1. Data Ingestion & Validation**
- **API Integration**: Yahoo Finance RESTful data extraction with rate limiting and error handling
- **Data Validation**: Schema validation, data profiling, and quality gates
- **Staging Strategy**: S3 data lake with structured file organization using `damg7245-crypto` bucket
- **Batch Processing**: Scheduled extraction with incremental loading patterns every 4 hours

**2. Stream Processing & CDC**
- **Snowflake Streams**: Real-time change data capture for incremental processing across BTC, ETH, DOGE tables
- **Event-Driven Triggers**: Conditional task execution based on data availability using stream monitoring
- **Change Tracking**: Comprehensive CDC implementation monitoring INSERT, UPDATE, DELETE operations

**3. Data Transformation & Processing**
- **Snowpark DataFrames**: Distributed processing using native Snowflake compute with lazy evaluation
- **Data Harmonization**: Cross-source standardization implemented in `HARMONIZE_CRYPTO_DATA_SP()` stored procedure
- **Business Logic**: Custom UDFs like `CALCULATE_VOLATILITY()` for domain-specific financial calculations
- **Data Quality**: Comprehensive validation and cleansing with duplicate removal using `dropDuplicates()`

**4. Orchestration & Workflow Management**
- **DAG-based Scheduling**: Complex dependency management with Snowflake Tasks in cascading execution
- **Resource Orchestration**: Dynamic warehouse scaling and cost optimization through automated sizing
- **Error Handling**: Comprehensive retry logic and failure recovery with JavaScript stored procedures

---

## Technology Stack

| **Data Engineering Layer** | **Technology** | **Purpose** |
|----------------------------|----------------|-------------|
| **Data Sources** | Yahoo Finance API, RapidAPI | External cryptocurrency market data ingestion |
| **Data Lake** | AWS S3 | Raw data staging and archival storage |
| **Data Warehouse** | Snowflake Data Cloud | Analytical data storage and distributed compute |
| **Processing Engine** | Snowpark Python | Native distributed data processing framework |
| **Stream Processing** | Snowflake Streams | Real-time change data capture and CDC |
| **Orchestration** | Snowflake Tasks | Workflow management and automated scheduling |
| **Development** | Jupyter Notebooks | Interactive data engineering development environment |
| **CI/CD** | GitHub Actions | Infrastructure as code and automated deployment |

---

## Repository Structure

```
Crypto_Analytics_Snowflake_Dataengineering_pipeline_streaming/
├── 📁 notebooks/                   # Data engineering pipeline notebooks
│   ├── 01.Yahoo_Finance_API/       # Data extraction and ingestion layer
│   ├── 02.Load_raw_data_from_csv_files/ # Bronze layer data loading
│   ├── 03.Data_Harmonization/      # Silver layer transformations
│   ├── 04.Data_Analytics/          # Gold layer analytics and aggregations
│   └── 05.Task_Orchestration/      # Workflow orchestration and automation
├── 📁 scripts/                     # Infrastructure and deployment scripts
│   ├── api_call.py                # Automated data extraction pipeline
│   ├── deploy_notebooks.sql       # Infrastructure as code deployment
│   ├── setup.sql                  # Environment provisioning
│   └── teardown.sql               # Resource cleanup and decommissioning
├── 📁 .github/workflows/           # CI/CD automation pipelines
├── 📁 assets/                      # Architecture diagrams and documentation
├── 00_start_here.ipynb            # Data engineering quickstart guide
└── requirements.txt               # Python dependencies
```

---

## Data Engineering Pipeline Components

### **1. Data Ingestion Engine** (`01.Yahoo_Finance_API`)

**Implementation Features:**
- Multi-threaded API integration with connection pooling and exponential backoff
- Comprehensive data validation framework with schema inference and quality profiling
- Time-partitioned batch processing with checkpointing for fault tolerance
- Statistical analysis calculations including returns, volatility, and correlation metrics

The notebook implements sophisticated error handling and data quality validation, ensuring robust data extraction from Yahoo Finance with proper serialization to CSV format for downstream processing.

### **2. Bronze Layer - Raw Data Loading** (`02.Load_raw_data_from_csv_files`)

**Implementation Features:**
- **Snowpark DataFrame API** with distributed processing and lazy evaluation
- **Dynamic warehouse scaling** implemented through automated resource management
- **Schema evolution** with automatic data type detection and conversion
- **Bulk loading optimization** using efficient COPY operations with performance tuning

```python
# Reference: notebooks/02.Load_raw_data_from_csv_files/02.Load_raw_data_from_csv_files.ipynb
def load_raw_table(session, table_name, file_name, schema="RAW_CRYPTO"):
    df = session.read.option("header", True) \
                     .option("infer_schema", True) \
                     .csv(stage_path)
    
    # Convert date string to DATE type and numeric columns to FLOAT
    df = df.with_column(date_col, F.to_date(df[date_col]))
    df.write.mode("overwrite").save_as_table(f"{schema}.{table_name}")
```

### **3. Silver Layer - Data Harmonization** (`03.Data_Harmonization`)

**Implementation Features:**
- **Cross-source data unification** with standardized schema across BTC, ETH, DOGE
- **Advanced data quality framework** with comprehensive validation and cleansing rules
- **Custom UDF development** for complex financial calculations and statistical analysis
- **Change data capture integration** using Snowflake Streams for incremental processing

```python
# Reference: notebooks/03.Data_Harmonization/03.Data_Harmonization.ipynb
def standardize_crypto_df(df, symbol):
    return df.withColumn("crypto_symbol", F.lit(symbol)) \
            .withColumn("date_day", F.to_date(F.col('"date"'))) \
            .withColumn("price_change_24h", F.col('"close"') - F.col('"open"')) \
            .withColumn("price_change_percentage_24h", 
                        (F.col('"close"') - F.col('"open"')) / F.col('"open"') * 100)
```

**Advanced Volatility Calculation UDF:**
```sql
-- Reference: notebooks/03.Data_Harmonization/03.Data_Harmonization.ipynb
CREATE OR REPLACE FUNCTION CRYPTO_DB.HARMONIZED_CRYPTO.CALCULATE_VOLATILITY(prices ARRAY)
RETURNS FLOAT
LANGUAGE PYTHON
RUNTIME_VERSION = '3.8'
HANDLER = 'calculate_volatility'
AS
$$
def calculate_volatility(prices):
    # Calculate daily returns manually
    daily_returns = []
    for i in range(1, len(prices)):
        if prices[i-1] != 0:
            daily_return = (prices[i] - prices[i-1]) / prices[i-1]
            daily_returns.append(daily_return)
    
    # Calculate standard deviation and annualize (252 trading days)
    volatility = std_dev * math.sqrt(252)
    return float(volatility)
$$;
```

### **4. Gold Layer - Analytics Engine** (`04.Data_Analytics`)

**Implementation Features:**
- **Dimensional modeling** with star schema design for analytical workloads
- **Technical indicator calculations** including RSI, moving averages, and volatility metrics
- **Time-series analytics** with complex window functions and statistical analysis
- **Performance optimization** through materialized views and intelligent caching

The analytics layer generates comprehensive cryptocurrency analysis including technical indicators for trading signals (RSI overbought/oversold conditions), moving averages for trend analysis, volatility calculations for risk assessment, and performance benchmarking across multiple time horizons with statistical correlation analysis.

### **5. Orchestration Engine** (`05.Task_Orchestration`)

**Implementation Features:**
- **DAG-based workflow management** with complex dependency chains and conditional execution
- **Event-driven architecture** using stream-based triggers for reactive processing
- **Advanced resource orchestration** with dynamic compute allocation and cost optimization
- **Comprehensive error handling** with retry mechanisms and failure recovery patterns

```sql
-- Reference: notebooks/05.Task_Orchestration/05.Task_Orchestration.ipynb
CREATE OR REPLACE TASK CRYPTO_DB.HARMONIZED_CRYPTO.HARMONIZE_CRYPTO_TASK
    WAREHOUSE = CRYPTO_WH
    AFTER CRYPTO_DB.HARMONIZED_CRYPTO.LOAD_CRYPTO_TASK
    WHEN SYSTEM$STREAM_HAS_DATA('CRYPTO_DB.HARMONIZED_CRYPTO.RAW_CRYPTO_STREAM_BTC')
    OR SYSTEM$STREAM_HAS_DATA('CRYPTO_DB.HARMONIZED_CRYPTO.RAW_CRYPTO_STREAM_ETH')
    OR SYSTEM$STREAM_HAS_DATA('CRYPTO_DB.HARMONIZED_CRYPTO.RAW_CRYPTO_STREAM_DOGE')
AS
CALL CRYPTO_DB.HARMONIZED_CRYPTO.HARMONIZE_CRYPTO_DATA_SP();
```

**JavaScript Stored Procedure for Complex Data Loading:**
```javascript
// Reference: notebooks/05.Task_Orchestration/05.Task_Orchestration.ipynb
CREATE OR REPLACE PROCEDURE CRYPTO_DB.HARMONIZED_CRYPTO.LOAD_CRYPTO_DATA_SP()
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS '
try {
  const CRYPTO_FILES = [
    {file: "BTC_raw_daily.csv", table: "BTC"},
    {file: "ETH_raw_daily.csv", table: "ETH"},
    {file: "DOGE_raw_daily.csv", table: "DOGE"}
  ];
  
  // Process each cryptocurrency with MERGE operations for upsert functionality
  for (const crypto of CRYPTO_FILES) {
    var mergeStmt = snowflake.createStatement({
      sqlText: `MERGE INTO CRYPTO_DB.RAW_CRYPTO.${tableName} target
                USING crypto_temp_${tableName} source
                ON target."date" = source."date"
                WHEN MATCHED THEN UPDATE SET ...
                WHEN NOT MATCHED THEN INSERT ...`
    });
  }
} catch (error) {
  return { status: "error", message: error.message };
}
';
```

---

## Data Architecture & Modeling

### **Bronze Layer (Raw Data Zone)**
```sql
RAW_CRYPTO.{SYMBOL} (
    date DATE PRIMARY KEY,
    open FLOAT, high FLOAT, low FLOAT, close FLOAT,
    volume FLOAT, adjclose FLOAT
);
```

### **Silver Layer (Harmonized Data Zone)**
```sql
HARMONIZED_CRYPTO.CRYPTO_HARMONIZED (
    crypto_symbol VARCHAR(10),
    timestamp TIMESTAMP_NTZ,
    date_day DATE,
    open FLOAT, high FLOAT, low FLOAT, close FLOAT, volume FLOAT,
    adj_close FLOAT,
    price_change_24h FLOAT,
    price_change_percentage_24h FLOAT,
    volatility_7d FLOAT,
    normalized_price FLOAT,
    PRIMARY KEY (crypto_symbol, timestamp)
);
```

### **Gold Layer (Analytics-Optimized Zone)**
```sql
ANALYTICS_CRYPTO.DAILY_PERFORMANCE (
    crypto_symbol VARCHAR(10),
    date_day DATE,
    open_price FLOAT, high_price FLOAT, low_price FLOAT, close_price FLOAT,
    daily_return FLOAT, daily_return_pct FLOAT,
    moving_avg_7d FLOAT, moving_avg_30d FLOAT,
    rsi_14d FLOAT, daily_volatility FLOAT,
    volume_change_pct FLOAT
);
```

---

## Performance Optimization & Monitoring

### **Resource Optimization Implemented**
- **Auto-scaling Compute**: Dynamic warehouse sizing (XSMALL → LARGE → XSMALL) implemented in data loading notebooks
- **Stream-based Processing**: CDC with Snowflake Streams processes only changed data, reducing compute costs
- **Bulk Loading Operations**: Optimized COPY statements with efficient file formats and parallel processing
- **Intelligent Caching**: Snowflake's automatic result caching for repeated analytical queries

### **Performance Monitoring Implementation**
```sql
-- Pipeline execution monitoring implemented in orchestration notebook
SELECT * FROM TABLE(INFORMATION_SCHEMA.TASK_HISTORY(
    SCHEDULED_TIME_RANGE_START => DATEADD('DAY', -1, CURRENT_TIMESTAMP())
)) WHERE DATABASE_NAME = 'CRYPTO_DB' ORDER BY scheduled_time DESC;
```

### **Data Quality Monitoring**
- **Null rate validation** across all pipeline stages with automated quality scoring
- **Duplicate detection** using `dropDuplicates()` in Snowpark transformations
- **Schema validation** with automatic data type inference and conversion
- **Data freshness tracking** monitoring time between data generation and processing

---

## Technical References

### **Data Engineering Documentation**
- **[Data Engineering with Notebooks - Complete Tutorial](https://codelabs-preview.appspot.com/?file_id=1YSeHJtOA5iL07o71Xsk5OWpftGxDQF0aYC6Bi9oy7Ro/#0)** - Comprehensive implementation guide
- [Snowflake Documentation](https://docs.snowflake.com/) - Platform and data engineering documentation
- [Snowpark Python API Reference](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/index.html) - Distributed processing framework
- [Lab 1: Data Engineering Pipelines with Snowpark Python](https://quickstarts.snowflake.com/guide/data_engineering_pipelines_with_snowpark_python/) - Pipeline design patterns
- [Lab 2: Data Engineering with Notebooks](https://quickstarts.snowflake.com/guide/data_engineering_with_notebooks/) - Interactive development workflows

### **API & Integration References**
- [Yahoo Finance API Documentation](https://pypi.org/project/yfinance/) - Financial market data integration
- [RapidAPI - Yahoo Finance](https://rapidapi.com/apidojo/api/yahoo-finance1/) - API integration patterns
- [AWS S3 API Documentation](https://docs.aws.amazon.com/s3/) - Data lake integration

---

<div align="center">

**Advanced Data Engineering Pipeline for Cryptocurrency Analytics**

[⭐ Star this repo](https://github.com/uk1601/Crypto_Analytics_Snowflake_Dataengineering_pipeline_streaming) • [📊 View Architecture](assets/Architecture_diagram.png) • [📚 Complete Tutorial](https://codelabs-preview.appspot.com/?file_id=1YSeHJtOA5iL07o71Xsk5OWpftGxDQF0aYC6Bi9oy7Ro/#0)

</div>
