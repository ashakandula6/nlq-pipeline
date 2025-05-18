import psycopg2
from pymongo import MongoClient
import mysql.connector
import pandas as pd
from bson.objectid import ObjectId

def execute_postgres_query(db_params, query):
    conn = psycopg2.connect(**db_params)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def execute_mariadb_query(db_params, query):
    conn = mysql.connector.connect(**db_params)
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def execute_mongodb_query(db_name, query):
    client = MongoClient('mongodb://localhost:27017/')
    db = client[db_name]
    collection = db[query['collection']]
    results = collection.find(query.get('filter', {}))
    results_list = []
    for doc in results:
        doc['_id'] = str(doc['_id'])
        results_list.append(doc)
    df = pd.DataFrame(results_list)
    client.close()
    return df