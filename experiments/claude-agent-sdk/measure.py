# Essai préparé mais NON exécuté : le Claude Agent SDK ne fonctionne qu'avec les
# modèles Claude, et le protocole commun utilise Gemini. Il faut une clé
# ANTHROPIC_API_KEY dans le fichier .env pour le lancer. Les résultats ne seront
# pas directement comparables (modèle différent).
import asyncio
import statistics
import time
from typing import Any

from dotenv import load_dotenv
from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ResultMessage,
    ToolUseBlock,
    create_sdk_mcp_server,
    query,
    tool,
)

load_dotenv()

FRAMEWORK = "Claude Agent SDK"
MODELE = "claude-haiku-5-5"
REPETITIONS = 10
PAUSE = 10  # secondes entre deux essais


def texte(contenu: str) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": contenu}]}


@tool("get_balance", "Renvoie le solde d'un compte ('courant' ou 'livret').", {"account": str})
async def get_balance(args: dict[str, Any]) -> dict[str, Any]:
    return texte({"courant": "1 250 €", "livret": "8 400 €"}.get(args["account"], "Compte inconnu"))


@tool(
    "get_transactions",
    "Renvoie les transactions des trois derniers mois supérieures à un montant en euros.",
    {"min_amount": float},
)
async def get_transactions(args: dict[str, Any]) -> dict[str, Any]:
    transactions = [("Loyer", 780), ("Garage", 620), ("Courses", 95), ("Billets de train", 510)]
    resultat = [f"{nom} : {montant} €" for nom, montant in transactions if montant >= args["min_amount"]]
    return texte("\n".join(resultat) or "Aucune transaction")


# Les outils sont servis par un serveur MCP exécuté dans le même processus
banque = create_sdk_mcp_server(name="banque", version="1.0.0", tools=[get_balance, get_transactions])

options = ClaudeAgentOptions(
    model=MODELE,
    system_prompt="Tu es un assistant bancaire. Utilise les outils, n'invente jamais de données.",
    mcp_servers={"banque": banque},
    tools=[],  # aucun outil intégré (fichiers, commandes) : seulement les outils bancaires
    allowed_tools=["mcp__banque__get_balance", "mcp__banque__get_transactions"],
    setting_sources=[],  # n'applique aucune configuration locale de Claude Code
)

# Chaque scénario : une question et les outils qui doivent être appelés
SCENARIOS = [
    ("Quel est le solde de mon compte courant ?", {"get_balance"}),
    ("Quelles dépenses dépassent 500 € ?", {"get_transactions"}),
    ("Quel est mon solde courant, et quelles dépenses dépassent 500 € ?", {"get_balance", "get_transactions"}),
    ("Bonjour, que peux-tu faire pour moi ?", set()),
]


async def poser(question):
    outils_appeles, resultat = set(), None
    async for message in query(prompt=question, options=options):
        if isinstance(message, AssistantMessage):
            for bloc in message.content:
                if isinstance(bloc, ToolUseBlock):
                    # Nom complet de la forme mcp__banque__get_balance
                    outils_appeles.add(bloc.name.removeprefix("mcp__banque__"))
        elif isinstance(message, ResultMessage):
            resultat = message
    if resultat is None:
        raise RuntimeError("aucun message de résultat reçu")
    return outils_appeles, resultat


async def main():
    print("framework;question;duree_mediane_s;duree_min_s;duree_max_s;appels_modele;tokens_entree;tokens_sortie;reussite;erreurs")

    for question, outils_attendus in SCENARIOS:
        durees, appels, entrees, sorties, reussites = [], [], [], [], 0

        for _ in range(REPETITIONS):
            debut = time.perf_counter()
            try:
                outils_appeles, resultat = await poser(question)
            except Exception as erreur:
                print(f"  essai en échec : {type(erreur).__name__} : {str(erreur)[:200]}")
                await asyncio.sleep(PAUSE)
                continue
            durees.append(time.perf_counter() - debut)

            usage = resultat.usage or {}
            appels.append(resultat.num_turns)
            entrees.append(
                usage.get("input_tokens", 0)
                + usage.get("cache_read_input_tokens", 0)
                + usage.get("cache_creation_input_tokens", 0)
            )
            sorties.append(usage.get("output_tokens", 0))
            reussites += outils_appeles == outils_attendus
            await asyncio.sleep(PAUSE)

        if durees:
            print(
                f"{FRAMEWORK};{question};{statistics.median(durees):.2f};{min(durees):.2f};{max(durees):.2f};"
                f"{statistics.median(appels):.0f};{statistics.median(entrees):.0f};"
                f"{statistics.median(sorties):.0f};{reussites}/{len(durees)};{REPETITIONS - len(durees)}"
            )


asyncio.run(main())
