
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

from tools import get_country_info, get_weather

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
model_name = os.getenv("GROQ_MODEL")

if not api_key:
    raise RuntimeError("GROQ_API_KEY environment variable is missing.")

if not model_name:
    raise RuntimeError("GROQ_MODEL environment variable is missing.")

llm = ChatGroq(
    model=model_name,
    temperature=0,
    api_key=api_key,
)

agent = create_react_agent(
    model=llm,
    tools=[get_weather, get_country_info],
    prompt=(
        "You are a helpful travel assistant. "
        "Use the available tools when the user asks for live weather "
        "or factual country information. Do not invent tool results. "
        "If a tool fails, explain the limitation clearly."
    ),
)


def ask_agent(question: str) -> str:
    result = agent.invoke(
        {"messages": [{"role": "user", "content": question}]}
    )
    return str(result["messages"][-1].content)
