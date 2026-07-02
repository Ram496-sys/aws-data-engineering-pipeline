# 🚀 Enterprise Data Engineering Pipeline

A production-style **Data Engineering Project** built using **PySpark, PostgreSQL, AWS Glue, Amazon S3, Glue Data Catalog, and Athena**.

This project demonstrates how raw customer data is ingested, validated, transformed, and loaded into a warehouse using both **local** and **AWS cloud** architectures.

---

# 📌 Project Architecture

```
                 Source System
                      │
                      ▼
              customers.csv
                      │
                      ▼
               Amazon S3 (Raw)
                      │
                      ▼
              AWS Glue (PySpark)
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
  Processed Data              Rejected Data
        │                           │
        ▼                           ▼
 Amazon S3                    Amazon S3
        │
        ▼
 Glue Crawler
        │
        ▼
 Glue Data Catalog
        │
        ▼
 Athena SQL
```

---

# 🛠 Tech Stack

- Python
- PySpark
- PostgreSQL
- AWS Glue
- Amazon S3
- AWS IAM
- AWS Glue Data Catalog
- Amazon Athena
- Git
- GitHub

---

# 📂 Project Structure

```
enterprise-data-engineering-project

├── config/
├── data/
│   ├── raw/
│   ├── processed/
│   └── rejected/
│
├── docs/
│
├── drivers/
│
├── glue_jobs/
│   └── customer_etl.py
│
├── loaders/
├── readers/
├── scripts/
├── sql/
├── tests/
├── transformers/
├── utils/
├── validators/
│
├── README.md
```

---

# ✅ Features

- Generate synthetic customer data
- Modular PySpark ETL pipeline
- Data validation
    - Null Validation
    - Email Validation
    - Phone Validation
    - State Validation
    - Duplicate Validation
- Customer Transformation
- Incremental Processing
- Watermark Handling
- Audit Logging
- PostgreSQL Loading
- AWS Glue Migration
- Amazon S3 Data Lake
- Glue Crawler
- Glue Data Catalog
- Athena Query Engine

---

# ☁ AWS Services Used

- Amazon S3
- AWS Glue
- AWS IAM
- Glue Data Catalog
- Amazon Athena

---

# 📊 ETL Flow

```
CSV
 │
 ▼
Read
 │
 ▼
Validate
 │
 ▼
Transform
 │
 ▼
Processed
 │
 ▼
AWS S3
 │
 ▼
Glue Catalog
 │
 ▼
Athena
```

---

# ▶ How to Run (Local)

```bash
python scripts/generate_customers.py
```

```bash
python glue_jobs/customer_etl.py
```

---

# ☁ AWS Workflow

1. Upload CSV to Amazon S3
2. Execute AWS Glue Job
3. Write processed data back to S3
4. Run Glue Crawler
5. Query using Athena

---

# 📚 Skills Demonstrated

- Data Engineering
- ETL Development
- PySpark
- AWS Glue
- Amazon S3
- Athena
- SQL
- PostgreSQL
- Data Validation
- Incremental Loading
- Git Workflow

---

# 📈 Future Improvements

- AWS Step Functions
- Amazon RDS PostgreSQL
- CloudWatch Monitoring
- Secrets Manager
- CI/CD Pipeline
- Delta Lake
- Apache Iceberg

---

# 👨‍💻 Author

Ram

Enterprise Data Engineering Project