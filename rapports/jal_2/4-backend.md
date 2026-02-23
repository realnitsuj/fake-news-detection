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

# Architecture Backend : Le Moteur d'Analyse

Le backend de cette application sert de **passerelle** entre les interfaces utilisateurs et les modèles de Deep Learning. Son rôle est de gérer la validation, la communication sécurisée et l'interprétation des données.

---

## Responsabilités du Module

Le backend remplit trois fonctions principales :

1. **Sécurisation des secrets** : Gestion du Token API via variables d'environnement (`.env`).
2. **Normalisation** : Transformation du texte brut en format compatible pour l'IA.
3. **Traduction des résultats** : Transformer le retour via l'API en texte compréhensible par l'utilisateur.

---

## Architecture Interne du Code

Le backend est segmenté en **deux composants** pour garantir la maintenabilité et éviter le code spaghetti.

### 1. Le Point d'Entrée — `main.py`

C'est lui qui contrôle l'application. Il reçoit les données entrantes, y applique les règles de validation (longueur minimale du texte), et construit la réponse finale suivant un schéma de réponse prédéfini.

### 2. Le Service de Communication IA — `ai_service.py`

Ce service est le point central de la connexion à l'IA :

- **Gestion des requêtes HTTP** : Utilisation de `requests` pour dialoguer avec le Cloud.
- **Routage Dynamique** : Connexion au Router Hugging Face pour optimiser la disponibilité.
- **Gestion de la résilience** : Paramétrage du `wait_for_model` pour éviter les plantages lors du chargement des modèles IA sur le serveur distant.

---

## Choix du Modèle

Nous avons choisi un modèle réputé basé sur l'architecture **RoBERTa**, enrichi sur des articles comportant ou non des fake news. Ce choix n'est pas définitif, mais permet d'avoir une vision claire du fonctionnement de notre code.

> **Modèle utilisé** : [`hamzab/roberta-fake-news-classification`](https://huggingface.co/hamzab/roberta-fake-news-classification)

---

##  Flux de Traitement des Données

Le backend transforme le texte brut en verdict compréhensible en **cinq étapes** :

```
Texte brut → Validation → Authentification → Analyse IA → Parsing → Post-traitement → JSON
```


1. Lecture du texte : Le système réceptionne le texte et valide son format (longueur minimale) pour filtrer les requêtes inutiles.
2. Authentification : Il injecte de manière sécurisée la clé API pour autoriser la communication avec les serveurs de Hugging Face.
3. Traitement par L’IA : Le texte est transmis au modèle RoBERTa, qui réalise une analyse sémantique profonde pour détecter les marqueurs de désinformation.
4. Parsing : Le backend simplifie la réponse de l'IA (listes imbriquées) pour n'en extraire que les valeurs essentielles : le label et le score.
5. Post-traitement : Il traduit ces statistiques en information humaine. Le score est converti en pourcentage et le label technique devient un verdict clair et lisible.
Ce flux garantit que l'interface finale reçoit une donnée **fiable, lisible et prête à être affichée**.

---

##  Format de Sortie

Le backend ne renvoie pas de texte brut, mais un **objet JSON standardisé**. Cette structure permet de connecter n'importe quel Frontend sans modifier le code serveur.

```json
{
  "is_fake": true,
  "confidence_score": 0.9997,
  "label_detected": "FAKE",
  "message": "Attention, ce contenu semble suspect.",
  "model_version": "hamzab/roberta-fake-news-classification"
}
```

---

##  Sécurité &  Performance

Pour garantir la sécurité on stock les informations importante dans des variables d’environnement (dans .env) pour empêcher la fuite des clés API sur les dépôts de code publics. Et pour permettre d’améliorer la performance, nous avons construit l’application afin de pouvoir facilement changer le modèle (ici une instance de Roberta), à la seule condition de changer le format que l’on récupère sans le JSON.

---

## Perspectives d'Évolution

Par la suite, nous pouvons penser changer le modèle pour prendre un modèle de type LLM, permettant de justifier le verdict. Cela permettrait d’afficher ces détails aux utilisateurs pour mieux comprendre les raisons derrière un résultat. On pourra le faire assez facilement, grâce à l’architecture expliqué au-dessus. 
