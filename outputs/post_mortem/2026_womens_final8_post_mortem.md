# Post-Mortem - U SPORTS Women's Final 8 2026

## Final Results

Source checked: 2026 U SPORTS Women's Basketball Championship bracket, March 4-8, 2026.

### Medal Games

| Game | Result | Model read |
| :--- | :--- | :--- |
| Gold | Saskatchewan 77, UNB 68 | Saskatchewan won as the tournament's true top-end team, despite being only 30.9% for gold after QF. |
| Bronze | Calgary 66, Laval 59 | Calgary covered a bigger medal-game spread than the semi-final style model would have implied. |
| 5th place | Carleton 60, TMU 58 | Consolation games were tight and noisy; motivational differences mattered. |

### Championship Bracket

| Round | Result |
| :--- | :--- |
| QF | Laval 57, TMU 54 |
| QF | Saskatchewan 71, UBC 55 |
| QF | UNB 81, Carleton 63 |
| QF | Calgary 58, McGill 45 |
| SF | Saskatchewan 55, Laval 43 |
| SF | UNB 70, Calgary 66 |
| Bronze | Calgary 66, Laval 59 |
| Final | Saskatchewan 77, UNB 68 |

### Consolation Bracket

| Round | Result |
| :--- | :--- |
| Consolation SF | TMU 68, UBC 66 |
| Consolation SF | Carleton 64, McGill 62 |
| 5th place | Carleton 60, TMU 58 |

## What The Model Got Right

- Saskatchewan vs UBC was nailed: projected 71-56, actual 71-55.
- Calgary vs McGill was directionally clean: projected Calgary by 12, actual Calgary by 13.
- Laval was correctly flagged as a dangerous host against TMU; the model had TMU only -0.5 and Laval won outright.
- Saturday semi-final moneylines were both right: UNB over Calgary and Saskatchewan over Laval.

## Main Misses

- UNB was massively underrated pre-tournament. The model gave UNB 0.0% gold / 0.9% silver / 0.2% bronze before QF, then UNB reached the final.
- The QF forecast overtrusted Carleton against UNB. Projected Carleton 77-65; actual UNB 81-63.
- After QF, UNB was probably overcorrected. The updated medal sim made UNB the gold favorite at 43.5%, but Saskatchewan was still the better championship profile.
- Finals scoring was goofy. The semi-final model environment was low/controlled, but the medal games landed at 145 and 125 total points. The gold game especially did not behave like a normal elimination projection.
- Big spread cover spots need more respect. Saskatchewan and Calgary both created clearer medal-game separation than a neutral late-tournament model would suggest.

## Lessons Learned For Next Year

1. Watch games during the season before U SPORTS 8 Ultime.
   Box scores caught outcomes, but not enough player archetype detail: rim pressure, foul pressure, late-clock creators, defensive pressure tolerance, and who can actually travel into a national environment.

2. Add a finals/medal-game scoring adjustment.
   Finals are not just another neutral-court playoff game. Pace, foul strategy, pressure free throws, late-game extension, and rotation shortening can push totals into weird territory.

3. Separate "team quality" from "matchup shock".
   UNB's Katie Butts-type interior advantage broke the Carleton projection. The model needs a better high-impact player override, especially for foul-drawing frontcourt players.

4. Treat host and crowd effects as nonlinear.
   Laval beating TMU and staying medal-relevant was not just a small home bump. Host energy can create upset equity early, then still leave the team vulnerable against deeper opponents later.

5. Do not let one QF result oversteer the medal simulation.
   UNB deserved a big upgrade after QF, but not enough to pass Saskatchewan as the most likely champion without a stronger prior adjustment.

6. Build a "big spread cover" flag.
   When a superior team has a depth/athleticism edge and the opponent is emotionally or physically extended, the model should allow a wider late-tournament margin band.

## Next-Year Checklist

- Track 5-8 regular season games before nationals, prioritizing contenders and conference finalists.
- Create player-level notes for primary scorers, rim pressure, foul rate, rebounding, and guard pressure.
- Add a medal-game total boost or volatility band.
- Add a high-impact player override for elite usage/rebounding/foul-pressure profiles.
- Add a host-team split: early upset boost, later fatigue/depth penalty.
- Backtest final/bronze games separately from quarter-finals.
- Keep pre-tournament priors stronger after one-game shocks.

## Bottom Line

The model was useful on Saskatchewan, Calgary, Laval danger, and Saturday winners, but it was not seasoned enough. Next year, the edge comes from combining the numbers with actual game-watching before the 8 Ultime, then treating medal games as their own beast: goofy scores, wider spread-cover windows, and bigger player-specific swings.
