# Prototype de l'architecture

Prototype très simple qui reprend **exactement l'arborescence du projet** (`backend/`,
`agents/agent_01/`, `frontend/`) et remplit chaque fichier avec une version minimale
mais fonctionnelle. Il sert à voir ce que doit contenir chaque fichier et comment
les morceaux s'appellent entre eux.

Simplifications par rapport au vrai projet :

- **un seul client** (`demo` / `demo`), un seul conseiller ;
- **pas de PostgreSQL** : `backend/database.py` garde les données en mémoire
  (`FakeDB`), `backend/models/` contient de simples dataclasses au lieu des modèles
  SQLAlchemy ; tout est perdu au redémarrage du backend ;
- mot de passe en clair, jetons de session en mémoire, sans expiration ni verrouillage
  après plusieurs échecs, pas de journal d'audit ;
- `app/security.py` et `app/dependencies.py` existent ici alors qu'ils ne sont pas
  encore créés dans le projet (ils y sont mentionnés dans les docstrings).

## Qui appelle qui

| Processus | Port | Fichiers principaux |
| --- | --- | --- |
| Backend (FastAPI) | 8000 | `backend/app/main.py` : routes `/api` (`app/api/`) et serveur MCP `/mcp` (`app/mcp/server.py`), qui appellent tous deux `app/services/` |
| Agent (LangChain, AG-UI) | 8001 | `agents/agent_01/main.py` (point d'entrée AG-UI), `agent.py` (modèle et boucle), `tools.py` (client MCP), `ui.py` (A2UI) |
| Runtime CopilotKit | 4000 | `frontend/runtime.ts` (relais page ↔ agent) |
| Page React (Vite) | 5173 | `frontend/src/App.tsx`, `pages/`, `catalog/` (un fichier par composant A2UI), `api.ts` (appels directs au backend) |

Parcours d'une question :

1. la page se connecte (`POST /api/auth/login`) et reçoit un jeton de session ;
2. elle envoie la question au runtime avec `Authorization: Bearer <jeton>` et son
   catalogue de composants ; le runtime transmet les deux à l'agent ;
3. `main.py` range le jeton dans la configuration de l'exécution
   (`config["configurable"]["auth_token"]`), invisible pour le modèle ;
4. le modèle appelle un outil MCP ; l'intercepteur de `tools.py` ajoute le jeton à
   l'appel ; `app/mcp/server.py` retrouve le client avec ce jeton et appelle le service ;
5. le modèle appelle `show_interface` (`ui.py`) avec des composants du catalogue ;
   la page les affiche avec ses composants React ;
6. pour un virement, l'agent ne fait que `prepare_transfer` ; le client confirme dans
   le composant `TransferConfirmation`, qui appelle directement
   `POST /api/transfers/{id}/confirm` avec son mot de passe.

## Lancement

Le prototype utilise l'environnement Python de la racine (`requirements.txt`).
Copier `agents/agent_01/.env.example` en `agents/agent_01/.env` et y mettre la clé de
la passerelle IMT, puis copier `frontend/.env.example` en `frontend/.env`.

```powershell
# Une seule fois
cd frontend; npm install; cd ..

# Terminal 1 : backend
cd backend; ..\..\..\venv\Scripts\python -m uvicorn app.main:app --port 8000
# Terminal 2 : agent (le backend doit déjà tourner)
cd agents\agent_01; ..\..\..\..\venv\Scripts\python main.py
# Terminal 3 : runtime CopilotKit
cd frontend; npm run runtime
# Terminal 4 : page
cd frontend; npm run dev
```

Ouvrir http://localhost:5173, se connecter avec `demo` / `demo`, puis demander par
exemple « Montre-moi mes comptes », « Combien ai-je dépensé en restaurants en
octobre ? » ou « Fais un virement de 50 € à Marie Dupont pour le dîner ».

## Tests

```powershell
cd backend; ..\..\..\venv\Scripts\python -m pytest tests
cd agents\agent_01; ..\..\..\..\venv\Scripts\python -m pytest tests
```

Les tests du backend appellent le serveur MCP en JSON-RPC sur `/mcp/` avec le
`TestClient` de FastAPI (sans `initialize`, possible en mode `stateless_http`).
