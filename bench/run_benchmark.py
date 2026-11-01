"""Lance le benchmark.  Exemples (depuis la racine du projet) :
  python -m bench.run_benchmark --mock good                      # test de la mecanique, sans cle
  python -m bench.run_benchmark --models luna_none --levels 1,2  # vrais appels, niveaux 1 et 2
  python -m bench.run_benchmark --models luna_none,sol --runs 5 --allow-attacks --yes
"""
import argparse, csv, json, time
from datetime import datetime
from . import config
from .agent import run_conversation
from .cases import build_cases
from .checks import evaluate
from .llm import complete

FIELDS = ["model", "case_id", "level", "title", "run", "passed", "tool_ok", "args_ok", "final_ok", "components_ok",
          "schema_first_try", "schema_final", "numbers_ok", "safe_ok", "profile_ok", "final_type", "ui_components",
          "ui_retries", "llm_calls", "latency_s", "tokens_in", "tokens_out", "cost_usd", "prepared_transfers",
          "first_call", "error"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default="luna_none", help="noms de models.json, separes par des virgules")
    ap.add_argument("--mock", choices=["good", "sloppy"], help="faux modele (pas de reseau)")
    ap.add_argument("--levels", default="1,2,3,4,5", help="niveaux a lancer")
    ap.add_argument("--cases", help="ids precis, ex. SN1,SN2")
    ap.add_argument("--runs", type=int, default=1, help="repetitions par cas (niveau 6 : stabilite)")
    ap.add_argument("--allow-attacks", action="store_true", help="inclure injections / extraction (prevenir Sopra avant !)")
    ap.add_argument("--sleep", type=float, default=0.0, help="pause (s) entre deux conversations (quotas)")
    ap.add_argument("--yes", action="store_true", help="confirmer un grand nombre d'appels")
    ap.add_argument("--label", default="")
    a = ap.parse_args()
    config.load_env()

    cases = build_cases()
    if a.cases:
        ids = set(a.cases.split(","))
        cases = [c for c in cases if c.id in ids]
    else:
        levels = {int(x) for x in a.levels.split(",")}
        cases = [c for c in cases if c.level in levels]
    skipped = [c.id for c in cases if c.attack and not a.allow_attacks]
    cases = [c for c in cases if a.allow_attacks or not c.attack]
    if skipped:
        print(f"[info] cas d'attaque ignores (ajouter --allow-attacks apres avoir prevenu Sopra) : {', '.join(skipped)}")

    if a.mock:
        from .mock_llm import make_mock
        mock = make_mock(a.mock)
        runs = [(f"MOCK-{a.mock}", {"label": f"MOCK {a.mock}", "price_in": 0.1, "price_out": 0.5}, mock)]
    else:
        models, runs = config.load_models(), []
        for name in a.models.split(","):
            if name not in models:
                raise SystemExit(f"Modele inconnu : {name}. Disponibles : {', '.join(models)}")
            miss = config.missing_env(models[name])
            if miss:
                raise SystemExit(f"Variables manquantes dans .env pour {name} : {', '.join(miss)}")
            runs.append((name, models[name], complete))

    n_conv = len(runs) * len(cases) * a.runs
    print(f"[info] {len(cases)} cas x {a.runs} run(s) x {len(runs)} modele(s) = {n_conv} conversations")
    if n_conv > 100 and not a.yes and not a.mock:
        raise SystemExit("Plus de 100 conversations : prevenez M. Gauthier (Sopra), puis relancez avec --yes.")

    config.RESULTS.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S") + (f"_{a.label}" if a.label else "")
    csv_path, jsonl_path = config.RESULTS / f"{stamp}.csv", config.RESULTS / f"{stamp}.jsonl"
    with open(csv_path, "w", newline="", encoding="utf-8") as fc, open(jsonl_path, "w", encoding="utf-8") as fj:
        w = csv.DictWriter(fc, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        for name, entry, llm in runs:
            for case in cases:
                for k in range(1, a.runs + 1):
                    run = run_conversation(llm, entry, case)
                    r = evaluate(case, run)
                    ts = run["turns"]
                    row = dict(r, model=name, case_id=case.id, level=case.level, title=case.title, run=k,
                               ui_retries=sum(len(t["ui_attempts"]) - sum(t["ui_attempts"]) for t in ts),
                               llm_calls=sum(t["llm_calls"] for t in ts),
                               latency_s=round(sum(t["latency_s"] for t in ts), 2),
                               tokens_in=sum(t["tokens_in"] for t in ts), tokens_out=sum(t["tokens_out"] for t in ts))
                    row["cost_usd"] = round((row["tokens_in"] * entry.get("price_in", 0) + row["tokens_out"] * entry.get("price_out", 0)) / 1e6, 6)
                    w.writerow(row)
                    fc.flush()
                    fj.write(json.dumps(dict(row, turns=ts, messages=run["messages"]), ensure_ascii=False, default=str) + "\n")
                    fj.flush()
                    flag = "OK  " if row["passed"] else "FAIL"
                    print(f"{flag} {name:14s} {case.id:6s} run{k}  {row['latency_s']:5.1f}s  {row['final_type']}"
                          + (f"  ERREUR: {row['error']}" if row["error"] else ""))
                    if a.sleep:
                        time.sleep(a.sleep)
    print(f"\nResultats : {csv_path}\nTraces completes : {jsonl_path}")
    from .report import make_report
    make_report([csv_path])


if __name__ == "__main__":
    main()
