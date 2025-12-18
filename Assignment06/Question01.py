import streamlit as st
import time
import os
import requests
from dotenv import load_dotenv
from groq import Groq
from datetime import datetime

st.set_page_config(page_title="Multi-LLM Chatbot", page_icon="💬", layout="wide")

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("GROQ_API_KEY missing in .env")
    st.stop()

groq_client = Groq(api_key=GROQ_API_KEY)
LM_STUDIO_URL = "http://127.0.0.1:1234/v1/chat/completions"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "model_choice" not in st.session_state:
    st.session_state.model_choice = "Groq"

with st.sidebar:
    st.title("⚙️ Settings")

    st.session_state.model_choice = st.radio(
        "Choose Model",
        ["Groq", "LM Studio"]
    )

    if st.button("➕ New Chat"):
        st.session_state.messages = []
        st.rerun()

st.title("💬 Multi-LLM Chatbot")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

def groq_stream(messages):
    stream = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        stream=True
    )
    full_response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            full_response += content
            yield content
            time.sleep(0.02)
    return full_response

def lm_studio_call(messages):
    payload = {
        "model": "local-model",  
        "messages": messages,
        "temperature": 0.7
    }

    response = requests.post(LM_STUDIO_URL, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

user_input = st.chat_input("Ask something...")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        if st.session_state.model_choice == "Groq":
            full_reply = st.write_stream(groq_stream(st.session_state.messages))
        else:
            full_reply = lm_studio_call(st.session_state.messages)
            st.markdown(full_reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": full_reply
    })
    st.rerun()
