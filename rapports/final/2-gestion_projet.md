# Gestion de Projet et Planification

Pour assurer le bon déroulement du développement de **VerifAI** et respecter les échéances du plan de cours, une approche de gestion hybride a été adoptée. L'outil **GitHub Projects** a permis de maintenir un backlog détaillé (méthodologie Agile) tout en générant automatiquement un diagramme de Gantt pour la planification macroscopique.

## Backlog et Division du travail

Le projet a été découpé en tâches techniques précises. Chaque tâche du backlog a été assignée à un responsable clair, garantissant une division équitable du travail. 

Le tableau de bord a utilisé un système d'étiquettes (`Labels`) pour catégoriser les pôles d'expertise :

- **Développement Backend & Architecture (`backend`, `archi`, `dev`) :** Géré principalement par Mattéo GOUHIER (mise en place de l'API FastAPI, codage du prototype MVP).
- **Interface & Expérience Utilisateur (`frontend`, `design`) :** Assuré par Paul MATHÉ (intégration de l'interface graphique) et Justin BOSSARD (création des maquettes).
- **Gestion & Recherche (`gestion`, `recherche`) :** Suivi administratif et bibliographique piloté collectivement pour assurer la conformité avec les jalons.
- **Données & Intelligence Artificielle (`data`, `IA`, `science`) :** Phase de sélection des datasets, mise en place de l'architecture RAG et intégration des modèles pilotée par l'ensemble de l'équipe.

En fin de projet, l'ensemble des tickets a été clôturé et le code source a été fusionné sur la branche principale du dépôt.

## Diagramme de Gantt et Calendrier de réalisation

La vue chronologique a permis de visualiser les dépendances et de paralléliser les efforts. Le calendrier s'est structuré autour de quatre grandes phases :

**Phase 1 : Idéation et État de l'art (20 Jan. au 27 Jan.) - *[Terminé]***
- Création de l'identité de la startup (Nom et Logo VerifAI).
- Recherche bibliographique.
- Choix de la stack technique (Python, PyTorch, Vite).

**Phase 2 : Prototypage et Maquettage (27 Jan. au 24 Fév.) - *[Terminé]***
- **27 Jan - 03 Fév :** Création des maquettes conceptuelles de l'interface.
- **03 Fév - 24 Fév :** Développement en parallèle du Frontend (interface graphique) et du Backend (mise en place de l'API de base et création des routes de test).
- **Mi-Février :** Connexion Front-Back et validation du Prototype Minimum Viable (MVP).

**Phase 3 : Intelligence Artificielle (24 Fév. au 31 Mars) - *[Terminé]***
- Pivot technologique vers l'architecture hybride RAG (abandon du fine-tuning).
- Déploiement de la base de données vectorielle (ChromaDB) et des scripts de collecte automatisée (flux RSS Le Monde et France 24).
- Intégration du modèle Llama 3 pour la génération d'explications et de justifications.
- Élaboration de la stratégie marketing et de l'analyse persona.

**Phase 4 : Tests et Rendu Final (31 Mars au 28 Avril) - *[Terminé]***
- Évaluation des performances du modèle (précision, analyse de la confiance, identification des biais).
- Tests de facilité d'utilisation de la plateforme et évaluation du positionnement concurrentiel.
- Clôture du backlog GitHub, préparation de la soutenance et rédaction du rapport final.

![Diagramme de Gantt](gantt.png){width=100%}
