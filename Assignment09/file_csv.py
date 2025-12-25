import pandas as pd
import pandasql as ps
import os
from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI


def csv_question(csv_file, question):

    if csv_file is None:
        return "Please upload a CSV file."

    if question is None or question.strip() == "":
        return "Please enter a question."

    csv_file.seek(0)
    df = pd.read_csv(csv_file)
    df.columns = df.columns.str.lower()   

    llm_sql = init_chat_model(
        model="llama-3.3-70b-versatile",
        model_provider="openai",
        base_url="https://api.groq.com/openai/v1",
        api_key=os.getenv("groq_api")
    )

    llm_input = f"""
    Table Name: data
    Table Schema: {df.dtypes}
    Question: {question}
    Instruction:
        Write a SQL query for the above question.
        Generate SQL query only in plain text format and nothing else.
        If you cannot generate the query, then output 'Error'.
    """

    result = llm_sql.invoke(llm_input)
    query = result.content.strip()

    if query.lower() == "error":
        return "Could not generate a valid SQL query for this question."

    try:
        ans = ps.sqldf(query, {"data": df})
    except Exception as e:
        return f"Error executing SQL: {e}"

    llm_summary = ChatOpenAI(
        base_url="http://127.0.0.1:1234/v1",
        model="google/gemma-3n-e4b",
        api_key="dummy_api"
    )

    summary_prompt = (
        f"Give a short English summary.\n"
        f"Question: {question}\n"
        f"Answer:\n{ans.to_string(index=False)}"
    )

    summary_text = ""
    for chunk in llm_summary.stream(summary_prompt):
        if chunk.content:
            summary_text += chunk.content
    # with open(file_name,"a")as f:
    #     f.write(summary_text)
    return summary_text



            
def info_csv(csv_file):
    if csv_file is not None:
        csv_file.seek(0)
        df = pd.read_csv(csv_file)
        return df.head(), df.dtypes
    return None, None

    
    
if __name__ == "__main__":
    file = input("upload file : ")
    question = input("enter question : ")
    print(info_csv(file))
    print(csv_question(file, question))

    
    
    
    