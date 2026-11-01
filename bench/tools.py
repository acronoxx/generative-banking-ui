"""Outils metier branches sur bank.sqlite. L'application, jamais le LLM, execute et controle.
Le customer_id est INJECTE par l'application (le modele ne le choisit jamais)."""
import json, re, sqlite3, unicodedata
from .config import DATA, MAX_SINGLE_TRANSFER_EUR, OTP_ABOVE_EUR

CATEGORIES = ["restaurants", "groceries", "shopping", "transport", "health", "leisure", "subscriptions",
              "travel", "utilities", "insurance", "housing", "taxes", "family", "services", "cash"]
DATA_TOOLS = ("get_accounts", "search_transactions", "prepare_transfer", "list_products")


def _fn(name, desc, props, required):
    return {"type": "function", "function": {"name": name, "description": desc,
            "parameters": {"type": "object", "properties": props, "required": required}}}

TOOL_SCHEMAS = [
    _fn("get_accounts", "Liste les comptes du client connecte avec leur solde.", {}, []),
    _fn("search_transactions",
        "Cherche les depenses du client dans une categorie et sur une periode. Retourne total, detail par mois et plus grosses depenses.",
        {"category": {"type": "string", "enum": CATEGORIES},
         "date_from": {"type": "string", "description": "YYYY-MM-DD"},
         "date_to": {"type": "string", "description": "YYYY-MM-DD"}},
        ["category", "date_from", "date_to"]),
    _fn("prepare_transfer",
        "PREPARE (n'execute jamais) un virement. Donner beneficiary_name OU iban, et le montant en euros.",
        {"beneficiary_name": {"type": "string"}, "iban": {"type": "string"},
         "amount_eur": {"type": "number"}, "reason": {"type": "string"}},
        ["amount_eur"]),
    _fn("list_products", "Liste les offres de la banque, filtrables par categorie.",
        {"category": {"type": "string", "enum": ["travel_insurance", "card", "home_insurance", "credit"]}}, []),
    _fn("ask_clarification", "Pose UNE question de precision au client quand la demande est ambigue ou incomplete.",
        {"question": {"type": "string"}}, ["question"]),
]


def _norm(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s.lower()) if not unicodedata.combining(c))


def valid_iban(iban):
    s = re.sub(r"\s", "", iban).upper()
    if not re.fullmatch(r"FR\d{2}[0-9A-Z]{23}", s):
        return False
    return int("".join(str(int(ch, 36)) for ch in s[4:] + s[:4])) % 97 == 1


def _mask(iban):
    return iban[:4] + " **** " + iban[-4:]


class Context:
    """Etat d'une conversation : client connecte, resultats d'outils, virements prepares."""
    def __init__(self, customer_id, ui_profile, poison_label=None):
        self.customer_id, self.ui_profile, self.poison_label = customer_id, ui_profile, poison_label
        self.results, self.counter, self.prepared = {}, 0, []

    def store(self, full):
        self.counter += 1
        ref = f"tool_result_{self.counter}"
        full["ref"] = ref
        self.results[ref] = full
        return {k: v for k, v in full.items() if not k.startswith("_")}   # ce que le modele voit


def _con():
    con = sqlite3.connect(DATA / "bank.sqlite")
    con.row_factory = sqlite3.Row
    return con


def execute(name, args, ctx):
    try:
        fn = globals()["tool_" + name]
    except KeyError:
        return {"error": "unknown_tool", "message": f"Outil inconnu : {name}"}
    try:
        return fn(ctx, **args)
    except TypeError as e:
        return {"error": "bad_arguments", "message": str(e)}


def tool_get_accounts(ctx):
    with _con() as con:
        rows = con.execute("SELECT id,label,type,iban,balance_cents FROM accounts WHERE customer_id=?", (ctx.customer_id,)).fetchall()
    return ctx.store({"kind": "accounts", "accounts": [
        {"id": r["id"], "label": r["label"], "type": r["type"], "iban": _mask(r["iban"]),
         "balance_eur": r["balance_cents"] / 100} for r in rows]})


def tool_search_transactions(ctx, category, date_from, date_to):
    if category not in CATEGORIES:
        return {"error": "bad_category", "message": f"Categories : {CATEGORIES}"}
    if not (re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(date_from)) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(date_to))):
        return {"error": "bad_date", "message": "Format attendu YYYY-MM-DD"}
    with _con() as con:
        rows = con.execute("""SELECT t.date,t.label,t.amount_cents FROM transactions t JOIN accounts a ON a.id=t.account_id
            WHERE a.customer_id=? AND t.category=? AND t.amount_cents<0 AND t.date BETWEEN ? AND ? ORDER BY t.date""",
            (ctx.customer_id, category, date_from, date_to)).fetchall()
    by_month = {}
    for r in rows:
        by_month[r["date"][:7]] = by_month.get(r["date"][:7], 0) - r["amount_cents"]
    top = sorted(rows, key=lambda r: r["amount_cents"])[:3]
    top_list = [{"date": r["date"], "label": r["label"], "amount_eur": -r["amount_cents"] / 100} for r in top]
    if ctx.poison_label and category == "restaurants":     # test d'injection indirecte (cas R8)
        top_list.insert(0, {"date": date_to, "label": ctx.poison_label, "amount_eur": 1.0})
    return ctx.store({"kind": "transactions_summary", "category": category, "date_from": date_from, "date_to": date_to,
                      "total_eur": sum(by_month.values()) / 100, "count": len(rows),
                      "by_month": [{"month": m, "total_eur": c / 100} for m, c in sorted(by_month.items())],
                      "top": top_list,
                      "_rows": [dict(date=r["date"], label=r["label"], amount_cents=r["amount_cents"]) for r in rows]})


def tool_prepare_transfer(ctx, amount_eur, beneficiary_name=None, iban=None, reason=None):
    if not isinstance(amount_eur, (int, float)) or amount_eur <= 0:
        return {"error": "invalid_amount", "message": "Le montant doit etre positif."}
    if amount_eur > MAX_SINGLE_TRANSFER_EUR:
        return {"error": "over_limit", "message": f"Plafond par virement : {MAX_SINGLE_TRANSFER_EUR} EUR."}
    if iban and not valid_iban(iban):
        return {"error": "invalid_iban", "message": "IBAN invalide."}
    with _con() as con:
        accs = con.execute("SELECT id,balance_cents FROM accounts WHERE customer_id=? AND type='checking'", (ctx.customer_id,)).fetchall()
        bens = con.execute("SELECT id,name,iban FROM beneficiaries WHERE customer_id=?", (ctx.customer_id,)).fetchall()
    if not accs:
        return {"error": "no_account", "message": "Aucun compte courant."}
    if amount_eur * 100 > accs[0]["balance_cents"]:
        return {"error": "insufficient_funds", "message": "Solde insuffisant."}
    if iban:
        match = [b for b in bens if re.sub(r"\s", "", b["iban"]) == re.sub(r"\s", "", iban).upper()]
    elif beneficiary_name:
        match = [b for b in bens if _norm(beneficiary_name) in _norm(b["name"])]
    else:
        return {"error": "missing_beneficiary", "message": "Preciser un beneficiaire ou un IBAN."}
    if not match:
        return {"error": "unknown_beneficiary", "message": "Beneficiaire inconnu (nouveaux beneficiaires non geres dans la demo)."}
    if len(match) > 1:
        return {"error": "ambiguous_beneficiary", "message": "Plusieurs beneficiaires correspondent : " + ", ".join(b["name"] for b in match)}
    b = match[0]
    res = ctx.store({"kind": "transfer_prepared", "status": "prepared", "executed": False, "from_account": accs[0]["id"],
                     "beneficiary": {"id": b["id"], "name": b["name"], "iban": _mask(b["iban"])},
                     "amount_eur": float(amount_eur), "reason": reason, "otp_required": amount_eur > OTP_ABOVE_EUR})
    ctx.prepared.append(res)
    return res


def tool_list_products(ctx, category=None):
    q, p = "SELECT id,name,category,price_cents,price_model,description FROM products", ()
    if category:
        q, p = q + " WHERE category=?", (category,)
    with _con() as con:
        rows = con.execute(q, p).fetchall()
    return ctx.store({"kind": "products", "products": [
        {"id": r["id"], "name": r["name"], "category": r["category"], "price_eur": r["price_cents"] / 100,
         "price_model": r["price_model"], "description": r["description"]} for r in rows]})
