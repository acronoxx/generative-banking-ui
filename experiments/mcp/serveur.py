# Serveur MCP exposant les deux outils bancaires des essais.
# Lancé par le client (transport stdio), il n'a pas besoin d'être démarré à la main.
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("banque")


@mcp.tool()
def get_balance(account: str) -> str:
    """Renvoie le solde d'un compte ('courant' ou 'livret')."""
    return {"courant": "1 250 €", "livret": "8 400 €"}.get(account, "Compte inconnu")


@mcp.tool()
def get_transactions(min_amount: float) -> str:
    """Renvoie les transactions des trois derniers mois supérieures à un montant en euros."""
    transactions = [("Loyer", 780), ("Garage", 620), ("Courses", 95), ("Billets de train", 510)]
    resultat = [f"{nom} : {montant} €" for nom, montant in transactions if montant >= min_amount]
    return "\n".join(resultat) or "Aucune transaction"


if __name__ == "__main__":
    mcp.run()  # transport stdio par défaut
