import numpy as np
from predictor import Final8TemporalPredictor
from config import CONFIG

class Final8Simulator:
    def __init__(self):
        self.predictor = Final8TemporalPredictor()
        self.teams = {
            "UNB": {"name": "UNB", "seed": 2, "ppg": 78.5, "pa": 76.1, "recent_ppg": 82.5, "recent_pa": 61.0, "sos_adj": 2.0, "pressure_index": 0.3, "coach_factor": 0.75},
            "Calgary": {"name": "Calgary", "seed": 3, "ppg": 71.9, "pa": 55.7, "recent_ppg": 61.0, "recent_pa": 45.0, "sos_adj": 2.4, "pressure_index": 0.5, "coach_factor": 0.85},
            "Saskatchewan": {"name": "Saskatchewan", "seed": 5, "ppg": 82.7, "pa": 52.5, "recent_ppg": 64.5, "recent_pa": 58.0, "sos_adj": 2.6, "pressure_index": 0.4, "coach_factor": 1.0},
            "Laval": {"name": "Laval", "seed": 8, "ppg": 71.1, "pa": 51.4, "recent_ppg": 56.5, "recent_pa": 49.0, "sos_adj": 1.0, "pressure_index": 0.3, "coach_factor": 0.85},
            "TMU": {"name": "TMU", "seed": 1, "ppg": 76.1, "pa": 55.8, "recent_ppg": 64.0, "recent_pa": 60.0, "sos_adj": 2.2, "pressure_index": 0.95, "coach_factor": 0.90},
            "Carleton": {"name": "Carleton", "seed": 7, "ppg": 65.0, "pa": 57.1, "recent_ppg": 61.5, "recent_pa": 68.0, "sos_adj": 1.9, "pressure_index": 0.8, "coach_factor": 0.95},
            "McGill": {"name": "McGill", "seed": 6, "ppg": 61.1, "pa": 56.1, "recent_ppg": 48.0, "recent_pa": 51.5, "sos_adj": 0.8, "pressure_index": 0.6, "coach_factor": 0.55},
            "UBC": {"name": "UBC", "seed": 4, "ppg": 70.0, "pa": 55.3, "recent_ppg": 56.0, "recent_pa": 67.0, "sos_adj": 2.1, "pressure_index": 0.7, "coach_factor": 0.60}
        }

    def simulate_match(self, t1_n, t2_n, stage='championship'):
        has_rest = (stage == 'championship')
        proj = self.predictor.predict(self.teams[t1_n], self.teams[t2_n], ctx={'stage': stage, 'has_rest': has_rest})
        t1_wins, scores_a, scores_b = 0, [], []
        for _ in range(CONFIG["ITERATIONS"]):
            s1, s2 = np.random.normal(proj['score_a'], proj['sigma_a']), np.random.normal(proj['score_b'], proj['sigma_b'])
            if s1 > s2: t1_wins += 1
            scores_a.append(s1); scores_b.append(s2)
        
        prob = t1_wins / CONFIG["ITERATIONS"]
        avg_a, avg_b = np.mean(scores_a), np.mean(scores_b)
        def get_ml(p): return int(-100*(p/(1-p))) if p > 0.5 else int(100*((1-p)/p))

        return {
            "avg_a": avg_a, "avg_b": avg_b, "prob_a": prob*100, "prob_b": (1-prob)*100,
            "ml_a": get_ml(prob), "ml_b": get_ml(1-prob),
            "spread": round(abs(avg_a-avg_b)*2)/2, "total": round((avg_a+avg_b)*2)/2
        }

    def run_dashboard(self, matches, stage_label, stage_key):
        print("="*65 + f"\n--- DASHBOARD ANALYTIQUE : {stage_label} ---\n" + "="*65)
        for time, t1_n, t2_n in matches:
            res = self.simulate_match(t1_n, t2_n, stage=stage_key)
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
        print("="*65 + "\n")

if __name__ == "__main__":
    sim = Final8Simulator()
    # Vendredi - Consolation
    friday_matches = [("17h00", "Carleton", "McGill"), ("19h00", "UBC", "TMU")]
    sim.run_dashboard(friday_matches, "DEMI-FINALES DE CONSOLATION (VENDREDI)", "consolation")
    
    # Samedi - Demi-Finales de Championnat
    saturday_matches = [("15h00", "UNB", "Calgary"), ("18h00", "Saskatchewan", "Laval")]
    sim.run_dashboard(saturday_matches, "DEMI-FINALES DE CHAMPIONNAT (SAMEDI)", "championship")