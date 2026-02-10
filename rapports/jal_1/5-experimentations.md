# Expérimentations possibles
Pour ce Jalon 2, nous avons défini un protocole expérimental visant à comparer différentes approches de détection et à valider la robustesse de notre solution, en exploitant spécifiquement notre stack technique (PyTorch, FastAPI, Hugging Face).

## Expérience 1 : Comparaison de Paradigmes (Supervisé vs Outliers)

L'objectif est de déterminer si l'approche par "Détection d'Anomalies" est plus pertinente que la classification classique pour repérer des fake news jamais vues auparavant.

* **Implémentation Technique :**
    * **Approche A (Supervisée - Baseline) :** Nous utiliserons **Hugging Face** pour récupérer et fine-tuner un modèle **DistilBERT** avec **PyTorch** sur le dataset ISOT complet. Ce modèle apprendra explicitement les caractéristiques textuelles du mensonge.
    * **Approche B (Non-Supervisée - Outliers) :** Nous extrairons les vecteurs (embeddings) des "Vraies News" via le modèle Transformer, puis nous entraînerons un algorithme de détection d'anomalies (type Isolation Forest via **Python**) pour apprendre la norme journalistique.
* **Test de Performance et Latence :** Outre la précision, nous mesurerons le temps d'inférence moyen en millisecondes en exposant ces modèles via une API **FastAPI**, validant leur viabilité pour une application web.

## Expérience 2 : Robustesse de la Détection Hybride (Simulation Watermark)

Cette expérience vise à valider l'approche "hybride" (identifiée dans l'état de l'art Bao et al. 2024) face à la compression des réseaux sociaux.

* **Protocole :** Création via un script **Python** d'un mini-dataset d'images Deepfakes composé de deux groupes : "bruts" et "marqués" (injection d'un watermark invisible).
* **Test de Résistance :** Nous appliquerons une compression JPEG progressive (qualité 90%, 70%, 50%) pour simuler un partage réel.
* **Comparaison :** Nous comparerons la robustesse d'un détecteur visuel classique (CNN entraîné sous **PyTorch**) face à notre décodeur de watermark.
* **Hypothèse :** Le modèle PyTorch (CNN) devrait voir sa performance chuter sous compression, tandis que le décodage du watermark restera stable.

## Expérience 3 : Évaluation Automatisée de la Pédagogie (LLM-as-a-Judge)

Plutôt qu'une validation manuelle, nous automatiserons l'évaluation de la qualité des explications fournies par VerifAI en utilisant l'infrastructure **Hugging Face**.

* **Génération A/B :** Pour un échantillon de fake news, nous générerons deux types d'explications via un LLM open-source (ex: Mistral) récupéré sur **Hugging Face** : une version "Factuelle brute" et une version "Pédagogique".
* **Juge Automatique :** Un second LLM agira comme juge pour noter chaque explication sur 10 selon des critères d'Empathie et de Clarté.
* **Analyse :** Cette méthode permet une validation quantitative rapide et reproductible de notre module éducatif.

