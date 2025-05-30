from mcp.server.fastmcp import FastMCP
import requests
import os

TMDB_ACCESS_TOKEN = os.environ.get("TMDB_ACCESS_TOKEN")

mcp = FastMCP("Movie Search")


@mcp.tool()
def search_movies(year: int):
    url = f"https://api.themoviedb.org/3/discover/movie?year={year}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    return response.text


if __name__ == "__main__":
    mcp.run(transport="streamable-http")