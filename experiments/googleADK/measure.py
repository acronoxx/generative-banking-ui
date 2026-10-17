# Mesure du framework Google ADK selon le protocole commun (voir README.md) :
# même agent bancaire (gemini-3.5-flash-lite, outils get_balance et get_transactions),
# 4 scénarios répétés 10 fois. Affiche une ligne CSV par scénario.
# Lancement : venv\Scripts\python measure.py

import asyncio
import statistics
import time
import uuid

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.genai import types

load_dotenv()

FRAMEWORK = "Google ADK"
REPETITIONS = 10
PAUSE = 10  # secondes entre deux essais, pour respecter le quota gratuit


def get_balance(account: str) -> str:
    """Renvoie le solde d'un compte ('courant' ou 'livret')."""
    return {"courant": "1 250 €", "livret": "8 400 €"}.get(account, "Compte inconnu")


def get_transactions(min_amount: float) -> str:
    """Renvoie les transactions des trois derniers mois supérieures à un montant en euros."""
    transactions = [("Loyer", 780), ("Garage", 620), ("Courses", 95), ("Billets de train", 510)]
    resultat = [f"{nom} : {montant} €" for nom, montant in transactions if montant >= min_amount]
    return "\n".join(resultat) or "Aucune transaction"


agent = Agent(
    name="assistant_bancaire",
    model="gemini-3.5-flash-lite",
    instruction="Tu es un assistant bancaire. Utilise les outils, n'invente jamais de données.",
    tools=[get_balance, get_transactions],
    # Délai maximal de 60 s par appel (exprimé en millisecondes)
    generate_content_config=types.GenerateContentConfig(http_options=types.HttpOptions(timeout=60_000)),
)
runner = InMemoryRunner(agent=agent, app_name="mesures")

# Chaque scénario : une question et les outils qui doivent être appelés
SCENARIOS = [
    ("Quel est le solde de mon compte courant ?", {"get_balance"}),
    ("Quelles dépenses dépassent 500 € ?", {"get_transactions"}),
    ("Quel est mon solde courant, et quelles dépenses dépassent 500 € ?", {"get_balance", "get_transactions"}),
    ("Bonjour, que peux-tu faire pour moi ?", set()),
]


async def poser(question):
    # Une session neuve par essai, pour que l'historique ne s'accumule pas
    session = await runner.session_service.create_session(
        app_name="mesures", user_id="client", session_id=str(uuid.uuid4())
    )
    message = types.Content(role="user", parts=[types.Part(text=question)])
    evenements = []
    async for evenement in runner.run_async(user_id="client", session_id=session.id, new_message=message):
        evenements.append(evenement)
    return evenements


async def main():
    print("framework;question;duree_mediane_s;duree_min_s;duree_max_s;appels_modele;tokens_entree;tokens_sortie;reussite;erreurs")

    for question, outils_attendus in SCENARIOS:
        durees, appels, entrees, sorties, reussites = [], [], [], [], 0

        for _ in range(REPETITIONS):
            debut = time.perf_counter()
            try:
                evenements = await poser(question)
            except Exception as erreur:
                print(f"  essai en échec : {type(erreur).__name__} : {str(erreur)[:200]}")
                await asyncio.sleep(PAUSE)
                continue
            durees.append(time.perf_counter() - debut)

            outils_appeles = {appel.name for e in evenements for appel in e.get_function_calls()}
            # Chaque réponse du modèle porte ses propres compteurs de tokens
            usages = [e.usage_metadata for e in evenements if e.usage_metadata]

            appels.append(len(usages))
            entrees.append(sum(u.prompt_token_count or 0 for u in usages))
            sorties.append(sum((u.candidates_token_count or 0) + (u.thoughts_token_count or 0) for u in usages))
            reussites += outils_appeles == outils_attendus
            await asyncio.sleep(PAUSE)

        if durees:
            print(
                f"{FRAMEWORK};{question};{statistics.median(durees):.2f};{min(durees):.2f};{max(durees):.2f};"
                f"{statistics.median(appels):.0f};{statistics.median(entrees):.0f};"
                f"{statistics.median(sorties):.0f};{reussites}/{len(durees)};{REPETITIONS - len(durees)}"
            )


asyncio.run(main())
