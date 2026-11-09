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

Les composants d'interface sont eux aussi déclarés par la page
(`frontend/src/catalogue.tsx`) : le catalogue A2UI de base plus des composants
bancaires (`SoldeCompte`, `Transaction`, `Alerte`). Leur schéma est envoyé à
l'agent, qui l'ajoute à son prompt et compose l'interface avec l'outil
`afficher_interface`. Cet outil valide les composants (ids, racine, catalogue,
propriétés requises) et renvoie les erreurs au modèle pour qu'il corrige.
Pour ajouter un composant, il suffit d'ajouter sa définition (schéma zod et
description) et son rendu React dans ce fichier.

Les outils `generate_a2ui` et `render_a2ui` de CopilotKit (option
`injectA2UITool` du runtime) ne fonctionnent pas avec Gemini :
`generate_a2ui` lance un sous-agent dans une autre boucle asyncio (« bound to a
different event loop »), et les arguments de `render_a2ui` ne sont pas diffusés
en AG-UI (Gemini envoie l'appel d'outil en un seul morceau), donc la surface
reste en chargement. L'interface passe donc par le résultat de l'outil.

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

Si le quota gratuit de `gemini-3.5-flash-lite` est épuisé (erreur 429), lancer
l'agent avec un autre modèle : `$env:GEMINI_MODEL="gemini-3.5-flash"` dans le
terminal 1, avant la commande.

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
