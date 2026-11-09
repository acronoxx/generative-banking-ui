# API bancaire REST ordinaire, à laquelle on ajoute seulement un « manuel » UTCP.
# Les outils restent les routes existantes : aucun serveur intermédiaire n'est ajouté.
import uvicorn
from fastapi import FastAPI

app = FastAPI()
API = "http://127.0.0.1:8100"

SOLDES = {"courant": 1250, "livret": 8400}
TRANSACTIONS = [("Loyer", 780), ("Garage", 620), ("Courses", 95), ("Billets de train", 510)]


# --- Routes existantes de l'API -------------------------------------------
@app.get("/comptes/{account}/solde")
def solde(account: str):
    return {"compte": account, "solde": SOLDES.get(account)}


@app.get("/transactions")
def transactions(min_amount: float = 0):
    return [{"libelle": nom, "montant": montant} for nom, montant in TRANSACTIONS if montant >= min_amount]


# --- Manuel UTCP : décrit comment appeler directement ces routes ----------
@app.get("/utcp")
def manuel():
    return {
        "manual_version": "1.0.0",
        "utcp_version": "1.0.2",
        "tools": [
            {
                "name": "get_balance",
                "description": "Renvoie le solde d'un compte ('courant' ou 'livret').",
                "tags": ["banque"],
                "inputs": {"type": "object", "properties": {"account": {"type": "string"}}, "required": ["account"]},
                "tool_call_template": {
                    "call_template_type": "http",
                    "url": API + "/comptes/{account}/solde",
                    "http_method": "GET",
                },
            },
            {
                "name": "get_transactions",
                "description": "Renvoie les transactions des trois derniers mois supérieures à un montant en euros.",
                "tags": ["banque"],
                "inputs": {"type": "object", "properties": {"min_amount": {"type": "number"}}, "required": ["min_amount"]},
                "tool_call_template": {
                    "call_template_type": "http",
                    "url": API + "/transactions",
                    "http_method": "GET",
                },
            },
        ],
    }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8100)
