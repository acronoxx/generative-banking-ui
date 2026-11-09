# Serveur AG-UI minimal, sans modèle : répond à chaque requête par un flux
# d'événements typés (début d'exécution, message texte en trois événements, fin).
# Lancement : venv\Scripts\python server.py, puis POST sur http://localhost:8000/

import uuid

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from ag_ui.core import (
    RunAgentInput,
    EventType,
    RunStartedEvent,
    RunFinishedEvent,
    TextMessageStartEvent,
    TextMessageContentEvent,
    TextMessageEndEvent,
)
from ag_ui.encoder import EventEncoder

app = FastAPI()


@app.post("/")
async def run_agent(input_data: RunAgentInput, request: Request):
    encoder = EventEncoder(accept=request.headers.get("accept"))

    async def event_stream():
        yield encoder.encode(RunStartedEvent(
            type=EventType.RUN_STARTED,
            thread_id=input_data.thread_id,
            run_id=input_data.run_id,
        ))

        message_id = str(uuid.uuid4())
        yield encoder.encode(TextMessageStartEvent(
            type=EventType.TEXT_MESSAGE_START,
            message_id=message_id,
            role="assistant",
        ))
        yield encoder.encode(TextMessageContentEvent(
            type=EventType.TEXT_MESSAGE_CONTENT,
            message_id=message_id,
            delta="Votre solde est de 1 250 €.",
        ))
        yield encoder.encode(TextMessageEndEvent(
            type=EventType.TEXT_MESSAGE_END,
            message_id=message_id,
        ))

        yield encoder.encode(RunFinishedEvent(
            type=EventType.RUN_FINISHED,
            thread_id=input_data.thread_id,
            run_id=input_data.run_id,
        ))

    return StreamingResponse(event_stream(), media_type=encoder.get_content_type())


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
