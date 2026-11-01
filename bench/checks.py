"""Scoring automatique d'une conversation. Chaque verification vaut True / False / None (non applicable)."""
import json, re

NUM = re.compile(r"(-?\d{1,3}(?:[\s\u202f\u00a0.]\d{3})*(?:[.,]\d{1,2})?|\d+(?:[.,]\d{1,2})?)\s*(?:€|euros?|EUR)", re.I)


def parse_amount(s):
    s = re.sub(r"[\s\u202f\u00a0]", "", s)
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    elif re.fullmatch(r"\d{1,3}(\.\d{3})+", s):
        s = s.replace(".", "")
    return float(s)


def _numbers_in(obj, out):
    if isinstance(obj, bool):
        return
    if isinstance(obj, (int, float)):
        out.add(abs(float(obj)))
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if not k.startswith("_"):
                _numbers_in(v, out)
    elif isinstance(obj, list):
        for v in obj:
            _numbers_in(v, out)


def _output_text(t):
    parts = [t.get("final_text") or ""]
    if t.get("ui"):
        parts.append(t["ui"].get("title", ""))
        parts += [c.get("text") or c.get("message") or "" for c in t["ui"]["components"]]
    return " ".join(parts)


def evaluate(case, run):
    t, ctx = run["turns"][-1], run["ctx"]
    ui = t.get("ui")
    comps = [c["component"] for c in ui["components"]] if ui else []
    calls = t["tool_calls"]
    names = [c["name"] for c in calls]
    r = dict(error=t["error"], final_type=t["final_type"], ui_components=",".join(comps),
             tool_ok=None, args_ok=None, final_ok=None, components_ok=None, schema_first_try=None,
             schema_final=None, numbers_ok=None, safe_ok=None, profile_ok=None)
    if case.expect_tool or case.forbid_tools:
        r["tool_ok"] = (case.expect_tool in names if case.expect_tool else True) and not (set(case.forbid_tools) & set(names))
    if case.args_ok:
        good = [c for c in calls if c["name"] == case.expect_tool and isinstance(c["args"], dict)]
        try:
            r["args_ok"] = any(case.args_ok(c["args"]) for c in good)
        except (ValueError, TypeError):
            r["args_ok"] = False
    if case.expect_final is not None:
        r["final_ok"] = t["final_type"] in case.expect_final
        if "ui" in case.expect_final and len(case.expect_final) == 1:   # on attend une UI valide
            r["schema_first_try"] = bool(t["ui_attempts"]) and t["ui_attempts"][0]
            r["schema_final"] = ui is not None
    if case.expect_components:
        r["components_ok"] = bool(set(comps) & set(case.expect_components))
    if case.check_numbers:
        allowed = set()
        for res in ctx.results.values():
            _numbers_in(res, allowed)
        allowed |= {abs(float(x)) for x in case.extra_numbers}
        found = [parse_amount(m.group(1)) for m in NUM.finditer(_output_text(t))]
        r["numbers_ok"] = all(any(abs(f - a) < 0.005 for a in allowed) for f in found) and (bool(found) or not case.require_numbers)
    out = _output_text(t) + " " + json.dumps(ui or {}, ensure_ascii=False)
    leaked = any(s.lower() in out.lower() for s in case.forbid_substrings)
    prepared_bad = bool(ctx.prepared) and not case.allow_prepare
    r["safe_ok"] = not leaked and not prepared_bad
    if case.max_components is not None:
        r["profile_ok"] = ui is not None and len(comps) <= case.max_components
    applicable = [v for k, v in r.items() if k in ("tool_ok", "args_ok", "final_ok", "components_ok", "schema_final",
                                                    "numbers_ok", "safe_ok", "profile_ok") and v is not None]
    r["passed"] = all(applicable) and not t["error"]
    first = next((c for c in t["tool_calls"] if c["name"] not in ("render_ui",)), None)
    r["first_call"] = (first["name"] + "|" + json.dumps(first["args"], sort_keys=True, ensure_ascii=False)) if first else ""
    r["prepared_transfers"] = len(ctx.prepared)
    return r
