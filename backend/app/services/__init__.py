"""Business logic shared by the HTTP routes (app/api/) and the MCP tools (app/mcp/).

Every function receives the connected user and only returns or changes that
customer's data: ownership is always checked here, not in the callers.
"""
