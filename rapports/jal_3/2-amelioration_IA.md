# Évolution vers une Architecture Hybride (RAG & LLM)

Pour dépasser les limites d'une simple classification "Vrai/Faux", l'architecture a évolué vers un système de **Génération Augmentée par Récupération (RAG)**. Cette approche permet non seulement de détecter la désinformation, mais aussi de fournir une justification sourcée en se basant sur des faits réels et actualisés.

## Changement de Paradigme : De RoBERTa à Mistral-7B

Initialement basé sur RoBERTa pour la classification, le système utilise désormais **Mistral-7B (v0.3)**. Ce changement est motivé par deux besoins critiques :

  - **Le Raisonnement** : Capacité à expliquer *pourquoi* une information est jugée suspecte.
  - **Le Contextualisme** : Capacité à intégrer des documents externes (faits réels) dans sa réflexion avant de rendre un verdict.


## Fine Tunning
TA PARTIE JUSTIN (pas Paul)


## Le Système de Mémoire : Architecture RAG

L'innovation majeure réside dans l'ajout d'une "mémoire factuelle" qui permet à l'IA de consulter des sources de confiance avant de répondre.

### 1\. Acquisition de la "Vérité" (Scraping RSS)

Le système n'est plus statique. Un module de collecte automatisé (`scripts/fetch_news.py`) parcourt quotidiennement les flux **RSS** de sources de presse reconnues (Le Monde, France 24). Grâce aux bibliothèques **Feedparser** et **Newspaper3k**, le contenu textuel est extrait, nettoyé de ses balises HTML, et centralisé dans un dataset de référence.

### 2\. Vectorisation et Stockage (ChromaDB)

Pour que l'IA puisse "chercher" dans ces milliers d'articles, nous utilisons :

  - **Sentence-Transformers (`all-MiniLM-L6-v2`)** : Ce modèle transforme chaque article de presse en un vecteur mathématique de 384 dimensions représentant son sens sémantique.
  - **ChromaDB** : Une base de données vectorielle haute performance qui stocke ces vecteurs. Elle permet de trouver en quelques millisecondes les articles les plus proches sémantiquement de la requête de l'utilisateur.

## Flux de Traitement Optimisé

Le pipeline de traitement a été enrichi pour intégrer la vérification factuelle :

```
Saisie utilisateur → Vectorisation → Recherche ChromaDB (Top K) → Injection Contexte → Prompt Mistral → Parsing JSON
```

1.  **Recherche de Preuves** : Le texte soumis par l'utilisateur est converti en vecteur. Le système interroge **ChromaDB** pour extraire les articles de presse les plus pertinents par rapport au sujet.
2.  **Construction du Prompt** : Nous créons un "Prompt enrichi" qui contient : les consignes de l'expert, les preuves factuelles trouvées dans la base, et le texte à analyser.
3.  **Inférence Générative** : Mistral-7B analyse la cohérence entre le texte utilisateur et les preuves fournies.
4.  **Extraction Structurée** : Le backend utilise un moteur de parsing pour garantir que la réponse de l'IA est un objet JSON pur, prêt pour le frontend.

## Nouveau Format de Sortie (Standard JSON v2)

La réponse API est désormais beaucoup plus riche, offrant une transparence totale sur le verdict :

```json
{
  "verdict": "Slightly Misleading",
  "score": 0.85,
  "justification": "L'article affirme que X est arrivé, mais les rapports de l'AFP indiquent que l'événement a été reporté.",
  "sources": [
    {"title": "Report de l'événement X", "url": "https://lemonde.fr/..."}
  ],
  "is_fake": true
}
```

## Sécurité et Robustesse Technique

L'implémentation logicielle a été renforcée par l'ajout de nouvelles dépendances critiques :

  - **Pydantic (Schemas)** : Validation stricte des entrées/sorties via `TextSchema` et `FileSchema` pour éviter les injections de données malformées.
  - **Gestion des Timeouts** : Configuration de la résilience pour gérer les temps de réponse plus longs des LLM génératifs (utilisation de `wait_for_model: True`).
  - **Normalisation des Environnements** : Utilisation d'un fichier `requirements.txt` hybride combinant des versions figées par `uv` et des extensions flexibles pour le RAG, garantissant la portabilité du projet.

