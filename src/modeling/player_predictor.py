import math
import pandas as pd

class PlayerGranularPredictor:
    def __init__(self):
        # Poids de l'avantage du terrain (PEPS) distribué par joueuse
        self.hca_player_boost = 0.5 
        # Multiplicateur de logit pour la régression
        self.logit_multiplier = 0.033 
        
    def calculate_adjusted_minutes(self, projected_mins: float, tz_penalty: int) -> float:
        """
        Réduit les minutes effectives d'une joueuse basée sur le voyagement.
        Une étoile qui joue 35 minutes à domicile n'en jouera que 31 ou 32 
        d'efficaces après 3 fuseaux horaires.
        """
        # On assume une perte de 5% d'endurance par fuseau horaire traversé vers l'Est
        if tz_penalty > 0:
            fatigue_drag = 1 - (tz_penalty * 0.05)
            return projected_mins * fatigue_drag
        return projected_mins

    def calculate_team_rating(self, players: list, team_ast_pct: float, tz_penalty: int, is_home: bool = False) -> float:
        """
        Agrège le Net Rating de l'équipe en fonction du BPM des joueuses, 
        ajusté pour la fatigue et la cohésion d'équipe.
        """
        team_total_rating = 0.0
        
        for player in players:
            # 1. Ajustement des minutes selon le décalage horaire
            adj_mins = self.calculate_adjusted_minutes(player['proj_mins'], tz_penalty)
            
            # 2. Contribution pondérée (BPM ajusté au prorata des minutes jouées sur 40)
            player_contribution = player['bpm'] * (adj_mins / 40.0)
            
            # 3. Avantage du terrain (seulement pour Laval)
            if is_home:
                player_contribution += (self.hca_player_boost * (adj_mins / 40.0))
                
            team_total_rating += player_contribution
            
        # 4. Multiplicateur de Cohésion (AST%)
        # Un AST% de 60% (0.60) donne un boost de 1.1x au rating de l'équipe
        cohesion_multiplier = 1 + ((team_ast_pct - 0.50) * 1.5) 
        
        return team_total_rating * cohesion_multiplier

    def predict_game(self, team_a_name: str, team_a_players: list, team_a_ast: float, team_a_tz: int,
                     team_b_name: str, team_b_players: list, team_b_ast: float, team_b_tz: int) -> dict:
        
        rating_a = self.calculate_team_rating(team_a_players, team_a_ast, team_a_tz, is_home=(team_a_name=="Rouge et Or"))
        rating_b = self.calculate_team_rating(team_b_players, team_b_ast, team_b_tz, is_home=(team_b_name=="Rouge et Or"))
        
        margin = (rating_a - rating_b) * self.logit_multiplier
        prob_a = 1 / (1 + math.exp(-margin))
        
        return {
            "Matchup": f"{team_a_name} vs {team_b_name}",
            f"{team_a_name} Rating": round(rating_a, 2),
            f"{team_b_name} Rating": round(rating_b, 2),
            f"{team_a_name}_Win_Prob": round(prob_a * 100, 1),
            f"{team_b_name}_Win_Prob": round((1 - prob_a) * 100, 1)
        }

# --- Execution Block avec les données compilées ---
if __name__ == "__main__":
    predictor = PlayerGranularPredictor()
    
    # Base de données compilée : Échantillon Laval vs TMU
    # BPM (Box Plus-Minus) : Impact net par 100 possessions.
    roster_laval = [
        {"name": "Sabrine Khelifi", "bpm": 8.5, "proj_mins": 32.0},
        {"name": "Léa-Sophie Verret", "bpm": 7.2, "proj_mins": 30.0},
        {"name": "Julia Denis", "bpm": 4.1, "proj_mins": 25.0},
        {"name": "Florence Fortin", "bpm": 3.8, "proj_mins": 20.0},
        {"name": "Banc consolidé", "bpm": 0.5, "proj_mins": 93.0} # Reste des 200 minutes
    ]
    
    roster_tmu = [
        {"name": "TMU Star 1", "bpm": 11.2, "proj_mins": 34.0},
        {"name": "TMU Star 2", "bpm": 9.5, "proj_mins": 32.0},
        {"name": "TMU Starter 3", "bpm": 5.0, "proj_mins": 28.0},
        {"name": "TMU Starter 4", "bpm": 4.5, "proj_mins": 26.0},
        {"name": "Banc consolidé", "bpm": 1.2, "proj_mins": 80.0}
    ]
    
    # Matchup Jeudi 20h00
    result = predictor.predict_game(
        team_a_name="Rouge et Or", 
        team_a_players=roster_laval, 
        team_a_ast=0.635, # 63.5% Cohésion
        team_a_tz=0,      # Aucun voyagement
        
        team_b_name="TMU", 
        team_b_players=roster_tmu, 
        team_b_ast=0.591, # 59.1% Cohésion
        team_b_tz=0       # Même fuseau horaire (EST)
    )
    
    print("--- PROJECTIONS GRANULAIRES (BASE: JOUEUSES & COHÉSION) ---")
    for key, value in result.items():
        print(f"{key}: {value}")