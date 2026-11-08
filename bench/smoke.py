"""Niveaux 0 et 1 : connexion + un appel d'outil, pour chaque modele configure dans .env.
  python -m bench.smoke              (tous les modeles dont les variables sont presentes)
  python -m bench.smoke luna_none    (un seul)"""
import sys
from . import config
from .llm import complete
from .tools import TOOL_SCHEMAS

HINTS = {"UnsupportedParamsError": "LiteLLM refuse un parametre : verifier allowed_openai_params dans bench/llm.py.",
         "reasoning_effort": "Function calling refuse avec un effort de raisonnement : utiliser luna_none (effort none) ou l'API Responses.",
         "401": "Cle refusee : verifiez AZURE_API_KEY.", "404": "Deploiement introuvable : verifiez LLM_DEPLOYMENT_* (nom du DEPLOIEMENT) et AZURE_API_BASE.",
         "content_filter": "Bloque par le filtre de contenu Azure : a noter comme resultat de test.",
         "api_version": "Version d'API refusee : demandez la bonne a M. Gauthier."}


def main():
    config.load_env()
    models = config.load_models()
    names = sys.argv[1:] or list(models)
    for name in names:
        entry = models[name]
        miss = config.missing_env(entry)
        if miss:
            print(f"- {name}: ignore (variables manquantes : {', '.join(miss)})")
            continue
        print(f"\n=== {name} : {entry['label']} ===")
        msgs = [{"role": "system", "content": "Tu es l'assistant de Gen-UI Bank. Date : 2026-10-08."}]
        for label, user, tools in (("N0 appel simple", "Reponds uniquement : ok", None),
                                   ("N1 appel d'outil", "Combien ai-je depense en restaurants en juillet, aout et septembre 2026 ?", TOOL_SCHEMAS)):
            try:
                r = complete(entry, msgs + [{"role": "user", "content": user}], tools)
                print(f"[OK ] {label}: {r.latency_s:.2f}s, tokens {r.tokens_in}/{r.tokens_out}")
                print("      outils :", [(c['name'], c['arguments']) for c in r.tool_calls] or "aucun", "| texte :", (r.content or "")[:80])
            except Exception as e:  # noqa
                print(f"[ERR] {label}: {e.__class__.__name__}: {str(e)[:250]}")
                for k, h in HINTS.items():
                    if k in str(e):
                        print("      ->", h)


if __name__ == "__main__":
    main()
