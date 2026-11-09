# Mesure du framework OpenAI Agents SDK selon le protocole commun (voir README.md) :
# même agent bancaire (gemini-3.5-flash-lite, outils get_balance et get_transactions),
# 4 scénarios répétés 10 fois. Affiche une ligne CSV par scénario.
# Lancement : venv\Scripts\python measure.py
# Gemini est appelé par son point d'accès compatible avec l'API d'OpenAI.

import os
import statistics
import time

from dotenv import load_dotenv
from agents import (
    Agent,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    Runner,
    ToolCallItem,
    function_tool,
    set_tracing_disabled,
)

load_dotenv()

FRAMEWORK = "OpenAI Agents SDK"
REPETITIONS = 10
PAUSE = 10  # secondes entre deux essais, pour respecter le quota gratuit

# Pas de clé OpenAI : les traces, envoyées par défaut à OpenAI, sont désactivées
set_tracing_disabled(True)

# Gemini est appelé par son point d'accès compatible avec l'API d'OpenAI
client = AsyncOpenAI(
    api_key=os.environ["GOOGLE_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    timeout=60,
    max_retries=0,
)
model = OpenAIChatCompletionsModel(model="gemini-3.5-flash-lite", openai_client=client)


@function_tool
def get_balance(account: str) -> str:
    """Renvoie le solde d'un compte ('courant' ou 'livret')."""
    return {"courant": "1 250 €", "livret": "8 400 €"}.get(account, "Compte inconnu")


@function_tool
def get_transactions(min_amount: float) -> str:
    """Renvoie les transactions des trois derniers mois supérieures à un montant en euros."""
    transactions = [("Loyer", 780), ("Garage", 620), ("Courses", 95), ("Billets de train", 510)]
    resultat = [f"{nom} : {montant} €" for nom, montant in transactions if montant >= min_amount]
    return "\n".join(resultat) or "Aucune transaction"


agent = Agent(
    name="Assistant bancaire",
    instructions="Tu es un assistant bancaire. Utilise les outils, n'invente jamais de données.",
    model=model,
    tools=[get_balance, get_transactions],
)

# Chaque scénario : une question et les outils qui doivent être appelés
SCENARIOS = [
    ("Quel est le solde de mon compte courant ?", {"get_balance"}),
    ("Quelles dépenses dépassent 500 € ?", {"get_transactions"}),
    ("Quel est mon solde courant, et quelles dépenses dépassent 500 € ?", {"get_balance", "get_transactions"}),
    ("Bonjour, que peux-tu faire pour moi ?", set()),
]

print("framework;question;duree_mediane_s;duree_min_s;duree_max_s;appels_modele;tokens_entree;tokens_sortie;reussite;erreurs")

for question, outils_attendus in SCENARIOS:
    durees, appels, entrees, sorties, reussites = [], [], [], [], 0

    for _ in range(REPETITIONS):
        debut = time.perf_counter()
        try:
            result = Runner.run_sync(agent, question)
        except Exception as erreur:
            print(f"  essai en échec : {type(erreur).__name__} : {str(erreur)[:200]}")
            time.sleep(PAUSE)
            continue
        durees.append(time.perf_counter() - debut)

        outils_appeles = {item.raw_item.name for item in result.new_items if isinstance(item, ToolCallItem)}
        usage = result.context_wrapper.usage

        appels.append(usage.requests)
        entrees.append(usage.input_tokens)
        sorties.append(usage.output_tokens)
        reussites += outils_appeles == outils_attendus
        time.sleep(PAUSE)

    if durees:
        print(
            f"{FRAMEWORK};{question};{statistics.median(durees):.2f};{min(durees):.2f};{max(durees):.2f};"
            f"{statistics.median(appels):.0f};{statistics.median(entrees):.0f};"
            f"{statistics.median(sorties):.0f};{reussites}/{len(durees)};{REPETITIONS - len(durees)}"
        )
