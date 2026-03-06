import math
from config import CONFIG

class Final8TemporalPredictor:
    def __init__(self):
        self.hca_base = CONFIG["HCA_BOOST"]
        self.qf_friction = CONFIG["QF_FRICTION"]
        self.sos_weight = CONFIG["SOS_WEIGHT"]

    def predict(self, team_a, team_b, ctx=None):
        # 1. Base Power
        pwr_a = (team_a['ppg'] * self.qf_friction) + (team_a.get('sos_adj', 1.0) * self.sos_weight)
        pwr_b = (team_b['ppg'] * self.qf_friction) + (team_b.get('sos_adj', 1.0) * self.sos_weight)

        # 2. Lockdown Défensif (Multiplicateur)
        supp_a = (team_b.get('pa', 63) / 63) * (1 + (team_a.get('dna_factor', 0.5) * 0.12))
        supp_b = (team_a.get('pa', 63) / 63) * (1 + (team_b.get('dna_factor', 0.5) * 0.12))

        # 3. Calcul
        res_a = pwr_a * supp_a
        res_b = pwr_b * supp_b

        # 4. Spécifique Laval
        if team_a['name'] == "Laval":
            res_a += self.hca_base + 3.0 
            res_a -= (team_a.get('pressure_index', 0.5) * 6.0)

        sigma = 8.5 - (team_a.get('coach_factor', 0.7) * 3.0)
        return {"score_a": res_a, "score_b": res_b, "sigma_a": sigma, "sigma_b": sigma}