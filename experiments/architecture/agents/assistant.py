# Agent « assistant bancaire » (port 8000) : le seul agent de l'architecture.
#   - LangChain orchestre le modèle et les appels d'outils (function calling)
#   - AG-UI diffuse l'exécution vers la page, sous forme d'événements
#   - les outils métier ne sont pas définis ici : la page les déclare (WebMCP)
#     et l'agent les reçoit à chaque requête
#   - A2UI décrit l'interface à afficher, en données et non en code

from uuid import uuid4

import uvicorn
from ag_ui_a2ui_toolkit import (
    BASIC_CATALOG_ID,
    create_surface,
    update_components,
    update_data_model,
    wrap_as_operations_envelope,
)
from ag_ui_langgraph import LangGraphAgent, add_langgraph_fastapi_endpoint
from copilotkit import CopilotKitMiddleware
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver
from typing_extensions import TypedDict

from banque import COMPTES, TRANSACTIONS

load_dotenv()

# Interface d'une carte : uniquement des composants du catalogue A2UI.
# Les valeurs ne sont pas écrites ici, elles sont liées au modèle de données.
CARTE = [
    {"id": "root", "component": "Card", "child": "contenu"},
    {"id": "contenu", "component": "Column", "children": ["titre", "liste"]},
    {"id": "titre", "component": "Text", "text": {"path": "/titre"}, "variant": "h3"},
    {"id": "liste", "component": "List", "children": {"path": "/lignes", "componentId": "ligne"}},
    {"id": "ligne", "component": "Row", "children": ["libelle", "valeur"], "justify": "spaceBetween"},
    {"id": "libelle", "component": "Text", "text": {"path": "libelle"}},
    {"id": "valeur", "component": "Text", "text": {"path": "valeur"}, "variant": "h4"},
]


class Ligne(TypedDict):
    libelle: str
    valeur: str


def afficher_carte(titre: str, lignes: list[Ligne]) -> str:
    """Affiche à l'utilisateur une carte : un titre et des lignes, libellé à gauche et valeur à droite.
    À utiliser pour présenter des comptes ou des transactions lus avec un autre outil."""
    surface = f"carte-{uuid4().hex[:8]}"
    return wrap_as_operations_envelope([
        create_surface(surface, BASIC_CATALOG_ID),
        update_components(surface, CARTE),
        update_data_model(surface, {"titre": titre, "lignes": lignes}),
    ])


agent = create_agent(
    model=init_chat_model("google_genai:gemini-3.5-flash-lite", timeout=60),
    # Le middleware ajoute à chaque requête les outils déclarés par la page
    tools=[afficher_carte],
    middleware=[CopilotKitMiddleware()],
    system_prompt=(
        "Tu es un assistant bancaire. Utilise les outils, n'invente jamais de données. "
        "Pour présenter des comptes ou des transactions, lis d'abord les données avec un outil, "
        "puis affiche-les avec afficher_carte au lieu de les écrire dans ta réponse."
    ),
    checkpointer=InMemorySaver(),
)

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Point d'entrée AG-UI : chaque étape de l'agent LangChain devient un événement AG-UI
add_langgraph_fastapi_endpoint(app, LangGraphAgent(name="assistant", graph=agent), "/")


# API bancaire classique, appelée par les outils de la page
@app.get("/api/comptes")
def lire_comptes():
    return COMPTES


@app.get("/api/transactions")
def lire_transactions(min_amount: float = 0):
    return [{"libelle": nom, "montant": f"{montant} €"} for nom, montant in TRANSACTIONS if montant >= min_amount]


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
