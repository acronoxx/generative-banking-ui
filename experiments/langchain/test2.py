# Essai LangChain : validation humaine d'un virement (HumanInTheLoopMiddleware),
# avec état sauvegardé par un checkpointer. Utilise un modèle Claude :
# clé ANTHROPIC_API_KEY requise dans .env.

from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

from dotenv import load_dotenv
load_dotenv()


def get_balance(account: str) -> str:
    """Renvoie le solde d'un compte ('courant' ou 'livret')."""
    return {"courant": "1 250 €", "livret": "8 400 €"}.get(account, "Compte inconnu")


def prepare_transfer(amount: float, beneficiary: str) -> str:
    """Effectue un virement d'un montant en euros vers un bénéficiaire."""
    return f"Virement de {amount} € vers {beneficiary} effectué."


agent = create_agent(
    model="anthropic:claude-haiku-5-5",
    tools=[get_balance, prepare_transfer],
    system_prompt="Tu es un assistant bancaire.",
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "prepare_transfer": {"allowed_decisions": ["approve", "reject"]},
                "get_balance": False,
            }
        )
    ],
    checkpointer=InMemorySaver(),
)

config = {"configurable": {"thread_id": "conversation-1"}}

result = agent.invoke(
    {"messages": [{"role": "user", "content": "Fais un virement de 500 € à Alice."}]},
    config=config,
    version="v2",
)

if result.interrupts:
    for interruption in result.interrupts:
        for action in interruption.value["action_requests"]:
            print("Action en attente :", action)

    choix = input("Confirmer ? (o/n) ")
    if choix == "o":
        decision = {"type": "approve"}
    else:
        decision = {"type": "reject", "message": "L'utilisateur a refusé. Ne pas réessayer."}

    agent.invoke(Command(resume={"decisions": [decision]}), config=config, version="v2")

agent.get_state(config).values["messages"][-1].pretty_print()
