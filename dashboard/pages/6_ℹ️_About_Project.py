import streamlit as st

st.set_page_config(
    page_title="About Project",
    page_icon="ℹ️",
    layout="wide"
)

st.title("ℹ️ About Crypto Intelligence Platform")

st.markdown("""
## Overview

Crypto Intelligence Platform is an end-to-end Data Engineering project that ingests
live cryptocurrency market data from the CoinGecko API, processes it using Apache Spark,
stores it in a Bronze-Silver-Gold Lakehouse architecture on Amazon S3, catalogs the
datasets with AWS Glue, queries them through Amazon Athena, and visualizes insights
using Streamlit.

---

## Technology Stack

- Python
- Apache Airflow
- Apache Spark
- Docker
- Amazon S3
- AWS Glue
- Amazon Athena
- Streamlit
- Plotly
- Pandas
- PyArrow

---

## Data Pipeline

CoinGecko API

↓

Bronze Layer (Raw JSON)

↓

Silver Layer (Validated & Partitioned Parquet)

↓

Gold Layer (Analytics Tables)

↓

AWS Glue Catalog

↓

Amazon Athena

↓

Interactive Dashboard

---

## Key Features

✅ Automated hourly ingestion

✅ Bronze / Silver / Gold architecture

✅ Idempotent processing

✅ Historical data storage

✅ Interactive analytics dashboard

✅ Data quality validation

✅ AWS cloud-native data lake

---

## Author

Om Kapkoti

B.Tech Mathematics & Data Science

MANIT Bhopal
""")