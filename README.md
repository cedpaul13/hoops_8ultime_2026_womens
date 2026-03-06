# Hoops 8 Ultime 2026 - Women's Basketball Analytics 🏀

Projet de prédiction analytique pour le Championnat féminin U Sports 2026 au PEPS (Québec).

---

## ⚡ LIVE DASHBOARD : PRÉDICTIONS

### Demi-Finales de Consolation (Vendredi)
| Heure | Match | Proj. Score | Win Prob | ML | Spread |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **17h00** | **Carleton (7) vs McGill (6)** | **50 - 47** | 63.27% (CAR) | -172 | CAR -3.0 |
| **19h00** | **UBC (4) vs TMU (1)** | **50 - 59** | 82.79% (TMU) | -481 | TMU -8.5 |

### Demi-Finales de Championnat (Samedi)
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

Le modèle **Temporal Predictor v1.5** a validé l'importance des variables de terrain et du resserrement défensif lors de la première journée.

- **Saskatchewan (5) vs UBC (4)** : Proj: 71-56 | Réel: **71-55**. Anticipation parfaite de la domination défensive des Huskies.
- **Calgary (3) vs McGill (6)** : Proj: 62-50 | Réel: **58-45**. Écart projeté de 12 vs 13 réel. Le départ lent (7-1) a maintenu le score sous le total projeté.
- **TMU (1) vs Laval (8)** : Spread proj: -0.5 | Réel: **54-57**. Identification réussie de la vulnérabilité du Seed #1 au PEPS.
- **MAE Globale (QF) : 9.0 points.**

> **Focus UNB vs Carleton** : L'anomalie **Katie Butts** (33 pts, 15 reb) a été la joueuse dominante des quarts de finale en dépassant sa moyenne de saison de 19 pts et 12 reb. Le modèle est désormais calibré avec un **Elite Player Factor** pour la suite.

---

## ⚙️ MÉTHODOLOGIE & STRUCTURE
- **K-Last Games (75%)** : Priorité sur la forme récente (Playoffs + QF) vs Saison (25%).
- **Monte Carlo** : 10,000 itérations pour stabiliser spreads et moneyline.
- **Dossiers** : `src/modeling/` (moteur), `outputs/predictions/` (archives).

## 📖 GLOSSAIRE RAPIDE
- **Recent_PPG/PA** : Moyenne sur les 5 derniers matchs.
- **Pressure Index** : Fatigue psychologique (0.95 = Stress élevé).
- **SOS_adj** : Force du calendrier normalisée entre conférences.