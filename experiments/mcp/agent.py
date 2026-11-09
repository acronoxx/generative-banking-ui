# Agent LangChain dont les outils proviennent du serveur MCP (serveur.py).
# L'agent ne définit aucun outil lui-même : il les découvre au démarrage.
import asyncio
import os
import sys

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

# Modèle des essais par défaut ; GEMINI_MODEL permet d'en changer (quota épuisé, par exemple)
MODELE = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite")

client = MultiServerMCPClient(
    {"banque": {"transport": "stdio", "command": sys.executable, "args": ["serveur.py"]}}
)


async def main():
    outils = await client.get_tools()
    print("Outils découverts :", [outil.name for outil in outils])

    agent = create_agent(
        model=init_chat_model(f"google_genai:{MODELE}", timeout=60, max_retries=0),
        tools=outils,
        system_prompt="Tu es un assistant bancaire. Utilise les outils, n'invente jamais de données.",
    )
    result = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "Quel est mon solde courant, et quelles dépenses dépassent 500 € ?"}]}
    )
    for message in result["messages"]:
        message.pretty_print()


asyncio.run(main())
