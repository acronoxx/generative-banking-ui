# Resultats du benchmark LLM

Sources : 20261108_235427_v6_full.csv

## Comparaison des modeles

| Modele | Conv. | Reussite | Outils | UI valide 1er essai | Chiffres exacts | Robustesse | Retries | Erreurs | Latence p50 / p95 (s/appel) | Tokens in/out | Cout / 100 conv. ($) | Note /100* |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| luna_none | 29 | 97 % | 100 % | 100 % | 100 % | 92 % | 0 | 1 | 1.6 / 1.9 | 2459 / 81 | 0.029 | 99 |

*Note automatique : poids outils 25, UI 25, chiffres 15, robustesse 15, latence 10, cout 5 (renormalises). Le critere 'francais et profil' (5 points) reste manuel : lecture humaine, niveau 7.

## Resultats par niveau

| Modele | Niveau | Conv. | Reussite |
|---|---|---|---|
| luna_none | 1 | 6 | 100 % |
| luna_none | 2 | 6 | 100 % |
| luna_none | 3 | 2 | 100 % |
| luna_none | 4 | 12 | 92 % |
| luna_none | 5 | 3 | 100 % |

## Echecs a analyser

| Modele | Cas | Run | Type final | Verifications en echec | Erreur |
|---|---|---|---|---|---|
| luna_none | H4-03 | 1 | error | final_ok | BadRequestError: litellm.BadRequestError: OpenAIException - The response was fil |