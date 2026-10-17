# Premier essai LangChain : initialisation du modèle Gemini (aucun appel).

from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()
model = init_chat_model("google_genai:gemini-3.5-flash-lite", timeout=60, max_retries=0)
