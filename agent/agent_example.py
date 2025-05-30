import os
import asyncio
import requests
from langchain.agents import Tool
from langchain_community.utilities import SerpAPIWrapper
from langgraph.prebuilt import create_react_agent
from langchain_ollama.chat_models import ChatOllama

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


async def main():
    tools = [search_tool, weather_tool]
    agent = create_react_agent(
        ChatOllama(model="llama3.2:1b"),
        tools
    )
    msg = input("You: ")
    while msg.lower() != "exit":
        response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": msg}]}
        )
        for msg in response["messages"]:
            msg.pretty_print()
        msg = input("You: ")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())