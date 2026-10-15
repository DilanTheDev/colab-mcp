# Vercel ASGI entrypoint for colab-mcp HTTP/SSE transport.
#
# NOTE: The Colab WebSocket back-channel requires a persistent process, which
# Vercel's serverless functions do not support. This entrypoint exposes the MCP
# HTTP/SSE interface but the open_colab_browser_connection tool will time out
# unless you deploy to a long-running host (Railway, Fly.io, a plain VPS, etc.)
# that can keep the WebSocket server alive. Vercel works for the MCP transport
# layer itself (tool listing, stateless calls) but not for live Colab sessions.

from contextlib import asynccontextmanager

from fastmcp import FastMCP
from colab_mcp.session import ColabSessionProxy

_mcp = FastMCP(name="ColabMCP")
_session_mcp: ColabSessionProxy | None = None


@asynccontextmanager
async def _lifespan(app):
    global _session_mcp
    _session_mcp = ColabSessionProxy(server_mode=True, ws_host="0.0.0.0")
    await _session_mcp.start_proxy_server()
    _mcp.mount(_session_mcp.proxy_server)
    for middleware in _session_mcp.middleware:
        _mcp.add_middleware(middleware)
    yield
    await _session_mcp.cleanup()


app = _mcp.http_app(transport="streamable-http")
app.router.lifespan_context = _lifespan
