# Hoops 8 Ultime 2026 - Women's Basketball Analytics

Projet de prédiction analytique pour le Championnat féminin U Sports 2026 au PEPS (Québec).

## Performance (Phase QF)
- **Modèle :** Temporal Predictor (Version 1.0)
- **Marge d'Erreur Moyenne (MAE) :** 9.0 points (Validé sur les quarts de finale 2019-2025).
- **Highlight :** Match TMU-Laval projeté à 60-59 (Réel : 54-57).

## Méthodologie
- **Simulation Monte Carlo :** N=10,000 itérations par match.
- **Friction Défensive :** Multiplicateur de suppression (0.83) pour les tournois nationaux.
- **Biais Bayésien :** Prior sur le seed officiel (Strength: 1.1) pour stabiliser les probabilités de médailles.

## Structure
- `src/modeling/` : Moteur de prédiction et simulateurs.
- `data/results/` : Résultats réels pour validation continue.
- `outputs/predictions/` : Archives des probabilités pré-tournoi.

## Glossaire des Variables (Acronymes)
- **PPG (Points Per Game)** : Moyenne de points marqués par match en saison régulière.
- **PA (Points Allowed)** : Moyenne de points encaissés par match (mesure l'efficacité défensive).
- **SOS (Strength of Schedule)** : Force du calendrier basée sur la difficulté des adversaires affrontés.
- **SOS_adj** : Ajustement du SOS normalisant les écarts entre les conférences (CW, OUA, RSEQ, AUS).
- **DNA Factor** : Coefficient de "pedigree" (0.0 à 1.0) basé sur l'historique de succès au tournoi national.
- **Coach Factor** : Indice d'expérience et de succès des entraîneurs en situation de haute pression.
- **Pressure Index** : Facteur de fatigue psychologique ou environnementale (ex: jouer à domicile).
