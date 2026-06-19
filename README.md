# Hoops 8 Ultime 2026 - Women's Basketball Analytics

Analytics and prediction project for the 2026 U SPORTS Women's Final 8 at PEPS in Quebec City. This repository uses Monte Carlo simulation models and recent-form analysis to project national tournament results.

---

## Official Links & Results

- **Host site (Rouge et Or)**: [Official 8 Ultime Site](https://rougeetor.ulaval.ca/8ultime/)
- **U SPORTS Championship**: [Championship Central](https://fr.usports.ca/championships/2025-26/2025-26_Basketball_Feminin/index)

### Daily Results Tracking

- [Quarter-finals - Thursday, March 5](https://fr.usports.ca/sports/wbkb/composite?d=2026-03-05)
- [Consolation Semi-finals - Friday, March 6](https://fr.usports.ca/sports/wbkb/composite?d=2026-03-06)
- [Consolation Final & Championship Semi-finals - Saturday, March 7](https://fr.usports.ca/sports/wbkb/composite?d=2026-03-07)
- [Bronze Medal Game & Final - Sunday, March 8](https://fr.usports.ca/sports/wbkb/composite?d=2026-03-08)

---

## Live Dashboard: Predictions

### Consolation Semi-finals - Friday, March 6

| Time | Matchup | Projected Score | Win Prob | ML | Spread |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **17:00** | **Carleton (7) vs McGill (6)** | **50 - 47** | 63.27% (CAR) | -172 | CAR -3.0 |
| **19:00** | **UBC (4) vs TMU (1)** | **50 - 59** | 82.79% (TMU) | -481 | TMU -8.5 |

### Championship Semi-finals - Saturday, March 7

| Time | Matchup | Projected Score | Win Prob | ML | Spread |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **15:00** | **UNB (2) vs Calgary (3)** | **66 - 64** | 57.56% (UNB) | -135 | UNB -1.5 |
| **18:00** | **Saskatchewan (5) vs Laval (8)** | **63 - 55** | 79.83% (SAS) | -395 | SAS -8.0 |

---

## Medal Probabilities - Post-QF

*Monte Carlo simulation, N=10,000*

| Team (Seed) | Gold | Silver | Bronze |
| :--- | :---: | :---: | :---: |
| **UNB (2)** | **43.5%** | 14.1% | 38.7% |
| **Saskatchewan (5)** | **30.9%** | 54.8% | 5.6% |
| **Calgary (3)** | **24.4%** | 18.1% | 47.0% |
| **Laval (8)** | **1.3%** | 13.0% | 8.7% |

---

## Performance Analysis - Quarter-finals

The heuristic model, nicknamed **Temporal Predictor**, validated the importance of venue context and defensive tightening on the first day of the tournament.

- **Saskatchewan (5) vs UBC (4)**: Projected 71-56 | Actual **71-55**. Near-perfect read on the Huskies' defensive control.
- **Calgary (3) vs McGill (6)**: Projected 62-50 | Actual **58-45**. Projected margin of 12 vs actual margin of 13. An exceptionally slow start kept the total below projection, while the spread read stayed accurate.
- **TMU (1) vs Laval (8)**: Projected spread TMU -0.5 | Actual **Laval 57, TMU 54**. The model correctly identified the No. 1 seed's vulnerability against PEPS pressure.
- **Overall QF MAE: 9.0 points.**

### UNB vs Carleton Focus: The Katie Butts Effect

UNB #21 **Katie Butts** was the first day's biggest swing factor. Her 33 points and 15 rebounds on 9/14 shooting exceeded her season averages and put constant pressure on the rim. That pressure created foul trouble for Carleton and pushed two key players out of the game. The model was recalibrated with an **Elite Player Factor** to better capture this kind of individual playoff impact.

### Final Post-Mortem

- [Final recap, official scores, and lessons learned](outputs/post_mortem/2026_womens_final8_post_mortem.md)

---

## Methodology & Structure

- **K-Last Games (75%)**: Recent form is weighted heavily, including playoff and QF performance, compared with regular-season form (25%).
- **Monte Carlo**: 10,000 simulations stabilize win probabilities and moneyline-style odds.
- **Folders**: `src/modeling/` contains the model engine; `outputs/predictions/` stores prediction archives.

## Quick Glossary

- **Recent_PPG/PA**: Points scored and allowed over the last five games.
- **Pressure Index**: Psychological or environmental stress indicator, where 0.95 represents high stress.
- **SOS_adj**: Conference-normalized strength of schedule across CW, OUA, RSEQ, and AUS.
- **MAE**: Mean Absolute Error, used pre-QF to validate model accuracy.
