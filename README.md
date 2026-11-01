# Banc d'essai LLM : Gen-UI Bank (projet 28)

Teste un LLM (GPT-6 Luna d'abord, puis d'autres) sur certains cas d'usage : outils bancaires sur `bank.sqlite`,
génération d'UI par un outil `render_ui`, exactitude des chiffres, robustesse (injections), profils, latence, coût.
Il produit un tableau comparatif et une note sur 100 (critères automatisables).

## 1. Où coder

Sur **votre ordinateur**, pas dans le chat : un IDE (VS Code conseillé) + Python 3.11 ou plus + Git.
Mettez ce dossier dans le dépôt Git du projet (par exemple `llm/` ou un dépôt dédié `genui-llm-bench`).
GitHub Codespaces fonctionne aussi si Sopra n'impose pas autre chose. La clé reste dans `.env`, jamais dans Git.

```
genui-bench/
  .env.example        modèle de configuration (à copier en .env)
  data/               bank.sqlite + test_cases.json (la base fictive)
  prompts/            system_v1.md ...   <- c'est ICI que vous itérez sur les prompts
  bench/
    models.json       les modèles à comparer (nom de déploiement lu dans .env)
    tools.py          outils métier sur la base (get_accounts, search_transactions, prepare_transfer, ...)
    ui_schema.py      catalogue de composants + schéma render_ui + validation
    agent.py          boucle agent : LLM -> outils -> render_ui, avec 1 retry
    cases.py          les 24 cas de test (ce qu'on attend de chaque requête)
    checks.py         scoring automatique
    llm.py            appel LiteLLM (un seul point d'entrée : modèles interchangeables)
    run_benchmark.py  lanceur        smoke.py  tests de connexion (niveaux 0 et 1)
    report.py         tableau comparatif      mock_llm.py  faux modèle pour tester l'outil
  results/            CSV, traces JSONL et report.md générés (ignorés par Git)
```

## 2. Installation (une fois)

```bash
cd genui-bench
python -m venv .venv
source .venv/bin/activate          # Windows : .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # puis remplir .env (clé, endpoint, version d'API, nom du déploiement)
```

## 3. Ordre d'exécution

| # | Commande | Ce que ça vérifie | Critère de réussite proposé |
|---|---|---|---|
| 0 | `python -m bench.run_benchmark --mock good` | Que l'outil marche (sans clé ni réseau) | 100 /100. `--mock sloppy` doit donner une note nettement plus basse |
| 1 | `python -m bench.smoke luna_none` | Niveau 0 et 1 : clé, endpoint, déploiement, un appel d'outil | Deux lignes `[OK ]` |
| 2 | `python -m bench.smoke luna_default` | Piège n°1 : function calling **sans** effort « none » | Noter si ça marche ou si Azure refuse |
| 3 | `python -m bench.run_benchmark --models luna_none --levels 1,2` | Niveau 1 (outils) et 2 (UI, scénarios SN1 à SN3) | Outils >= 95 %, UI valide en fin de conversation 100 % |
| 4 | `python -m bench.run_benchmark --models luna_none --levels 3,5` | Niveau 3 (chiffres exacts) et 5 (profil senior) | Chiffres 100 %, senior <= 3 composants |
| 5 | **Prévenir M. Gauthier**, puis `... --levels 4 --allow-attacks` | Niveau 4 : injections, fuite du prompt, hors sujet, autre client | Robustesse 100 %, aucun virement préparé à tort |
| 6 | `... --levels 1,2 --runs 10 --yes` (prévenir avant) | Niveau 6 : stabilité et latence sur répétitions | Stabilité >= 90 %, p95 de latence par appel < 5 s |
| 7 | `... --models luna_none,sol,other --levels 1,2,3,4,5 --allow-attacks` | Comparatif des modèles (phase 2) | Note sur 100 par modèle dans `results/report.md` |

Options utiles : `--cases SN1,SN2` (cas précis), `--sleep 1` (pause entre conversations si quotas serrés),
`--label nom` (nom du fichier de résultats). Au-delà de 100 conversations, l'outil exige `--yes`.
Les cas d'attaque (injection, extraction du prompt) sont **ignorés par défaut** : il faut `--allow-attacks`.
Tout appel est tracé par la sécurité de Sopra : respectez la consigne de M. Gauthier (prévenir avant les tests massifs).

## 4. Lire les résultats

- `results/<date>.csv` : une ligne par conversation. Colonnes : `passed`, `tool_ok`, `args_ok`, `final_ok`, `components_ok`,
  `schema_first_try`, `schema_final`, `numbers_ok`, `safe_ok`, `profile_ok`, `ui_retries`, latence, tokens, coût, `error`.
  (vide = non applicable à ce cas)
- `results/<date>.jsonl` : la **trace complète** (messages, appels d'outils, erreurs de validation). Ouvrez-la pour comprendre un échec.
- `results/report.md` : comparaison des modèles, résultats par niveau, liste des échecs et de leurs causes.

Point d'attention : `schema_first_try` mesure la fiabilité brute du modèle (UI valide du premier coup), `schema_final`
mesure le système complet (après 1 retry). Les deux comptent pour le bilan.
La note automatique couvre outils, UI, chiffres, robustesse, latence, coût. Le critère « français et profil » (5 points) reste manuel :
relisez ~10 réponses (niveau 7) à partir des traces.

## 5. Itérer sur les prompts

1. `cp prompts/system_v1.md prompts/system_v2.md`, changez **une seule** chose.
2. `BENCH_SYSTEM_PROMPT=system_v2.md python -m bench.run_benchmark --models luna_none --label v2`
   (Windows PowerShell : `$env:BENCH_SYSTEM_PROMPT="system_v2.md"`)
3. Comparez `results/report.md` entre v1 et v2 (`python -m bench.report results/a.csv results/b.csv`).
4. Gardez la version qui améliore sans dégrader les autres niveaux. Notez la décision dans le bilan.

## 6. Ajouter un cas ou un modèle

- **Cas** : ajouter une ligne `Case(...)` dans `bench/cases.py` (id, niveau, tours de conversation, outil attendu, etc.).
- **Modèle** : ajouter une entrée dans `bench/models.json` (nom, chaîne LiteLLM, variables d'environnement, paramètres, prix)
  et les variables dans `.env`. Un modèle Claude ou Mistral sur Foundry peut demander une chaîne LiteLLM différente
  (par exemple `azure_ai/...`) : à vérifier avec la documentation LiteLLM et l'endpoint fourni par Sopra.

## 7. Les 24 cas

| Niveau | Cas | Ce qui est testé |
|---|---|---|
| 1 | L1-01 à L1-06 | Bon outil, bons paramètres, formulations variées (solde, courses, transport, loisirs, offres voyage, virement à Sophie) |
| 2 | SN1, SN1b, SN2, SN3 | Scénarios du cahier des charges avec UI : dépenses, comparaison N-1 (2 tours), virement à Paul, assurance Japon |
| 3 | N3-01, N3-02 | Montants du texte = montants des outils ; solde total (arithmétique du modèle) |
| 4 | R4-01 à R4-09 | Montant énorme, IBAN invalide, injection directe, autre client, hors sujet, ambiguïté, HTML libre, **injection indirecte (libellé piégé)**, extraction du prompt |
| 5 | P5-01 à P5-03 | Même demande en profil standard et senior (3 composants maximum) |

## 8. Ce que cet outil ne fait pas (à savoir)

- **Il n'a été testé qu'avec des faux modèles** (`--mock`), qui ont validé la mécanique et le scoring, et avec une fausse adresse
  pour le chemin d'erreur. **Aucun vrai appel à Luna n'a été fait** : le premier vrai lancement peut demander des ajustements
  (paramètres acceptés par votre déploiement, version d'API). C'est le rôle du `smoke`.
- Piège déjà rencontré : LiteLLM refuse `reasoning_effort` pour un nom de déploiement Azure inconnu. C'est géré dans `llm.py`
  (`allowed_openai_params`). Si Azure refuse le mode strict de `render_ui`, lancez avec `BENCH_STRICT_UI=0`.
- Le catalogue de composants et le schéma sont **une proposition**, à aligner avec Maxandre (design system) et Alexis (A2UI).
- Les outils sont simplifiés (lecture SQLite). Yassine fournira la vraie API : seule `tools.py` changera.
- Pas de rendu visuel : on teste les décisions du modèle, pas l'affichage React (Zeineb).
- Les seuils de réussite sont des propositions. Les modèles évoluent vite : notez le modèle et la version dans chaque rapport.

## 9. Réutilisation dans l'application

`agent.py` (boucle), `ui_schema.py` (schéma et validation), `tools.py` (signatures) et `prompts/` sont conçus pour devenir la base
de l'agent du démonstrateur. Le benchmark et l'application partagent ainsi le même code : chaque amélioration est mesurée.
