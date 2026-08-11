from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
import httpx

mcp = FastMCP("Dog API Server", host="0.0.0.0")

@mcp.tool()
async def get_dog_breeds() -> str:
    """Fetch dog breeds from the Dog API."""
    async with httpx.AsyncClient() as client:
        response = await client.get("https://dogapi.dog/api/v2/breeds")
        return response.text

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "operational", "server": "Dog API Server"}

app.mount("/mcp", mcp.sse_app())
