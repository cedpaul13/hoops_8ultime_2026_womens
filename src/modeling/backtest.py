from predictor import Final8TemporalPredictor
import math

def run_modern_backtest():
    predictor = Final8TemporalPredictor()
    
    # Échantillon validé : Ère Pace & Space (2019-2025)
    teams_hist = {
        # 2025
        "UNB_25": {"name": "UNB", "ppg": 76.5, "pa": 71.0, "sos_adj": 1.2, "dna_factor": 0.65, "coach_factor": 0.65},
        "Carleton_25": {"name": "Carleton", "ppg": 69.0, "pa": 56.0, "sos_adj": 1.9, "dna_factor": 0.95, "coach_factor": 0.95},
        "Sask_25": {"name": "Saskatchewan", "ppg": 81.2, "pa": 53.0, "sos_adj": 2.6, "dna_factor": 0.98, "coach_factor": 1.0},
        "UBC_25": {"name": "UBC", "ppg": 72.0, "pa": 59.0, "sos_adj": 2.1, "dna_factor": 0.80, "coach_factor": 0.60},
        # 2024
        "Laval_24": {"name": "Laval", "ppg": 70.1, "pa": 52.0, "sos_adj": 1.0, "dna_factor": 0.88, "coach_factor": 0.85, "pressure_index": 0.9},
        "Alberta_24": {"name": "Alberta", "ppg": 74.0, "pa": 61.0, "sos_adj": 2.2, "dna_factor": 0.75, "coach_factor": 0.80},
        "Sask_24": {"name": "Saskatchewan", "ppg": 84.5, "pa": 55.0, "sos_adj": 2.5, "dna_factor": 0.98, "coach_factor": 1.0},
        "Calgary_24": {"name": "Calgary", "ppg": 71.0, "pa": 58.0, "sos_adj": 2.2, "dna_factor": 0.82, "coach_factor": 0.85},
        # 2022
        "TMU_22": {"name": "TMU", "ppg": 79.0, "pa": 54.0, "sos_adj": 2.4, "dna_factor": 0.85, "coach_factor": 0.90},
        "UPEI_22": {"name": "UPEI", "ppg": 68.0, "pa": 62.0, "sos_adj": 0.9, "dna_factor": 0.50, "coach_factor": 0.65},
        # 2019 (Seuil de stabilité Pace & Space)
        "Ottawa_19": {"name": "Ottawa", "ppg": 74.5, "pa": 58.0, "sos_adj": 2.1, "dna_factor": 0.82, "coach_factor": 0.80},
        "Laval_19": {"name": "Laval", "ppg": 72.0, "pa": 54.0, "sos_adj": 1.1, "dna_factor": 0.92, "coach_factor": 0.90, "pressure_index": 0.8}
    }

    tests = [
        {"a": "UNB_25", "b": "Carleton_25", "real": (74, 71), "label": "QF 2025: UNB vs CAR"},
        {"a": "Sask_25", "b": "UBC_25", "real": (75, 55), "label": "QF 2025: SAS vs UBC"},
        {"a": "Sask_24", "b": "Calgary_24", "real": (85, 54), "label": "QF 2024: SAS vs CAL"},
        {"a": "Laval_24", "b": "Alberta_24", "real": (65, 57), "label": "QF 2024: LAV vs ALB"},
        {"a": "TMU_22", "b": "UPEI_22", "real": (80, 49), "label": "QF 2022: TMU vs UPEI"},
        {"a": "Laval_19", "b": "Ottawa_19", "real": (73, 62), "label": "QF 2019: LAV vs OTT"}
    ]

    print("="*65 + "\nBACKTEST : ÈRE MODERNE (2019-2025)\n" + "="*65)
    errors = []
    for t in tests:
        res = predictor.predict(teams_hist[t['a']], teams_hist[t['b']])
        p_a, p_b = int(round(res['score_a'])), int(round(res['score_b']))
        r_a, r_b = t['real']
        err = abs(p_a - r_a) + abs(p_b - r_b)
        errors.append(err)
        print(f"{t['label']}:\n  Réel: {r_a}-{r_b} | Proj: {p_a}-{p_b} | Erreur: {err} pts\n")

    print(f"Marge d'erreur moyenne (Ère Moderne): {round(sum(errors)/len(errors), 2)} points")

if __name__ == "__main__":
    run_modern_backtest()