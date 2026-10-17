# Client A2A : découvre l'agent par son Agent Card, puis lui confie une tâche
# en streaming pour observer les changements d'état successifs.
import asyncio

import httpx
from a2a.client import A2ACardResolver, ClientConfig, create_client
from a2a.helpers import new_text_message
from a2a.types import Role, SendMessageRequest


async def main():
    async with httpx.AsyncClient() as http:
        carte = await A2ACardResolver(httpx_client=http, base_url="http://127.0.0.1:9999").get_agent_card()
    print("Agent découvert :", carte.name, "|", [c.name for c in carte.skills])

    client = await create_client(agent=carte, client_config=ClientConfig(streaming=True))
    requete = SendMessageRequest(message=new_text_message("Quel est le solde de mon livret ?", role=Role.ROLE_USER))
    async for evenement in client.send_message(requete):
        print("---")
        print(evenement)
    await client.close()


asyncio.run(main())
