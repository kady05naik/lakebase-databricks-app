# Lakebase Todo App

A simple Todo application built with Streamlit and deployed as a Databricks App, backed by **Lakebase Autoscaling** — Databricks' fully managed, PostgreSQL-compatible operational database built directly into the Data Intelligence Platform.

## What this demonstrates

Most of my Databricks experience is on the analytical (OLAP) side — Delta Lake, Medallion pipelines, Gold-layer datasets feeding BI reports. This project is a hands-on introduction to the operational (OLTP) side: a real PostgreSQL database living inside the same governed platform, with runtime authentication, connection pooling, and standard CRUD operations.

Specifically, the app covers:

- **Endpoint discovery** — locating the Lakebase host at runtime via the Databricks SDK, rather than a static connection string
- **OAuth token management** — generating and refreshing scoped database credentials before they expire, with a safety margin
- **Connection pooling** — reusing a small pool of live Postgres connections instead of opening a new one per request
- **Safe SQL** — using `psycopg.sql.Identifier()` for object names and parameterized `%s` placeholders for user input, to prevent SQL injection
- **A layered app structure** — configuration, connection handling, schema setup, CRUD logic, and UI kept in separate modules

## Architecture

```
app-source-code/
├── db/
│   ├── __init__.py     Package exports
│   ├── connection.py   Endpoint discovery, token management, connection pool
│   ├── crud.py         CRUD operations: add, get, toggle, delete
│   └── schema.py       Schema and table setup
├── app.py              Main entry point
├── app.yaml             App configuration
├── config.py            Configuration and workspace client
└── requirements.txt     Python dependencies
```

## Tech stack

Python · Streamlit · Databricks SDK · Lakebase (PostgreSQL) · psycopg / psycopg_pool

## Origin

Built as part of a hands-on Databricks training exercise (Databricks EMEA Festival, Lakebase bonus lab). The application code and structure in this repository are my own implementation, written and deployed by me.

## About me

Azure Data Engineer with 3+ years building ETL/ELT pipelines and Medallion Lakehouse architectures on Azure Data Factory, Databricks, and Delta Lake.

📫 [LinkedIn](https://linkedin.com/in/kadambari-naik) · [GitHub](https://github.com/kady05naik)
