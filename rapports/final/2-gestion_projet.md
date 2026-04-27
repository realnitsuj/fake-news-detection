# Gestion de Projet et Planification

Pour assurer le bon déroulement du développement de **VerifAI** et respecter les échéances du plan de cours, nous avons opté pour une approche de gestion hybride. Nous utilisons l'outil **GitHub Projects**, qui nous permet de maintenir un backlog détaillé (méthodologie Agile) tout en générant automatiquement un diagramme de Gantt pour la planification macroscopique.

## Backlog et Division du travail

Le projet a été découpé en tâches techniques précises. Pour répondre aux exigences de réalisation en équipe, chaque tâche de notre backlog est assignée à un responsable clair, garantissant une division équitable du travail. 

Le tableau de bord utilise un système d'étiquettes (`Labels`) pour catégoriser les pôles d'expertise :

- **Développement Backend & Architecture (`backend`, `archi`, `dev`) :** Géré principalement par Mattéo GOUHIER (ex: mise en place de l'API FastAPI, codage du prototype MVP).
- **Interface & Expérience Utilisateur (`frontend`, `design`) :** Assuré par Paul MATHÉ (intégration de l'interface graphique) et Justin BOSSARD (création des maquettes).
- **Gestion & Recherche (`gestion`, `recherche`) :** Suivi administratif et bibliographique piloté par le reste de l'équipe pour assurer la conformité avec les jalons.
- **Données & Intelligence Artificielle (`data`, `IA`, `science`) :** Phase de sélection des datasets et protocoles préparatoires pour le modèle de détection.


Chaque tâche est associée à un Jalon cible (`Milestone`) et possède un statut de progression (*Todo*, *In Progress*, *Done*).


## Diagramme de Gantt et Calendrier de réalisation

La vue chronologique de GitHub Projects nous permet de visualiser les dépendances et de paralléliser nos efforts. Le calendrier est structuré autour des quatre grandes phases du projet :

**Phase 1 : Idéation et État de l'art (Jalon 1 - 20 Jan. au 27 Jan.) - *[Terminé]***

- Création de l'identité de la startup (Nom et Logo VerifAI).
- Recherche bibliographique et sélection du dataset (WELFake).
- Choix de la stack technique (Python, PyTorch, Vite).

**Phase 2 : Prototypage et Maquettage (Jalon 2 - 27 Jan. au 24 Fév.) - *[Terminé]***
Cette phase concentre l'essentiel de nos efforts actuels de développement.

- **27 Jan - 03 Fév :** Création des maquettes conceptuelles de l'interface.
- **03 Fév - 24 Fév :** Développement en parallèle du Frontend (interface graphique) et du Backend (mise en place de l'API de base et création des routes de test).
- **Mi-Février :** Connexion Front-Back et validation du Prototype Minimum Viable (MVP).

**Phase 3 : Intelligence Artificielle (Jalon 3 - 24 Fév. au 31 Mars) - *[À venir]***
Une fois le prototype fonctionnel validé, l'effort basculera sur le moteur scientifique.

- Création de la base de données finalisée.
- Implémentation et entraînement du modèle de détection de Fake News.
- Intégration du LLM (Large Language Model) pour la génération automatique d'explications destinées aux utilisateurs.
- Rédaction de l'étude de marché marketing.

**Phase 4 : Tests et Rendu Final (31 Mars au 28 Avril) - *[]***

- Évaluation des performances du modèle face aux concurrents.
- Tests de facilité d'utilisation de la plateforme.
- Rédaction du rapport final complet et préparation de la soutenance.
