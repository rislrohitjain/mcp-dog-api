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

sse_app = mcp.sse_app()

# Add root GET route handler to sse_app so root URL can also serve as SSE endpoint
sse_endpoint_handler = sse_app.routes[0].endpoint
sse_app.routes.append(Route("/", endpoint=sse_endpoint_handler, methods=["GET"]))

# Insert OPTIONS preflight handler at the beginning of routes
sse_app.routes.insert(0, Route("/{path:path}", lambda r: Response(status_code=200), methods=["OPTIONS"]))

# Enable CORS middleware
sse_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount sse_app at /mcp and /
app.mount("/mcp", sse_app)
app.mount("/", sse_app)
