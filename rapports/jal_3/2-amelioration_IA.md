# Évolution vers une Architecture Hybride (RAG & LLM)

Pour dépasser les limites d'une simple classification "Vrai/Faux", l'architecture a évolué vers un système de **Génération Augmentée par Récupération (RAG)**. Cette approche permet non seulement de détecter la désinformation, mais aussi de fournir une justification sourcée en se basant sur des faits réels et actualisés.

## Changement de Paradigme : De RoBERTa à Llamma 3

Initialement basé sur RoBERTa pour la classification, le système utilise désormais **Llama 3**. Ce changement est motivé par deux besoins :

  - **Le Raisonnement** : Capacité à expliquer *pourquoi* une information est jugée suspecte. RoBERTa ne donnait qu'une réponse Vrai/Faux, mais Llama, en tant que LLM, permet de justifier le choix.
  - **Le Contexte** : Capacité à comprendre le contexte global de l'article, et pas seulement une phrase isolée.


## Fine Tunning
TA PARTIE JUSTIN (pas Paul)


## Le Système de Mémoire : Architecture RAG

L'innovation majeure réside dans l'ajout d'une "mémoire factuelle" qui permet à l'IA de consulter des sources de confiance avant de répondre.

### 1\. Scraping RSS

Le système n'est plus statique. Un module de collecte automatisé (`scripts/fetch_news.py`) s'execute tout les jours pour parcourir les flux **RSS** de sources de presse reconnues (Le Monde et France 24). Grâce aux bibliothèques **Feedparser** et **Newspaper3k**, le contenu textuel est extrait, nettoyé de ses balises HTML, et centralisé dans un dataset de référence.

### 2\. Vectorisation et Stockage (ChromaDB)

Pour que l'IA puisse "chercher" dans ces milliers d'articles, nous utilisons :

  - **Sentence-Transformers (`all-MiniLM-L6-v2`)** : Ce modèle transforme chaque article de presse en un vecteur mathématique de 384 dimensions représentant son sens sémantique.
  - **ChromaDB** : Une base de données vectorielle haute performance qui stocke ces vecteurs. Elle permet de trouver rapidement les articles les plus proches sémantiquement de la requête de l'utilisateur.

### 3\. Prompt Enrichi 

Maintenant, avant chaque requête, on récupère l'article de notre base le plus proche sémentiquement du texte à analyser, ainsi qu'un score de similitude, qu'on envoie à notre LLM pour qu'il rende son verdict avec les informations actuelles.

## Nouveau Format de Sortie (Standard JSON v2)

La réponse API est désormais beaucoup plus riche, offrant une transparence totale sur le verdict :

```json
{
  "verdict": "Slightly Misleading",
  "confiance": 0.85,
  "catégorie": "Politique",
  "justification": "L'article affirme que X est arrivé, mais les rapports de l'AFP indiquent que l'événement a été reporté.",
  
}
```
## Flux final

### 1\. Entrée 
URL ou texte soumis par l'utilisateur.

### 2\. Récupération 
Le système extrat les preuves de la base de données factuelles (ChromaDB).

### 3\. Travail du LLM 
Llama 3 analyse le texte utilisateur au regard de l'article de notre base avec lequel il a été fournis.

### 4\. Sortie 
Production du JSON structuré.

## Sécurité et Robustesse Technique

L'implémentation logicielle a été renforcée par l'ajout de nouvelles dépendances critiques :

  - **Pydantic (Schemas)** : Validation stricte des entrées/sorties via `TextSchema` et `FileSchema` pour éviter les injections de données malformées.
  - **Gestion des Timeouts** : Configuration de la résilience pour gérer les temps de réponse plus longs des LLM génératifs (utilisation de `wait_for_model: True`).
  - **Normalisation des Environnements** : Utilisation d'un fichier `requirements.txt` hybride combinant des versions figées par `uv` et des extensions flexibles pour le RAG, garantissant la portabilité du projet.

