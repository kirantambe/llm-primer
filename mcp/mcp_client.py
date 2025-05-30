from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_ollama.chat_models import ChatOllama

client = MultiServerMCPClient(
    {
        "movies": {
            # Ensure your start your weather server on port 8000
            "url": "http://localhost:8000/mcp",
            "transport": "streamable_http",
        }
    }
)

async def main():
    tools = await client.get_tools()
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