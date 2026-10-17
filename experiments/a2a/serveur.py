# Agent « comptes » exposé en A2A, sans modèle : il répond par une règle fixe.
# L'essai sert à observer la découverte (Agent Card) et le cycle de vie d'une tâche.
import uvicorn
from starlette.applications import Starlette

from a2a.helpers import get_message_text, new_task_from_user_message, new_text_message, new_text_part
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.routes import create_agent_card_routes, create_jsonrpc_routes
from a2a.server.tasks import InMemoryTaskStore, TaskUpdater
from a2a.types import AgentCapabilities, AgentCard, AgentInterface, AgentSkill, TaskState

SOLDES = {"courant": "1 250 €", "livret": "8 400 €"}


class AgentComptes(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        tache = context.current_task or new_task_from_user_message(context.message)
        if not context.current_task:
            await event_queue.enqueue_event(tache)

        suivi = TaskUpdater(event_queue=event_queue, task_id=tache.id, context_id=tache.context_id)
        await suivi.update_status(state=TaskState.TASK_STATE_WORKING, message=new_text_message("Consultation des comptes..."))

        demande = (get_message_text(context.message) or "").lower()
        comptes = [nom for nom in SOLDES if nom in demande] or list(SOLDES)
        resultat = "\n".join(f"{nom} : {SOLDES[nom]}" for nom in comptes)

        # Le résultat est rendu sous forme d'artefact, puis la tâche est terminée
        await suivi.add_artifact(parts=[new_text_part(text=resultat, media_type="text/plain")])
        await suivi.update_status(state=TaskState.TASK_STATE_COMPLETED)

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise NotImplementedError("Annulation non prise en charge")


carte = AgentCard(
    name="Agent comptes",
    description="Donne le solde des comptes du client (données fictives).",
    version="1.0.0",
    default_input_modes=["text/plain"],
    default_output_modes=["text/plain"],
    capabilities=AgentCapabilities(streaming=True),
    supported_interfaces=[AgentInterface(protocol_binding="JSONRPC", url="http://127.0.0.1:9999", protocol_version="1.0")],
    skills=[
        AgentSkill(
            id="soldes",
            name="Soldes",
            description="Renvoie le solde du compte courant et du livret.",
            tags=["banque"],
            examples=["Quel est le solde de mon livret ?"],
        )
    ],
)

gestionnaire = DefaultRequestHandler(agent_executor=AgentComptes(), task_store=InMemoryTaskStore(), agent_card=carte)
app = Starlette(routes=[*create_agent_card_routes(carte), *create_jsonrpc_routes(gestionnaire, "/")])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9999)
