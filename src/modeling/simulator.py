import numpy as np
import math
from predictor import Final8TemporalPredictor
from config import CONFIG

class Final8Simulator:
    def __init__(self):
        self.predictor = Final8TemporalPredictor()
        self.teams = {
            "Saskatchewan": {"name": "Saskatchewan", "seed": 5, "ppg": 82.7, "pa": 52.5, "sos_adj": 2.6, "dna_factor": 0.98, "coach_factor": 1.0, "pressure_index": 0.5},
            "UNB": {"name": "UNB", "seed": 2, "ppg": 78.5, "pa": 76.1, "sos_adj": 1.2, "dna_factor": 0.65, "coach_factor": 0.65, "pressure_index": 0.6},
            "Laval": {"name": "Laval", "seed": 8, "ppg": 71.1, "pa": 51.4, "sos_adj": 1.0, "dna_factor": 0.88, "coach_factor": 0.85, "pressure_index": 0.9},
            "TMU": {"name": "TMU", "seed": 1, "ppg": 76.1, "pa": 55.8, "sos_adj": 2.2, "dna_factor": 0.85, "coach_factor": 0.90, "pressure_index": 0.8},
            "Calgary": {"name": "Calgary", "seed": 3, "ppg": 71.9, "pa": 55.7, "sos_adj": 2.4, "dna_factor": 0.82, "coach_factor": 0.85, "pressure_index": 0.6},
            "UBC": {"name": "UBC", "seed": 4, "ppg": 70.0, "pa": 55.3, "sos_adj": 2.1, "dna_factor": 0.80, "coach_factor": 0.60, "pressure_index": 0.5},
            "Carleton": {"name": "Carleton", "seed": 7, "ppg": 65.0, "pa": 57.1, "sos_adj": 1.9, "dna_factor": 0.95, "coach_factor": 0.95, "pressure_index": 0.7},
            "McGill": {"name": "McGill", "seed": 6, "ppg": 61.1, "pa": 56.1, "sos_adj": 0.8, "dna_factor": 0.78, "coach_factor": 0.55, "pressure_index": 0.4}
        }
        self.iterations = CONFIG["ITERATIONS"]

    def simulate_match(self, t1_n, t2_n, iterations=None):
        if iterations is None:
            iterations = self.iterations
        t1, t2 = self.teams[t1_n], self.teams[t2_n]
        proj = self.predictor.predict(t1, t2)
        t1_wins = 0
        scores_a, scores_b = [], []
        
        for _ in range(iterations):
            s1 = np.random.normal(proj['score_a'], proj['sigma_a'])
            s2 = np.random.normal(proj['score_b'], proj['sigma_b'])
            if int(round(s1)) == int(round(s2)):
                s1 += 0.5 if t1['coach_factor'] > t2['coach_factor'] else -0.5
            if s1 > s2: t1_wins += 1
            scores_a.append(s1); scores_b.append(s2)
        
        prob = t1_wins / iterations
        avg_a, avg_b = np.mean(scores_a), np.mean(scores_b)
        
        def get_ml(p):
            if p >= 0.999: return -10000
            if p <= 0.001: return 10000
            return int(-100 * (p/(1-p))) if p > 0.5 else int(100 * ((1-p)/p))

        return {
            "avg_a": avg_a, "avg_b": avg_b,
            "prob_a": round(prob * 100, 2), "prob_b": round((1-prob) * 100, 2),
            "ml_a": get_ml(prob), "ml_b": get_ml(1-prob),
            # Logique d'arrondi à 0.5 pour le spread et le total
            "spread": round(abs(avg_a - avg_b) * 2) / 2,
            "total": round((avg_a + avg_b) * 2) / 2
        }

    def run_dashboard(self):
        matches = [("12h30", "UNB", "Carleton"), ("14h30", "Calgary", "McGill"), 
                   ("18h00", "Saskatchewan", "UBC"), ("20h00", "TMU", "Laval")]
        
        print("="*65)
        print("--- DASHBOARD ANALYTIQUE : QUARTS DE FINALE (OFFICIEL) ---")
        print("="*65)
        
        for time, t1_n, t2_n in matches:
            res = self.simulate_match(t1_n, t2_n)
            t1, t2 = self.teams[t1_n], self.teams[t2_n]
            
            print(f"-----------------------------------------------------------------")
            print(f"HEURE DU MATCH : {time}")
            print(f"  PROJ SCORE : {t1_n} ({t1['seed']}) {int(round(res['avg_a']))} - {int(round(res['avg_b']))} {t2_n} ({t2['seed']})")
            print(f"  ---------------------------------------------------------")
            print(f"  WIN PROB: {t1_n} {res['prob_a']:.2f}% | {t2_n} {res['prob_b']:.2f}%")
            print(f"  ML:       {t1_n} ({res['ml_a']:+d}) | {t2_n} ({res['ml_b']:+d})")
            fav = t1_n if res['avg_a'] > res['avg_b'] else t2_n
            print(f"  SPREAD:       {fav} -{res['spread']:.1f}")
            print(f"  TOTAL (O/U):  {res['total']:.1f}")
        
        print("-----------------------------------------------------------------")
        print("="*65)

if __name__ == "__main__":
    sim = Final8Simulator()
    sim.run_dashboard()