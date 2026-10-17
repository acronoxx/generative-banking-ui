# Essai LangChain : agent avec les deux outils bancaires, pour une question.

from langchain.agents import create_agent

from dotenv import load_dotenv
load_dotenv()

def get_balance(account: str) -> str:
    """Renvoie le solde d'un compte ('courant' ou 'livret')."""
    soldes = {"courant": "1 250 €", "livret": "8 400 €"}
    return soldes.get(account, "Compte inconnu")


def get_transactions(min_amount: float) -> str:
    """Renvoie les transactions des trois derniers mois supérieures à un montant en euros."""
    transactions = [("Loyer", 780), ("Garage", 620), ("Courses", 95), ("Billets de train", 510)]
    resultat = [f"{nom} : {montant} €" for nom, montant in transactions if montant >= min_amount]
    return "\n".join(resultat) or "Aucune transaction"


agent = create_agent(
    model="google_genai:gemini-3.8-flash",
    tools=[get_balance, get_transactions],
    system_prompt="Tu es un assistant bancaire. Utilise les outils, n'invente jamais de données.",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "Quel est mon solde courant, et quelles dépenses dépassent 500 € ?"}]}
)

for message in result["messages"]:
    message.pretty_print()
