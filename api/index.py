from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mcp.server.fastmcp import FastMCP
from starlette.responses import Response
from starlette.routing import Route
import httpx

mcp = FastMCP("Dog API Server", host="0.0.0.0")

@mcp.tool()
async def get_dog_breeds() -> str:
    """Fetch dog breeds from the Dog API."""
    async with httpx.AsyncClient() as client:
        response = await client.get("https://dogapi.dog/api/v2/breeds")
        return response.text

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sse_app = mcp.sse_app()
sse_app.routes.insert(0, Route("/{path:path}", lambda r: Response(status_code=200), methods=["OPTIONS"]))
sse_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "operational", "server": "Dog API Server"}

app.mount("/mcp", sse_app)
