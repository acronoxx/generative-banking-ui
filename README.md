# SoprIA — Application bancaire conversationnelle

## Présentation du projet

**SoprIA** est une application bancaire conversationnelle conçue pour simplifier les interactions et les opérations bancaires grâce à une interface intuitive et dynamique.

L'application permet aux utilisateurs d'exprimer leurs besoins en langage naturel à travers un assistant bancaire.

Développée sous forme de **Single Page Application (SPA)**, SoprIA propose une interface dynamique dans laquelle les différentes fonctionnalités bancaires peuvent s'afficher sans rechargement de la page.

Le projet est actuellement en cours de développement. Le frontend est réalisé avec React et TypeScript et préparé pour une future intégration avec le backend.

## Technologies utilisées

- **React** — Création des composants et des interfaces utilisateur.
- **TypeScript** — Typage des données et sécurisation du code.
- **Vite** — Serveur de développement et outil de compilation.
- **CSS Modules** — Organisation des styles par composant.
- **ESLint** — Vérification de la qualité et de la cohérence du code.

## Fonctionnalités actuelles

- Interface conversationnelle avec un assistant bancaire.
- Historique des conversations et actions bancaires rapides.
- Consultation du profil utilisateur et des préférences bancaires.
- Affichage des informations sur les comptes et les cartes bancaires.
- Interface responsive adaptée aux différents écrans.
- Composants réutilisables.
- Utilisation de données fictives (*mock data*) pour faciliter l'intégration future du backend.

### Fonctionnalités en cours de développement

- Interface dynamique de virement bancaire.
- Intégration avec les API et le backend.
- Assistant bancaire basé sur l'intelligence artificielle.
- Authentification et sécurisation des opérations bancaires.
- Sauvegarde persistante des données utilisateurs et des transactions.

**Remarque :** Le frontend utilise actuellement des données fictives. Les opérations bancaires réelles et les fonctionnalités d'intelligence artificielle ne sont pas encore connectées à des services réels.

## Structure du projet

```text
generative-banking-ui/
├── frontend/
│   ├── src/
│   │   ├── components/   # Composants réutilisables
│   │   ├── features/     # Fonctionnalités de l'application
│   │   ├── pages/        # Pages de l'application
│   │   ├── styles/       # Styles globaux et charte graphique
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── README.md
└── README.md
```

## Installation et lancement

### Prérequis

- Node.js
- npm
- Git

### Étapes d'installation

**1. Cloner le dépôt**

```bash
git clone https://github.com/acronoxx/generative-banking-ui.git
```

**2. Se placer dans le dossier frontend**

```bash
cd generative-banking-ui/frontend
```

**3. Installer les dépendances**

```bash
npm install
```

**4. Lancer le serveur de développement**

```bash
npm run dev
```

**5. Ouvrir l'application**

Accéder à l'adresse indiquée par Vite, généralement :

`http://localhost:5173/`

## Architecture et organisation

Le frontend suit une **architecture modulaire organisée par fonctionnalités**.

- Les composants communs sont réutilisés dans les différentes parties de l'application.
- Chaque fonctionnalité dispose de ses propres composants, types et données.
- Les données fictives sont séparées de l'interface utilisateur.
- TypeScript permet de définir des structures de données cohérentes.
- Les styles communs respectent la charte graphique de SoprIA.
- L'organisation du code facilite la maintenance et l'intégration future du backend.

## Travail collaboratif

SoprIA est développé dans le cadre d'un projet en équipe.

Chaque membre peut travailler sur une branche dédiée afin de développer ses fonctionnalités indépendamment.

La branche **`frontend_dev`** est consacrée au développement de l'interface frontend.

## Documentation

Pour plus de détails sur l'architecture, les composants et le fonctionnement du frontend, consulter le [README du frontend](frontend/README.md).

## État du projet

**Projet académique en cours de développement.**

L'application est actuellement centrée sur la réalisation des interfaces, la mise en place des interactions et la préparation de l'intégration avec le backend.

Les services bancaires réels et les fonctionnalités avancées d'intelligence artificielle seront intégrés dans les prochaines étapes du projet.
