# Mesure du framework AWS Strands Agents selon le protocole commun (voir README.md) :
# même agent bancaire (gemini-3.5-flash-lite, outils get_balance et get_transactions),
# 4 scénarios répétés 10 fois. Affiche une ligne CSV par scénario.
# Lancement : venv\Scripts\python measure.py

import statistics
import time

from dotenv import load_dotenv
from strands import Agent, tool
from strands.models.gemini import GeminiModel

load_dotenv()

FRAMEWORK = "AWS Strands Agents"
REPETITIONS = 10
PAUSE = 10  # secondes entre deux essais, pour respecter le quota gratuit

# La clé est lue dans GOOGLE_API_KEY ; délai maximal de 60 s par appel (en millisecondes)
model = GeminiModel(model_id="gemini-3.5-flash-lite", client_args={"http_options": {"timeout": 60_000}})


@tool
def get_balance(account: str) -> str:
    """Renvoie le solde d'un compte ('courant' ou 'livret')."""
    return {"courant": "1 250 €", "livret": "8 400 €"}.get(account, "Compte inconnu")


@tool
def get_transactions(min_amount: float) -> str:
    """Renvoie les transactions des trois derniers mois supérieures à un montant en euros."""
    transactions = [("Loyer", 780), ("Garage", 620), ("Courses", 95), ("Billets de train", 510)]
    resultat = [f"{nom} : {montant} €" for nom, montant in transactions if montant >= min_amount]
    return "\n".join(resultat) or "Aucune transaction"


def creer_agent():
    # Un agent neuf à chaque essai : historique et compteurs repartent de zéro
    return Agent(
        model=model,
        tools=[get_balance, get_transactions],
        system_prompt="Tu es un assistant bancaire. Utilise les outils, n'invente jamais de données.",
        callback_handler=None,  # pas d'affichage de la réponse dans la console
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
        agent = creer_agent()
        debut = time.perf_counter()
        try:
            result = agent(question)
        except Exception as erreur:
            print(f"  essai en échec : {type(erreur).__name__} : {str(erreur)[:200]}")
            time.sleep(PAUSE)
            continue
        durees.append(time.perf_counter() - debut)

        metriques = result.metrics
        outils_appeles = set(metriques.tool_metrics)
        usage = metriques.accumulated_usage

        appels.append(metriques.cycle_count)
        entrees.append(usage["inputTokens"])
        sorties.append(usage["outputTokens"])
        reussites += outils_appeles == outils_attendus
        time.sleep(PAUSE)

    if durees:
        print(
            f"{FRAMEWORK};{question};{statistics.median(durees):.2f};{min(durees):.2f};{max(durees):.2f};"
            f"{statistics.median(appels):.0f};{statistics.median(entrees):.0f};"
            f"{statistics.median(sorties):.0f};{reussites}/{len(durees)};{REPETITIONS - len(durees)}"
        )
