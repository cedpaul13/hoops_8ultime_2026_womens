from predictor import Final8TemporalPredictor
from config import CONFIG

def run_backtest():
    predictor = Final8TemporalPredictor()
    
    # Base de données historique 
    teams_hist = {
        "Sask_25": {"name": "Saskatchewan", "seed": 1, "ppg": 81.2, "pa": 53.0, "recent_ppg": 84.0, "recent_pa": 54.0, "sos_adj": 2.6, "coach_factor": 1.0},
        "UBC_25": {"name": "UBC", "seed": 4, "ppg": 72.0, "pa": 59.0, "recent_ppg": 68.0, "recent_pa": 62.0, "sos_adj": 2.1, "coach_factor": 0.60},
        
        "Carleton_24": {"name": "Carleton", "seed": 1, "ppg": 70.5, "pa": 54.0, "recent_ppg": 72.0, "recent_pa": 52.0, "sos_adj": 2.2, "coach_factor": 0.95},
        "Queens_24": {"name": "Queen's", "seed": 3, "ppg": 73.0, "pa": 58.0, "recent_ppg": 54.0, "recent_pa": 59.0, "sos_adj": 1.8, "coach_factor": 0.80},
        
        "Sask_24": {"name": "Saskatchewan", "seed": 2, "ppg": 84.5, "pa": 55.0, "recent_ppg": 82.0, "recent_pa": 56.0, "sos_adj": 2.5, "coach_factor": 1.0},
        "Laval_24": {"name": "Laval", "seed": 4, "ppg": 70.1, "pa": 52.0, "recent_ppg": 66.0, "recent_pa": 51.0, "sos_adj": 1.0, "coach_factor": 0.85},
        
        "TMU_22": {"name": "TMU", "seed": 1, "ppg": 79.0, "pa": 54.0, "recent_ppg": 78.0, "recent_pa": 55.0, "sos_adj": 2.4, "coach_factor": 0.90},
        "Winnipeg_22": {"name": "Winnipeg", "seed": 2, "ppg": 72.0, "pa": 58.5, "recent_ppg": 71.0, "recent_pa": 60.0, "sos_adj": 2.2, "coach_factor": 0.75},
        
        "Laval_19": {"name": "Laval", "seed": 1, "ppg": 72.0, "pa": 54.0, "recent_ppg": 73.0, "recent_pa": 53.0, "sos_adj": 1.1, "coach_factor": 0.90},
        "Ottawa_19": {"name": "Ottawa", "seed": 2, "ppg": 74.5, "pa": 58.0, "recent_ppg": 70.0, "recent_pa": 60.0, "sos_adj": 2.1, "coach_factor": 0.80},
        
        "Alberta_24_Cons": {"name": "Alberta", "seed": 5, "ppg": 74.0, "pa": 61.0, "recent_ppg": 75.0, "recent_pa": 62.0, "sos_adj": 2.2, "coach_factor": 0.80},
        "SMU_25_Cons": {"name": "Saint Mary's", "seed": 7, "ppg": 68.0, "pa": 56.0, "recent_ppg": 65.0, "recent_pa": 58.0, "sos_adj": 1.5, "coach_factor": 0.75}
    }

    tests = [
        {"a": "Sask_25", "b": "UBC_25", "real": (85, 63), "stage": "championship", "label": "Semi 2025: Sask vs UBC"},
        {"a": "Carleton_24", "b": "Queens_24", "real": (74, 40), "stage": "championship", "label": "Semi 2024: Carleton vs Queen's"},
        {"a": "Sask_24", "b": "Laval_24", "real": (64, 57), "stage": "championship", "label": "Semi 2024: Sask vs Laval"},
        {"a": "TMU_22", "b": "Winnipeg_22", "real": (70, 48), "stage": "championship", "label": "Semi 2022: TMU vs Winnipeg"},
        {"a": "Laval_19", "b": "Ottawa_19", "real": (73, 62), "stage": "championship", "label": "Semi 2019: Laval vs Ottawa"},
        {"a": "Alberta_24_Cons", "b": "Queens_24", "real": (71, 65), "stage": "consolation", "label": "Consol 2024: Alberta vs Queen's"},
        {"a": "Sask_25", "b": "SMU_25_Cons", "real": (75, 58), "stage": "consolation", "label": "Consol 2025: Sask vs SMU"}
    ]

    print("="*65 + "\nBACKTEST : SEMIS & CONSOLATIONS (2019-2025)\n" + "="*65)
    
    total_error = 0
    for t in tests:
        t1, t2 = teams_hist[t['a']], teams_hist[t['b']]
        res = predictor.predict(t1, t2, ctx={'stage': t['stage'], 'has_rest': (t['stage'] == 'championship')})
        
        p_a, p_b = res['score_a'], res['score_b']
        
        # BRIS D'ÉGALITÉ ANALYTIQUE : Si l'écart est < 1 pt, on applique le Coach Factor
        if abs(p_a - p_b) < 1.0:
            if t1['coach_factor'] > t2['coach_factor']: p_a += 1.0
            else: p_b += 1.0

        p_a_r, p_b_r = int(round(p_a)), int(round(p_b))
        r_a, r_b = t['real']
        err = abs(p_a_r - r_a) + abs(p_b_r - r_b)
        total_error += err
        print(f"{t['label']} ({t['stage']}):\n  Réel: {r_a}-{r_b} | Proj: {p_a_r}-{p_b_r} | Erreur: {err} pts\n")

    print(f"Marge d'erreur moyenne (Globale): {round(total_error / len(tests), 2)} points\n" + "="*65)

if __name__ == "__main__":
    run_backtest()