# Function calling « à la main », sans framework : c'est la boucle que les
# frameworks d'orchestration automatisent. Chaque étape est affichée.
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODELE = "gemini-3.5-flash-lite"


def get_balance(account: str) -> str:
    return {"courant": "1 250 €", "livret": "8 400 €"}.get(account, "Compte inconnu")


def get_transactions(min_amount: float) -> str:
    transactions = [("Loyer", 780), ("Garage", 620), ("Courses", 95), ("Billets de train", 510)]
    resultat = [f"{nom} : {montant} €" for nom, montant in transactions if montant >= min_amount]
    return "\n".join(resultat) or "Aucune transaction"


FONCTIONS = {"get_balance": get_balance, "get_transactions": get_transactions}

# 1. Déclaration des outils : un nom, une description et un schéma JSON des paramètres
DECLARATIONS = [
    {
        "name": "get_balance",
        "description": "Renvoie le solde d'un compte ('courant' ou 'livret').",
        "parameters": {"type": "object", "properties": {"account": {"type": "string"}}, "required": ["account"]},
    },
    {
        "name": "get_transactions",
        "description": "Renvoie les transactions des trois derniers mois supérieures à un montant en euros.",
        "parameters": {"type": "object", "properties": {"min_amount": {"type": "number"}}, "required": ["min_amount"]},
    },
]

client = genai.Client(http_options={"timeout": 60_000})
config = types.GenerateContentConfig(
    system_instruction="Tu es un assistant bancaire. Utilise les outils, n'invente jamais de données.",
    tools=[types.Tool(function_declarations=DECLARATIONS)],
    # Le SDK Python peut exécuter lui-même les fonctions : désactivé pour voir chaque étape
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
)

historique = [types.Content(role="user", parts=[types.Part(text="Quel est mon solde courant, et quelles dépenses dépassent 500 € ?")])]

for tour in range(1, 6):
    # 2. Le modèle reçoit la conversation et les déclarations
    reponse = client.models.generate_content(model=MODELE, contents=historique, config=config)
    usage = reponse.usage_metadata
    print(f"\n=== Appel {tour} au modèle ({usage.prompt_token_count} tokens en entrée, {usage.candidates_token_count} en sortie)")

    appels = reponse.function_calls or []
    if not appels:
        print("Réponse finale :\n" + reponse.text)
        break

    # 3. Le modèle n'exécute rien : il demande un ou plusieurs appels
    historique.append(reponse.candidates[0].content)
    resultats = []
    for appel in appels:
        print(f"Demande d'appel : {appel.name}({json.dumps(appel.args, ensure_ascii=False)})")
        # 4. L'application exécute la fonction et renvoie le résultat au modèle
        sortie = FONCTIONS[appel.name](**appel.args)
        print(f"Résultat renvoyé : {sortie!r}")
        resultats.append(types.Part.from_function_response(name=appel.name, response={"result": sortie}))
    historique.append(types.Content(role="user", parts=resultats))
