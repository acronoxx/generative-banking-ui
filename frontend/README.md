# SoprIA — Frontend

Page d’accueil de l’assistant bancaire SoprIA, réalisée avec **React, TypeScript et Vite**. Les composants utilisent des CSS Modules et les styles communs sont regroupés dans `src/styles/`. La refactorisation conserve le contenu, le rendu et les interactions de la démonstration.

## Démarrer

Utilisez Node.js **22.19 ou plus récent** pour les commandes de développement et les tests natifs. Depuis le dossier `frontend` :

```sh
npm install
npm run dev
```

Sous PowerShell, si l’exécution de `npm.ps1` est bloquée, utilisez `npm.cmd` à la place de `npm`.

```sh
npm run build
npm run preview
```

## Vérifier le projet

```sh
npm run lint
npm test
npm run build
```

- `lint` vérifie le code TypeScript et les règles React Hooks.
- `test` utilise le lanceur intégré de Node.js, sans bibliothèque de test supplémentaire. Les tests couvrent les identités des conversations, les titres, la conservation de l’historique, les messages multilignes et les fichiers joints. Le fichier de test `.mjs` importe directement le module TypeScript avec `--experimental-strip-types` ; les types Node restent hors de la configuration TypeScript du navigateur.
- `build` lance les vérifications TypeScript existantes avant de générer la version de production dans `dist/`.

## Organisation

```text
src/
├── main.tsx                            # Montage React et import des styles globaux
├── App.tsx                             # Point d’entrée de l’application
├── pages/
│   ├── HomePage.tsx                     # Assemblage de la page et état des informations
│   └── HomePage.module.css
├── components/
│   ├── WelcomeSection.tsx              # Section de présentation de l’accueil
│   ├── WelcomeSection.module.css
│   ├── InformationDialog.tsx           # Dialogue spécifique aux informations SoprIA
│   ├── InformationDialog.module.css
│   ├── brand/                          # BrandLogo, BrandMark et styles du logo
│   ├── layout/                         # Header, Footer et leurs CSS Modules
│   └── ui/
│       └── Icon.tsx                    # Icônes SVG réutilisables et typées
├── features/
│   └── assistant/
│       ├── components/                 # Chaque composant possède son CSS Module
│       │   ├── ChatWorkspace.tsx
│       │   ├── ConversationSidebar.tsx
│       │   ├── AgentToolbar.tsx
│       │   ├── AgentWelcome.tsx
│       │   ├── QuickActions.tsx
│       │   ├── MessageList.tsx
│       │   └── MessageComposer.tsx
│       ├── data/
│       │   └── assistant.data.ts       # Conversations initiales et opérations rapides
│       ├── hooks/
│       │   └── useAssistantDemo.ts     # État local et actions de conversation
│       ├── conversation.ts             # Création des échanges et mise à jour de l’historique
│       ├── conversation.test.mjs       # Tests des règles de conversation
│       └── types.ts                    # Message, Conversation et QuickAction
├── data/
│   └── information.ts                  # Contenu des fenêtres d’information
└── styles/
    ├── global.css                      # Reset, typographie, accessibilité et utilitaires
    ├── layout.css                      # Structure globale et largeur de page
    └── tokens.css                      # Couleurs, dégradé et rayons communs
```

Les SVG de marque restent dans `components/brand/` : ils sont déjà des composants locaux réutilisables. Aucun dossier `assets/`, `services/` ou `utils/` vide n’est nécessaire.

`pages/` contient les pages complètes. `WelcomeSection` reste un composant de présentation spécifique à l’application dans le dossier `components/` existant, avec son CSS Module ; aucun sous-dossier supplémentaire n’est nécessaire.

### Responsabilités

| Élément | Rôle |
| --- | --- |
| `HomePage` | Assemble le header, l’introduction, l’assistant et le footer ; choisit le sujet du dialogue d’information. |
| `Header` / `Footer` | Affichent la navigation et déclenchent les informations via des callbacks. |
| `WelcomeSection` | Affiche le titre, le texte d’introduction et le symbole de marque. |
| `ChatWorkspace` | Assemble l’interface de conversation, utilise le hook et gère le focus de la saisie. |
| `ConversationSidebar` | Affiche l’historique ; garde la recherche et son filtre dans son propre état local. |
| `AgentToolbar` / `AgentWelcome` | Présentent le sélecteur et le message d’accueil de l’assistant. |
| `QuickActions` | Affiche les actions issues des données statiques et transmet le prompt choisi. |
| `MessageList` | Affiche les messages et fait défiler le dernier message dans la zone visible. |
| `MessageComposer` | Gère le formulaire, les raccourcis clavier et le champ fichier natif ; reçoit le brouillon et la pièce jointe par props. |
| `useAssistantDemo` | Possède les conversations, la sélection, le brouillon et la pièce jointe ; expose les actions sans dépendre du DOM. |
| `conversation.ts` | Crée les identités et les réponses de démonstration ; ajoute les échanges sans modifier l’historique précédent. |
| `InformationDialog` | Affiche les contenus SoprIA et synchronise le dialogue HTML natif avec le sujet sélectionné. |

Les styles spécifiques restent à côté du composant. `global.css` est importé une seule fois dans `main.tsx` et charge les tokens et la structure commune. Les listes reçues par les composants de présentation sont typées en lecture seule.

Les cartes d’action et les lignes de conversation restent dans leurs listes respectives : un composant supplémentaire pour chaque bouton n’apporterait pas de responsabilité distincte. Aucun store global, contexte ou nouvel outil de routage n’a été ajouté.

## Interactions disponibles

- Création, sélection et recherche de conversations.
- Préremplissage de la saisie par les quatre opérations rapides.
- Envoi avec le bouton ou la touche Entrée ; Maj + Entrée pour un retour à la ligne.
- Sélection et retrait d’un fichier joint ; seul son nom est affiché.
- Fenêtres d’aide, profil, guide des prompts et informations du pied de page.
- Mise en page adaptée au bureau, à la tablette et au mobile.
- Navigation clavier, indicateurs de focus, libellés accessibles et dialogues natifs.

## Périmètre frontend

Aucun backend, appel API, authentification ou opération bancaire réelle. Les conversations restent uniquement en mémoire et disparaissent au rechargement. Aucun contenu de fichier n’est lu ou envoyé. Les réponses affichées indiquent explicitement qu’il s’agit d’une démonstration.

Lors de l’ajout d’un backend, introduisez un service API dans la fonctionnalité `assistant` et appelez-le depuis le hook en ajoutant les états de chargement et d’erreur. Les réponses locales actuelles sont dans `features/assistant/conversation.ts` ; les composants de présentation peuvent conserver leurs responsabilités.

Le logo est une reproduction SVG locale de la référence. Il peut être remplacé par les fichiers officiels dans `components/brand/`.
