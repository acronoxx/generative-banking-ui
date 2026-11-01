"""Abstraction LLM : un seul point d'appel, reponse normalisee (FC1 : modeles interchangeables)."""
import os, time
from dataclasses import dataclass, field
from .config import resolved_model


@dataclass
class Reply:
    content: str | None
    tool_calls: list = field(default_factory=list)   # [{"id","name","arguments"(str JSON)}]
    tokens_in: int = 0
    tokens_out: int = 0
    latency_s: float = 0.0


def complete(entry, messages, tools):
    import litellm  # import tardif : le mode --mock n'en a pas besoin
    env = entry.get("env", {})
    kwargs = dict(model=resolved_model(entry), messages=messages, tools=tools, tool_choice="auto")
    for k in ("api_base", "api_key", "api_version"):
        if k in env:
            kwargs[k] = os.environ[env[k]]
    kwargs.update(entry.get("params", {}))
    if entry.get("params"):
        # LiteLLM ne connait pas les noms de DEPLOIEMENT Azure personnalises et refuserait ces parametres
        # (UnsupportedParamsError) avant meme d'appeler Azure. On les autorise explicitement.
        kwargs["allowed_openai_params"] = list(entry["params"])
    # Pas de drop_params : si un parametre (ex. reasoning_effort) est refuse, on veut VOIR l'erreur.
    last_err = None
    for attempt in range(3):
        t0 = time.perf_counter()
        try:
            resp = litellm.completion(**kwargs)
            break
        except Exception as e:  # noqa
            last_err = e
            if "429" in str(e) or e.__class__.__name__ == "RateLimitError":
                time.sleep(2 ** (attempt + 1))
                continue
            raise
    else:
        raise last_err
    dt = time.perf_counter() - t0
    msg = resp.choices[0].message
    calls = [{"id": c.id, "name": c.function.name, "arguments": c.function.arguments or "{}"}
             for c in (msg.tool_calls or [])]
    u = getattr(resp, "usage", None)
    return Reply(msg.content, calls, getattr(u, "prompt_tokens", 0) or 0,
                 getattr(u, "completion_tokens", 0) or 0, dt)
