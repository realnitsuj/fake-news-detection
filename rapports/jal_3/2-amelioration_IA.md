# Évolution vers une Architecture Hybride (RAG & LLM)

Pour dépasser les limites d'une simple classification "Vrai/Faux", l'architecture a évolué vers un système de **Génération Augmentée par Récupération (RAG)**. Cette approche permet non seulement de détecter la désinformation, mais aussi de fournir une justification sourcée en se basant sur des faits réels et actualisés.

## Changement de Paradigme : De RoBERTa à Llamma 3

Initialement basé sur RoBERTa pour la classification, le système utilise désormais **Llama 3**. Ce changement est motivé par deux besoins :

  - **Le Raisonnement** : Capacité à expliquer *pourquoi* une information est jugée suspecte. RoBERTa ne donnait qu'une réponse Vrai/Faux, mais Llama, en tant que LLM, permet de justifier le choix.
  - **Le Contexte** : Capacité à comprendre le contexte global de l'article, et pas seulement une phrase isolée.


## Abandon du Fine-Tuning au profit du Prompt Engineering

La stratégie initiale envisageait un fine-tuning supervisé (SFT) sur un jeu de données spécifique (comme FakeNewsNet). Cette approche a été écartée au profit du *Prompt Engineering* couplée à l'architecture RAG, en raison de plusieurs contraintes techniques et méthodologiques.

### Les atouts théoriques du Fine-Tuning

Bien que non retenu pour l'itération actuelle, le fine-tuning supervisé (SFT) présente des avantages majeurs qui justifiaient son étude initiale :

- **Standardisation stricte du format :** L'entraînement permet de contraindre le modèle à générer systématiquement une structure de données exacte (JSON strict), éliminant le besoin de validations syntaxiques côté serveur.
- **Optimisation de la latence d'inférence :** Un modèle fine-tuné intégrant les directives de formatage dans ses poids nécessite un prompt utilisateur plus court (aucun exemple few-shot requis). La réduction du nombre de tokens en entrée diminue mécaniquement le temps d'apparition du premier mot généré (Time To First Token), et allège la consommation de mémoire VRAM lors de la phase d'inférence.
- **Spécialisation sémantique :** Cette méthode permet d'inculquer profondément un style rédactionnel précis (ton journalistique, neutre, vocabulaire expert) qu'un prompt seul peine parfois à maintenir sur de longues générations.
- **Efficacité matérielle :** Le fine-tuning permet à des modèles de petite taille (ici 8 milliards de paramètres) d'atteindre des performances comparables à des modèles massifs beaucoup plus complexes et coûteux à héberger en production.

### Risques de biais par données synthétiques

Trois sources de données principales ont été identifiées lors de la phase de recherche initiale :

- **Webz.io** : Un répertoire regroupant des contenus thématiques et des exemples de désinformation.
- **ISOT** : Un jeu de données binaire distinguant des articles réels et factices.
- **FakeNewsNet** : Un dépôt agrégeant des données vérifiées provenant de PolitiFact et GossipCop.

Pour générer un dataset permettant le fine-tuning du modèle, il est impératif de coupler chaque article (titre et texte) à son verdict (vrai/faux) et à une justification textuelle précise. Cependant, ces datasets manquent de la justification native nécessaire à notre architecture. Bien que Webz.io propose des contenus textuels plus denses, son exploitation a été écartée car le traitement de son volume brut excédait les ressources matérielles disponibles pour cette phase, et il ne fournit pas de verdicts de vérité validés par des experts. FakeNewsNet, bien qu'offrant une structure claire avec des labels de vérité, présente comme limite majeure l'absence totale de justifications textuelles expliquant ses verdicts.

La constitution manuelle d'un jeu de données comprenant des milliers d'exemples de désinformation, accompagnés de justifications précises rédigées par des humains, nécessite des ressources hors de portée pour l'envergure de ce projet. Ce manque force l'usage de données synthétiques pour entraîner le modèle. Cependant, la génération de ces justifications de manière synthétique introduit des risques sévères de biais :

* **Généralisation abusive :** Des justifications trop stéréotypées ou basiques entraînent le modèle à reproduire des patrons de phrases figés plutôt qu'à analyser réellement le texte soumis.
* **Incohérence sémantique :** Tenter de forcer une trop grande variété dans les justifications sans lien direct avec les faits réels augmente drastiquement le risque d'hallucinations lors de la génération.
* **Surapprentissage (Overfitting) :** L'usage d'un jeu de données de taille réduite ou répétitif forcerait le modèle à mémoriser des exemples spécifiques au lieu d'apprendre la structure logique universelle de la détection, dégradant ainsi ses performances globales.

### Démarche superflue pour les LLM modernes

Le système repose désormais sur Llama 3 (version *Instruct*). Ce modèle est nativement optimisé pour suivre des directives complexes, adopter un comportement spécifique (expert en vérification) et produire des formats de sortie stricts (ici JSON). Réentraîner les poids (même via PEFT/QLoRA) d'un modèle de plusieurs milliards de paramètres uniquement pour lui imposer une structure de réponse est disproportionné par rapport aux gains attendus.

### Agilité et synergie avec le RAG

Le *Few-Shot Prompting* (intégration de quelques exemples parfaits d'entrée/sortie directement dans la requête) s'avère plus efficace. 

- **Flexibilité :** Le schéma JSON attendu et les critères d'analyse peuvent être modifiés instantanément dans le prompt, sans nécessiter de nouveaux cycles de calculs GPU coûteux.
- **Séparation des préoccupations :** Dans l'architecture RAG, la vérité factuelle provient de la base vectorielle (ChromaDB), non des poids internes du modèle. Le prompt engineering permet d'injecter ce contexte externe proprement, laissant le modèle se concentrer sur l'analyse logique plutôt que sur la restitution de faits appris lors d'un éventuel fine-tuning.
- **Cycle de développement accéléré :** L'ajustement d'un prompt s'effectue en temps réel. À l'inverse, modifier une instruction via fine-tuning exige un cycle complet et chronophage (préparation des données, entraînement, évaluation). De plus, la maintenance est simplifiée par le versionnage d'un simple code texte, évitant la gestion d'artefacts de modèles lourds (fichiers de plusieurs gigaoctets).
- **Exploitation de la fenêtre de contexte :** Llama 3 dispose d'une large capacité d'ingestion (plus de 8000 tokens). Il est donc possible d'injecter simultanément des instructions complexes, des exemples d'entrée/sortie et les documents issus du RAG sans saturer le modèle, rendant la compression des règles de formatage dans les poids du réseau obsolète.


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

