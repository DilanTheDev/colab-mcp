# Vercel ASGI entrypoint for colab-mcp.
#
# Exposes the MCP streamable-http transport so remote clients can list tools
# and make calls. The live Colab WebSocket back-channel requires a persistent
# process and is not available in Vercel's serverless runtime; use
# `colab-mcp --transport streamable-http` on a persistent host for that.

from fastmcp import FastMCP

mcp = FastMCP(name="ColabMCP")

app = mcp.http_app(transport="streamable-http")
