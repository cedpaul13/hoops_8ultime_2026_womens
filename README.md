# Hoops 8 Ultime 2026: U SPORTS Women's Final 8 Analytics

Eight teams, one national title, four days at PEPS. I built a model to call the 2026 U SPORTS Women's Final 8 before tip-off, then watched the tournament argue with it — hardest of all on the team it had given a 0.0% chance at gold.

**The full story, results and visuals live [here](https://cedpaul13.github.io/hoops_8ultime_2026_womens/).**

The site is available in English and French.

Why it's worth the click:

* A near-exact quarterfinal call — Saskatchewan projected 71–56 over UBC, final score 71–55
* Laval flagged as a live underdog against the No. 1 seed — and they won it outright
* Both Saturday semifinal moneylines called correctly
* A team given a 0.0% shot at gold before the tournament reached the final — and the model's original pick still walked away with it anyway

---

## Dig deeper

* [Post-mortem: the full technical accounting](./outputs/post_mortem/2026_womens_final8_post_mortem.md)
* [Model configuration](./src/modeling/config.py)
* [Team data & metrics glossary](./data/team_metrics.csv)
* [Companion project: March Madness 2026](https://cedpaul13.github.io/March_Madness_2026/)

---

## Run the pipeline

This repository holds the code behind the model, nicknamed the Temporal Predictor: recent-form weighting, conference-normalized strength of schedule, situational adjustments (home court, rest, pressure), and Monte Carlo bracket simulation.

**1. Create the environment**

```bash
conda env create -f environment.yml
conda activate hoops_8ultime_2026
```

**2. Explore the model**

* `src/modeling/predictor.py` — `Final8TemporalPredictor`, single-game projections
* `src/modeling/simulator.py` — Monte Carlo match simulation and team database
* `src/modeling/tournament_bracket.py` — full bracket simulation, medal probabilities
* `src/modeling/backtest.py` — historical validation, 2019–2025
* `src/modeling/config.py` — tunable weights and situational factors

Prediction archives live in `outputs/predictions/`; raw and processed data live in `data/`.
