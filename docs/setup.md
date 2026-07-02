# Project Setup Guide

## Prerequisites

- Python 3.11+
- Java 17+
- PostgreSQL 17+
- Git
- AWS Account
- AWS CLI (Optional)

---

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/aws-data-engineering-pipeline.git
```

---

## Create Virtual Environment

```bash
python -m venv .venv
```

Activate

Windows

```bash
.venv\Scripts\activate
```

Install Packages

```bash
pip install -r requirements.txt
```

---

## PostgreSQL

Create Database

```sql
CREATE DATABASE enterprise_sales_db;
```

Execute all SQL files inside

```
sql/migrations
```

---

## Generate Sample Data

```bash
python scripts/generate_customers.py
```

---

## Run Local ETL

```bash
python glue_jobs/customer_etl.py
```

---

## AWS Setup

Create

- S3 Bucket
- IAM Role
- Glue Job
- Glue Crawler
- Athena Database

Upload

```
customers.csv
```

Run Glue Job

Run Glue Crawler

Query using Athena.

---

Project is ready.