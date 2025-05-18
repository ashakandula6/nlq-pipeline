# Natural Language Query (NLQ) Pipeline

A Streamlit-based chatbot that enables natural language queries across PostgreSQL, MongoDB, and MariaDB databases, leveraging Gemini Flash LLM for query generation and schema automation.

## 📖 Overview
This project allows users to query databases using natural language (e.g., “Show me sales data from 2024”). It dynamically extracts database schemas using `schema_detector.py`, connects to databases with `db_connectors.py`, and generates queries via `query_generator.py`, improving accessibility for non-technical users.

## 🛠️ Features
- Natural language query interface via Streamlit (`app.py`).
- Supports PostgreSQL, MongoDB, and MariaDB.
- Schema automation for dynamic query generation.
- Powered by Gemini Flash LLM and Google Generative AI API.

## 📁 Project Structure

nlq-pipeline/
├── app.py               # Main Streamlit app
├── db_connectors.py     # Database connection logic
├── query_generator.py   # Query generation using Gemini Flash LLM
├── schema_detector.py   # Schema extraction logic
├── requirements.txt     # Dependencies
├── sample_data/         # Sample database setup scripts
│   ├── mariadb_setup.sql
│   ├── mongodb_setup.js
│   ├── postgres_setup.sql
└── .gitignore           # Excludes pycache, venv, .env
