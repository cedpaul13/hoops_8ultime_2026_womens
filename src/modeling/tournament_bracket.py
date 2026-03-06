import numpy as np
from tqdm import tqdm
from simulator import Final8Simulator
from config import CONFIG

class BracketSimulator:
    def __init__(self):
        self.sim = Final8Simulator()
        self.podiums = {name: {"Gold": 0, "Silver": 0, "Bronze": 0} for name in self.sim.teams.keys()}
        self.seed_bias_strength = CONFIG["SEED_BIAS"]
        self.n_iterations = CONFIG["ITERATIONS"]

    def play_bracket_match(self, t1_n, t2_n, stage='championship'):
        t1, t2 = self.sim.teams[t1_n], self.sim.teams[t2_n]
        proj = self.sim.predictor.predict(t1, t2, ctx={'stage': stage})
        
        # Biais de Seed (Prior)
        prior_a = (8 - t1['seed']) * self.seed_bias_strength
        prior_b = (8 - t2['seed']) * self.seed_bias_strength
        
        # CORRECTION : Utilisation du sigma stable (6.5) au lieu d'un % du score
        s1 = np.random.normal(proj['score_a'] + prior_a, proj['sigma_a'])
        s2 = np.random.normal(proj['score_b'] + prior_b, proj['sigma_b'])
        
        if int(round(s1)) == int(round(s2)):
            # Utilisation du coach_factor pour briser l'égalité
            s1 += 1.0 if t1.get('coach_factor', 0.5) > t2.get('coach_factor', 0.5) else -1.0
            
        return (t1_n, t2_n) if s1 > s2 else (t2_n, t1_n)

    def run_simulation(self):
        print(f"Simulation de {self.n_iterations} tournois (Monte Carlo - Phase Post-QF)")
        for _ in tqdm(range(self.n_iterations), desc="Progression"):
            # Bracket Post-QF
            w1, w2, w3, w4 = "UNB", "Calgary", "Saskatchewan", "Laval"
            w_s1, l_s1 = self.play_bracket_match(w1, w2, stage='championship')
            w_s2, l_s2 = self.play_bracket_match(w3, w4, stage='championship')
            gold, silver = self.play_bracket_match(w_s1, w_s2, stage='championship')
            bronze, _ = self.play_bracket_match(l_s1, l_s2, stage='championship')
            self.podiums[gold]["Gold"] += 1; self.podiums[silver]["Silver"] += 1; self.podiums[bronze]["Bronze"] += 1

    def show_results(self):
        print("\n" + "="*65 + f"\nRAPPORT ANALYTIQUE : PROBABILITÉS DE MÉDAILLES (N={self.n_iterations})\n" + "="*65)
        print(f"{'Équipe (Seed)':<22} | {'Or':>8} | {'Argent':>8} | {'Bronze':>8}\n" + "-" * 65)
        sorted_teams = sorted(self.podiums.items(), key=lambda x: (x[1]['Gold'], x[1]['Silver']), reverse=True)
        for name, stats in sorted_teams:
            if stats['Gold'] + stats['Silver'] + stats['Bronze'] > 0:
                print(f"{name + ' (' + str(self.sim.teams[name]['seed']) + ')':<22} | {(stats['Gold']/self.n_iterations)*100:>7.1f}% | {(stats['Silver']/self.n_iterations)*100:>7.1f}% | {(stats['Bronze']/self.n_iterations)*100:>7.1f}%")
        print("="*65 + "\n")
        
if __name__ == "__main__":
    bracket = BracketSimulator(); bracket.run_simulation(); bracket.show_results()