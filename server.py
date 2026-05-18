import uvicorn
from starlette.types import ASGIApp, Receive, Scope, Send
from mcp.server.fastmcp import FastMCP
from tools.club_tools import find_club_nearby_tools, register_club_tools, join_club_tools
from tools.club_event_tools import find_event_nearby_tools, join_event_tools, register_club_event_tools
from tools.profile_tools import find_user_nearby_tools, register_profile_tools
from tools.recommendation_tools import register_recommendation_tools
from tools.search_tools import register_search_tools
from tools.tournament_tools import find_tournament_nearby_tools, register_tournament_tools
from auth.request_context import set_request_headers

# Tạo MCP server
mcp = FastMCP("badmintonnet")

# Register tools
register_club_tools(mcp)
join_club_tools(mcp)
register_club_event_tools(mcp)
register_profile_tools(mcp)
register_tournament_tools(mcp)
join_event_tools(mcp)
find_tournament_nearby_tools(mcp)
find_club_nearby_tools(mcp)
find_event_nearby_tools(mcp)
find_user_nearby_tools(mcp)
register_recommendation_tools(mcp)
register_search_tools(mcp)


class AuthMiddleware:
    """Raw ASGI middleware — safe for SSE/streaming responses."""

    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] == "http":
            headers = dict(scope.get("headers", []))
            # Starlette stores headers as (bytes, bytes) tuples
            decoded = {k.decode(): v.decode() for k, v in headers.items()}
            set_request_headers(decoded)
        await self.app(scope, receive, send)


if __name__ == "__main__":
    app = mcp.sse_app()
    app.add_middleware(AuthMiddleware)
    uvicorn.run(app, host="0.0.0.0", port=3001)
