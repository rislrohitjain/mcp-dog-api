from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
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

# Enable CORS middleware on SSE app
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

# OAuth Discovery Endpoints for Gemini Spark / Custom App integrations
@app.get("/.well-known/oauth-authorization-server")
@app.get("/.well-known/openid-configuration")
async def oauth_discovery():
    return {
        "issuer": "https://mcp-dog-api.vercel.app",
        "authorization_endpoint": "https://mcp-dog-api.vercel.app/authorize",
        "token_endpoint": "https://mcp-dog-api.vercel.app/token",
        "response_types_supported": ["code"],
        "grant_types_supported": ["authorization_code"],
        "code_challenge_methods_supported": ["plain", "S256"]
    }

# OAuth Authorize Endpoint - automatically redirects back to Gemini's redirect_uri
@app.get("/authorize")
async def authorize(request: Request):
    redirect_uri = request.query_params.get("redirect_uri", "")
    state = request.query_params.get("state", "")
    if redirect_uri:
        sep = "&" if "?" in redirect_uri else "?"
        target = f"{redirect_uri}{sep}code=success_code&state={state}"
        return RedirectResponse(target, status_code=302)
    return JSONResponse({"status": "authorized"})

# OAuth Token Endpoint
@app.post("/token")
@app.get("/token")
async def token():
    return JSONResponse({
        "access_token": "success_token_12345",
        "token_type": "Bearer",
        "expires_in": 86400
    })

# Mount sse_app at /mcp and /
app.mount("/mcp", sse_app)
app.mount("/", sse_app)
