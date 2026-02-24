---
title: |
  ![](/data/logo-uqac.pdf){height=1in}

  Jalon 2
---

# Introduction

Ce rapport s'articule autour de trois axes principaux :

1. La planification et la gestion de projet, détaillant le backlog et le calendrier de réalisation.
2. La conception frontend, exposant les maquettes conceptuelles et les choix technologiques pour l'interface utilisateur.
3. L'architecture backend, décrivant la mise en place de l'API, le flux de traitement des données et l'intégration initiale du modèle d'intelligence artificielle.

L'objectif de cette étape est de démontrer la mise en place d'un prototype fonctionnel (MVP) capable d'effectuer une vérification de base.

***

Pour rappel, notre projet est hébergé publiquement sur GitHub : <https://github.com/realnitsuj/fake-news-detection>.

Pour tester, il suffit de cloner le répertoire, puis :

- Pour le frontend, aller dans le dossier `frontend/`, et exécuter :

    ```sh
    npm install && npm run dev
    ```

    Le frontend sera disponible sur <http://localhost:5173>.

- Pour le backend, aller dans `backend/`, et exécuter :

    ```sh
    uv python install 3.12 && uv run fastapi dev
    ```

    Le backend sera disponible sur <http://127.0.0.1:8000>.
