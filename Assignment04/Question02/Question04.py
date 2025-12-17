import streamlit as st
import time
import os
import pandas as pd
from dotenv import load_dotenv
from groq import Groq
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Manthan's Chatbot",
    page_icon="💬",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
    body { background-color: #000000; }

    section[data-testid="stSidebar"] {
        background-color: #2F2F4F;
    }

    section[data-testid="stSidebar"] * {
        color: #E6E6FA;
    }

    .stChatMessage {
        padding: 12px;
        border-radius: 12px;
    }

    .stButton > button {
        border-radius: 8px;
        width: 100%;
    }

    textarea {
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- ENV ----------------
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ API key not found.")
    st.stop()

client = Groq(api_key=api_key)

# ---------------- FILES ----------------
USERS_FILE = "users.csv"

if not os.path.exists(USERS_FILE):
    pd.DataFrame(columns=["userid", "username", "password"]).to_csv(USERS_FILE, index=False)

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None

if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat" not in st.session_state:
    cid = datetime.now().strftime("%Y%m%d%H%M%S")
    st.session_state.current_chat = cid
    st.session_state.chats[cid] = []

# ---------------- AUTH HELPERS ----------------
def load_users():
    try:
        df = pd.read_csv(USERS_FILE)
        return df if not df.empty else pd.DataFrame(columns=["userid", "username", "password"])
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=["userid", "username", "password"])

def register_user(username, password):
    users = load_users()
    if username in users["username"].values:
        return False

    new_user = pd.DataFrame(
        [[len(users) + 1, username, password]],
        columns=["userid", "username", "password"]
    )
    users = pd.concat([users, new_user], ignore_index=True)
    users.to_csv(USERS_FILE, index=False)
    return True

def authenticate_user(username, password):
    users = load_users()
    if users.empty:
        return None

    user = users[
        (users["username"] == username) &
        (users["password"] == password)
    ]
    return None if user.empty else user.iloc[0].to_dict()

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("💬 Manthan's Chatbot")

    if st.session_state.user is None:
        menu = st.radio("Menu", ["Home", "Login", "Register"])
    else:
        # -------- CHATBOT SIDEBAR (UNCHANGED UI) --------
        if st.button("➕ New Chat"):
            cid = datetime.now().strftime("%Y%m%d%H%M%S")
            st.session_state.current_chat = cid
            st.session_state.chats[cid] = []
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

        st.divider()
        if st.button("Logout"):
            st.session_state.user = None
            st.rerun()

# ---------------- MAIN ----------------
st.title("💬 Manthan's Chatbot")

# -------- NOT LOGGED IN --------
if st.session_state.user is None:
    if menu == "Home":
        st.info("Please login or register to use the chatbot.")

    elif menu == "Register":
        st.subheader("Register")
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")

        if st.button("Register"):
            if register_user(u, p):
                st.success("Registered successfully. Login now.")
            else:
                st.error("Username already exists.")

    elif menu == "Login":
        st.subheader("Login")
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")

        if st.button("Login"):
            user = authenticate_user(u, p)
            if user:
                st.session_state.user = user
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")

# -------- LOGGED IN → CHATBOT --------
else:
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
