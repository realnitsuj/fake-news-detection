# État de l'art

## Survey of fake news detection using machine intelligence approach (Pal et al., 2023)

Pal, A., Pranav, & Pradhan, M. (2023). Survey of fake news detection using machine intelligence approach. *Data & Knowledge Engineering*. [hhttps://doi.org/10.1016/j.datak.2022.102118](https://doi.org/10.1016/j.datak.2022.102118)

Cet article propose une vue d’ensemble des approches de détection automatique de fake news basées sur l’intelligence artificielle. Les auteurs distinguent principalement trois grandes familles de méthodes : celles fondées sur le contenu textuel de la nouvelle (caractéristiques lexicales, stylistiques, représentations vectorielles), celles qui exploitent le contexte social (profils utilisateurs, structure des interactions, graphes de diffusion), et les approches hybrides qui combinent plusieurs sources de signaux.

Le survey passe en revue les principaux jeux de données publics (Kaggle et ISOT) ainsi que les métriques d’évaluation classiques telles que l’accuracy, la précision, le rappel et le F1-score. Il compare les performances de modèles d’apprentissage automatique “classiques” (SVM, régressions, arbres de décision) avec des architectures d’apprentissage profond plus récentes (CNN, RNN, Transformers). Les auteurs soulignent plusieurs défis récurrents : difficulté de généraliser un modèle entraîné sur un domaine ou une plateforme vers un autre, sensibilité à la qualité de l’annotation et manque d’explicabilité des décisions, ce qui limite la confiance que peuvent accorder les utilisateurs aux systèmes de détection.

---

## A systematic review of multimodal fake news detection on social media using deep learning models (Nasser et al., 2025)

Nasser, M., Arshad, N. I., & Sugathan, S. K. (2025). A systematic review of multimodal fake news detection on social media using deep learning models. *Results in Engineering*. [https://doi.org/10.1016/j.rineng.2025.104752](https://doi.org/10.1016/j.rineng.2025.104752)  

Cette revue systématique s’intéresse spécifiquement aux approches multimodales appliquées aux réseaux sociaux, où les fake news combinent souvent texte, images et parfois vidéos. Les auteurs analysent les architectures de deep learning qui fusionnent plusieurs modalités : réseaux convolutionnels ou Vision Transformers pour les images, RNN/Transformers pour le texte, et parfois des modules supplémentaires pour intégrer des métadonnées ou des signaux comportementaux issus des plateformes sociales.  

Les résultats présentés montrent que les modèles multimodaux atteignent en général de meilleures performances que les approches uniquement textuelles, notamment sur des plateformes comme Twitter, Facebook ou Weibo, où les contenus visuels jouent un rôle important dans la diffusion de la désinformation. Cependant, la revue met en évidence plusieurs limites : complexité et coût de calcul élevés, besoin de grandes quantités de données annotées de manière cohérente, difficulté à expliquer quelles parties du texte ou de l’image ont conduit à la décision du modèle. Ces contraintes sont importantes pour notre projet, qui vise une solution utilisable en pratique, avec un accent sur l’explicabilité et l’éducation des utilisateurs plutôt que sur la seule performance brute.

---

## Truth Sleuth & Trend Bender (Logé & Ghori, 2025)

Logé, C., & Ghori, R. (2025). Truth Sleuth & Trend Bender: AI Agents to fact-check YouTube videos & influence opinions. arXiv. [https://doi.org/10.48550/arXiv.2507.10577](https://doi.org/10.48550/arXiv.2507.10577)

Cette recherche se concentre sur l'automatisation du fact-checking pour les contenus multimédias (YouTube), avec deux agents spécialisés.

### Truth Sleuth - L'Agent de Vérification des Faits

Truth Sleuth est conçu pour vérifier automatiquement le contenu de vidéos YouTube. D’abord, il extrait les affirmations clés de la vidéo analysée. Ensuite, Truth Sleuth utilise la technologie **Retrieval-Augmented Generation (RAG)** pour vérifier les faits, c’est-à-dire qu’il va chercher des données de confiance (souvent classées en trois catégories : gold, silver et bronze) en rapport avec les informations à vérifier. Cette méthode interroge des moteurs de recherche et d'autres sources considérées comme fiables.

> *« Truth Sleuth extracts claims from a YouTube video, uses a Retrieval-Augmented Generation (RAG) approach drawing on sources like Wikipedia, Google Search, Google FactCheck - to accurately assess their veracity. »* (Logé & Ghori, 2025)

Enfin, l'agent rédige une réponse grâce à ses connaissances et aux informations contextuelles ajoutées, afin d’indiquer si chaque affirmation est vraie ou non, et fournit des sources et des explications détaillées. L’avantage de cette méthode est de réduire les hallucinations liées aux IA, en poussant le modèle à s’appuyer sur des sources vérifiables plutôt que de laisser l’IA répondre librement avec ses biais.

### Trend Bender - L'Agent de Persuasion

Trend Bender génère des commentaires dans le but de convaincre les spectateurs, en étant doté d'un mécanisme d'auto-évaluation. L’agent génère une première réponse, qu’il réinjecte ensuite comme entrée dans un nouveau prompt afin de l’améliorer et de la corriger.

> *« With a carefully set up self-evaluation loop, this agent is able to iteratively improve its style and refine its output. »* (Logé & Ghori, 2025)

Dans cet article, ce qui nous intéresse particulièrement pour notre projet est de constater que l’utilisation du RAG dans la détection de fake news et le fact-checking automatisé est très récente et active (article de 2025). Il met aussi en avant l’importance de la qualité et de la classification des sources externes utilisées pour la vérification, ce qui rejoint notre réflexion sur la sélection de données fiables et la façon d’expliquer les résultats à l’utilisateur.

---

## Multi-Agent Systems for Misinformation (Gautam, 2025)

Gautam, Aditya. (2025). Multi-agent Systems for Misinformation Lifecycle: Detection, Correction and Source Identification. arXiv, 23 mai 2025. [https://arxiv.org/abs/2505.17511](https://arxiv.org/abs/2505.17511)

Contrairement à l'approche avec deux agents de Logé & Ghori, cette solution propose une méthode à cinq agents autonomes, chacun se concentrant sur un aspect spécifique du cycle de vie de la désinformation.

### Les cinq agents spécialisés

- **La Classification** : trie et catégorise le type de désinformation détecté.  
- **L’Indexation** : gère et actualise l'infrastructure de vérification en tenant une archive des données vérifiées et fiables.  
- **L'Extraction** : se concentre sur la collecte et la traçabilité des preuves, récupère les preuves vérifiées et remonte à l’origine de la désinformation.  
- **La Correction** : corrige les informations et effectue des modifications basées sur les preuves identifiées.  
- **La Vérification** : vérifie la qualité finale des corrections apportées et suit la crédibilité des sources.  

> *« In contrast to single-agent or monolithic architectures, our approach employs five specialized agents: an Indexer agent […], a Classifier agent […], an Extractor agent […], a Corrector agent […] and a Verification agent for validating outputs and tracking source credibility. »* (Gautam, 2025)

### Avantages de l’approche à 5 agents

Cette architecture possède plusieurs avantages. L'amélioration de RAG et, plus généralement, du pipeline de traitement, provient de l’ajout d’agents pour diviser la tâche, ce qui permet une optimisation indépendante de chaque étape.

> *« By decomposing the misinformation lifecycle into specialized agents our framework enhances scalability, modularity, and explainability. »* (Gautam, 2025)

Il est ainsi plus facile de déterminer d’où provient une erreur ou quel module doit être amélioré, puisqu’on peut associer chaque décision à un agent. La modularité permet l'amélioration indépendante de chaque composant. Enfin, la séparation des responsabilités contribue à réduire certains biais, en limitant la concentration de toutes les décisions dans un seul modèle monolithique.

### Défis et limitations

Malgré ses avantages, le coût d’utilisation est élevé, puisque la mise en œuvre de cinq agents autonomes implique des coûts de calcul et d'infrastructure importants. La latence est également problématique, car la multiplication des interactions entre agents augmente la durée totale du traitement. Dans un environnement où la vitesse de détection est un enjeu majeur (par exemple sur les réseaux sociaux durant une campagne électorale), cette latence peut devenir un frein à l’adoption.