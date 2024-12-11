import os
from langchain_groq import ChatGroq
from langchain.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_community.tools.sql_database.tool import (
    QuerySQLDataBaseTool, InfoSQLDatabaseTool, ListSQLDatabaseTool, QuerySQLCheckerTool
)
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate, ChatPromptTemplate
from langchain_core.prompts import SystemMessagePromptTemplate
from langchain.agents import AgentExecutor, AgentType
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment variable setup
groq_api_key = os.getenv("GROQ_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

def initialize_agent():
    try:
        # Load environment variables
        groq_api_key = os.getenv("GROQ_API_KEY")
        llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")

        # Connect to the database
        db = SQLDatabase.from_uri("sqlite:///chinook.db", sample_rows_in_table_info=3)

        # Define example queries
        examples = [
            {"input": "List all artists.", "query": "SELECT * FROM Artist;"},
            {"input": "Find all albums for the artist 'AC/DC'.",
             "query": "SELECT * FROM Album WHERE ArtistId = (SELECT ArtistId FROM Artist WHERE Name = 'AC/DC');"},
            {"input": "List all tracks in the 'Rock' genre.",
             "query": "SELECT * FROM Track WHERE GenreId = (SELECT GenreId FROM Genre WHERE Name = 'Rock');"},
            {"input": "Find the total duration of all tracks.",
             "query": "SELECT SUM(Milliseconds) FROM Track;"},
            {"input": "List all customers from Canada.",
             "query": "SELECT * FROM Customer WHERE Country = 'Canada';"},
            {"input": "How many tracks are there in the album with ID 5?",
             "query": "SELECT COUNT(*) FROM Track WHERE AlbumId = 5;"},
            {"input": "Find the total number of Albums.",
             "query": "SELECT COUNT(DISTINT(AlbumId)) FROM Invoice;"},
            {"input": "List all tracks that are longer than 5 minutes.",
             "query": "SELECT * FROM Track WHERE Milliseconds > 300000;"},
            {"input": "Who are the top 5 customers by total purchase?",
             "query": "SELECT CustomerId, SUM(Total) AS TotalPurchase FROM Invoice GROUP BY CustomerId ORDER BY TotalPurchase DESC LIMIT 5;"},
            {"input": "How many employees are there",
             "query": "SELECT COUNT(*) FROM \"Employee\""},
        ]

        # Initialize embeddings and example selector
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        example_selector = SemanticSimilarityExampleSelector.from_examples(
            examples, embeddings, FAISS, k=3, input_keys=["input"])

        # Define tools for the SQL Agent
        sql_db_query = QuerySQLDataBaseTool(db=db)
        sql_db_schema = InfoSQLDatabaseTool(db=db)
        sql_db_list_tables = ListSQLDatabaseTool(db=db)
        sql_db_query_checker = QuerySQLCheckerTool(db=db, llm=llm)
        tools = [sql_db_query, sql_db_schema, sql_db_list_tables, sql_db_query_checker]

        # Define the prompt template
        system_prefix = """
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
Thought: I now know the final answer
Final Answer: the final answer to the original input question
"""

        suffix = """
Begin!
Question: {input}
Thought:{agent_scratchpad}
"""

        dynamic_few_shot_prompt_template = FewShotPromptTemplate(
            example_selector=example_selector,
            example_prompt=PromptTemplate.from_template("User input: {input}\nSQL query: {query}"),
            input_variables=["input"],
            prefix=system_prefix,
            suffix=suffix,
        )

        full_prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate(prompt=dynamic_few_shot_prompt_template),
        ])

        # Create and return the agent executor
        agent_executor = create_sql_agent(
            llm,
            db=db,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            prompt=full_prompt,
            extra_tools=tools,
            verbose=True,
            max_iterations=10,
            max_execution_time=90,
            handle_parsing_errors=True,
            agent_executor_kwargs={"return_intermediate_steps": True},
        )
        return agent_executor
    except Exception as e:
        raise RuntimeError(f"Initialization failed: {e}")

