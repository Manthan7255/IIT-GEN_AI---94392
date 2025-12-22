
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call
from langchain.tools import tool
import os
import requests
from dotenv import load_dotenv
load_dotenv()

@tool
def calculator(expression: str) -> str:
    """
    Evaluates a basic arithmetic expression.
    """
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Calculation error: {e}"


@tool
def read_file(filepath: str) -> str:
    """
    Reads and returns content of a text file.
    """
    if not os.path.exists(filepath):
        return "Error: File not found"
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


@tool
def get_weather(city: str) -> str:
    """
    Returns current weather of a city.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "Error: OPENWEATHER_API_KEY not found"

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={api_key}&units=metric"
    )
    response = requests.get(url)

    if response.status_code != 200:
        return "Error: Unable to fetch weather"

    data = response.json()
    return f"{city}: {data['main']['temp']}°C, {data['weather'][0]['description']}"


@tool
def knowledge_lookup(query: str) -> str:
    """
    Simple knowledge lookup tool.
    """
    knowledge_base = {
        "langchain": "LangChain is a framework for building applications using LLMs.",
        "llm": "LLM stands for Large Language Model.",
        "agent": "An agent decides when to call tools to solve tasks."
    }
    return knowledge_base.get(query.lower(), "No knowledge found")

@wrap_model_call
def logging_middleware(request, handler):
    print("\n===== BEFORE MODEL CALL =====")
    print(request.messages)

    response = handler(request)

    print("===== AFTER MODEL CALL =====")
    print(response.result[0].content)

    return response


@wrap_model_call
def limit_context_middleware(request, handler):
    request.messages = request.messages[-5:]
    return handler(request)

llm = init_chat_model(
    model="google/gemma-3-4b",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="not-needed"
)

agent = create_agent(
    model=llm,
    tools=[calculator, read_file, get_weather, knowledge_lookup],
    middleware=[logging_middleware, limit_context_middleware],
    system_prompt="You are a helpful assistant. Use tools when required. Answer briefly."
)

conversation = []

while True:
    user_input = input("\nYou: ")
    if user_input.lower() == "exit":
        break

    conversation.append({"role": "user", "content": user_input})

    result = agent.invoke({"messages": conversation})

    ai_msg = result["messages"][-1]
    print("AI:", ai_msg.content)

    conversation = result["messages"]

    print("\n--- MESSAGE HISTORY ---")
    for msg in conversation:
        print(msg)
