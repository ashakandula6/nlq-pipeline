import streamlit as st
from schema_detector import get_postgres_schema, get_mariadb_schema, get_mongodb_schema, generate_schema_description
from db_connectors import execute_postgres_query, execute_mariadb_query, execute_mongodb_query
from query_generator import generate_query
import json

st.title("NLQ Pipeline with Multiple Databases")

# Database selection
db_type = st.selectbox("Select Database", ["PostgreSQL", "MariaDB", "MongoDB"])

# Database parameters
if db_type == "PostgreSQL":
    db_config = {
        "dbname": "sample",
        "user": "postgres",
        "password": "Ashapavani@97",
        "host": "localhost",
        "port": "5432"
    }
elif db_type == "MariaDB":
    db_config = {
        "database": "sample",
        "user": "root",
        "password": "Ashapavani@97",
        "host": "localhost",
        "port": 3306
    }
else:  # MongoDB
    db_config = {"db_name": "sample"}

# Get schema
try:
    if db_type == "PostgreSQL":
        schema = get_postgres_schema(db_config)
    elif db_type == "MariaDB":
        schema = get_mariadb_schema(db_config)
    else:
        schema = get_mongodb_schema(db_config["db_name"])
except Exception as e:
    st.error(f"Error retrieving schema: {str(e)}")
    st.stop()

# Display schema
st.subheader("Database Schema")
schema_desc = generate_schema_description(schema)
st.write(schema_desc)

# Natural language query input
nl_query = st.text_input("Enter your query in natural language (e.g., 'Show all customers')", key="nl_query_input")

if st.button("Execute Query"):
    if nl_query:
        # Clear previous results
        st.session_state.pop("query_result", None)
        
        # Generate query
        generated_query = generate_query(nl_query, schema, db_type.lower())
        st.write(f"Generated Query: {generated_query}")
        
        # Execute query
        try:
            if db_type == "PostgreSQL":
                result = execute_postgres_query(db_config, generated_query)
            elif db_type == "MariaDB":
                result = execute_mariadb_query(db_config, generated_query)
            else:  # MongoDB
                try:
                    generated_query_dict = json.loads(generated_query)
                except json.JSONDecodeError as e:
                    st.error(f"Invalid MongoDB query format: {generated_query}. Error: {str(e)}")
                    st.stop()
                result = execute_mongodb_query(db_config["db_name"], generated_query_dict)
            
            st.session_state.query_result = result
        except Exception as e:
            st.error(f"Error executing query: {str(e)}")
    else:
        st.warning("Please enter a query.")

# Display result
if "query_result" in st.session_state:
    st.subheader("Query Result")
    st.dataframe(st.session_state.query_result)