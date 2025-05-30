import os
import requests
from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType
from langchain_ollama import OllamaLLM
from langchain_community.utilities import SerpAPIWrapper
from langchain.memory import ConversationBufferMemory

SERP_API_KEY = os.getenv("SERP_API_KEY")
if not SERP_API_KEY:
    raise ValueError("Please set the SERP_API_KEY environment variable.")


# Weather Tool: checks weather for a given city (now generalized)
def check_weather(city: str) -> str:
    response = requests.get(f"http://wttr.in/{city}?format=3")
    return response.text if response.status_code == 200 else f"Could not get weather for {city}."

weather_tool = Tool(
    name="WeatherChecker",
    func=check_weather,
    description="Check current weather in a city. Input should be a city name like 'Mumbai'."
)

# General-purpose search tool using SerpAPI
def serp_search(search_text: str) -> str:
    
    search = SerpAPIWrapper(serpapi_api_key=SERP_API_KEY)
    return search.run(search_text)

search_tool = Tool(
    name="SearchWithSerpAPI",
    func=serp_search,
    description="Search anything using Google via SerpAPI. Input should be a natural language search query. Can be used to search flights"
)

# Use a local Ollama model
llm = OllamaLLM(model="qwen3:0.6b")  # Or 'mistral', 'llama2', etc.

# Add memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Initialize the agent
agent = initialize_agent(
    tools=[search_tool, weather_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    memory=memory
)


print("Chat with your agent! Type 'exit' to quit.\n")
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    response = agent.run(user_input)
    print("Agent:", response)
