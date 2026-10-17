# Exemple d'architecture

Exemple minimal qui fait collaborer les technologies de l'état de l'art autour
d'un seul agent : LangChain, AG-UI, A2UI, WebMCP et CopilotKit.

| Processus | Port | Rôle |
| --- | --- | --- |
| `agents/assistant.py` | 8000 | Agent LangChain exposé en AG-UI, outil d'affichage A2UI, API bancaire |
| `frontend/runtime.ts` | 4000 | Runtime CopilotKit, relais entre la page et l'agent |
| `frontend/` (Vite) | 5173 | Page React : conversation CopilotKit et outils de la page (WebMCP) |

Les outils métier (`consulter_comptes`, `consulter_transactions`) sont définis
dans la page (`frontend/src/outils.ts`). Ils sont déclarés au navigateur avec
WebMCP et transmis à l'agent, qui les appelle ; ils s'exécutent dans la page.

## Lancement

Créer un fichier `.env` dans ce dossier avec `GOOGLE_API_KEY=...`, puis ouvrir trois terminaux.

```powershell
# Une seule fois (Python 3.13)
py -3.13 -m venv venv
.\venv\Scripts\python -m pip install -r requirements.txt
cd frontend; npm install; cd ..

# Terminal 1
cd agents; ..\venv\Scripts\python assistant.py
# Terminal 2
cd frontend; npm run runtime
# Terminal 3
cd frontend; npm run dev
```

Ouvrir http://localhost:5173 et demander par exemple : « Montre-moi mes comptes. »

Le runtime CopilotKit met une vingtaine de secondes à démarrer.

## WebMCP

La déclaration au navigateur (`frontend/src/webmcp.ts`) n'a lieu que si celui-ci
expose `document.modelContext` (Chrome avec l'essai WebMCP activé). Sans cela,
les outils restent transmis à l'agent et l'exemple fonctionne normalement.
Vérifié dans Chrome 155 avec le drapeau `chrome://flags/#enable-webmcp-testing` :
`document.modelContext.getTools()` liste les deux outils, et `executeTool()` les
exécute dans la page.

## Différence avec l'architecture retenue

Cet exemple a été réalisé avant le choix de placer les outils côté serveur.
Dans l'architecture retenue (état de l'art, section 8), les outils sont
regroupés dans un serveur MCP appelé par l'agent, et WebMCP n'est pas utilisé :
il ne sert qu'aux agents intégrés au navigateur.
