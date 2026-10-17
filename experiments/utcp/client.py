# Client UTCP sans modèle : lit le manuel de l'API, puis appelle les outils
# directement sur leurs routes HTTP d'origine.
import asyncio

from utcp.utcp_client import UtcpClient


async def main():
    manuel = {"name": "banque", "call_template_type": "http", "url": "http://127.0.0.1:8100/utcp", "http_method": "GET"}
    client = await UtcpClient.create(config={"manual_call_templates": [manuel]})

    outils = await client.search_tools("solde transactions", limit=10)
    print("Outils découverts :", [outil.name for outil in outils])

    print("get_balance(courant) :", await client.call_tool("banque.get_balance", {"account": "courant"}))
    print("get_transactions(500) :", await client.call_tool("banque.get_transactions", {"min_amount": 500}))
    await client.close()


asyncio.run(main())
