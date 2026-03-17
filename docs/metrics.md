# Protocole d'expérimentation et métriques de succès

Ce document formalise la Task #5: définir comment évaluer objectivement la qualité, la robustesse et la performance de VerifAI.

## 1. Objectif

Valider que le prototype est:

- fiable sur la détection de fake news;
- suffisamment rapide pour un usage réel;
- stable sur l'API;
- acceptable en expérience utilisateur.

## 2. Périmètre évalué

- Backend: endpoints de santé et d'analyse.
- Frontend: parcours utilisateur saisie -> résultat.
- Modèle: qualité de classification.

## 3. Jeux de données

- Jeu principal: WELFake (ou ISOT si validé par l'équipe).
- Découpage recommandé: 70% entraînement, 15% validation, 15% test.
- Le jeu de test doit être gelé avant les mesures finales.

## 4. Métriques de succès

### 4.1 Qualité de classification

- F1 macro >= 0.85
- Recall classe FAKE >= 0.88
- Précision (precision) classe FAKE >= 0.85
- AUC >= 0.90

### 4.2 Performance API

- Latence p95 <= 3 secondes (hors cold start)
- Latence p99 <= 8 secondes
- Taux d'erreurs 5xx < 1%
- Disponibilité endpoint d'analyse >= 99%

### 4.3 Expérience utilisateur

- Taux de complétion d'analyse >= 95%
- Temps d'affichage du résultat <= 1 seconde après réponse API
- Taux d'échecs de validation côté saisie < 5%

## 5. Méthode d'exécution

- Campagne A: 200 requêtes de test texte.
- Campagne B: 50 requêtes URL.
- Campagne C: test de charge légère, 10 utilisateurs concurrents pendant 5 minutes.
- Rejouer chaque campagne 3 fois et conserver moyenne + écart-type.

## 6. Critères Go / No-Go

- Go: toutes les métriques critiques atteignent leur seuil.
- No-Go: au moins une métrique critique échoue.

Métriques critiques:

- Recall classe FAKE
- F1 macro
- Latence p95
- Taux d'erreurs 5xx

## 7. Livrables attendus pour clôturer la Task #5

- Ce document validé par l'équipe.
- Un tableau des résultats mesurés versus seuils.
- Une décision formelle Go ou No-Go.
- Une liste d'actions correctives priorisées si No-Go.

## 8. Tableau de résultats (à remplir)

| Métrique | Valeur mesurée | Seuil | Statut |
|---|---:|---:|---|
| F1 macro |  | >= 0.85 |  |
| Recall FAKE |  | >= 0.88 |  |
| Precision FAKE |  | >= 0.85 |  |
| AUC |  | >= 0.90 |  |
| Latence p95 (s) |  | <= 3 |  |
| Latence p99 (s) |  | <= 8 |  |
| Erreurs 5xx (%) |  | < 1 |  |
| Disponibilité (%) |  | >= 99 |  |
| Complétion analyse (%) |  | >= 95 |  |
| Affichage résultat (s) |  | <= 1 |  |
| Erreurs validation saisie (%) |  | < 5 |  |

## 9. Journal des validations

- Date:
- Participants:
- Version backend:
- Version frontend:
- Décision:
- Commentaires:
