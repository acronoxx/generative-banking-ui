# Observabilité en local : l'agent LangChain des mesures est instrumenté avec
# OpenTelemetry (OpenInference) et ses traces sont envoyées à Phoenix, lancé
# sur ce poste (`phoenix serve`). Aucune trace ne quitte la machine.
#
# Lancement : terminal 1 `phoenix serve`, terminal 2 `python trace_agent.py`,
# puis ouvrir http://localhost:6006 pour parcourir les traces.

import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from openinference.instrumentation.langchain import LangChainInstrumentor
from phoenix.client import Client
from phoenix.otel import register

load_dotenv()

PROJET = "assistant-bancaire"

# Exporteur OpenTelemetry vers le Phoenix local ; chaque étape de LangChain
# (agent, appel du modèle, appel d'outil) devient un span
fournisseur = register(endpoint="http://localhost:6006/v1/traces", project_name=PROJET, batch=False)
LangChainInstrumentor().instrument(tracer_provider=fournisseur)


def get_balance(account: str) -> str:
    """Renvoie le solde d'un compte ('courant' ou 'livret')."""
    return {"courant": "1 250 €", "livret": "8 400 €"}.get(account, "Compte inconnu")


def get_transactions(min_amount: float) -> str:
    """Renvoie les transactions des trois derniers mois supérieures à un montant en euros."""
    transactions = [("Loyer", 780), ("Garage", 620), ("Courses", 95), ("Billets de train", 510)]
    resultat = [f"{nom} : {montant} €" for nom, montant in transactions if montant >= min_amount]
    return "\n".join(resultat) or "Aucune transaction"


modele = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
agent = create_agent(
    model=init_chat_model(f"google_genai:{modele}", timeout=60, max_retries=0),
    tools=[get_balance, get_transactions],
    system_prompt="Tu es un assistant bancaire. Utilise les outils, n'invente jamais de données.",
)

for question in [
    "Quel est le solde de mon compte courant ?",
    "Quel est mon solde courant, et quelles dépenses dépassent 500 € ?",
]:
    reponse = agent.invoke({"messages": [{"role": "user", "content": question}]})
    print(question, "->", reponse["messages"][-1].text)

# Relecture des traces depuis Phoenix, pour vérifier ce qui a été enregistré
spans = Client(base_url="http://localhost:6006").spans.get_spans_dataframe(project_identifier=PROJET)
colonnes = [
    "name",
    "span_kind",
    "latency_ms",
    "attributes.llm.token_count.prompt",
    "attributes.llm.token_count.completion",
    "attributes.input.value",
]
spans["latency_ms"] = (spans["end_time"] - spans["start_time"]).dt.total_seconds() * 1000
print(f"\n{len(spans)} spans enregistrés, {spans['context.trace_id'].nunique()} traces")
print(spans[[c for c in colonnes if c in spans.columns]].sort_values("name").to_string(max_colwidth=60))
