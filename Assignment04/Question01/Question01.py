import streamlit as st
import time
import os
from dotenv import load_dotenv
from groq import Groq
from datetime import datetime

st.set_page_config(
    page_title="Manthan's Chatbot",
    page_icon="💬",
    layout="wide"
)

st.markdown("""
<style>
    body {
        background-color: #ffffff;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #1e1e2f;
    }

    section[data-testid="stSidebar"] * {
        color: #ffffff;
    }

    /* Chat message bubble */
    .stChatMessage {
        padding: 12px;
        border-radius: 12px;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        width: 100%;
    }

    /* Input box */
    textarea {
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ API key not found. Check your .env file.")
    st.stop()

client = Groq(api_key=api_key)

if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat" not in st.session_state:
    chat_id = datetime.now().strftime("%Y%m%d%H%M%S")
    st.session_state.current_chat = chat_id
    st.session_state.chats[chat_id] = []

with st.sidebar:
    st.title("💬 Manthan's Chatbot")

    if st.button("➕ New Chat"):
        chat_id = datetime.now().strftime("%Y%m%d%H%M%S")
        st.session_state.current_chat = chat_id
        st.session_state.chats[chat_id] = []
        st.rerun()

    st.divider()

    st.subheader("📂 Your Chats")
    search = st.text_input("🔍 Search chats")

    for cid, msgs in st.session_state.chats.items():
        preview = msgs[0]["content"][:30] + "..." if msgs else "New Chat"
        if search.lower() in preview.lower():
            if st.button(preview, key=cid):
                st.session_state.current_chat = cid
                st.rerun()

    st.divider()

    st.subheader("📚 Library")
    st.caption("Saved prompts & notes (coming soon)")

    st.subheader("🚀 Projects")
    st.caption("Your AI projects (coming soon)")

st.title("💬 Manthan's Chatbot")

messages = st.session_state.chats[st.session_state.current_chat]

for msg in messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

def groq_stream(messages):
    stream = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        stream=True
    )
    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
            time.sleep(0.02)

user_input = st.chat_input("Type your message...")

if user_input:
    messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        reply = st.write_stream(groq_stream(messages))

    messages.append({"role": "assistant", "content": reply})
