# Évolution vers une Architecture Hybride (RAG & LLM)

Pour dépasser les limites d'une simple classification "Vrai/Faux", l'architecture a évolué vers un système de **Génération Augmentée par Récupération (RAG)**. Cette approche permet non seulement de détecter la désinformation, mais aussi de fournir une justification sourcée en se basant sur des faits réels et actualisés.

## Changement de Paradigme : De RoBERTa à Llamma 3

Initialement basé sur RoBERTa pour la classification, le système utilise désormais **Llama 3**. Ce changement est motivé par deux besoins :

  - **Le Raisonnement** : Capacité à expliquer *pourquoi* une information est jugée suspecte. RoBERTa ne donnait qu'une réponse Vrai/Faux, mais Llama, en tant que LLM, permet de justifier le choix.
  - **Le Contexte** : Capacité à comprendre le contexte global de l'article, et pas seulement une phrase isolée.

<!-- ## Fine Tunning -->
<!---->
<!-- La phase de fine-tuning vise à transformer un modèle généraliste en un expert en détection de désinformation, capable de répondre selon un format JSON strict compatible avec le backend de VerifAI. -->
<!---->
<!-- ### Choix des données -->
<!---->
<!-- Pour les données, nous avions pré selectionné plusieurs sets au premier jalon : -->
<!---->
<!-- - Webz.io : répertoire de fake news uniquement (<https://github.com/Webhose/fake-news-dataset>), de nouvelles de plusieurs thématiques (<https://github.com/Webhose/free-news-datasets>) ou plus spécifiques (<https://github.com/Webhose/financial-news-dataset>) -->
<!-- - ISOT : <https://www.kaggle.com/datasets/csmalarkodi/isot-fake-news-dataset>, jeu de données contenant des articles réels et factices. -->
<!-- - FakeNewsNet : un dépôt agrégeant des données de PolitiFact et GossipCop. -->
<!---->
<!-- Le choix s'est porté sur FakeNewsNet. Bien que Webz.io propose des contenus plus denses (textes intégraux), son volume brut nécessitait des ressources matérielles de traitement hors de portée pour cette phase du projet. ISOT, bien que binaire et efficace, manquait de granularité sur les métadonnées (catégories, sources contextuelles). FakeNewsNet offre un compromis optimal : une structure claire facilitant l'apprentissage supervisé, avec un accès aux titres, aux sources (Politique ou Divertissement) et aux labels de vérité validés par des experts. -->
<!---->
<!-- La limite majeure de FakeNewsNet pour ce projet réside dans l'absence de justifications textuelles natives expliquant les verdicts. Pour pallier ce manque et répondre aux exigences du schéma JSON cible, une étape de complétion a été appliquée. Des justifications synthétiques et des scores de confiance variables ont été injectés dans le jeu de données. Cette stratégie permet d'enseigner au modèle la structure syntaxique d'une explication et le respect strict du format attendu, indépendamment de la véracité absolue du texte d'entraînement. -->
<!---->
<!-- *** -->
<!---->
<!-- Voici les étapes pour utiliser le dataset : -->
<!---->
<!-- ```bash -->
<!-- git clone https://github.com/kaidmml/fakenewsnet -->
<!-- cd fakenewsnet -->
<!---->
<!-- # Fixex à une version de python ancienne, par rapport aux dépendances -->
<!-- conda create -n fakenewsnet python=3.6 -->
<!-- source ~/.bashrc -->
<!-- conda activate fakenewsnet -->
<!-- pip install "setuptools<58.0.0" -->
<!-- pip install -r requirements.txt -->
<!---->
<!-- # Adapter la configuration à nos besoins -->
<!-- $EDITOR code/config.json -->
<!-- # Nous avons enlever les tweets : `"data_features_to_collect" : ["news_articles"]` -->
<!-- # On peut paralléliser, selon son nombre de coeurs : `"num_process": 8,` -->
<!---->
<!-- # Lancer le code -->
<!-- cd code/ -->
<!-- nohup python -m resource_server.app &> keys_server.out& -->
<!-- nohup python main.py &> data_collection.out& -->
<!-- ``` -->
<!---->
<!-- Pour suivre la progression du set en cours *uniquement* (sachant qu'il y en a 4) : -->
<!---->
<!-- ```bash -->
<!-- tail -n 1 data_collection.out  -->
<!--   7%|-         | 1202/16817 [3:49:09<21:28:06,  4.95s/it]  -->
<!-- ``` -->
<!---->
<!-- On a alors les articles téléchargés dans `fakenewsnet_dataset` (sauf changement dans `config.json`) : -->
<!---->
<!---->
<!-- ### Préparation du dataset -->
<!---->
<!-- Les données brutes de FakeNewsNet ont été converties au format JSONL. Chaque entrée suit une structure d'instruction spécifique (SFT - Supervised Fine-Tuning) incluant les balises `[INST]` du modèle Mistral. -->
<!---->
<!-- Chaque exemple d'entraînement comprend : -->
<!---->
<!-- 1. Le texte de l'article. -->
<!-- 2. Une réponse attendue structurée contenant : le verdict, un score de confiance, la catégorie et une justification. -->
<!---->
<!-- ```json -->
<!-- # Exemple de structure de donnée pour l'entraînement -->
<!-- { -->
<!--   "text": "<s>[INST] Analyse le texte suivant... [/INST] {\"verdict\": \"FAUX\", \"confiance\": 0.95, \"categorie\": \"Politique\", \"justification\": \"...\"}</s>" -->
<!-- } -->
<!-- ``` -->
<!---->
<!-- ### Configuration technique -->
<!---->
<!-- L'entraînement a été réalisé sur un GPU NVIDIA T4 via Google Colab. Pour optimiser l'usage de la mémoire vidéo (VRAM), la méthode QLoRA (Quantized Low-Rank Adaptation) a été utilisée : -->
<!---->
<!-- - Quantification 4-bit : Réduction du poids du modèle pour tenir dans les 16 Go de la carte T4. -->
<!-- - PEFT (Parameter-Efficient Fine-Tuning) : Seule une petite fraction des paramètres est modifiée, accélérant l'apprentissage sans perdre les connaissances générales du modèle. -->
<!---->
<!-- ### Processus d'entraînement -->
<!---->
<!-- L'entraînement a été configuré sur 3 époques, ce qui risque de dépasser la durée permise par Colab.   -->
<!-- Une stratégie de sauvegarde par points de contrôle (checkpoints) a été mise en place sur Google Drive. Cette précaution permet de reprendre l'entraînement en cas d'interruption de la session Colab sans perdre la progression. -->
<!---->
<!-- ![Capture d'écran de l'interface Colab pendant le fine tuning](colab.png) -->
<!---->
<!-- ### Intégration et format de sortie -->
<!---->
<!-- Le modèle fine-tuné est configuré pour produire une sortie JSON pure. Cette standardisation est cruciale pour l'intégration avec le service `ai_service.py` du backend. Le système peut ainsi extraire automatiquement les données pour les afficher à l'utilisateur final de manière structurée. -->
<!---->

## Abandon du Fine-Tuning au profit du Prompt Engineering

La stratégie initiale envisageait un fine-tuning supervisé (SFT) sur un jeu de données spécifique (comme FakeNewsNet). Cette approche a été écartée au profit du *Prompt Engineering* couplée à l'architecture RAG, en raison de plusieurs contraintes techniques et méthodologiques.

### Risques de biais par données synthétiques

Les jeux de données ouverts de détection de fausses nouvelles (ex: FakeNewsNet, ISOT) fournissent des labels binaires mais manquent de justifications textuelles détaillant le raisonnement. La génération de ces justifications de manière synthétique pour entraîner le modèle introduit des risques sévères de biais :

* **Généralisation abusive :** Des justifications trop stéréotypées ou basiques entraînent le modèle à recracher des modèles de phrases plutôt qu'à analyser le texte réel.
* **Incohérence sémantique :** Tenter de forcer une trop grande variété dans les justifications sans lien direct avec les faits réels augmente drastiquement le risque d'hallucinations.
* **Surapprentissage (Overfitting) :** Un jeu de données de petite taille forcerait le modèle à mémoriser les exemples spécifiques plutôt qu'à apprendre la structure logique, détériorant ses performances globales.

### Démarche superflue pour les LLM modernes

Le système repose désormais sur des modèles avancés comme Llama 3 (version *Instruct*). Ces modèles sont nativement optimisés pour suivre des directives complexes, adopter un comportement spécifique (expert en vérification) et produire des formats de sortie stricts (ici JSON). Réentraîner les poids (même via PEFT/QLoRA) d'un modèle de plusieurs milliards de paramètres uniquement pour lui imposer une structure de réponse est disproportionné et inutile.

### Agilité et synergie avec le RAG

Le *Few-Shot Prompting* (intégration de quelques exemples parfaits d'entrée/sortie directement dans la requête) s'avère plus efficace. 
* **Flexibilité :** Le schéma JSON attendu et les critères d'analyse peuvent être modifiés instantanément dans le prompt, sans nécessiter de nouveaux cycles de calculs GPU coûteux.
* **Séparation des préoccupations :** Dans l'architecture RAG, la vérité factuelle provient de la base vectorielle (ChromaDB), non des poids internes du modèle. Le prompt engineering permet d'injecter ce contexte externe proprement, laissant le modèle se concentrer sur l'analyse logique plutôt que sur la restitution de faits appris lors d'un éventuel fine-tuning.

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

