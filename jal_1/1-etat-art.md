# État de l'art

# Truth Sleuth & Trend Bender (Logé & Ghori, 2025)

Logé, C., & Ghori, R. (2025). Truth Sleuth & Trend Bender: AI Agents to fact-check YouTube videos & influence opinions. arXiv. [https://doi.org/10.48550/arXiv.2507.10577](https://doi.org/10.48550/arXiv.2507.10577)

Cette recherche se concentre sur l'automatisation du fact-checking pour les contenus multimédias (YouTube), avec deux agents spécialisés.

## Truth Sleuth - L'Agent de Vérification des Faits

Truth Sleuth est conçu pour vérifier automatiquement le contenu de vidéos Youtube. D’abord il extrait les affirmations clés de la vidéo analysée. Ensuite, Truth Sleuth utilise la technologie **Retrieval-Augmented Generation (RAG)** pour vérifier les faits. C’est à dire qu’il va chercher des données de confiances (souvent classées en 3 catégories de confiances : Gold, silver et bronze) en rapport avec les informations à vérifier. Cette méthode utilise les moteurs de recherche et d'autres sources fiables.

> *« Truth Sleuth extracts claims from a YouTube video, uses a Retrieval-Augmented Generation (RAG) approach drawing on sources like Wikipedia, Google Search, Google FactCheck - to accurately assess their veracity »* (Logé & Ghori, 2025).

Enfin, l'agent rédige une réponse grâce à ses connaissances et les informations contextuelles ajoutées ; afin d’indiquer si chaque affirmation est vraie ou non et rajoute des sources et des explications détaillées. L’avantage de cette méthode est de réduire les hallucinations liées aux IA, en poussant le modèle à utiliser des sources vérifiables, plutôt que de laisser l’IA répondre librement avec ses biais.

## Trend Bender - L'Agent de Persuasion

Trend Bender génère des commentaires dans le but de convaincre les spectateurs, dotés d'un mécanisme d'auto-évaluation, donc l’agent génère une réponse qu’il va lui même reprendre en entrée d’un nouveau prompt afin de l’améliorer et de le corriger.

> *« With a carefully set up self-evaluation loop, this agent is able to iteratively improve its style and refine its output. »* (Logé & Ghori, 2025).

Dans cet article, ce qui nous intéresse par rapport à notre sujet est donc de voir que l’utilisation du RAG dans la détection de fake news est d’actualité car l’article date de 2025. Et nous a fait chercher des informations sur la méthode de classification des données cherchées, afin de détecter si elles sont de qualités ou non.

---

# Multi-Agent Systems for Misinformation (Gautam, 2025)

Gautam, Aditya. "Multi-agent Systems for Misinformation Lifecycle: Detection, Correction and Source Identification." arXiv, 23 mai 2025, arxiv.org/abs/2505.17511

Contrairement à l'approche avec deux agents précédente, cette solution propose une méthode à cinq agents autonomes, chacun se concentrant sur un aspect spécifique du problème.

## Les Cinq Agents Spécialisés

* **La Classification :** va trier et catégoriser le type de désinformation détecté.
* **L’indexation :** gère et actualise l'infrastructure de vérification en tenant une archive des données vérifiées et fiables.
* **L'Extraction :** se concentre sur la collecte et la traçabilité des preuves. Il récupère les preuves vérifiées et va chercher l'origine de la désinformation.
* **La Correction :** corrige les informations et effectue des modifications basées sur les preuves identifiées.
* **La Vérification :** vérifie la qualité finale des corrections apportées.

> *« In contrast to single-agent or monolithic architectures, our approach employs five specialized agents: an Indexer agent [...], a Classifier agent [...], an Extractor agent [...], a Corrector agent [...] and a Verification agent for validating outputs and tracking source credibility. »* (Gautam, 2025).

## Avantages de l’approche à 5 Agents

Cette architecture possède plusieurs avantages. L'amélioration de RAG provient de l’ajout d’agents pour diviser la tâche, ce qui permet une optimisation indépendante de la tâche.

> *« By decomposing the misinformation lifecycle into specialized agents our framework enhances scalability, modularity, and explainability. »* (Gautam, 2025).

Il est aussi plus facile de déterminer d’où provient une erreur ou qu’est-ce qui devrait être amélioré, car il est plus facile de voir quel agent a pris quelle décision. La modularité permet l'amélioration indépendante de chaque agent. Enfin, la réduction des biais vient de la séparation des responsabilités.

## Défis et Limitations

Malgré ses avantages, le coût d’utilisation est élevé, puisque la mise en marche de cinq agents autonomes implique des coûts importants. La latence est également problématique, car avoir 5 agents augmente grandement le nombre d’interactions. Dans un environnement où la vitesse de détection est un enjeu majeur, cette latence peut devenir problématique.
