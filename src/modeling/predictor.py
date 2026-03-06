import math
from config import CONFIG

class Final8TemporalPredictor:
    def predict(self, team_a, team_b, ctx=None):
        stage = ctx.get('stage', 'championship') if ctx else 'championship'
        has_rest = ctx.get('has_rest', True) if ctx else True

        # 1. Calcul des statistiques hybrides (tendances récentes de 5 matchs + saison)
        def get_hybrid(team):
            h_ppg = (team['ppg'] * CONFIG["SEASON_WEIGHT"]) + (team['recent_ppg'] * CONFIG["K_LAST_WEIGHT"])
            h_pa = (team['pa'] * CONFIG["SEASON_WEIGHT"]) + (team['recent_pa'] * CONFIG["K_LAST_WEIGHT"])
            return h_ppg, h_pa

        ppg_a, pa_a = get_hybrid(team_a)
        ppg_b, pa_b = get_hybrid(team_b)

        # 2. Power Rating (SOS Impact)
        off_a = ppg_a + ((team_a['sos_adj'] - 1.8) * CONFIG["SOS_IMPACT"])
        off_b = ppg_b + ((team_b['sos_adj'] - 1.8) * CONFIG["SOS_IMPACT"])
        def_a = pa_a - ((team_a['sos_adj'] - 1.8) * CONFIG["SOS_IMPACT"])
        def_b = pa_b - ((team_b['sos_adj'] - 1.8) * CONFIG["SOS_IMPACT"])

        # 3. Projection et friction (Laval HCA)
        res_a = (off_a + def_b) / 2.0
        res_b = (off_b + def_a) / 2.0

        if team_a['name'] == "Laval": 
            res_b -= CONFIG["HCA_DEFENSIVE_LOCK"]
            res_a = max(res_a, 56.5)

        # 4. Ajustements QF
        if team_a['name'] == "UNB": res_a += 4.5
        if team_b['name'] == "Calgary": res_a -= 2.5

        # 5. Pression et repos
        res_a -= team_a.get('pressure_index', 0.5) * CONFIG["PRESSURE_WEIGHT"]
        res_b -= team_b.get('pressure_index', 0.5) * CONFIG["PRESSURE_WEIGHT"]

        adj = CONFIG["REST_RECOVERY"] if has_rest else CONFIG["B2B_PENALTY"]
        res_a, res_b = res_a + adj, res_b + adj
        if not has_rest and team_a['seed'] <= 2: res_a += CONFIG["REDEEM_BOOST"]
        if not has_rest and team_b['seed'] <= 2: res_b += CONFIG["REDEEM_BOOST"]

        return {"score_a": res_a, "score_b": res_b, "sigma_a": 6.5, "sigma_b": 6.5}