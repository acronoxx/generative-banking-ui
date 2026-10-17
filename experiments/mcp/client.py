# Client MCP sans modèle : découvre les outils du serveur puis en appelle un.
# Sert à observer ce qui circule, indépendamment de tout LLM.
import asyncio
import json
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

serveur = StdioServerParameters(command=sys.executable, args=["serveur.py"])


async def main():
    async with stdio_client(serveur) as (lecture, ecriture):
        async with ClientSession(lecture, ecriture) as session:
            init = await session.initialize()
            print("Serveur :", init.serverInfo.name, "| protocole", init.protocolVersion)

            outils = await session.list_tools()
            for outil in outils.tools:
                print(f"\nOutil {outil.name} : {outil.description}")
                print(json.dumps(outil.inputSchema, ensure_ascii=False, indent=2))

            resultat = await session.call_tool("get_transactions", {"min_amount": 500})
            print("\nAppel de get_transactions(min_amount=500) :")
            for bloc in resultat.content:
                print(bloc.text)


asyncio.run(main())
