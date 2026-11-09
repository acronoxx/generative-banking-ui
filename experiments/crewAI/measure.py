# Mesure du framework CrewAI selon le protocole commun (voir README.md) :
# même agent bancaire (gemini-3.5-flash-lite, outils get_balance et get_transactions),
# 4 scénarios répétés 10 fois. Affiche une ligne CSV par scénario.
# Lancement : venv\Scripts\python measure.py (Python 3.13 au plus)

import statistics
import time

from dotenv import load_dotenv
from crewai import LLM, Agent
from crewai.tools import tool

load_dotenv()

FRAMEWORK = "CrewAI (traces désactivées)"
REPETITIONS = 10
PAUSE = 10  # secondes entre deux essais, pour respecter le quota gratuit

outils_appeles = set()
journal = open("resultats.csv", "a", encoding="utf-8")


def noter(ligne):
    # Affiche la ligne et l'ajoute au fichier resultats.csv
    print(ligne)
    journal.write(ligne + "\n")
    journal.flush()


@tool("get_balance")
def get_balance(account: str) -> str:
    """Renvoie le solde d'un compte ('courant' ou 'livret')."""
    outils_appeles.add("get_balance")
    return {"courant": "1 250 €", "livret": "8 400 €"}.get(account, "Compte inconnu")


@tool("get_transactions")
def get_transactions(min_amount: float) -> str:
    """Renvoie les transactions des trois derniers mois supérieures à un montant en euros."""
    outils_appeles.add("get_transactions")
    transactions = [("Loyer", 780), ("Garage", 620), ("Courses", 95), ("Billets de train", 510)]
    resultat = [f"{nom} : {montant} €" for nom, montant in transactions if montant >= min_amount]
    return "\n".join(resultat) or "Aucune transaction"


# Chaque scénario : une question et les outils qui doivent être appelés
SCENARIOS = [
    ("Quel est le solde de mon compte courant ?", {"get_balance"}),
    ("Quelles dépenses dépassent 500 € ?", {"get_transactions"}),
    ("Quel est mon solde courant, et quelles dépenses dépassent 500 € ?", {"get_balance", "get_transactions"}),
    ("Bonjour, que peux-tu faire pour moi ?", set()),
]


def creer_agent():
    # Un agent neuf à chaque essai, pour que les compteurs de tokens repartent de zéro
    return Agent(
        role="Assistant bancaire",
        goal="Répondre aux questions du client sur ses comptes",
        backstory="Tu es un assistant bancaire. Utilise les outils, n'invente jamais de données.",
        llm=LLM(model="gemini/gemini-3.5-flash-lite", timeout=60),
        tools=[get_balance, get_transactions],
        verbose=False,
    )


def lire(usage, cle):
    if usage is None:
        return 0
    if isinstance(usage, dict):
        return usage.get(cle, 0) or 0
    return getattr(usage, cle, 0) or 0


noter("framework;question;duree_mediane_s;duree_min_s;duree_max_s;appels_modele;tokens_entree;tokens_sortie;reussite;erreurs")

for question, outils_attendus in SCENARIOS:
    durees, appels, entrees, sorties, reussites = [], [], [], [], 0

    for _ in range(REPETITIONS):
        outils_appeles.clear()
        agent = creer_agent()
        debut = time.perf_counter()
        try:
            result = agent.kickoff(question)
        except Exception as erreur:
            noter(f"  essai en échec : {type(erreur).__name__} : {str(erreur)[:200]}")
            time.sleep(PAUSE)
            continue
        durees.append(time.perf_counter() - debut)

        usage = result.usage_metrics
        appels.append(lire(usage, "successful_requests"))
        entrees.append(lire(usage, "prompt_tokens"))
        sorties.append(lire(usage, "completion_tokens"))
        reussites += set(outils_appeles) == outils_attendus
        time.sleep(PAUSE)

    if durees:
        noter(
            f"{FRAMEWORK};{question};{statistics.median(durees):.2f};{min(durees):.2f};{max(durees):.2f};"
            f"{statistics.median(appels):.0f};{statistics.median(entrees):.0f};"
            f"{statistics.median(sorties):.0f};{reussites}/{len(durees)};{REPETITIONS - len(durees)}"
        )

journal.close()
