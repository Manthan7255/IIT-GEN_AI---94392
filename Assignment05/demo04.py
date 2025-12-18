import os
import requests
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    print("ERROR: GROQ_API_KEY not found in .env file")
    exit()

user_prompt = input("Enter your prompt: ")

# =========================
# GROQ API CONFIG
# =========================
groq_url = "https://api.groq.com/openai/v1/chat/completions"

groq_headers = {
    "Authorization": f"Bearer {groq_api_key}",
    "Content-Type": "application/json"
}

groq_payload = {
    "model": "llama-3.3-70b-versatile",
    "messages": [
        {"role": "user", "content": user_prompt}
    ]
}

groq_start = time.time()
groq_response = requests.post(
    groq_url,
    headers=groq_headers,
    json=groq_payload
)
groq_time = time.time() - groq_start

if groq_response.status_code == 200:
    groq_text = groq_response.json()["choices"][0]["message"]["content"]
else:
    groq_text = f"Groq API Error: {groq_response.text}"

# =========================
# LM STUDIO (LOCAL LLM)
# =========================
lmstudio_url = "http://127.0.0.1:1234/v1/chat/completions"

lmstudio_headers = {
    "Authorization": "Bearer lm-studio",
    "Content-Type": "application/json"
}

lmstudio_payload = {
    "model": "openai/gpt-oss-20b",
    "messages": [
        {"role": "user", "content": user_prompt}
    ],
    "temperature": 0.7
}

lm_start = time.time()
lm_response = requests.post(
    lmstudio_url,
    headers=lmstudio_headers,
    json=lmstudio_payload
)
lm_time = time.time() - lm_start

if lm_response.status_code == 200:
    lm_text = lm_response.json()["choices"][0]["message"]["content"]
else:
    lm_text = f"LM Studio Error: {lm_response.text}"

# =========================
# OUTPUT
# =========================
print("\n================ GROQ RESPONSE ================")
print(groq_text)
print("Time Taken:", round(groq_time, 3), "seconds")

print("\n============= LM STUDIO RESPONSE ==============")
print(lm_text)
print("Time Taken:", round(lm_time, 3), "seconds")

print("\n=============== SPEED COMPARISON ===============")
if groq_time < lm_time:
    print("Groq is faster than LM Studio")
elif lm_time < groq_time:
    print("LM Studio is faster than Groq")
else:
    print("Both have similar response time")
