# AWS Migration

## Local Architecture

```
CSV

↓

PySpark

↓

PostgreSQL

↓

Warehouse
```

---

## AWS Architecture

```
CSV

↓

Amazon S3

↓

AWS Glue

↓

Processed S3

↓

Glue Crawler

↓

Glue Catalog

↓

Athena
```

---

## Services Used

- Amazon S3
- AWS Glue
- Glue Data Catalog
- Athena
- IAM

---

## Migration Changes

| Local | AWS |
|-------|------|
| Local CSV | Amazon S3 |
| SparkSession | GlueContext |
| Local Files | S3 Storage |
| CSV Output | S3 Output |
| Local Execution | Glue Job | 

---

## Benefits

- Serverless
- Auto Scaling
- Managed Spark
- Low Cost
- SQL on S3
- Easy Monitoring