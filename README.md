# VerifAI — Détection de désinformation assistée par IA

## Présentation

VerifAI est un outil de détection de désinformation développé dans le cadre du cours d'Atelier pratique en cybersécurité II (8INF970) à l'UQAC. L'application utilise une architecture hybride de Génération Augmentée par Récupération (RAG) pour analyser la fiabilité de contenus textuels, d'URLs ou de fichiers.

Le système compare les entrées utilisateurs avec une base de données factuelle alimentée par des flux RSS de sources reconnues (Le Monde, France 24). Un verdict est ensuite généré par le modèle Llama 3, accompagné d'un score de confiance et d'une justification explicable.

## Fonctionnalités

- **Analyse multi-sources** : Prise en charge de texte brut, de liens URL et de fichiers (PDF, TXT).
- **Architecture RAG** : Utilisation de ChromaDB et du modèle d'embedding `all-MiniLM-L6-v2` pour une recherche sémantique précise.
- **Intelligence Artificielle** : Traitement par Meta-Llama-3.1-8B-Instruct via l'API Hugging Face.
- **Interface intuitive** : Frontend moderne sous React pour une consultation rapide des résultats.

## Prérequis

- **Docker** et **Docker Compose** installés sur la machine.
- Un jeton d'accès **Hugging Face** (HF_TOKEN), en lecture.

## Configuration du Jeton Hugging Face

Pour utiliser le modèle de langage, une clé d'API est nécessaire. Un guide officiel est disponible : <https://huggingface.co/docs/hub/security-tokens>.

Sinon :

1. Créer un compte sur [Hugging Face](https://huggingface.co/).
2. Accéder aux paramètres du compte (**Settings**) puis à l'onglet **Access Tokens**.
3. Cliquer sur **New token**, nommer le jeton (ex: `VerifAI`) et sélectionner le rôle **Read**.
4. Copier le jeton généré (commençant par `hf_...`).

## Installation et Exécution

1. **Cloner le dépôt** :

   ```bash
   git clone <url-du-depot>
   cd fake-news-detection
   ```

2. **Configurer l'environnement** :

   Modifier `backend/.env` pour y ajouter le jeton Hugging Face :

   ```env
   HUGGINGFACE_TOKEN=hf_...
   ```

3. **Lancer le projet avec Docker** :

   À la racine du projet, exécuter la commande suivante :
   ```bash
   docker compose up --build
   ```

4. **Accéder à l'application** :

   - Interface utilisateur (Frontend) : [http://localhost:8080](http://localhost:8080)
   - API Documentation (Swagger) : [http://localhost:8000/docs](http://localhost:8000/docs)

## Architecture Technique

- **Backend** : FastAPI.
- **Frontend** : React avec Tailwind CSS.
- **Base vectorielle** : ChromaDB.
- **Modèles** : Sentence-Transformers & Llama 3.

## Auteurs

Projet réalisé par l'équipe VerifAI dans le cadre du module Cybersécurité II :

- Justin Bossard
- Mattéo Gouhier
- Paul Mathé
- Samuel Plet
- Léo Raclet
