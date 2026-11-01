"""Catalogue de composants + schema render_ui + validation.
Source unique : COMPONENT_SPECS genere a la fois le JSON Schema envoye au modele et la validation.
(Dans l'application finale : meme schema, valide cote serveur avec Zod / JSON Schema.)"""
from .config import strict_ui

PRODUCT_IDS = ["PRD-001", "PRD-002", "PRD-003", "PRD-004", "PRD-005"]
MAX_COMPONENTS = 6

# nom -> {champ: "string" | "string[]" | [valeurs autorisees]}
COMPONENT_SPECS = {
    "SummaryCard":      {"label": "string", "data_ref": "string", "field": ["total_eur", "count"]},
    "BarChart":         {"data_refs": "string[]"},
    "TransactionTable": {"data_ref": "string"},
    "AccountList":      {"data_ref": "string"},
    "OfferCard":        {"product_id": PRODUCT_IDS},
    "TransferForm":     {"data_ref": "string"},
    "ErrorFallback":    {"message": "string"},
    "TextBlock":        {"text": "string"},
}
# type de resultat d'outil que le composant a le droit de referencer
REQUIRED_KIND = {"SummaryCard": "transactions_summary", "BarChart": "transactions_summary",
                 "TransactionTable": "transactions_summary", "AccountList": "accounts",
                 "TransferForm": "transfer_prepared"}


def _field_schema(spec):
    if spec == "string":
        return {"type": "string"}
    if spec == "string[]":
        return {"type": "array", "items": {"type": "string"}}
    return {"type": "string", "enum": spec}


def _component_schema(name, fields):
    props = {"component": {"type": "string", "enum": [name]}}
    props.update({k: _field_schema(v) for k, v in fields.items()})
    return {"type": "object", "additionalProperties": False, "required": list(props), "properties": props}


def render_ui_tool():
    return {"type": "function", "function": {
        "name": "render_ui", "strict": strict_ui(),
        "description": ("Affiche l'interface au client. N'utilise QUE les composants du catalogue. "
                        "Les donnees sont referencees par data_ref (valeur 'ref' d'un resultat d'outil), "
                        "jamais recopiees. Maximum %d composants." % MAX_COMPONENTS),
        "parameters": {"type": "object", "additionalProperties": False, "required": ["title", "components"],
                       "properties": {"title": {"type": "string"},
                                      "components": {"type": "array", "items": {"anyOf": [
                                          _component_schema(n, f) for n, f in COMPONENT_SPECS.items()]}}}}}}


def validate_ui(ui, results):
    """Retourne la liste des erreurs (vide = valide). Messages lisibles : renvoyes au modele pour le retry."""
    errs = []
    if not isinstance(ui, dict):
        return ["La sortie doit etre un objet {title, components}."]
    extra = set(ui) - {"title", "components"}
    if extra:
        errs.append(f"Champs inconnus a la racine : {sorted(extra)}")
    if not isinstance(ui.get("title"), str):
        errs.append("title manquant ou non texte.")
    comps = ui.get("components")
    if not isinstance(comps, list) or not comps:
        return errs + ["components doit etre une liste non vide."]
    if len(comps) > MAX_COMPONENTS:
        errs.append(f"Trop de composants ({len(comps)} > {MAX_COMPONENTS}).")
    for i, c in enumerate(comps):
        if not isinstance(c, dict) or c.get("component") not in COMPONENT_SPECS:
            errs.append(f"components[{i}] : composant inconnu {c.get('component') if isinstance(c, dict) else c!r}. "
                        f"Autorises : {sorted(COMPONENT_SPECS)}")
            continue
        name, spec = c["component"], COMPONENT_SPECS[c["component"]]
        missing, unknown = set(spec) - set(c), set(c) - set(spec) - {"component"}
        if missing:
            errs.append(f"{name} : champs manquants {sorted(missing)}")
        if unknown:
            errs.append(f"{name} : champs non autorises {sorted(unknown)}")
        for k, sp in spec.items():
            if k not in c:
                continue
            v = c[k]
            if sp == "string" and not isinstance(v, str):
                errs.append(f"{name}.{k} doit etre un texte.")
            elif sp == "string[]" and not (isinstance(v, list) and v and all(isinstance(x, str) for x in v)):
                errs.append(f"{name}.{k} doit etre une liste de textes non vide.")
            elif isinstance(sp, list) and v not in sp:
                errs.append(f"{name}.{k} = {v!r} non autorise. Valeurs : {sp}")
        refs = [c["data_ref"]] if isinstance(c.get("data_ref"), str) else (c.get("data_refs") or [])
        for r in refs:
            if not isinstance(r, str) or r not in results:
                errs.append(f"{name} : data_ref inconnu {r!r} (utilise la valeur 'ref' d'un resultat d'outil).")
            elif name in REQUIRED_KIND and results[r].get("kind") != REQUIRED_KIND[name]:
                errs.append(f"{name} ne peut pas afficher {r} (type {results[r].get('kind')}, attendu {REQUIRED_KIND[name]}).")
    return errs
