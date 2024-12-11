# Real-Time SQL Database Q&A

This project allows users to interact with an SQLite database (Chinook) in real-time via a natural language interface using Streamlit. It leverages a machine learning agent to convert user queries into SQL commands and execute them on the database.

## Features
- Real-time natural language to SQL query conversion
- User-friendly interface with Streamlit
- Provides the executed SQL query and intermediate steps
- Handles different SQL operations, such as selecting, counting, and filtering data

## Requirements
- Python 3.7 or later
- Streamlit
- LangChain
- Google Generative AI
- FAISS
- SQLite
- Other necessary dependencies specified in `requirements.txt`

## Setup

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/sql-query-agent.git
    cd sql-query-agent
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up environment variables:
    - Create a `.env` file in the root directory and add the following:
    ```bash
    GROQ_API_KEY=your_groq_api_key
    ```

4. Ensure you have the SQLite database (`chinook.db`) in the project directory.

## Running the Application

1. Run the Streamlit app:
    ```bash
    streamlit run main.py
    ```

2. Open the application in your browser:
    - The default URL will be: `http://localhost:8501`

## How to Use

- Enter an SQL query or a natural language question (e.g., "List all artists") in the input box.
- The application will process the query and display the result along with the executed SQL queries.

## Example Queries
- "List all artists"
- "Find all albums for the artist 'AC/DC'"
- "How many employees are there?"
- "Find the total duration of all tracks"

## Files Overview

- `main.py`: Main Streamlit app that handles user input and displays results.
- `agent_setup.py`: Initializes the agent and sets up the connection to the database.
- `query_handler.py`: Processes the user query and interacts with the agent to fetch results.

## License

This project is licensed under the MIT License.

