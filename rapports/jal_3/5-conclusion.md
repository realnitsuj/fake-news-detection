# Conclusion

Le Jalon 3 a confirmé la pertinence de l'architecture hybride (RAG & Llama 3) pour transformer VerifAI en un outil d'explication de la désinformation. Avec une précision globale de 72 % et un taux de détection des faits avérés de 95 %, les bases techniques et le positionnement marketing (B2C/B2B) sont désormais solidement établis.

Cependant, l’analyse de performance a révélé des zones de vulnérabilité, qui définissent nos objectifs pour le rendu final :

1. **Optimisation de la précision et robustesse sémantique :** L'objectif est d'atteindre une précision cible de 85 % en renforçant le modèle face aux théories du complot pseudo-scientifiques et aux absurdités formulées simplement, qui constituent actuellement nos principaux faux positifs.
1. **Implémentation du filtrage de fiabilité :** Intégrer un module de "vraisemblance de base" et un seuil de rejet automatique pour les scores de confiance inférieurs à 35 %. Cela permettra de substituer les erreurs par une réponse "Incertain", garantissant la fiabilité du verdict pour l'utilisateur.
1. **Standardisation et rigueur de classification :** Affiner la logique du label "PARTIEL" pour qu'il ne s'applique qu'aux contenus dont la véracité est réellement mixte, éliminant ainsi les incohérences de notation observées durant les tests.
1. **Évaluation comparative et finale :** Conformément aux exigences du cours, le rendu final inclura une comparaison rigoureuse de la performance de VerifAI par rapport aux solutions concurrentes, tout en finalisant une interface utilisateur fluide et un code source prêt pour un déploiement commercial.

Nous devrons également établir :

1. **Exploitation algorithmique des données temporelles :** Intégrer une véritable dimension temporelle dans le processus de détection (par exemple, analyser la chronologie de parution des articles ou l'évolution d'une rumeur dans le temps) pour dépasser la simple collecte quotidienne et améliorer concrètement les performances de classification.
1. **Définition du modèle d'affaires et de la tarification :** Conformément aux exigences du plan de cours, établir une stratégie de prix concurrentielle en analysant les coûts opérationnels et en choisissant un modèle de revenus (ex : freemium ou licence B2B) adapté aux besoins de nos personas.


En adressant ces points, VerifAI passera d'un prototype analytique performant à une solution mature, capable de s'imposer comme une solution courante contre la désinformation.


# Références {-}
