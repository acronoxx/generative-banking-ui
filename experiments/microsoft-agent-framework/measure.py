# Mesure du framework Microsoft Agent Framework selon le protocole commun (voir README.md) :
# même agent bancaire (gemini-3.5-flash-lite, outils get_balance et get_transactions),
# 4 scénarios répétés 10 fois. Affiche une ligne CSV par scénario.
# Lancement : venv\Scripts\python measure.py

import asyncio
import statistics
import time

from dotenv import load_dotenv
from agent_framework import Agent
from agent_framework_gemini import GeminiChatClient
from google import genai

load_dotenv()

FRAMEWORK = "Microsoft Agent Framework"
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


# La clé est lue dans GOOGLE_API_KEY ; délai maximal de 60 s par appel (en millisecondes)
client = GeminiChatClient(
    model="gemini-3.5-flash-lite",
    client=genai.Client(http_options={"timeout": 60_000}),
)
agent = Agent(
    client,
    "Tu es un assistant bancaire. Utilise les outils, n'invente jamais de données.",
    name="assistant_bancaire",
    tools=[get_balance, get_transactions],
)

# Chaque scénario : une question et les outils qui doivent être appelés
SCENARIOS = [
    ("Quel est le solde de mon compte courant ?", {"get_balance"}),
    ("Quelles dépenses dépassent 500 € ?", {"get_transactions"}),
    ("Quel est mon solde courant, et quelles dépenses dépassent 500 € ?", {"get_balance", "get_transactions"}),
    ("Bonjour, que peux-tu faire pour moi ?", set()),
]


async def main():
    print("framework;question;duree_mediane_s;duree_min_s;duree_max_s;appels_modele;tokens_entree;tokens_sortie;reussite;erreurs")

    for question, outils_attendus in SCENARIOS:
        durees, appels, entrees, sorties, reussites = [], [], [], [], 0

        for _ in range(REPETITIONS):
            debut = time.perf_counter()
            try:
                # Sans session transmise, chaque appel part d'une conversation vide
                result = await agent.run(question)
            except Exception as erreur:
                print(f"  essai en échec : {type(erreur).__name__} : {str(erreur)[:200]}")
                await asyncio.sleep(PAUSE)
                continue
            durees.append(time.perf_counter() - debut)

            # Chaque message « assistant » correspond à une réponse du modèle
            reponses = [m for m in result.messages if m.role == "assistant"]
            outils_appeles = {c.name for m in reponses for c in m.contents if c.type == "function_call"}
            usage = result.usage_details or {}

            appels.append(len(reponses))
            entrees.append(usage.get("input_token_count", 0))
            sorties.append(usage.get("output_token_count", 0))
            reussites += outils_appeles == outils_attendus
            await asyncio.sleep(PAUSE)

        if durees:
            print(
                f"{FRAMEWORK};{question};{statistics.median(durees):.2f};{min(durees):.2f};{max(durees):.2f};"
                f"{statistics.median(appels):.0f};{statistics.median(entrees):.0f};"
                f"{statistics.median(sorties):.0f};{reussites}/{len(durees)};{REPETITIONS - len(durees)}"
            )


asyncio.run(main())
