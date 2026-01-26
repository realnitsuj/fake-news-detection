# État de l'art
# Truth Sleuth & Trend Bender (Logé & Ghori, 2025)
Logé, C., & Ghori, R. (2025). Truth Sleuth & Trend Bender: AI Agents to fact-check YouTube videos & influence opinions. arXiv. https://doi.org/10.48550/arXiv.2507.10577

## Truth Sleuth - L'Agent de Vérification des Faits
Truth Sleuth est conçu pour vérifier automatiquement le contenu de vidéos Youtube. D’abord il extrait les affirmations clés de la vidéo analysée. Ensuite, Truth Sleuth utilise la technologie **Retrieval-Augmented Generation (RAG)** pour vérifier les faits. C’est à dire qu’il va chercher des données de confiances (souvent classées en 3 catégories de confiances : Gold, silver et bronze) en rapport avec les informations à vérifier. Ces données sont ensuite augmentées, c’est à dire qu’elles sont intégrées au texte fournis en entrée, afin de donner du contexte. Cette méthode utilise les moteurs de recherche et d'autres sources fiables. Enfin, l'agent rédige une réponse grâce à ses connaissances et les informations contextuelles ajoutées ; afin d’indiquer si chaque affirmation est vraie ou non et rajoute des sources et des explications détaillées.



L’avantage de cette méthode est de réduire les hallucinations liées aux IA, en poussant le modèle à utiliser des sources vérifiables, plutôt que de laisser l’IA répondre librement avec ses biais.

## Trend Bender - L'Agent de Persuasion
Trend Bender génère des commentaires dans le but de convaincre les spectateurs, dotés d'un mécanisme d'auto-évaluation, donc l’agent génère une réponse qu’il va lui même reprendre en entrée d’un nouveau prompt afin de l’améliorer et de le corriger.

Dans cet article, ce qui nous intéresse par rapport à notre sujet est donc de voir que l’utilisation du RAG dans la détection de fake news est d’actualité car l’article date de 2025. Et nous à fais chercher des informations sur la méthodes de classification des données cherchées, afin de détecter su elles sont de qualités ou non.

---

# Multi-Agent Systems for Misinformation (Gautam, 2025)
Gautam, Aditya. "Multi-agent Systems for Misinformation Lifecycle: Detection, Correction and Source Identification." arXiv, 23 mai 2025, arxiv.org/abs/2505.17511

Contrairement à l'approche avec deux agents précédente, cette solution propose une méthode à cinq agents autonomes, chacun se concentrant sur un aspect spécifique du problème.

## Les Cinq Agents Spécialisés
* **La Classification :** va trier et catégoriser le type de désinformation détecté. Les catégories sont : la propagande (information volontairement trompeuse créée pour influencer), les erreurs statistiques (mauvaise interprétation de données ou présentation trompeuse), les deepfakes, les contextualisations incorrectes, et les omissions intentionnelles. Cette classification permet de guider les agents suivants dans le type de corrections à réaliser.
* **L’indexation :** gère et actualise l'infrastructure de vérification en tenant une archive des données vérifiées et fiables. Il met à jour en continu des références officielles. Cette fonction assure que le système dispose toujours de données actuelles ce qui est important pour la détection de fake news qui est un domaine qui change constamment, avec de nouveaux sujets qui apparaissent chaque jour.
* **L'Extraction :** se concentre sur la collecte et la traçabilité des preuves. Il récupère les preuves vérifiées et va chercher l'origine de la désinformation, en analysant les métadonnées. Il y a donc une partie d’identification des sources de l’auteur et des modifications, l’analyse de la date de publication (plus c’est vieux, plus il y a de chance que l’information ai été contredite).
* **La Correction :** corrige les informations et effectue des modifications basées sur les preuves identifiées et les citations réelles. Ce n’est donc pas simplement détecter ce qui est faux mais aussi le corriger de la manière la plus claire afin d’avoir un effet sur les lecteurs. La communication est donc un point important de cet agent.
* **La Vérification :** vérifie la qualité finale des corrections apportées, en examinant la qualité et les sources et la cohérence logique pour vérifier que les explications sont claires et structurées.



## Avantages de l’approche à 5 Agents
Cette architecture possède plusieurs avantages. L'amélioration de RAG provient de l’ajout d’agents pour diviser la tâche, ce qui permet une optimisation indépendante de la tâche. Et grâce à l’indexation, on peut garder une base de données mise à jour sans affecter le processus global.

Il est aussi plus facile de déterminer d’où provient une erreur ou qu’est-ce qui devrait être améliorer, car il est plus facile de voir quel agent à pris quelle décision, car ces agents sont affectés à moins de tâches.

La modularité permet l'amélioration indépendante de chaque agent. Par exemple si une meilleure technique de classification existe, seul l’agent de classification va être amélioré.

Enfin, la réduction des biais vient de la séparation des responsabilités. Par exemple l’agent de classification peut être entraîné à reconnaître des types de désinformation sans connaître comment les sources seront vérifiées, ce qui réduit la probabilité d’avoir des biais qui se propagent.

## Défis et Limitations
Malgré ses avantages, le coût d’utilisation est élevé, puisque la mise en marche de cinq agents autonomes implique des coûts importants. Chaque appel d'API, chaque interaction entre agents génère des coûts qui s'additionnent.

La latence est également problématique. Car avoir 5 agents augmente grandement le nombre d’interactions. Dans un environnement où la vitesse de détection des interactions est un enjeu majeur, cette latence peut devenir problématique.
