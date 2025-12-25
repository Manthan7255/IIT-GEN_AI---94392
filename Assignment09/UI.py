from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
import pandas as pd
from pandasql import sqldf
from selenium import webdriver
from selenium.webdriver.common.by import By
import streamlit as st 
import time

llm = init_chat_model(
    model="google/gemma-3-4b",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="non-needed"
)

@tool
def csv_query_tool(question, csv_path):
    """
    Accepts a CSV file path and a user question.
    Converts question to SQL using LLM, executes on CSV using pandasql, 
    and returns result with explanation.
    """
    df = pd.read_csv(csv_path)
    schema = ", ".join([f"{col} ({dtype})" for col, dtype in zip(df.columns, df.dtypes)])

    sql_prompt = f"""
    You are an expert SQL developer.
    Table: df
    Schema: {schema}
    Convert the following user question into SQL:
    {question}
    Return only the SQL query.
    """

    sql_query = llm.invoke(sql_prompt).content.strip()

    try:
        result_df = sqldf(sql_query, {"df": df})
    except Exception as e:
        return f"SQL Error: {e}"

    # Explanation prompt
    explain_prompt = f"""
    You are a data analyst.
    Question: {question}
    SQL Query: {sql_query}
    Result: {result_df.to_string(index=False)}
    Explain the result in simple English.
    """

    explanation = llm.invoke(explain_prompt).content
    return explanation

# -------------------------
# Tool 2: Internship Selenium Agent
# -------------------------
@tool
def internship_tool(question):
    """
    Scrapes Sunbeam internship data using Selenium,
    answers user's question strictly based on scraped data.
    """
    url = "https://sunbeaminfo.in/internship"
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)

    internship_data = []
    rows = driver.find_elements(By.XPATH, '//div//table//tbody//tr')
    for row in rows:
        cols = row.find_elements(By.XPATH, './/td')
        if len(cols) >= 7:
            internship_data.append({
                "Batch": cols[1].text.strip(),
                "Batch_Duration": cols[2].text.strip(),
                "Start_Date": cols[3].text.strip(),
                "End_Date": cols[4].text.strip(),
                "Time": cols[5].text.strip(),
                "Fees_INR": cols[6].text.strip()
            })
    driver.quit()

    df = pd.DataFrame(internship_data)

    # LLM prompt to answer question based on DataFrame
    context = df.to_string(index=False)
    prompt = f"""
    You are an AI assistant.
    Answer the user's question strictly using the internship data below.
    Do not make assumptions outside the data.

    Internship Data:
    {context}

    Question:
    {question}

    Explain the answer in simple English.
    """

    response = llm.invoke(prompt)
    return response.content

# -------------------------
# Create the agent with both tools
# -------------------------
agent = create_agent(
    model=llm,
    tools=[csv_query_tool, internship_tool],
    system_prompt="You are a helpful assistant. Use the appropriate tool to answer questions."
)

# -------------------------
# Run interactive loop
# -------------------------
def info_csv(csv_file):
    if csv_file is not None:
        df = pd.read_csv(csv_file)
        return df.head(), df.dtypes
    return None, None



#------------UI------------
with st.sidebar:
    choice=["CSV-QNA","Scrapping"]
    option=st.selectbox("select for best output",choice)
st.title("Chat bot ")
st.write("Best for data scrapping and CSV-QNA.")

if option == "CSV-QNA":
    csv_path = st.text_input("enter file path..")

    if csv_path:
        head, types = info_csv(csv_path)
        st.dataframe(head)
        st.code(types)

        user_input = st.chat_input("Enter question.")

        if user_input:
            with st.spinner("Generating..."):
                result = agent.invoke({
                    "messages": [
                        {"role": "user", "content": f"{user_input}\nCSV_PATH={csv_path}"}
                    ]
                })
                
                llm_output = result["messages"][-1]
            st.write("AI:", llm_output.content)

else:
    user_input = st.chat_input("ask scrapping question...")

    if user_input:
        with st.spinner("Generating..."):
            result = agent.invoke({
                "messages": [
                    {"role": "user", "content": user_input}
                ]
            })
            
            llm_output = result["messages"][-1]
        st.write("AI:", llm_output.content)