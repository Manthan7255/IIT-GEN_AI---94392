import streamlit as st
import requests
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

# Load .env variables
load_dotenv()

# -------------------- CONFIG --------------------

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

# LLM config (LM Studio)
llm = init_chat_model(
    model="openai/gpt-oss-20b",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="not-needed"
)

def get_weather(city: str):
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }
    response = requests.get(WEATHER_API_URL, params=params, timeout=10)
    data = response.json()

    if response.status_code != 200:
        return None, data.get("message", "Error fetching weather")

    weather_info = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "condition": data["weather"][0]["description"]
    }
    return weather_info, None


def explain_weather_with_llm(weather: dict):
    prompt = f"""
    Explain the following weather information in simple English:

    City: {weather['city']}
    Temperature: {weather['temperature']} °C
    Feels like: {weather['feels_like']} °C
    Humidity: {weather['humidity']}%
    Condition: {weather['condition']}
    """

    response = llm.invoke(prompt)
    return response.content

st.set_page_config(page_title="Weather Explainer", page_icon="🌦️")

st.title("🌦️ Weather Explainer using LLM")

city = st.text_input("Enter city name")

if st.button("Get Weather"):
    if not city:
        st.warning("Please enter a city name.")
        st.stop()

    weather, error = get_weather(city)

    if error:
        st.error(error)
        st.stop()

    st.subheader("📊 Raw Weather Data")
    st.json(weather)

    st.subheader("🧠 LLM Explanation")
    with st.spinner("Asking AI to explain the weather..."):
        explanation = explain_weather_with_llm(weather)
        st.success(explanation)
