"""Configuration commune du banc d'essai."""
import json, os, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA, PROMPTS, RESULTS = ROOT / "data", ROOT / "prompts", ROOT / "results"
REFERENCE_DATE = "2026-10-08"       # "aujourd'hui" dans la base fictive
MAX_TURNS = 5                        # tours LLM max par message utilisateur
MAX_UI_RETRIES = 1                   # 1 seul retry si render_ui est invalide
MAX_SINGLE_TRANSFER_EUR = 2000
OTP_ABOVE_EUR = 100


def system_prompt_file():
    return os.getenv("BENCH_SYSTEM_PROMPT", "system_v1.md")


def load_env():
    try:
        from dotenv import load_dotenv
        load_dotenv(ROOT / ".env")
    except ImportError:
        pass


def strict_ui():
    return os.getenv("BENCH_STRICT_UI", "1") == "1"


def load_models():
    return json.loads((ROOT / "bench" / "models.json").read_text(encoding="utf-8"))


def missing_env(entry):
    """Variables d'environnement manquantes pour utiliser ce modele."""
    needed = set(re.findall(r"\{(\w+)\}", entry["model"])) | set(entry.get("env", {}).values())
    return sorted(v for v in needed if not os.getenv(v))


def resolved_model(entry):
    return re.sub(r"\{(\w+)\}", lambda m: os.environ[m.group(1)], entry["model"])
