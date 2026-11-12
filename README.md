# Hoops 8 Ultime 2026: U SPORTS Women's Final 8 Analytics

Eight teams, one national title, four days at the PEPS. I built a model to call the 2026 U SPORTS Women's Final 8 before tip-off, then watched the tournament argue with it — hardest of all on the team it had given a 0.0% chance at gold.

**The full story, results and visuals live [here](https://cedpaul13.github.io/hoops_8ultime_2026_womens/).**

The site is available in English and French.

The bilingual brief keeps each finding in one place: charts carry the figures, player cards carry individual performances, and prose adds context or limitations rather than repeating results. Backtest, team data and local coverage are expandable. The interface supports saved dark/light preferences, keyboard navigation and reduced motion; charts remain readable without JavaScript.

The self-contained site source is versioned in [`docs/index.html`](./docs/index.html). It needs no framework or build step. Editing or previewing it does not deploy it.

Why it's worth the click:

* A near-exact quarterfinal call — Saskatchewan projected 71–56 over UBC, final score 71–55
* Host Laval flagged as a live underdog against the No. 1 seed — and they won it outright, in front of 2,000+ at home
* Both Saturday semifinal moneylines called correctly
* A team given a 0.0% shot at gold before the tournament reached the final — and the model's original pick still walked away with it anyway

---

## Host: Université Laval & Québec City

The 54th edition of the championship was hosted by **Université Laval in Québec City**, March 4–8, 2026 — the **fifth time** the city has staged the U SPORTS women's Final 8, after 1987, 1991, 1996 and 2015. That is more than any other host in the tournament's history.

All eleven games were played at the **Amphithéâtre Desjardins**, the arena inside the PEPS complex, reconfigured to roughly 3,000 seats for the week (1,884 permanent, plus 1,208 removable bleachers at courtside). The tournament ran under the Sun Life banner, presented by Michelob Ultra and the Hilton Québec.

The host **Rouge et Or** entered as the No. 8 seed at 20–7 and immediately knocked off No. 1 TMU 57–54, on a Sabrine Khelifi three with 15 seconds left, before a home crowd of more than 2,000 — the first time a top seed had lost a Final 8 quarterfinal since 2006. Laval then fell to eventual champion Saskatchewan in the semifinal (55–43) and to Calgary in the bronze game (66–59), finishing fourth.

**Host & local coverage**

* [Rouge et Or — Le 8 Ultime (official host page)](https://rougeetor.ulaval.ca/8ultime/)
* [Radio-Canada — « Le Rouge et Or fait tomber les meilleures au pays »](https://ici.radio-canada.ca/nouvelle/2235306/rouge-or-basketball-feminin-championnat-khelifi-tmu)
* [Radio-Canada — « Le Rouge et Or au pied du podium canadien »](https://ici.radio-canada.ca/nouvelle/2236061/rouge-or-basketball-8-ultime-laval-championnat-feminin)
* [Le Soleil — « Dans les coulisses d'un tournoi national à Laval »](https://www.lesoleil.com/sports/2026/03/06/dans-les-coulisses-dun-tournoi-national-a-laval-X62LQXKAJBAR7LOYJGPKE77HDM/)
* [U SPORTS — championship returns to Québec in 2026](https://en.usports.ca/corporate/Releases/WBALL2026LAVAL)

---

## Dig deeper

* [Post-mortem: the full technical accounting](./outputs/post_mortem/2026_womens_final8_post_mortem.md)
* [Model configuration](./src/modeling/config.py)
* [Team data & metrics glossary](./data/team_metrics.csv)
* [Companion project: March Madness 2026](https://cedpaul13.github.io/March_Madness_2026/)

---

## Site quality checks

With Node.js 22 or newer:

```bash
npm ci
npx playwright install chromium firefox webkit
npm test
```

The suite checks keyboard navigation, mobile reflow, 200% text resizing, bilingual numbers, saved/blocked preferences, image failures, reduced motion and operation without JavaScript. Axe scans both languages and themes on desktop/mobile in Chromium, Firefox and WebKit. Deployment guards are tested with mocked Git/npm commands; external images are mocked for deterministic browser runs. These tests do not verify remote image availability, scientific model accuracy or production Core Web Vitals.

The [site workflow](./.github/workflows/site.yml) runs these checks on relevant pushes and pull requests. Automated accessibility scans complement, but do not replace, assistive-technology testing.

To publish, run `bash scripts/deploy_site.sh` explicitly. It runs the suite first and replaces `gh-pages` only if its remote tip has not changed since it was read. It never publishes `node_modules`, test reports or model data.

Alternatively, manually run **Site quality** on `main` in GitHub Actions with **Deploy the tested site to gh-pages** enabled. The Linux runner validates all three browsers before deployment, then runs the same guarded script and requests a Pages build. Ordinary pushes only validate the site.

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
