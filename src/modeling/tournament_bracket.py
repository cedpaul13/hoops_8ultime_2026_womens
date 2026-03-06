import numpy as np
from tqdm import tqdm
from simulator import Final8Simulator
from config import CONFIG

class BracketSimulator:
    def __init__(self):
        self.sim = Final8Simulator()
        self.podiums = {name: {"Gold": 0, "Silver": 0, "Bronze": 0} for name in self.sim.teams.keys()}
        # Utilisation de la config centralisée
        self.seed_bias_strength = CONFIG["SEED_BIAS"]
        self.n_iterations = CONFIG["ITERATIONS"]

    def play_bracket_match(self, t1_n, t2_n):
        t1, t2 = self.sim.teams[t1_n], self.sim.teams[t2_n]
        proj = self.sim.predictor.predict(t1, t2)
        
        # Application du Biais de Seed (Prior)
        prior_a = (8 - t1['seed']) * self.seed_bias_strength
        prior_b = (8 - t2['seed']) * self.seed_bias_strength
        
        s1 = np.random.normal(proj['score_a'] + prior_a, proj['sigma_a'])
        s2 = np.random.normal(proj['score_b'] + prior_b, proj['sigma_b'])
        
        if int(round(s1)) == int(round(s2)):
            s1 += 0.5 if t1['coach_factor'] > t2['coach_factor'] else -0.5
            
        winner = t1_n if s1 > s2 else t2_n
        loser = t2_n if winner == t1_n else t1_n
        
        diff = abs(s1 - s2)
        m_added = 22 if diff > 18 else (38 if diff < 6 else 32)
        
        return winner, loser, m_added

    def run_simulation(self, n=None):
        if n is None:
            n = self.n_iterations
            
        print(f"Simulation de {n} tournois (Monte Carlo - Config Validée)")
        for _ in tqdm(range(n), desc="Progression"):
            # QUARTS
            w1, l1, m1 = self.play_bracket_match("UNB", "Carleton")
            w2, l2, m2 = self.play_bracket_match("Calgary", "McGill")
            w3, l3, m3 = self.play_bracket_match("Saskatchewan", "UBC")
            w4, l4, m4 = self.play_bracket_match("TMU", "Laval")

            # DEMIS (Championnat)
            w_s1, l_s1, ms1 = self.play_bracket_match(w1, w2)
            w_s2, l_s2, ms2 = self.play_bracket_match(w3, w4)

            # FINALES
            gold, silver, _ = self.play_bracket_match(w_s1, w_s2)
            bronze, _, _ = self.play_bracket_match(l_s1, l_s2)

            self.podiums[gold]["Gold"] += 1
            self.podiums[silver]["Silver"] += 1
            self.podiums[bronze]["Bronze"] += 1

    def show_results(self, n=None):
        if n is None:
            n = self.n_iterations
        
        print("\n" + "="*65)
        print(f"RAPPORT ANALYTIQUE : PROBABILITÉS DE MÉDAILLES (N={n})")
        print("="*65)
        print(f"{'Équipe (Seed)':<22} | {'Or':>8} | {'Argent':>8} | {'Bronze':>8}")
        print("-" * 65)
        
        sorted_teams = sorted(self.podiums.items(), key=lambda x: x[1]['Gold'], reverse=True)
        for name, stats in sorted_teams:
            seed = self.sim.teams[name]['seed']
            label = f"{name} ({seed})"
            p_g, p_s, p_b = (stats['Gold']/n)*100, (stats['Silver']/n)*100, (stats['Bronze']/n)*100
            
            if p_g + p_s + p_b > 0.05:
                print(f"{label:<22} | {p_g:>7.1f}% | {p_s:>7.1f}% | {p_b:>7.1f}%")
        print("="*65 + "\n")

if __name__ == "__main__":
    bracket = BracketSimulator()
    bracket.run_simulation()
    bracket.show_results()