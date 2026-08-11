# FastMCP Dog API Server 🐶

A production-ready **Model Context Protocol (MCP)** server built with Python, FastMCP, FastAPI, and HTTPX to provide dog breed data from the [Dog API](https://dogapi.dog/api/v2/breeds). Designed for seamless integration with AI assistants like Gemini, Claude, Cursor, and Antigravity IDE.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128-green?logo=fastapi)
![Vercel](https://img.shields.io/badge/Vercel-Deployed-black?logo=vercel)
![License](https://img.shields.io/badge/License-MIT-brightgreen)

---

## 🌟 Live Endpoints

* **Production SSE Endpoint**: [`https://mcp-dog-api.vercel.app/sse`](https://mcp-dog-api.vercel.app/sse)
* **Secondary SSE Endpoint**: [`https://mcp-dog-api.vercel.app/mcp/sse`](https://mcp-dog-api.vercel.app/mcp/sse)
* **GitHub Repository**: [`https://github.com/rislrohitjain/mcp-dog-api`](https://github.com/rislrohitjain/mcp-dog-api)

---

## ✨ Features

- **Dog Breeds Tool**: Exposes the `get_dog_breeds` asynchronous tool to fetch real-time breed descriptions, attributes, and group data.
- **Server-Sent Events (SSE)**: Full MCP SSE transport implementation for continuous streaming communication with AI clients.
- **Cross-Origin Resource Sharing (CORS)**: Configured with edge-level and application-level CORS (`Access-Control-Allow-Origin: *`) for browser-based AI client handshakes.
- **Gemini Spark OAuth Support**: Includes auto-discovery (`/.well-known/oauth-authorization-server`), `/authorize`, and `/token` endpoints for zero-friction connection with Gemini Connected Apps.
- **Cloud Native**: Deployed serverless on Vercel with Python 3.12 runtime.

---

## 🛠️ Tech Stack

- **Framework**: FastMCP (`mcp>=1.2.0,<2.0.0`), FastAPI
- **HTTP Client**: `httpx`
- **ASGI Server**: Uvicorn
- **Deployment**: Vercel Serverless Functions (`@vercel/python`)

---

## 🚀 Local Development Setup

### Prerequisites
- Python 3.10+
- Git

### 1. Clone Repository
```bash
git clone https://github.com/rislrohitjain/mcp-dog-api.git
cd mcp-dog-api
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Server Locally
```bash
uvicorn api.index:app --host 0.0.0.0 --port 8000 --reload
```

* Local Status Endpoint: `http://172.18.177.164:8000/`
* Local SSE Endpoint: `http://172.18.177.164:8000/mcp/sse`

---

## 🔌 Connecting to AI Assistants

### Gemini Connected Apps
1. Open **Gemini** -> **Settings** -> **Connected Apps**.
2. Add a Custom MCP Server and paste:
   ```text
   https://mcp-dog-api.vercel.app/sse
   ```
3. Complete the auto-authorization step.

### Local Agent Config (`.agents/mcp_config.json`)
```json
{
  "mcpServers": {
    "dog-api-live": {
      "url": "https://mcp-dog-api.vercel.app/sse"
    }
  }
}
```

---

## 📂 Project Structure

```
mcp-dog-api/
├── api/
│   └── index.py            # FastMCP & FastAPI server implementation
├── .agents/
│   └── mcp_config.json     # MCP server configuration
├── requirements.txt        # Python package dependencies
├── vercel.json             # Vercel deployment & edge CORS configuration
├── .gitignore              # Git ignore rules
└── README.md               # Documentation
```

---

## 👤 Author & Profile

Created by **Rohit Jain**

* 🌐 **Portfolio & Resume**: [https://rohitjain-resume.vercel.app/](https://rohitjain-resume.vercel.app/)
* 🐙 **GitHub**: [@rislrohitjain](https://github.com/rislrohitjain)
* 📁 **Repository**: [rislrohitjain/mcp-dog-api](https://github.com/rislrohitjain/mcp-dog-api)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
