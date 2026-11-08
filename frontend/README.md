# SoprIA Frontend

## Project Overview

This is a banking assistant frontend built with React and TypeScript. It explores how users can describe banking requests through a conversational interface and view their profile, accounts, and preferences in one application. 

As a single-page application (SPA), it updates conversations and profile content without reloading the browser. 

## Technologies Used

- **React and React DOM** for components and local state.
- **TypeScript** for typed data models and component props.
- **Vite** with the React plugin for development and production builds.
- **CSS Modules** for component styles, with shared CSS design tokens.
- **ESLint** with TypeScript, React Hooks, and React Refresh rules.
- **Node.js built-in test runner** for conversation logic tests.

Navigation uses browser URL hashes and React hooks; no routing library or global state library is installed. Branding and icons use local SVG components.

## Current Features

### Implemented interface

- Create, select, and search conversations; view message history.
- Prefill messages using four banking quick actions.
- Send with the button or Enter; use Shift+Enter for a new line.
- Select or remove an attachment and display its filename.
- View a profile with personal details, account and card summaries, payment limits, security settings, and advisor information.
- Edit the demo email, phone, and postal address through a form.
- Navigate between Home and Profile with an active navigation indicator.
- Reuse a shared header, footer, help dialogs, icons, and branding.
- Adapt layouts to desktop, tablet, and mobile, with keyboard focus styles and labeled controls.

### Demo functionality and limits

Chat replies are predefined, and banking information is fictional. Conversations and profile edits remain in memory across page navigation and reset on browser reload. Attachment contents are neither read nor uploaded. Changed email addresses and phone numbers lose their verification badges.

Document downloads, photo changes, advisor contact, appointments, card controls, payment-limit changes, and security actions display an unavailable-feature message. They do not perform real operations.

### Feature status and remaining work

| Feature | Current status |
| --- | --- |
| Banking chatbot | Implemented with predefined responses. |
| User profile | Implemented using mock data, with local contact edits. |
| Bank transfer interface | In development; not yet integrated into this React frontend. |
| Real bank transfers | Awaiting backend integration. |

The transfer quick action currently prefills a message; it does not open a transfer form or send money. AI responses, authentication, persistent storage, official documents, and security verification also await backend integration.

## Project Structure

```text
src/
├── main.tsx                    # Mounts React and imports global styles
├── App.tsx                     # Shared shell, navigation, information dialogs
├── components/
│   ├── brand/                  # Local logo and brand mark
│   ├── layout/                 # Shared Header and Footer
│   ├── ui/                     # Typed SVG icons and reusable Dialog
│   ├── WelcomeSection.tsx
│   └── InformationDialog.tsx
├── data/
│   └── information.ts          # Help and informational dialog content
├── features/
│   ├── assistant/
│   │   ├── components/         # Chat, history, quick actions, composer
│   │   ├── data/               # Initial conversations and action prompts
│   │   ├── hooks/              # Local conversation state
│   │   ├── conversation.ts     # Demo exchanges and history updates
│   │   ├── conversation.test.mjs
│   │   └── types.ts
│   └── profile/
│       ├── components/         # Profile sections and edit dialog
│       ├── data/               # Mock profile and data access adapter
│       ├── hooks/              # Loading, retry, and local edits
│       ├── format.ts           # Date and currency formatting
│       └── types.ts
├── pages/                      # HomePage and ProfilePage assembly
└── styles/                     # Global styles, layout, and tokens.css
```

Feature logic stays in `features/`; pages assemble it with shared `components/`. Component styles use `.module.css` files. `main.tsx` imports `styles/global.css`, which loads shared layout rules and design tokens.

## Installation and Setup

Recommended: **Node.js 22.19 or later** and npm, verified locally with Node.js 22.19.0. This satisfies the installed Vite requirement (`^20.19.0 || >=22.12.0`) and supports the tests' `--experimental-strip-types` flag. The project does not currently declare a Node.js version in `package.json`.

1. Replace `<repository-url>` with your team's repository URL and clone it:

   ```sh
   git clone <repository-url> sopria
   ```

2. Enter the frontend directory:

   ```sh
   cd sopria/frontend
   ```

3. Install the versions recorded in `package-lock.json`:

   ```sh
   npm ci
   ```

4. Start the development server:

   ```sh
   npm run dev
   ```

5. Open the local URL printed by Vite, normally `http://localhost:5173`.

No environment variables or backend credentials are required for the current demo. If PowerShell blocks `npm.ps1`, use `npm.cmd` in place of `npm`.

Use `npm install` instead when intentionally adding or updating dependencies, and include the resulting lockfile changes in your branch.

Run these commands from `frontend/`:

| Command | Purpose |
| --- | --- |
| `npm run dev` | Start the Vite development server. |
| `npm run lint` | Check TypeScript/TSX code and React rules with ESLint. |
| `npm test` | Run the conversation logic tests with Node.js. |
| `npm run build` | Run TypeScript checks and generate `dist/`. |
| `npm run preview` | Serve the generated build locally after building. |

## How the Application Works

**Homepage:** `HomePage` displays the introduction and `ChatWorkspace`. The workspace combines conversation history, quick actions, messages, and the composer. `useAssistantDemo` manages local state; `conversation.ts` creates predefined replies and updates history. Quick actions only fill the input. Sending a message replaces the quick-action area with the conversation's messages.

**Navigation:** `App.tsx` listens for hash changes. `#/accueil` opens Home, `#/profil` opens Profile, and links such as `#/profil/securite` target profile sections. Both pages remain mounted, preserving their local state while switching views. Browser back and forward work without a full reload.

**Profile:** `useProfile` loads the mock profile through `getUserProfile`. Typed display components render the overview, personal information, banking preferences, and security cards. Loading, error/retry, and empty-profile states are included. The edit dialog updates local contact details; service-dependent actions open an information dialog.

## Mock Data and Future Backend Integration

Mock data lets the team develop the interface without a banking service:

- `src/features/assistant/data/assistant.data.ts`: initial conversations and quick-action prompts.
- `src/features/assistant/conversation.ts`: predefined assistant replies.
- `src/features/profile/data/profile.mock.ts`: fictional profile, accounts, card, limits, preferences, security, and advisor data.
- `src/data/information.ts`: shared informational text.

Each feature defines its models in `types.ts`, and presentation components consume typed props. To connect profile data, replace the mock adapter in `src/features/profile/data/profile.repository.ts` with an API client and connect contact updates in `useProfile` to backend persistence and validation. For chat, introduce service calls through `useAssistantDemo` with loading and error handling.

Authentication, authorization, banking validation, and persistence still require backend implementation. The frontend currently does not store banking data in `localStorage`.

## Development Guidelines

- Follow the existing feature folders and keep pages focused on assembly.
- Reuse shared components before introducing new ones.
- Define TypeScript models and keep mock data separate from UI code.
- Use CSS Modules and `src/styles/tokens.css` for consistent styling.
- Keep state near the feature that owns it and avoid duplicated logic.
- Keep demo behavior explicit; do not imply that banking operations succeeded.
- Before pushing, run `npm run lint`, `npm test`, and `npm run build`. Check both pages and responsive layouts when changing the UI.

The current automated tests cover conversation identities, titles, history, multiline messages, and attachment metadata; they are not a complete UI test suite.

## Git Workflow

Each contributor works on a dedicated feature branch. From the repository root, create one from the team's agreed base:

```sh
git switch <agreed-base-branch>
git switch -c feature/short-description
```

To resume it later, use `git switch feature/short-description`. After running the checks, commit your changes and push your branch to GitHub:

```sh
git add <changed-files>
git commit -m "Describe the change"
git push -u origin feature/short-description
```

Open a pull request against the team's agreed target branch when ready for review.
