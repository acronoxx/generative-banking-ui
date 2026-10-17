# Expérimentations de l'état de l'art

Chaque dossier est indépendant : il a son propre environnement (`venv/` ou
`node_modules/`, non versionnés) et son propre fichier `.env`, qui doit contenir
`GOOGLE_API_KEY=...` (clé Gemini).

## Frameworks d'orchestration : protocole commun

Le même agent bancaire (modèle `gemini-3.5-flash-lite`, deux outils
`get_balance` et `get_transactions`, données fictives) répond à quatre
scénarios, répétés 10 fois avec 10 s de pause entre deux essais (quota
gratuit). Le script `measure.*` de chaque dossier affiche une ligne CSV par
scénario ; les résultats obtenus sont dans `resultats.csv` lorsqu'ils ont été
enregistrés.

| Dossier | Langage | Lancement | État |
| --- | --- | --- | --- |
| `langchain/` | Python | `venv\Scripts\python measure.py` | mesuré |
| `langchain-js/` | TypeScript | `npm install` puis `node measure.ts` | mesuré |
| `mastra/` | TypeScript | `npm install` puis `node measure.ts` | mesuré |
| `crewAI/` | Python (≤ 3.13) | `venv\Scripts\python measure.py` | mesuré |
| `pydanticAI/` | Python | `venv\Scripts\python measure.py` | mesuré |
| `openAI-agents/` | Python | `venv\Scripts\python measure.py` | mesuré |
| `googleADK/` | Python | `venv\Scripts\python measure.py` | mesuré |
| `strands/` | Python | `venv\Scripts\python measure.py` | mesuré |
| `microsoft-agent-framework/` | Python | `venv\Scripts\python measure.py` | mesuré |
| `vercel-ai-sdk/` | TypeScript | `npm install` puis `node measure.ts` | mesuré |
| `claude-agent-sdk/` | Python | `venv\Scripts\python measure.py` | **non exécuté** : modèles Claude uniquement, clé `ANTHROPIC_API_KEY` requise |
| `spring-ai/` | Java 21 | `mvn spring-boot:run` | **non compilé** : aucun JDK sur le poste |

Création d'un environnement Python : `python -m venv venv` puis
`venv\Scripts\python -m pip install -r requirements.txt`.

Node 22.6 ou plus récent exécute directement les fichiers `.ts`
(`node measure.ts`). `npx tsc -p .` vérifie les types.

Quota : l'offre gratuite de Gemini est limitée à 500 requêtes par jour et par
modèle. Une série complète en consomme environ 70 ; au-delà, les essais
échouent en HTTP 429 jusqu'au lendemain.

## Interfaces génératives

| Dossier | Contenu | Lancement | État |
| --- | --- | --- | --- |
| `genui-ai-sdk/` | Agent `ToolLoopAgent` (outils + virement soumis à approbation) servi en Node, page React avec `useChat` | `npm install`, puis `npm run agent` et `npm run dev` (http://localhost:5173) | exécuté |
| `assistant-ui/` | Page construite avec les primitives d'assistant-ui, branchée sur le serveur de `genui-ai-sdk` | lancer d'abord `npm run agent` dans `genui-ai-sdk/`, puis `npm install` et `npm run dev` ici | exécuté |
| `tambo/` | Composants et outils enregistrés auprès de Tambo | `VITE_TAMBO_API_KEY=...` dans `.env`, puis `npm run dev` | **non exécuté** : clé Tambo requise |
| `openui/` | Catalogue OpenUI (6 composants), agent Gemini avec 3 outils répondant en OpenUI Lang, page React avec le `Renderer` | `npm install`, `npm run spec` (consigne et spécification), puis `npm run agent` et `npm run dev` (http://localhost:5173) | exécuté |

La variable `GEMINI_MODEL` (en PowerShell : `$env:GEMINI_MODEL="gemini-3.8-flash"`)
permet de changer de modèle dans `genui-ai-sdk/agent.ts`, `openui/server.ts` et `mcp/agent.py`
lorsque le quota du modèle par défaut est épuisé.

## Protocoles

| Dossier | Contenu | Lancement |
| --- | --- | --- |
| `function-calling/` | Boucle de function calling écrite à la main avec `google-genai` | `venv\Scripts\python boucle.py` |
| `mcp/` | Serveur MCP (`serveur.py`), client sans modèle (`client.py`), agent LangChain qui découvre les outils MCP (`agent.py`) | `venv\Scripts\python client.py` ou `agent.py` (le serveur est lancé par le client) |
| `a2a/` | Agent « comptes » exposé en A2A et client qui lit son Agent Card | `venv\Scripts\python serveur.py` puis, dans un autre terminal, `client.py` |
| `utcp/` | API REST ordinaire avec un manuel UTCP, et client UTCP | `venv\Scripts\python api.py` puis `client.py` |
| `ag-ui/` | Serveur AG-UI minimal (événements sans modèle) | `venv\Scripts\python server.py`, puis POST sur http://localhost:8000/ (l'ancien dossier `env/` est inutilisable : créé dans un autre dossier puis déplacé) |
| `architecture/` | Exemple complet : LangChain + AG-UI + A2UI + CopilotKit + WebMCP | voir `architecture/README.md` |

## Observabilité

| Dossier | Contenu | Lancement | État |
| --- | --- | --- | --- |
| `observabilite/` | Agent LangChain des mesures instrumenté avec OpenInference ; traces envoyées à Phoenix en local (base SQLite dans `donnees-phoenix/`, non versionnée) | `pip install -r requirements.txt`, puis `$env:PHOENIX_TELEMETRY_ENABLED="false"; $env:PHOENIX_WORKING_DIR="donnees-phoenix"; venv\Scripts\phoenix serve` et `venv\Scripts\python trace_agent.py` ; traces sur http://localhost:6006 | exécuté |

## Premiers essais

`langchain/test0.py`, `test1.py`, `test2.py` et `mastra/test1.ts` sont les
premières prises en main, antérieures aux scripts de mesure. `test2.py`
(validation humaine d'un virement) utilise un modèle Claude et demande
`ANTHROPIC_API_KEY`.

## Vérifications

Tous les fichiers Python compilent et passent `ruff` (règles E, F, W, B ; seules
quelques lignes dépassent 120 caractères). Les projets TypeScript passent
`tsc` (`npx tsc -b`, ou `npx tsc -p .` pour `langchain-js`, `vercel-ai-sdk` et
`mastra`). Les essais sans modèle (`ag-ui`, `mcp/client.py`, `a2a`, `utcp`) ont
été relancés avec succès ; les autres dépendent du quota Gemini.
