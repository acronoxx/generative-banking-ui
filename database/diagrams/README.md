# Generative Banking UI — Base de données et dataset

Ce document explique comment créer la base PostgreSQL du projet, générer le dataset synthétique, consulter les données avec DBeaver et partager une base commune avec l’équipe via Supabase.

> **Important :** les commandes ci-dessous correspondent à l’organisation du projet discutée (`backend/database.py`, modèles SQLAlchemy, migrations Alembic et `backend/seed_database.py`). Vérifiez les noms et paramètres dans le code si le projet a évolué.
>
> Toutes les données doivent rester synthétiques. N’utilisez pas de données réelles de clients ni d’identifiants bancaires réels.

## Sommaire

1. Architecture
2. Prérequis
3. Récupérer le projet et configurer l’environnement
4. Configurer PostgreSQL en local
5. Créer le schéma
6. Générer le dataset
7. Vérifier les données
8. Utiliser DBeaver
9. Partager la base avec Supabase
10. Exporter et importer une sauvegarde
11. Sécurité et Git
12. Dépannage

---

## 1. Architecture

Le projet distingue trois éléments :

- **Code versionné dans Git :** modèles, backend, migrations et script de génération.
- **Base PostgreSQL :** schéma et données du dataset.
- **Configuration privée :** mots de passe et URL de connexion, conservés dans un fichier `.env` local non versionné.

Pour travailler à plusieurs sur les mêmes données en temps réel, tous les backends doivent se connecter à la même instance PostgreSQL hébergée.

Des bases locales distinctes, même initialisées par le même script, ne partagent pas leurs modifications.

## 2. Prérequis

- Python, avec une version compatible avec le projet.
- PostgreSQL en local si le dataset doit être généré localement.
- Les dépendances Python du projet.
- Git.
- DBeaver, facultatif, pour consulter la base.
- Un projet Supabase, si l’équipe utilise une base partagée en ligne.
- Les outils clients PostgreSQL `pg_dump` et `pg_restore` pour exporter et importer une sauvegarde.

Sous Windows, ces outils peuvent se trouver dans un dossier similaire à :

```powershell
C:\Program Files\PostgreSQL\18\bin\pg_dump.exe
C:\Program Files\PostgreSQL\18\bin\pg_restore.exe
```

Adaptez le numéro de version à votre installation.

## 3. Récupérer le projet et configurer l’environnement

Depuis PowerShell :

```powershell
git clone <URL_DU_DEPOT>
cd generative-banking-ui
```

Si le dépôt est déjà cloné, ouvrez simplement son dossier.

Activez l’environnement virtuel existant :

```powershell
.\.venv\Scripts\Activate.ps1
```

Si l’environnement n’existe pas, créez-le avec Python 3.12, si cette version est compatible avec le projet :

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Installez les dépendances à partir du fichier de dépendances présent dans le dépôt. Par exemple, si le projet utilise `requirements.txt` :

```powershell
python -m pip install -r requirements.txt
```

Si le projet utilise `pyproject.toml`, `uv` ou un autre gestionnaire, suivez les instructions du dépôt.

### Configuration `.env`

Créez un fichier `.env` à partir de `.env.example`, si ce dernier existe. Renseignez les variables attendues par le code, notamment la connexion PostgreSQL.

Exemple indicatif, à adapter aux variables réellement lues par `backend/database.py` :

```dotenv
DATABASE_URL=postgresql://UTILISATEUR:MOT_DE_PASSE@HOTE:PORT/NOM_BASE
```

Ne publiez jamais ce fichier et ne partagez pas les secrets dans les issues GitHub, captures d’écran ou messages.

## 4. Configurer PostgreSQL en local

Pour la base locale du projet, les paramètres utilisés sont :

| Champ | Valeur |
|---|---|
| Hôte | `localhost` |
| Port | `5432` |
| Base | `generative_banking_ui` |
| Utilisateur | `postgres` ou un utilisateur local dédié |
| Mot de passe | Mot de passe PostgreSQL local |

Créez la base si elle n’existe pas encore.

La base doit être accessible avant d’appliquer les migrations ou d’exécuter le script de génération.

## 5. Créer le schéma

Le projet possède des modèles SQLAlchemy et des migrations Alembic.

Pour une base neuve, la commande habituelle est :

```powershell
alembic upgrade head
```

Exécutez-la depuis le dossier prévu par la configuration Alembic et avec le bon environnement virtuel et le bon `.env`.

**Attention :** vérifiez d’abord si `backend/seed_database.py` crée également les tables. N’appliquez pas plusieurs méthodes de création du schéma sans vérifier leur compatibilité. Utilisez la procédure de création prévue par le code actuel.

## 6. Générer le dataset

Le script de génération du projet est :

```text
backend/seed_database.py
```

Depuis la racine du dépôt, avec le bon environnement virtuel et la base locale ciblée dans la configuration :

```powershell
python backend/seed_database.py
```

Si `python` n’est pas reconnu dans PowerShell :

```powershell
.\.venv\Scripts\python.exe backend/seed_database.py
```

Le script génère des données bancaires synthétiques liées entre elles : utilisateurs, clients, conseillers, produits, comptes, souscriptions, cartes, catégories et transactions.

### Volumes de référence attendus

Les volumes de conception communiqués pour le dataset sont les suivants. Ils sont des **objectifs de référence**, et non une garantie indépendante du code exécuté. Vérifiez les nombres réels dans la base et les paramètres du générateur.

| Entité | Nombre cible |
|---|---:|
| Conseillers (`advisors`) | 500 |
| Clients (`customers`) | 100 000 |
| Utilisateurs (`users`) | 100 501 |
| Produits bancaires (`banking_products`) | 30 |
| Catégories (`categories`) | 30 |
| Comptes (`accounts`) | 150 000 |
| Souscriptions (`subscriptions`) | 120 000 |
| Cartes (`cards`) | 120 000 |
| Transactions (`transactions`) | 1 000 000 |

Le nombre d’utilisateurs correspond à 100 000 clients, 500 conseillers et un compte administrateur, si la version actuelle du générateur suit cette convention.

Les quantités réelles peuvent différer si le script a évolué, si des insertions ont échoué ou si le générateur a été exécuté plusieurs fois. Consultez `backend/seed_database.py` pour les constantes, les boucles et la stratégie de réinitialisation.

### Attention aux exécutions répétées

Avant de relancer le générateur, vérifiez s’il supprime/réinitialise les données ou s’il ajoute des lignes. Une seconde exécution peut produire des doublons ou échouer sur des contraintes d’unicité.

**Ne lancez pas le script de génération sur la base partagée Supabase** sans accord de l’équipe et sans comprendre précisément son effet.

## 7. Vérifier les données

### Avec DBeaver

1. Créez une connexion PostgreSQL.
2. Saisissez l’hôte, le port, la base, l’utilisateur et le mot de passe.
3. Cliquez sur **Test Connection**.
4. Développez la base, puis `Schemas` → `public` → `Tables`.
5. Ouvrez les tables et sélectionnez **View Data** pour inspecter les lignes.

### Avec SQL

Dans DBeaver, ouvrez un éditeur SQL et exécutez les requêtes suivantes :

```sql
SELECT COUNT(*) FROM customers;
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM accounts;
SELECT COUNT(*) FROM subscriptions;
SELECT COUNT(*) FROM cards;
SELECT COUNT(*) FROM transactions;
SELECT COUNT(*) FROM advisors;
SELECT COUNT(*) FROM banking_products;
SELECT COUNT(*) FROM categories;
```

Les noms exacts peuvent varier selon les modèles SQLAlchemy et les migrations. Si une table n’existe pas sous ce nom, vérifiez son nom dans l’arborescence DBeaver.

### Vérifier les relations

Inspectez quelques lignes et les clés étrangères afin de vérifier les relations entre :

- les comptes et les clients ;
- les cartes et les comptes ;
- les transactions et les comptes, cartes ou catégories ;
- les souscriptions et les clients et produits.

Les relations doivent respecter les contraintes définies dans le schéma.

## 8. Utiliser DBeaver

### Connexion à la base locale

| Champ | Valeur |
|---|---|
| Driver | PostgreSQL |
| Host | `localhost` |
| Port | `5432` |
| Database | `generative_banking_ui` |
| Username | `postgres` ou utilisateur local |
| Password | Mot de passe PostgreSQL local |

Cliquez sur **Test Connection**, puis **Finish** si le test réussit.

Pour la base Supabase, utilisez les paramètres fournis par le tableau de bord et activez SSL si nécessaire. Le mot de passe Supabase est distinct du mot de passe PostgreSQL local.

## 9. Partager la même base avec Supabase

Cette étape permet aux membres de l’équipe de travailler sur les mêmes données.

1. Créez un projet Supabase.
2. Ouvrez **Connect**.
3. Choisissez une méthode de connexion prise en charge par votre réseau.
4. Si la connexion directe exige IPv6 et que votre réseau ne le prend pas en charge, utilisez le **Session pooler**.
5. Récupérez les paramètres fournis par Supabase : hôte, port, base, utilisateur et mode SSL.
6. Configurez le `.env` local de chaque membre pour connecter son backend à cette même base distante.
7. Testez la connexion avant de lancer l’application.

Les paramètres dépendent du projet Supabase : ne copiez pas ceux d’un autre projet. Le mot de passe à utiliser est celui de la base Supabase.

### Si le dataset existe déjà en local

Utilisez la procédure d’export/import de la section suivante pour transférer le schéma et les données existantes.

Avant l’import, assurez-vous que la base distante ne contient pas déjà les tables applicatives. Si elle contient des données, faites une sauvegarde et définissez une stratégie de migration au lieu de lancer une restauration sans vérification.

Après l’import, vérifiez les volumes dans Supabase avant de connecter tous les membres.

## 10. Exporter et importer une sauvegarde

### Exporter la base locale

Sous Windows, si PostgreSQL 18 est installé dans `C:\Program Files\PostgreSQL\18\bin`, placez-vous dans le dossier du projet :

```powershell
cd "C:\Users\<UTILISATEUR>\OneDrive\Desktop\Projets_IMT\generative-banking-ui"
```

Adaptez le chemin à votre ordinateur.

Lancez ensuite :

```powershell
& "C:\Program Files\PostgreSQL\18\bin\pg_dump.exe" `
  -h localhost `
  -p 5432 `
  -U postgres `
  -d generative_banking_ui `
  -Fc `
  -f ".\generative_banking_ui.backup"
```

Saisissez le mot de passe PostgreSQL local si demandé. Pendant la saisie, PowerShell n’affiche aucun caractère : c’est normal.

Vérifiez que le fichier existe :

```powershell
Get-Item ".\generative_banking_ui.backup" |
  Select-Object Name, Length
```

### Importer dans Supabase

Utilisez uniquement les paramètres de connexion affichés dans **Connect** pour votre propre projet.

Exemple de commande à adapter :

```powershell
$env:PGSSLMODE = "require"

& "C:\Program Files\PostgreSQL\18\bin\pg_restore.exe" `
  --verbose `
  --no-owner `
  --no-privileges `
  --host="<HOTE_FOURNI_PAR_SUPABASE>" `
  --port=<PORT_FOURNI_PAR_SUPABASE> `
  --username="<UTILISATEUR_FOURNI_PAR_SUPABASE>" `
  --dbname="postgres" `
  ".\generative_banking_ui.backup"
```

Lorsque `pg_restore` demande un mot de passe, saisissez celui de la base Supabase. Aucun caractère ne s’affiche pendant la saisie.

**Précautions importantes :**

- Ne lancez la restauration qu’après avoir confirmé que la base cible est vide ou qu’une stratégie de restauration appropriée a été définie.
- `--no-owner` et `--no-privileges` évitent de restaurer les propriétaires et permissions locales qui ne correspondent pas nécessairement aux rôles Supabase.
- Certaines extensions, permissions ou fonctions PostgreSQL peuvent nécessiter une adaptation sur un service géré.
- Si la restauration échoue à mi-chemin, la base distante peut être partiellement remplie. Lisez les erreurs avant de réessayer.
- N’incluez jamais le mot de passe directement dans la commande ou dans un fichier versionné.

### Vérifier l’import

Dans Supabase → **Table Editor**, vérifiez les principales tables. Vous pouvez également exécuter les requêtes `COUNT(*)` de la section 7 dans l’éditeur SQL Supabase, en adaptant les noms si nécessaire.

## 11. Sécurité et Git

Le dépôt Git doit contenir le code nécessaire pour recréer la base, mais pas les secrets ni une sauvegarde volumineuse.

Ajoutez ces règles à `.gitignore` :

```gitignore
.env
.env.*
!.env.example
.venv/
__pycache__/
*.py[cod]
generative_banking_ui.backup
*.dump
*.sql
```

Ne mettez pas `.env` sur GitHub. Si des identifiants ont déjà été commités, les supprimer dans un commit ultérieur ne suffit pas : changez les secrets concernés.

Partagez avec l’équipe :

- le code source ;
- les modèles et migrations ;
- le script de génération ;
- un `.env.example` sans secrets ;
- ce README.

Ne partagez pas dans Git :

- les mots de passe ;
- les URI Supabase contenant les identifiants ;
- le fichier `.backup` ;
- des données bancaires réelles.

Utilisez des permissions adaptées pour l’accès à la base commune. Évitez de donner à tous les membres le rôle administrateur PostgreSQL si des droits plus limités suffisent.

## 12. Dépannage

### `pg_dump` ou `pg_restore` n’est pas reconnu

Utilisez le chemin complet vers l’exécutable :

```powershell
& "C:\Program Files\PostgreSQL\18\bin\pg_dump.exe" --version
& "C:\Program Files\PostgreSQL\18\bin\pg_restore.exe" --version
```

Adaptez le chemin si PostgreSQL est installé ailleurs.

### Rien ne s’affiche pendant la saisie du mot de passe

C’est normal dans PowerShell. Tapez le mot de passe et appuyez sur Entrée.

### Échec de connexion Supabase

- Vérifiez l’hôte, le port, l’utilisateur et le nom de la base dans le tableau de bord.
- Vérifiez le mot de passe Supabase, distinct du mot de passe PostgreSQL local.
- Vérifiez le mode SSL.
- Si la connexion directe exige IPv6 et que votre réseau ne le prend pas en charge, utilisez le Session pooler.
- Ne publiez pas les détails de connexion dans un ticket public.

### Une table existe déjà pendant la restauration

Arrêtez-vous et examinez l’état de la base distante. Ne supprimez pas les tables et ne relancez pas l’import sans comprendre quelles données sont déjà présentes.

### Les volumes ne correspondent pas aux valeurs de référence

Vérifiez les paramètres du générateur, les éventuelles erreurs d’insertion, les doublons et le nombre réel de lignes. Les valeurs du tableau sont des objectifs documentés, pas une garantie indépendante du code exécuté.

---

## Procédure recommandée pour un nouveau membre

1. Cloner le dépôt Git.
2. Installer les dépendances.
3. Créer son fichier `.env` local sans le committer.
4. Configurer la connexion à la base Supabase commune.
5. **Ne pas lancer `seed_database.py` sur la base commune.**
6. Démarrer le backend et vérifier qu’il lit les données attendues.

Ainsi, l’équipe partage le même code dans Git et la même base de données sur Supabase.
