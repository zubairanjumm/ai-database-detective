# AI Database Detective

AI Database Detective is a database investigation system that takes a business question, investigates a SQL database, runs multiple queries, analyzes the results, and produces an evidence-backed investigation report.

## What It Does

A user can ask a question such as:

> What is the total revenue for each order status?

The system:

1. Inspects the database schema.
2. Generates an SQL query.
3. Validates the SQL query.
4. Executes the query safely.
5. Analyzes the returned data.
6. Determines whether more evidence is needed.
7. Generates a follow-up query.
8. Executes the follow-up query.
9. Produces a final investigation report.
10. Exposes the investigation through a FastAPI endpoint.

## Architecture

```text
Business Question
       ↓
     FastAPI
       ↓
    LangGraph
       ↓
 Schema Inspection
       ↓
   SQL Generator
       ↓
   SQL Validator
       ↓
 Database Execution
       ↓
 Result Analyzer
       ↓
 Follow-up Investigation
       ↓
 Report Generator
       ↓
     JSON API
```

## Tech Stack

* Python
* FastAPI
* LangGraph
* SQLAlchemy
* SQLite
* PostgreSQL support
* Pandas
* Pydantic
* Pytest

## Project Structure

```text
ai-database-detective/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── schema_inspector.py
│   ├── models.py
│   ├── sql_generator.py
│   ├── sql_validator.py
│   ├── tools.py
│   ├── investigator.py
│   ├── graph.py
│   ├── analyzer.py
│   └── report.py
├── tests/
├── samples/
│   ├── business.db
│   └── create_database.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

Install the dependencies:

```powershell
uv sync
```

Create the sample database if needed:

```powershell
uv run python samples/create_database.py
```

## Run Tests

```powershell
uv run pytest
```

## Run the API

```powershell
uv run uvicorn app.main:app --reload
```

Open the API documentation:

```text
http://127.0.0.1:8000/docs
```

## Example Request

```json
{
  "question": "What is the total revenue for each order status?"
}
```

## Example Investigation

The sample database contains customers and orders.

The investigation can discover evidence such as:

* Cancelled orders: 1 order generating $90.00.
* Completed orders: 9 orders generating $3130.00.

The final report also includes the SQL queries and raw database results used as evidence.

## Database Support

The database layer uses SQLAlchemy, allowing the project to work with SQLite and providing support for PostgreSQL database connections.

The sample project currently uses SQLite so it can run locally without an external database server.

## Current Limitations

The current SQL generator uses deterministic rules for the sample investigation scenarios rather than a live language model.

The SQL validator currently focuses on preventing non-SELECT operations and should be hardened further before exposing the system to untrusted production databases.

The report interpretation is currently designed around the fields available in the sample investigation.

## Purpose

This project demonstrates how database tools, SQL generation, validation, iterative investigation, LangGraph workflows, and structured reporting can be combined into a database investigation system.
