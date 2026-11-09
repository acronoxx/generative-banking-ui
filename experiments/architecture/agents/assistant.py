# Agent « assistant bancaire » (port 8000) : le seul agent de l'architecture.
#   - LangChain orchestre le modèle et les appels d'outils (function calling)
#   - AG-UI diffuse l'exécution vers la page, sous forme d'événements
#   - les outils métier ne sont pas définis ici : la page les déclare (WebMCP)
#     et l'agent les reçoit à chaque requête
#   - A2UI décrit l'interface à afficher, en données et non en code ; l'agent la
#     compose avec le catalogue de composants déclaré par la page

import json
import os
from typing import Any
from uuid import uuid4

import uvicorn
from ag_ui_a2ui_toolkit import (
    BASIC_CATALOG_ID,
    create_surface,
    format_validation_errors,
    update_components,
    update_data_model,
    validate_a2ui_components,
    wrap_as_operations_envelope,
)
from ag_ui_langgraph import LangGraphAgent, add_langgraph_fastapi_endpoint
from copilotkit import CopilotKitMiddleware
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain.agents import create_agent
from langchain.agents.middleware import ModelRequest, dynamic_prompt
from langchain.chat_models import init_chat_model
from langchain.tools import ToolRuntime
from langgraph.checkpoint.memory import InMemorySaver

from banque import COMPTES, TRANSACTIONS

load_dotenv()

CONSIGNES = """Tu es un assistant bancaire. Utilise les outils, n'invente jamais de données.
Pour présenter des comptes ou des transactions, lis d'abord les données avec un outil,
puis affiche-les avec afficher_interface au lieu de les écrire dans ta réponse.
Utilise de préférence les composants SoldeCompte, Transaction et Alerte.

Format de components (A2UI v0.9, tableau plat) :
- chaque composant a un id unique et un champ component (nom d'un composant disponible) ;
- le composant racine a l'id "root" et est un conteneur (Card, Column ou Row) ;
- les propriétés sont directement sur l'objet ; les enfants sont référencés par id :
  children: ["id1", "id2"] pour plusieurs enfants, child: "id" pour un seul.
Exemple :
[{"id": "root", "component": "Column", "children": ["titre", "c1"]},
 {"id": "titre", "component": "Text", "text": "Vos comptes", "variant": "h3"},
 {"id": "c1", "component": "SoldeCompte", "nom": "Compte courant", "solde": "1 250 €"}]"""


def catalogue_de_la_page(state: dict) -> dict | None:
    """Catalogue A2UI déclaré par la page : le runtime le place dans state["ag-ui"]."""
    schema = (state.get("ag-ui") or {}).get("a2ui_schema")
    return json.loads(schema) if isinstance(schema, str) else schema


@dynamic_prompt
def consignes(request: ModelRequest) -> str:
    """Ajoute au prompt le schéma des composants déclarés par la page.

    CopilotKitMiddleware ne recopie pas state["ag-ui"] dans le prompt.
    """
    catalogue = catalogue_de_la_page(request.state)
    if not catalogue:
        return CONSIGNES
    return f"{CONSIGNES}\n\n## Composants disponibles (schéma JSON)\n{json.dumps(catalogue['components'])}"


def afficher_interface(components: list[dict[str, Any]], runtime: ToolRuntime, data: dict[str, Any] | None = None) -> str:
    """Affiche à l'utilisateur une interface composée avec les composants disponibles.

    Args:
        components: composants A2UI v0.9 (tableau plat, racine d'id "root").
        data: modèle de données facultatif, pour les valeurs liées par {"path": "/cle"}.
    """
    # L'interface passe par le résultat de l'outil : avec Gemini, les arguments d'un
    # appel d'outil ne sont pas diffusés en AG-UI, le runtime ne les verrait pas.
    catalogue = catalogue_de_la_page(runtime.state)
    verification = validate_a2ui_components(components=components, data=data, catalog=catalogue)
    if not verification["valid"]:
        # Renvoyées au modèle, qui corrige et rappelle l'outil
        return "Interface invalide, corrige et réessaie :\n" + format_validation_errors(verification["errors"])

    surface = f"interface-{uuid4().hex[:8]}"
    operations = [
        create_surface(surface, (catalogue or {}).get("catalogId", BASIC_CATALOG_ID)),
        update_components(surface, components),
    ]
    if data:
        operations.append(update_data_model(surface, data))
    return wrap_as_operations_envelope(operations)


agent = create_agent(
    # GEMINI_MODEL permet de changer de modèle lorsque le quota du modèle par défaut est épuisé
    model=init_chat_model(f"google_genai:{os.getenv('GEMINI_MODEL', 'gemini-3.5-flash-lite')}", timeout=60),
    # Le middleware ajoute à chaque requête les outils déclarés par la page
    tools=[afficher_interface],
    middleware=[CopilotKitMiddleware(), consignes],
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
