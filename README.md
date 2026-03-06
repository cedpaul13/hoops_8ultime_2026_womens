# Hoops 8 Ultime 2026 - Women's Basketball Analytics 🏀

Projet de prédiction analytique pour le Championnat féminin U Sports 2026 au PEPS (Québec). Ce dépôt utilise des modèles de simulation Monte Carlo et des analyses de tendances récentes pour projeter les résultats du tournoi national.

---

## 🔗 LIENS OFFICIELS & RÉSULTATS
- **Hôte (Rouge et Or)** : [Site Officiel du 8 Ultime](https://rougeetor.ulaval.ca/8ultime/)
- **Championnat U Sports** : [Page Centrale du Championnat](https://fr.usports.ca/championships/2025-26/2025-26_Basketball_Feminin/index)

### Suivi des résultats par jour
- [Quarts de Finale (Jeudi 05 mars)](https://fr.usports.ca/sports/wbkb/composite?d=2026-03-05)
- [Demi-Finales Consolation (Vendredi 06 mars)](https://fr.usports.ca/sports/wbkb/composite?d=2026-03-06)
- [Finales Consolation & Demi-Finales Championnat (Samedi 07 mars)](https://fr.usports.ca/sports/wbkb/composite?d=2026-03-07)
- [Match de Bronze & Finale (Dimanche 08 mars)](https://fr.usports.ca/sports/wbkb/composite?d=2026-03-08)

---

## ⚡ LIVE DASHBOARD : PRÉDICTIONS

### Demi-Finales de Consolation (Vendredi 06 mars)
| Heure | Match | Proj. Score | Win Prob | ML | Spread |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **17h00** | **Carleton (7) vs McGill (6)** | **50 - 47** | 63.27% (CAR) | -172 | CAR -3.0 |
| **19h00** | **UBC (4) vs TMU (1)** | **50 - 59** | 82.79% (TMU) | -481 | TMU -8.5 |

### Demi-Finales de Championnat (Samedi 07 mars)
| Heure | Match | Proj. Score | Win Prob | ML | Spread |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **15h00** | **UNB (2) vs Calgary (3)** | **66 - 64** | 57.56% (UNB) | -135 | UNB -1.5 |
| **18h00** | **Saskatchewan (5) vs Laval (8)** | **63 - 55** | 79.83% (SAS) | -395 | SAS -8.0 |

---
 
## 🏆 PROBABILITÉS DE MÉDAILLES (POST-QF)
*Simulation Monte Carlo (N=10,000)*

| Équipe (Seed) | Or | Argent | Bronze |
| :--- | :---: | :---: | :---: |
| **UNB (2)** | **43.5%** | 14.1% | 38.7% |
| **Saskatchewan (5)** | **30.9%** | 54.8% | 5.6% |
| **Calgary (3)** | **24.4%** | 18.1% | 47.0% |
| **Laval (8)** | **1.3%** | 13.0% | 8.7% |

---

## 📊 ANALYSE DE PERFORMANCE (PHASE QF)

Le modèle heuristique surnommé **Temporal Predictor** a validé l'importance des variables de terrain et du resserrement défensif lors de la première journée.

- **Saskatchewan (5) vs UBC (4)** : Proj: 71-56 | Réel: **71-55**. Anticipation quasi parfaite de la domination défensive des Huskies.
- **Calgary (3) vs McGill (6)** : Proj: 62-50 | Réel: **58-45**. Écart projeté de 12 vs 13 réel. Un départ exceptionnellement lent (7-1 après 6 min) a maintenu le score total sous les projections malgré un spread précis.
- **TMU (1) vs Laval (8)** : Spread proj: -0.5 | Réel: **54-57**. Identification réussie de la vulnérabilité du Seed #1 face à la pression du PEPS.
- **MAE Globale (QF) : 9.0 points.**

### Focus UNB vs Carleton : L'effet Katie Butts
La dominance de la joueuse de l'UNB #21, **Katie Butts**, a été le facteur X de cette première journée. Avec **33 pts et 15 rebonds** (9/14 au tir), elle a pulvérisé ses moyennes de saison (19 pts, 12 reb). Cette pression constante sur l'anneau a provoqué une crise de fautes chez Carleton, menant à l'exclusion de deux joueuses clés. Le modèle a été recalibré avec un **Elite Player Factor** pour refléter ce type d'impact individuel en phase éliminatoire.



---

## ⚙️ MÉTHODOLOGIE & STRUCTURE
- **K-Last Games (75%)** : Priorité sur la forme récente (playoffs + QF) vs saison régulière (25%).
- **Monte Carlo** : 10,000 itérations pour stabiliser les probabilités et les cotes Moneyline.
- **Dossiers** : `src/modeling/` (moteur), `outputs/predictions/` (archives).

## 📖 GLOSSAIRE RAPIDE
- **Recent_PPG/PA** : Moyenne sur les 5 derniers matchs.
- **Pressure Index** : Indice de fatigue psychologique ou environnementale (0.95 = Stress élevé).
- **SOS_adj** : Force du calendrier normalisée entre les conférences (CW, OUA, RSEQ, AUS).
- **MAE** : Mean Absolute Error (marge d'erreur moyenne). Utilisé pré-QF pour valider la précision du modèle.