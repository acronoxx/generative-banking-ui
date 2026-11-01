"""Boucle agent minimale : message -> LLM -> outils (executes par l'application) -> LLM -> render_ui.
Le LLM demande, l'application valide et execute. Rien n'est jamais execute par le modele."""
import json, sqlite3
from . import config
from .tools import TOOL_SCHEMAS, Context, execute
from .ui_schema import render_ui_tool, validate_ui


def build_system_prompt(customer_id, ui_profile_id):
    with sqlite3.connect(config.DATA / "bank.sqlite") as con:
        con.row_factory = sqlite3.Row
        p = con.execute("SELECT * FROM ui_profiles WHERE id=?", (ui_profile_id,)).fetchone()
    rules = (f"profil {p['label']} : {p['max_components_per_screen']} composants maximum par ecran ; "
             f"vocabulaire {p['vocabulary']} ; graphiques {p['chart_complexity']}.")
    text = (config.PROMPTS / config.system_prompt_file()).read_text(encoding="utf-8")
    for k, v in {"{date}": config.REFERENCE_DATE, "{customer_id}": customer_id,
                 "{ui_profile}": ui_profile_id, "{profile_rules}": rules}.items():
        text = text.replace(k, v)
    return text


def all_tools():
    return TOOL_SCHEMAS + [render_ui_tool()]


def _assistant_msg(reply):
    m = {"role": "assistant", "content": reply.content}
    if reply.tool_calls:
        m["tool_calls"] = [{"id": c["id"], "type": "function",
                            "function": {"name": c["name"], "arguments": c["arguments"]}} for c in reply.tool_calls]
    return m


def run_turn(llm, entry, messages, ctx):
    """Traite un message utilisateur deja ajoute a `messages`. Retourne la trace du tour."""
    t = dict(tool_calls=[], final_type=None, final_text=None, ui=None, ui_attempts=[], ui_errors=[],
             llm_calls=0, latency_s=0.0, tokens_in=0, tokens_out=0, error=None)
    tools = all_tools()
    for _ in range(config.MAX_TURNS):
        try:
            reply = llm(entry, messages, tools)
        except Exception as e:  # noqa : filtre de contenu, 429, parametre refuse...
            t["error"], t["final_type"] = f"{e.__class__.__name__}: {str(e)[:300]}", "error"
            return t
        t["llm_calls"] += 1
        t["latency_s"] += reply.latency_s
        t["tokens_in"] += reply.tokens_in
        t["tokens_out"] += reply.tokens_out
        messages.append(_assistant_msg(reply))
        if not reply.tool_calls:
            t["final_type"], t["final_text"] = "text", reply.content or ""
            return t
        terminal = None
        for c in reply.tool_calls:
            try:
                args = json.loads(c["arguments"] or "{}")
            except json.JSONDecodeError:
                args, result = {}, {"error": "invalid_json", "message": "Arguments non JSON."}
                t["tool_calls"].append({"name": c["name"], "args": c["arguments"], "error": "invalid_json"})
            else:
                if c["name"] == "render_ui":
                    errs = validate_ui(args, ctx.results)
                    t["ui_attempts"].append(not errs)
                    if errs:
                        t["ui_errors"].append(errs)
                        result = {"error": "invalid_ui", "details": errs}
                    else:
                        result = {"status": "displayed"}
                        terminal = terminal or ("ui", args)
                    t["tool_calls"].append({"name": "render_ui", "args": args, "error": errs[0] if errs else None})
                elif c["name"] == "ask_clarification":
                    result = {"status": "asked"}
                    terminal = terminal or ("clarification", args.get("question", ""))
                    t["tool_calls"].append({"name": c["name"], "args": args, "error": None})
                else:
                    result = execute(c["name"], args, ctx)
                    t["tool_calls"].append({"name": c["name"], "args": args, "error": result.get("error")})
            messages.append({"role": "tool", "tool_call_id": c["id"], "content": json.dumps(result, ensure_ascii=False)})
        if terminal:
            t["final_type"] = terminal[0]
            if terminal[0] == "ui":
                t["ui"] = terminal[1]
            else:
                t["final_text"] = terminal[1]
            return t
        if len(t["ui_attempts"]) - sum(t["ui_attempts"]) > config.MAX_UI_RETRIES:
            t["final_type"] = "fallback"        # l'application afficherait ErrorFallback (< 5 s)
            return t
    t["final_type"] = "max_turns"
    return t


def run_conversation(llm, entry, case):
    ctx = Context(case.customer, case.ui_profile, case.poison_label)
    messages = [{"role": "system", "content": build_system_prompt(case.customer, case.ui_profile)}]
    turns = []
    for text in case.turns:
        messages.append({"role": "user", "content": text})
        t = run_turn(llm, entry, messages, ctx)
        turns.append(t)
        if t["error"]:
            break
    return dict(turns=turns, ctx=ctx, messages=messages)
