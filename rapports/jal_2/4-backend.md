# Backend

Le backend met en œuvre une **API personnalisée** permettant notamment au frontend d'effectuer des actions telles que la vérification de texte ou le téléversement de fichiers.

## Structure

L’image suivante présente l’architecture actuelle de notre solution. Elle montre comment s’articule le rôle de notre serveur au sein du système, ainsi que la manière dont s’organisent les interactions entre l’IA et l’utilisateur à travers celui-ci.

![Schema Technique du Projet](schema-backend.png){height=290px}

## API

L’API est développée avec **FastAPI**, choisi pour :

- Son moteur asynchrone, idéal pour l’intégration d’IA et l’inférence.
- Sa compatibilité native avec **Pydantic**, qui facilite le typage des données.

Elle se structure autour de **deux catégories d’endpoints** :

- **`/ai`** : pour les prédictions et traitements liés à l’IA sur les données utilisateur.
- **`/files`** : pour la gestion de fichiers (images, PDF, etc.), notamment dans le cadre de la vérification de données provenant de sources variées.

## Prédiction

Parmi les tâches assurées par le serveur figure l’inférence du modèle d’IA sur les données utilisateur. Ce processus repose sur un script Python qui effectue une requête vers l’API de Hugging Face, analyse la réponse obtenue, puis transmet les résultats au serveur, lequel les renvoie finalement à l'utilisateur.
