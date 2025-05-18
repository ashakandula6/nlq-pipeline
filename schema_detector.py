import psycopg2
from pymongo import MongoClient
import mysql.connector
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

def get_postgres_schema(db_params):
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = 'public';
    """)
    rows = cursor.fetchall()
    schema = {}
    for table_name, column_name, data_type in rows:
        if table_name not in schema:
            schema[table_name] = []
        schema[table_name].append((column_name, data_type))
    conn.close()
    return schema

def get_mariadb_schema(db_params):
    conn = mysql.connector.connect(**db_params)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = DATABASE();
    """)
    rows = cursor.fetchall()
    schema = {}
    for table_name, column_name, data_type in rows:
        if table_name not in schema:
            schema[table_name] = []
        schema[table_name].append((column_name, data_type))
    conn.close()
    return schema

def get_mongodb_schema(db_name):
    client = MongoClient('mongodb://localhost:27017/')
    db = client[db_name]
    schema = {}
    for collection_name in db.list_collection_names():
        collection = db[collection_name]
        sample_doc = collection.find_one()
        if sample_doc:
            schema[collection_name] = [(k, type(v).__name__) for k, v in sample_doc.items() if k != '_id']
    client.close()
    return schema

def generate_schema_description(schema):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=os.getenv("GOOGLE_API_KEY"))
    schema_str = "\n".join([f"Table/Collection: {table}\nColumns/Fields: {cols}" for table, cols in schema.items()])
    prompt = f"Describe the following database schema in natural language:\n{schema_str}"
    response = llm.invoke(prompt)
    return response.content