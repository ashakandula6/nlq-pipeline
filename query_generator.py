from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()

def clean_sql_query(query_str):
    query_str = re.sub(r'```sql\s*', '', query_str, flags=re.IGNORECASE)
    query_str = re.sub(r'```', '', query_str)
    query_str = re.sub(r'^\s*sql\s+', '', query_str, flags=re.IGNORECASE)
    query_str = re.sub(r'^.*?(SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP)\b', r'\1', query_str, flags=re.IGNORECASE)
    query_str = query_str.strip()
    if not query_str.endswith(';'):
        query_str += ';'
    return query_str

def generate_query(nl_query, schema, db_type):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=os.getenv("GOOGLE_API_KEY"))
    
    schema_str = "\n".join([f"Table/Collection: {table}\nColumns/Fields: {cols}" for table, cols in schema.items()])
    
    if db_type in ['postgresql', 'mariadb']:
        prompt_template = PromptTemplate(
            input_variables=["schema", "query"],
            template="Given the schema:\n{schema}\nGenerate an SQL query for the following natural language query:\n{query}\nReturn only the SQL query as a string, without any Markdown formatting or additional text. For example, return 'SELECT * FROM customers;' directly."
        )
    else:  # mongodb
        prompt_template = PromptTemplate(
            input_variables=["schema", "query"],
            template="Given the schema:\n{schema}\nGenerate a MongoDB query for the following natural language query:\n{query}\nReturn the query as a JSON string in the format {{\"collection\": \"<collection_name>\", \"filter\": {{<filter_conditions>}}}}. For example, to find all customers, return {{\"collection\": \"customers\", \"filter\": {{}}}}. Ensure the output is a valid JSON string without any Markdown formatting or additional text."
        )

    prompt = prompt_template.format(schema=schema_str, query=nl_query)
    response = llm.invoke(prompt)
    generated_query = response.content.strip()

    if db_type in ['postgresql', 'mariadb']:
        generated_query = clean_sql_query(generated_query)
    elif db_type == 'mongodb':
        try:
            json.loads(generated_query)
        except json.JSONDecodeError:
            generated_query = '{"collection": "customers", "filter": {}}'
    
    return generated_query