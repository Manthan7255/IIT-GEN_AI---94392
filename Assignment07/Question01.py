import streamlit as st
import pandas as pd
from pandasql import sqldf
from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio" 
)

st.set_page_config(page_title="CSV Chat with SQL", layout="wide")
st.title("📊 CSV → SQL → Explanation")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("CSV loaded successfully")

    st.subheader("📌 Table Schema")
    schema_df = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str)
    })
    st.table(schema_df)

    st.subheader("👀 Data Preview")
    st.dataframe(df.head())

    user_question = st.text_input("Ask a question about the data (in English):")

    if user_question:
        sql_prompt = f"""
You are an expert SQL generator.

The table name is: products

Table schema:
{schema_df.to_string(index=False)}

User question:
{user_question}

Rules:
- Generate ONLY a valid SQLite SQL query
- Do NOT add explanations
- Do NOT use markdown
- Do NOT add semicolon
"""

        sql_response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": "You convert English questions into SQL queries."},
                {"role": "user", "content": sql_prompt}
            ],
            temperature=0
        )

        sql_query = sql_response.choices[0].message.content.strip()

        st.subheader("🧠 Generated SQL")
        st.code(sql_query, language="sql")

       
        try:
            result_df = sqldf(sql_query, {"products": df})

            st.subheader("📈 Query Result")
            st.dataframe(result_df)
            
            explain_prompt = f"""
User question:
{user_question}

SQL query:
{sql_query}

Query result:
{result_df.to_string(index=False)}

Explain the result in very simple English.
"""

            explanation = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {"role": "system", "content": "Explain data results in simple English."},
                    {"role": "user", "content": explain_prompt}
                ],
                temperature=0.3
            )

            st.subheader("📝 Explanation")
            st.write(explanation.choices[0].message.content)

        except Exception as e:
            st.error("SQL execution failed")
            st.code(str(e))
