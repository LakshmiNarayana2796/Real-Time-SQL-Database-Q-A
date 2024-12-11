
import streamlit as st
from agent_setup import initialize_agent
from query_handler import process_query

# Streamlit Title
st.title("Real-Time SQL Database Q&A")

# Initialize Agent
agent_executor = initialize_agent()

# User Input via Streamlit
query = st.text_input("Enter your SQL query:")
if query:
    with st.spinner("Processing your query..."):
        try:
            result, queries = process_query(agent_executor, query)
            st.write(result)
            st.write(queries)
        except Exception as e:
            st.error(f"Query execution failed: {e}")