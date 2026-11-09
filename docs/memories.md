# Mémoire de travail (pour reprendre la prochaine fois)

Projet IMT Atlantique « Projet 28 – UI AI Natives (Generative banking UI) », partenaire Sopra Steria.

## Règles de travail

- Répondre et rédiger les documents en français ; commentaires de code en anglais.
- Ne rien inventer : n'écrire que ce qui est vérifié, signaler ce qui n'a pas été testé.
- Rester dans le périmètre demandé, ne pas toucher aux autres fichiers.
- Ne pas commiter : l'équipe commite et crée les branches elle-même.
- Jamais de secret dans git ni dans une variable `VITE_` (elles sont publiques dans la page).
- Le mot de passe de la base Supabase se transmet directement entre membres de l'équipe, jamais par le dépôt.

## Où on en est

1. **État de l'art et essais** : terminés et fusionnés dans `main` (PR #1).
   - PDF : `docs/etat_de_l_art.pdf` (sources LaTeX dans `docs/etat_de_l_art/`, ignorées par git).
   - Essais : `experiments/`.
2. **Architecture** : en cours, branche `architecture`.
   - Document : `docs/architecture/architecture.tex` et son PDF (11 pages, compile sans erreur).
   - L'équipe crée l'ossature des dossiers, le document décrit l'architecture cible.
   - Non commité pour l'instant : `docs/architecture/`, `frontend/`, `agents/`, et deux modifications dans `experiments/architecture/` (variable `GEMINI_MODEL` dans `agents/assistant.py`, README mis à jour).

## Choix techniques retenus

- **Frontend** : React + Vite + TypeScript (Oxlint), CopilotKit. Le runtime CopilotKit (`runtime.ts`) est dans `frontend/`.
- **Protocoles** : AG-UI entre page/runtime et agent ; A2UI pour le catalogue de composants ; MCP pour les outils ; A2A seulement si on ajoute d'autres agents.
- **Agent** : Python, LangChain, modèle OpenAI, traces dans LangSmith (offre gratuite, un compte partagé).
- **Backend** : FastAPI, avec le serveur MCP monté sur `/mcp`.
- **Base** : PostgreSQL hébergée sur Supabase (données fictives déjà en ligne). Pas de Docker.
- **Ports** : page 5173, runtime 4000, agent 8001, backend 8000.
- `@ag-ui/client` doit être exactement à la version utilisée par CopilotKit (1.0.2, épinglée avec `--save-exact`). Sinon : erreur `HttpAgent is not assignable to AbstractAgent`.

## Principes de l'architecture

- L'agent ne touche jamais la base.
- La logique métier est dans `backend/app/services/`, partagée par `/api` et `/mcp`.
- L'identité vient du jeton de session : aucun outil ne prend de `customer_id`.
- Connexion par identifiant et mot de passe (pas de code PIN).
- Virement en deux temps : l'outil `prepare_transfer` crée une simulation en attente, puis la page appelle `POST /api/transfers/{id}/confirm` avec le mot de passe. Aucun outil ne peut exécuter un virement.
- Seule la personne chargée du backend lance les migrations Alembic sur la base partagée.

## Noms retenus (anglais)

- **Pages** : `Login.tsx`, `Assistant.tsx`.
- **Catalogue** (`frontend/src/catalog/`) : `AccountCard`, `TransactionList`, `SpendingChart`, `TransferConfirmation`, `ProductCard`, `AppointmentPicker`, `index.ts`.
- **Appels API de la page** : `api/auth.ts`, `api/transfers.ts`.
- **Agent** : `agents/agent_01/{main.py, agent.py, prompt.md, tools.py, ui/, tests/, requirements.txt, .env.example}`.
- **Backend** : `app/{main.py, api/{auth,accounts,transactions,transfers,products,advisors}.py, mcp/server.py, services/, schemas/, security.py}`.
- **Nouveaux modèles** : `user_sessions.py`, `audit_logs.py`, `beneficiaries.py`, `transfer_simulations.py`.
- **Outils MCP** : `list_accounts`, `get_recent_transactions`, `get_spending_by_category`, `compare_spending`, `list_beneficiaries`, `prepare_transfer`, `list_products`, `get_product_details`, `get_advisor`, `get_appointment_slots`.
- **Routes** : `/api/auth/login`, `/api/auth/logout`, `/api/transfers/{id}/confirm`, `/api/transfers/{id}/cancel`.

## État des fichiers

- **`frontend/`** : nettoyé (plus d'images, de `public/`, ni de `App.css`), `index.html` en `lang="fr"`, titre « Assistant bancaire ».
  - `src/main.tsx` : `CopilotKitProvider` avec `runtimeUrl={import.meta.env.VITE_RUNTIME_URL}`.
  - `src/vite-env.d.ts` : type de `VITE_RUNTIME_URL`.
  - `runtime.ts` : `process.loadEnvFile()`, puis `AGENT_URL` (défaut `http://127.0.0.1:8001/`) et `RUNTIME_PORT` (défaut 4000).
  - `.env.example` (versionné) : `VITE_RUNTIME_URL`, `RUNTIME_PORT`, `AGENT_URL`, `COPILOTKIT_TELEMETRY_DISABLED=true`.
  - `src/App.tsx` : `CopilotChat`.
- **`agents/agent_01/`** : `agent.py` et `prompt.md` encore vides, un `.env`.
- **Configuration** : un `.env` par dossier, avec un `.env.example` versionné.

## À faire / à vérifier

- Le modèle `User` stocke un `app_pin_hash` : il faudra le remplacer par un mot de passe haché (migration).
- Quand on aura les accès Supabase, tester la connexion depuis le backend et vérifier (non vérifié pour l'instant) :
  - connexion directe ou par le pooler (avec psycopg, plutôt le mode session que le mode transaction) ;
  - SSL obligatoire ou non ;
  - mise en pause des projets gratuits après inactivité.
- Écrire l'agent (`agent.py`, `prompt.md`, `tools.py`) et les routes/outils du backend.

## Astuces

- Les heredocs de Git Bash mangent les antislashs : pour le LaTeX, passer par l'éditeur ou un script Python.
- Débordements LaTeX : `\emergencystretch`, `columns=fullflexible`, retours à la ligne explicites dans les boîtes TikZ.
