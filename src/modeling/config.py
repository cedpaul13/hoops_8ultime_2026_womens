CONFIG = {
    # --- Pondération Temporelle (K-Last Games) ---
    "K_LAST_WEIGHT": 0.75,       # Poids des 5 derniers matchs (Playoffs/QF)
    "SEASON_WEIGHT": 0.25,       # Poids de la moyenne saisonnière
    
    # --- Facteurs de Terrain et Pression ---
    "HCA_DEFENSIVE_LOCK": 6.5,   # Verrou défensif de Laval au PEPS
    "SOS_IMPACT": 4.8,           
    "PAINT_STRENGTH": 0.35,      
    "PRESSURE_WEIGHT": 7.0,      # Impact de la nervosité (TMU/UBC)
    
    # --- Situatif & Bracket ---
    "B2B_PENALTY": -4.0,         # Vendredi (Consolation)
    "REST_RECOVERY": 2.5,        # Samedi (Demies)
    "REDEEM_BOOST": 3.5,         # Rachat favoris (TMU/Carleton)
    "SEED_BIAS": 0.5,            # Pour BracketSimulator
    "ITERATIONS": 10000
}