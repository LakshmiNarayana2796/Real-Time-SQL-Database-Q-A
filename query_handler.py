def process_query(agent_executor, query):
    result = agent_executor.invoke({"input": query})
    queries = []
    for (log, output) in result["intermediate_steps"]:
        if log.tool == 'sql_db_query':
            queries.append(log.tool_input)
    return result, queries