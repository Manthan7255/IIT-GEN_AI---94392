import streamlit as st
import pandas as pd
from pandasql import sqldf

st.set_page_config(page_title="CSV SQL Runner", layout="wide")
st.title("Run SQL on Uploaded CSV")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    # Read CSV into DataFrame
    df = pd.read_csv(uploaded_file)

    st.subheader("Preview of data")
    st.dataframe(df)

    st.subheader("Enter SQL query")
    default_query = "SELECT * FROM df LIMIT 5;"
    query = st.text_area("SQL query (use table name: df)", value=default_query, height=150)

    if st.button("Run query"):
        if query.strip():
            try:
                # sqldf can access df because it’s in the local/global namespace
                result = sqldf(query, {"df": df})
                st.subheader("Query result")
                st.dataframe(result)
            except Exception as e:
                st.error(f"Error executing query: {e}")
        else:
            st.warning("Please enter a SQL query.")
else:
    st.info("Please upload a CSV file to begin.")
