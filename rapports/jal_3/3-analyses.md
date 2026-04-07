# Analyses des résultats et des performances
## 1. Contexte et objectifs

VerifAI a été soumis à cinq sessions de test consécutives sous forme de validation croisée, à partir d'un dataset de 50 articles. Chaque session présente un ensemble d'énoncés variés — faits vérifiables, désinformations grossières, théories du complot et affirmations ambiguës — auxquels le modèle répond par une classification (`VRAI`, `FAUX` ou `PARTIEL`) accompagnée d'un score de confiance.

Ce rapport évalue la performance globale du système, identifie ses forces et faiblesses, et propose des pistes d'amélioration ciblées.

---

## 2. Métriques globales

| Indicateur | Valeur |
|---|---|
| Énoncés évalués (total) | 155 |
| Précision globale | **72 %** |
| Taux de vrais positifs (VRAI détecté correctement) | **95 %** |
| Taux de vrais négatifs (FAUX rejeté correctement) | **56 %** |
| Taux d'erreur global | **28 %** |
| Faux positifs (FAUX classé VRAI) | ~35 cas |
| Faux négatifs (VRAI classé PARTIEL ou FAUX) | ~9 cas |

La précision de 72 % constitue un point de départ solide. Le modèle excelle à valider les faits vrais (95 % de détection), mais peine à rejeter les désinformations : seulement 56 % des énoncés faux sont correctement identifiés comme tels.

---

## 3. Performance par session

![Précision par session](chart1_precision_session.png)

| Session | Énoncés | Succès | Précision |
|---|---|---|---|
| Session 1 | 28 | 20 | 71 % |
| Session 2 | 30 | 18 | 60 % |
| Session 3 | 29 | 20 | 69 % |
| Session 4 | 30 | 22 | 73 % |
| Session 5 | 29 | 21 | 72 % |

La session 2 constitue le creux de performance (60 %), notamment due à une forte proportion de prédictions `PARTIEL` appliquées à des énoncés clairement `FAUX`. Les sessions 4 et 5 montrent une amélioration notable, suggérant une certaine robustesse du modèle sur des ensembles diversifiés.

---

## 4. Répartition des résultats

![Répartition des résultats — toutes sessions](chart2_repartition.png)

La matrice de confusion révèle un déséquilibre clair : les vrais positifs (67) dominent largement, tandis que les faux positifs (35) constituent la principale source d'erreur. Les faux négatifs (9) restent rares mais préoccupants en raison de leur niveau de confiance élevé.

---

## 5. Analyse de la confiance

![Confiance moyenne par type de résultat](chart3_confiance.png)

Le comportement du score de confiance révèle un patron cohérent :

- **Vrais positifs** : confiance moyenne de **86 %** — le modèle est bien calibré sur les faits vérifiables.
- **Vrais négatifs** : confiance moyenne de **23 %** — la faible confiance sert efficacement d'indicateur de rejet pour les désinformations bien reconnues.
- **Faux positifs** : confiance moyenne de **33 %** — les erreurs sur les fausses informations se produisent surtout à faible confiance, ce qui laisse ouverte une stratégie de seuillage.
- **Faux négatifs** : confiance moyenne de **71 %** — problème plus sérieux : le modèle se trompe avec une haute confiance sur certains faits vrais.

![Distribution de la confiance](chart4_distribution.png)

> **Interprétation clé :** la confiance n'est pas encore un indicateur fiable d'exactitude pour les énoncés faux. Un score de 20 % peut correspondre à une bonne détection *ou* à un rejet injustifié d'une information vraie. En revanche, les énoncés vrais sont quasi systématiquement associés à une confiance ≥ 80 %.

---

## 6. Énoncés problématiques récurrents

![Énoncés problématiques récurrents](chart5_problematiques.png)

Certains énoncés ont échoué dans plusieurs sessions, révélant des angles morts systématiques du modèle.

### 6.1 Théories du complot plausibles en surface

Ces énoncés combinent un vocabulaire scientifique ou officiel avec une conclusion fausse. Le modèle les classe incorrectement en `VRAI` dans 3 à 4 sessions sur 5 :

- *"Les cheveux et les ongles continuent de pousser après la mort"* — mythe médical courant, échoue dans 4 sessions.
- *"La technologie 5G est directement responsable de la mort d'oiseaux migrateurs"* — 3 sessions en erreur.
- *"L'homme n'a jamais marché sur la Lune"* — 3 sessions en erreur, avec une confiance élevée (70 %).

### 6.2 Absurdités à formulation naïve

Paradoxalement, certains énoncés manifestement faux mais formulés de façon fantaisiste échappent au modèle :

- *"Les requins sont des robots espions"* — classé `VRAI` dans 3 sessions.
- *"Les oiseaux sont des drones de surveillance"* — 3 sessions en erreur.

Ces cas suggèrent que le modèle s'appuie peu sur la vraisemblance de base et davantage sur des marqueurs linguistiques de surface.

### 6.3 Affirmations ambiguës mal gérées

L'usage de la prédiction `PARTIEL` est appliqué de façon incohérente, parfois sur des énoncés entièrement faux (*traînées d'avions*, *télécharger Internet sur USB*) et parfois sur des faits vrais (*cœur humain*). Cette catégorie nécessite une définition plus stricte.

---

## 7. Points forts du système

- **Faits scientifiques établis** : photosynthèse, gravité, ébullition de l'eau, HTTPS, ransomware — précision quasi parfaite, confiance bien calibrée (80–100 %).
- **Désinformations grossières** : pyramides extraterrestres, Terre plate, eau de Javel curative — rejetées systématiquement et correctement.
- **Domaine cybersécurité** : détection fiable et confiante sur tous les énoncés techniques testés.
- **Faits géographiques et institutionnels** : Paris, OMS, Japon, UQAC — aucune erreur observée.

---

## 8. Faiblesses identifiées

| Catégorie | Problème | Impact |
|---|---|---|
| Théories du complot à vernis scientifique | Taux de faux positifs élevé | Élevé |
| Prédictions `PARTIEL` inconsistantes | Manque de critères clairs | Moyen |
| Haute confiance sur faux négatifs | Erreurs difficiles à filtrer a posteriori | Élevé |
| Absurdités formulées simplement | Contournement du filtre sémantique | Moyen |

---

## 9. Recommandations

**R1 — Introduire un seuil de rejet basé sur la confiance**
Les faux positifs apparaissent majoritairement à confiance ≤ 30 %. Configurer le système pour retourner une réponse `INCERTAIN` lorsque la confiance est inférieure à 35 % réduirait les erreurs sans dégrader la précision sur les vrais positifs.

**R2 — Renforcer la base d'entraînement sur les théories du complot**
Augmenter les exemples d'énoncés à structure pseudo-scientifique étiquetés `FAUX`, en particulier ceux liés aux vaccins, aux technologies de communication (5G) et aux théories géopolitiques.

**R3 — Standardiser la catégorie `PARTIEL`**
Définir des critères formels d'utilisation : `PARTIEL` ne devrait s'appliquer qu'aux énoncés dont une partie est vérifiable et l'autre non, jamais à des énoncés entièrement faux ou entièrement vrais.

**R4 — Intégrer un module de vraisemblance de base**
Les énoncés absurdes (requins robots, oiseaux drones) devraient déclencher un signal de rejet préemptif fondé sur la cohérence ontologique, avant toute analyse sémantique fine.

**R5 — Tests adversariaux systématiques**
Constituer un jeu de données dédié aux énoncés « limite », reformulés pour maximiser la vraisemblance de surface tout en étant faux, et les intégrer à chaque cycle d'évaluation.

---

## 10. Conclusion

VerifAI démontre une performance solide sur les faits établis et les désinformations évidentes, avec une précision globale de 72 % sur 155 énoncés hétérogènes. La principale vulnérabilité réside dans la gestion des fausses informations formulées de manière crédible ou pseudo-scientifique. Les pistes d'amélioration identifiées — seuillage par confiance, enrichissement des données d'entraînement et standardisation du label `PARTIEL` — sont toutes implémentables à court terme et devraient permettre d'atteindre une précision cible de 85 % lors des prochains cycles de test.

---
