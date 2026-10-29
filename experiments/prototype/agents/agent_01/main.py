"""AG-UI server of the banking assistant, called by the CopilotKit runtime.

Run from this folder: python main.py (the backend must already be running).
"""

import asyncio

import uvicorn
from ag_ui.core.types import RunAgentInput
from ag_ui.encoder import EventEncoder
from ag_ui_langgraph import LangGraphAgent
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

import config
from agent import build_agent
from tools import SESSION_TOKEN_KEY, load_backend_tools


def read_session_token(request: Request) -> str | None:
    """Return the Authorization header of the request ("Bearer <token>"), or None.

    The page sends it to the CopilotKit runtime, which forwards it to the agent by default.
    """
    return request.headers.get("authorization")


def create_app() -> FastAPI:
    """Create the AG-UI server.

    Our own endpoint instead of add_langgraph_fastapi_endpoint, which drops the request
    headers (the session token would be lost).
    """
    tools = asyncio.run(load_backend_tools())
    # emit_raw_events=False: the raw LangGraph events carry the run config, so the
    # session token would be streamed to the page (checked: 6 RAW events contained it)
    agent = LangGraphAgent(name="agent_01", graph=build_agent(tools), emit_raw_events=False)
    app = FastAPI()

    @app.post("/")
    async def run_agent(input_data: RunAgentInput, request: Request):
        # Clone per request: LangGraphAgent keeps per-run state on the instance
        run = agent.clone()
        run.config = {"configurable": {SESSION_TOKEN_KEY: read_session_token(request)}}
        encoder = EventEncoder(accept=request.headers.get("accept"))

        async def events():
            async for event in run.run(input_data):
                yield encoder.encode(event)

        return StreamingResponse(events(), media_type=encoder.get_content_type())

    return app


if __name__ == "__main__":
    uvicorn.run(create_app(), host="127.0.0.1", port=config.AGENT_PORT)
