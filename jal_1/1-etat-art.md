# État de l'art

## Survey of fake news detection using machine intelligence approach [@palSurveyFakeNews2023]

Cet article propose une vue d’ensemble complète des approches de détection automatique de fake news basées sur l’intelligence artificielle, en mettant l'accent sur la diversité des signaux exploités.

### Les trois familles de méthodes
Les auteurs classifient les approches en trois catégories distinctes :

- **Contenu textuel** : Analyse des caractéristiques lexicales, stylistiques et des représentations vectorielles du texte.
- **Contexte social** : Exploitation des profils utilisateurs, de la structure des interactions et des graphes de diffusion.
- **Approches hybrides** : Combinaison de plusieurs sources de signaux pour une robustesse accrue.

### Performance et Comparaison
Le survey passe en revue les principaux jeux de données publics (Kaggle et ISOT) et compare les performances des modèles. Il met en opposition les modèles d’apprentissage automatique “classiques” (SVM, régressions, arbres de décision) aux architectures d’apprentissage profond plus récentes (CNN, RNN, Transformers), démontrant la supériorité de ces dernières sur les tâches complexes.

### Défis identifiés
Les auteurs soulignent plusieurs obstacles majeurs : la difficulté de généraliser un modèle entraîné sur un domaine spécifique (domaine shift), la sensibilité à la qualité de l’annotation des données, et surtout le **manque d’explicabilité**. Ce dernier point est crucial car l'effet "boîte noire" limite la confiance que les utilisateurs finaux peuvent accorder aux systèmes de détection.


## A systematic review of multimodal fake news detection on social media using deep learning models [@nasserSystematicReviewMultimodal2025]

Cette revue systématique s’intéresse spécifiquement aux approches **multimodales** sur les réseaux sociaux, partant du constat que la désinformation moderne combine intrinsèquement texte et image.

### Architectures de fusion multimodale
Les auteurs analysent comment les architectures de deep learning fusionnent les modalités :

- **Images** : Utilisation de réseaux convolutionnels (CNN) ou de Vision Transformers.
- **Texte** : Utilisation de RNN ou de Transformers (BERT, etc.).
- **Métadonnées** : Intégration de modules supplémentaires pour les signaux comportementaux.

### Résultats et efficacité
Les résultats montrent que les modèles multimodaux surpassent systématiquement les approches uniquement textuelles, en particulier sur des plateformes riches en visuels comme Twitter, Facebook ou Weibo. L'image joue souvent un rôle de catalyseur dans la diffusion de la fausse information.

### Limites et contraintes techniques
La revue met en évidence des freins importants à l'adoption pratique : la complexité et le coût de calcul élevés, le besoin de jeux de données annotés massifs et cohérents, et la difficulté d'aligner l'explicabilité entre le texte et l'image (savoir quelle partie de l'image a déclenché la décision). Ces contraintes valident notre choix de privilégier une solution explicable et éducative plutôt qu'une performance brute opaque.


## Truth Sleuth & Trend Bender [@logeTruthSleuthTrend2025]

Cette recherche se concentre sur l'automatisation du fact-checking pour les contenus multimédias (YouTube), avec deux agents spécialisés.

### Truth Sleuth - L'Agent de Vérification des Faits

Truth Sleuth est conçu pour vérifier automatiquement le contenu de vidéos YouTube. D’abord, il extrait les affirmations clés de la vidéo analysée. Ensuite, Truth Sleuth utilise la technologie **Retrieval-Augmented Generation (RAG)** pour vérifier les faits, c’est-à-dire qu’il va chercher des données de confiance (souvent classées en trois catégories : gold, silver et bronze) en rapport avec les informations à vérifier. Cette méthode interroge des moteurs de recherche et d'autres sources considérées comme fiables.

> *« Truth Sleuth extracts claims from a YouTube video, uses a Retrieval-Augmented Generation (RAG) approach drawing on sources like Wikipedia, Google Search, Google FactCheck - to accurately assess their veracity. »* [@logeTruthSleuthTrend2025]

Enfin, l'agent rédige une réponse grâce à ses connaissances et aux informations contextuelles ajoutées, afin d’indiquer si chaque affirmation est vraie ou non, et fournit des sources et des explications détaillées. L’avantage de cette méthode est de réduire les hallucinations liées aux IA, en poussant le modèle à s’appuyer sur des sources vérifiables plutôt que de laisser l’IA répondre librement avec ses biais.

### Trend Bender - L'Agent de Persuasion

Trend Bender génère des commentaires dans le but de convaincre les spectateurs, en étant doté d'un mécanisme d'auto-évaluation. L’agent génère une première réponse, qu’il réinjecte ensuite comme entrée dans un nouveau prompt afin de l’améliorer et de la corriger.

> *« With a carefully set up self-evaluation loop, this agent is able to iteratively improve its style and refine its output. »* [@logeTruthSleuthTrend2025]

Dans cet article, ce qui nous intéresse particulièrement pour notre projet est de constater que l’utilisation du RAG dans la détection de fake news et le fact-checking automatisé est très récente et active (article de 2025). Il met aussi en avant l’importance de la qualité et de la classification des sources externes utilisées pour la vérification, ce qui rejoint notre réflexion sur la sélection de données fiables et la façon d’expliquer les résultats à l’utilisateur.


## Multi-Agent Systems for Misinformation [@gautamMultiagentSystemsMisinformation2025]

Contrairement à l'approche avec deux agents de @logeTruthSleuthTrend2025, cette solution propose une méthode à cinq agents autonomes, chacun se concentrant sur un aspect spécifique du cycle de vie de la désinformation.

### Les cinq agents spécialisés

- **La Classification** : trie et catégorise le type de désinformation détecté.
- **L’Indexation** : gère et actualise l'infrastructure de vérification en tenant une archive des données vérifiées et fiables.
- **L'Extraction** : se concentre sur la collecte et la traçabilité des preuves, récupère les preuves vérifiées et remonte à l’origine de la désinformation.
- **La Correction** : corrige les informations et effectue des modifications basées sur les preuves identifiées.
- **La Vérification** : vérifie la qualité finale des corrections apportées et suit la crédibilité des sources.

> *« In contrast to single-agent or monolithic architectures, our approach employs five specialized agents: an Indexer agent […], a Classifier agent […], an Extractor agent […], a Corrector agent […] and a Verification agent for validating outputs and tracking source credibility. »* [@gautamMultiagentSystemsMisinformation2025]

### Avantages de l’approche à 5 agents

Cette architecture possède plusieurs avantages. L'amélioration de RAG et, plus généralement, du pipeline de traitement, provient de l’ajout d’agents pour diviser la tâche, ce qui permet une optimisation indépendante de chaque étape.

> *« By decomposing the misinformation lifecycle into specialized agents our framework enhances scalability, modularity, and explainability. »* [@gautamMultiagentSystemsMisinformation2025]

Il est ainsi plus facile de déterminer d’où provient une erreur ou quel module doit être amélioré, puisqu’on peut associer chaque décision à un agent. La modularité permet l'amélioration indépendante de chaque composant. Enfin, la séparation des responsabilités contribue à réduire certains biais, en limitant la concentration de toutes les décisions dans un seul modèle monolithique.

### Défis et limitations

Malgré ses avantages, le coût d’utilisation est élevé, puisque la mise en œuvre de cinq agents autonomes implique des coûts de calcul et d'infrastructure importants. La latence est également problématique, car la multiplication des interactions entre agents augmente la durée totale du traitement. Dans un environnement où la vitesse de détection est un enjeu majeur (par exemple sur les réseaux sociaux durant une campagne électorale), cette latence peut devenir un frein à l’adoption.

## Automatic deception detection: : Methods for finding fake news [@conroyAutomaticDeceptionDetection2016]

Cette recherche passe en revue les technologies actuelles qui jouent un rôle clé dans l’adoption et le développement de la détection des fake news.

### Typologie des méthodes de détection

Cet article propose une classification claire des approches existantes en deux grandes catégories :

- **Approches linguistiques** : Analyse du contenu textuel pour identifier des "fuites linguistiques" (mots, syntaxe, sémantique, discours) associées à la tromperie, comme par example l’usage excessif de pronoms, de négations, ou d’émotions extrêmes pouvant trahir un texte mensonger.
- **Approches par réseaux** : Exploitation des métadonnées, des comportements sur les réseaux sociaux, ou des bases de connaissances structurées (comme DBpedia) pour évaluer la crédibilité d’une information, notament par la vérification de faits via des graphes de connaissances ou l’analyse des profils d’utilisateurs suspects.

### Hybridation des méthodes pour une détection robuste

Les auteurs plaident pour un système hybride intégrant :

1. **Linguistique** (analyse de surface, syntaxe profonde, sémantique, rhétorique) pour capter les indices textuels de tromperie.
2. **Réseaux** (comportements en ligne, liens entre sources, vérification par bases de données) pour ajouter une dimension contextuelle et sociale.
3. **Machine Learning** (SVM, Naïve Bayes) pour entraîner des classifieurs à partir de données annotées.

Les auteurs pointent d'ailleurs que la combinaison de l’analyse syntaxique, pour détecter des incohérences, et des graphes de connaissances, pour vérifier des faits, a montré des taux de précision allant jusqu’à 91% dans certains cas.

## Beyond News Contents: The Role of Social Context for Fake News Detection [@shuNewsContentsRole2019]

Cette recherche part du constat fondamental que la détection basée uniquement sur le contenu textuel est souvent inefficace, car les fausses nouvelles sont intentionnellement rédigées pour imiter le style des vraies nouvelles afin de tromper les lecteurs.

### Le Framework TriFN : Une approche tripartite

Les auteurs proposent le modèle TriFN (Tri-Relationship Fake News detection) qui modélise simultanément trois entités et leurs interactions:

- Les Éditeurs (Publishers) : Le modèle analyse le biais partisan des éditeurs. Un éditeur ayant un fort biais partisan (extrême gauche ou droite) est statistiquement plus enclin à publier des fausses nouvelles qu'un média grand public neutre.
- Les Utilisateurs : Le modèle intègre les interactions sociales et le score de crédibilité des utilisateurs. Les utilisateurs peu crédibles ou malveillants tendent à partager davantage de désinformation que les utilisateurs fiables.
- Le Contenu : L'analyse textuelle classique reste présente mais est enrichie par les deux vecteurs précédents.

### Résultats et détection précoce

Les expérimentations menées sur les jeux de données FakeNewsNet (BuzzFeed et PolitiFact) démontrent deux points cruciaux pour notre projet :

- Supériorité du contexte social : Les fonctionnalités basées sur le contexte social (qui publie, qui partage) se révèlent plus performantes que celles basées uniquement sur le texte (comme l'analyse linguistique LIWC).
- Détection précoce (Early Detection) : Le modèle TriFN parvient à atteindre un score F1 supérieur à 80% moins de 48 heures après la publication d'une nouvelle, prouvant qu'il est possible de détecter une fake news tôt dans son cycle de diffusion, même avec des interactions limitées.

***

Cette étude indique que l'inclusion de données temporelles et contextuelles est indispensable. Elle suggère que notre solution ne doit pas analyser le texte seulement, mais prendre en compte l'écosystème de sa diffusion (source et partages).

## Fake news detection: A survey of graph neural network methods [@phanFakeNewsDetection2023]

Ce survey récent justifie l'utilisation des structures de graphes pour modéliser la complexité des réseaux sociaux, là où les méthodes d'apprentissage classiques échouent souvent à capturer les relations d'interdépendance entre les utilisateurs et les contenus.

### La domination des GCN

L'étude analyse 27 articles majeurs et révèle que les Graph Convolutional Networks (GCN) sont la technique dominante (utilisée dans plus de 74% des cas étudiés). Contrairement à l'analyse de texte isolée, les GCN permettent de propager l'information à travers le réseau : si un utilisateur malveillant partage une news, cette information "contamine" le score de fiabilité de la news via les arêtes du graphe.

### Quatre approches de détection

Les auteurs classifient les méthodes de détection via GNN en quatre catégories:

- Basée sur la connaissance (Knowledge-based) : Vérification des faits via des graphes de connaissances externes (Fact-checking).
- Basée sur le style (Style-based) : Analyse des intentions trompeuses via le style d'écriture.
- Basée sur le contexte (Context-based) : Analyse de la crédibilité des utilisateurs et des éditeurs.
- Basée sur la propagation (Propagation-based) : Analyse de la cascade de diffusion de l'information (qui partage quoi et quand).

### Défis pour la détection précoce

L'article soulève un point critique pour notre projet : la détection précoce (Early Detection). Les méthodes basées sur la propagation sont très performantes mais nécessitent que la news ait déjà été partagée massivement. Pour une détection rapide (avant la viralité), les auteurs suggèrent de privilégier les approches basées sur le contexte (analyser la source dès la publication) ou d'utiliser des GNN hétérogènes capables de traiter simultanément le texte, l'image et le profil utilisateur dès les premiers instants.

## Personalizing LLM Responses to Combat Political Misinformation [@promaPersonalizingLLMResponses2025]

Cette étude récente, présentée à la conférence ACM UMAP 2025, aborde la lutte contre la désinformation sous un angle psychologique et cognitif. Les auteurs partent du constat que le simple "Fact-Checking" (vérification des faits) échoue souvent car il se heurte aux croyances préétablies des utilisateurs, provoquant un phénomène de dissonance cognitive.

### L'approche User-Centric et la Persuasion

Les chercheurs proposent une pipeline utilisant des modèles de langage (LLM) pour générer des réponses correctives **personnalisées**. Contrairement aux approches génériques où le même message est diffusé à tous, ce système repose sur deux piliers :
1.  **Grounding (Ancrage) :** L'utilisation de techniques RAG (Retrieval Augmented Generation) pour récupérer des preuves factuelles incontestables.
2.  **Rhetorical Styling (Adaptation Rhétorique) :** L'analyse du profil linguistique et des traits de personnalité de l'utilisateur pour adapter la formulation de la réponse. L'IA n'impose pas la vérité brutalement, mais adopte un ton (empathique, analytique ou assertif) qui résonne avec les valeurs de l'utilisateur pour contourner ses mécanismes de défense.

### Résultats et efficacité pédagogique

L'étude démontre que les réponses personnalisées sont significativement plus efficaces pour réduire les fausses croyances que les corrections standards. Elle valide l'efficacité du "micro-ciblage" éthique : l'IA agit comme un pédagogue capable d'expliquer l'erreur en suivant le cheminement de pensée de l'utilisateur, transformant la confrontation en dialogue.

***

Cet article est fondamental pour le **volet éducatif** de notre projet. Il confirme que le module d'explication de notre solution ne doit pas se contenter de résumer les faits, mais doit adopter une approche "centrée utilisateur". Pour maximiser l'impact pédagogique, nous devrons potentiellement adapter le ton des explications générées par LLM, assurant ainsi que l'utilisateur comprenne et accepte le verdict de détection sans se sentir jugé.

## Pluggable Watermarking of Deepfake Models for Deepfake Detection [@10.24963/ijcai.2024/37]

Publié lors de la conférence IJCAI 2024, cet article marque un tournant technologique en passant de la détection "passive" (analyser les pixels) à une défense "active" via le marquage des modèles génératifs. Face à des Deepfakes de plus en plus réalistes où la détection passive atteint ses limites et manque de robustesse, cette méthode propose d'intervenir à la source.

### La Défense Active et le concept "Pluggable"

Les auteurs présentent une méthode de tatouage numérique (watermarking) qualifiée de "pluggable" (enfichable) et efficace. L'innovation majeure réside dans le fait qu'elle s'intègre à des modèles de Deepfake déjà entraînés sans nécessiter un réentraînement complet, fonctionnant indépendamment de la méthode d'entraînement originale du modèle génératif.

Techniquement, l'outil utilise la "sparsification" des noyaux de convolution dans le décodeur du modèle génératif. Il identifie les positions des paramètres redondants via une stratégie d'élagage (pruning) pour y injecter une signature invisible. Ainsi, chaque image générée contient intrinsèquement une preuve mathématique de son origine artificielle sans altérer la qualité visuelle.

### Robustesse et Architecture Hybride

Pour garantir la détection, le système utilise un encodage BCH (Bose-Chaudhuri-Hocquenghem), un code correcteur d'erreur qui permet d'identifier le watermark même après des altérations ou des transformations avec perte. Les expérimentations, menées sur huit types majeurs de modèles de Deepfake (dont StyleGAN et SimSwap), montrent un taux de précision moyen supérieur à 94%. Cette approche dissocie la détection de la qualité visuelle de l'image, offrant une fiabilité que les méthodes passives ne peuvent garantir seules.

***

Cette recherche justifie l'adoption d'une **architecture hybride** pour notre solution. Elle suggère d'intégrer, en plus de nos algorithmes de détection visuelle (probabilistes), un module capable de lire ces signatures numériques (déterministes). Cela nous positionne comme une solution "future-proof", prête pour un écosystème où la régulation imposera le marquage des contenus générés par IA. Notre outil ne se contentera pas de "deviner" le faux via l'analyse d'artefacts, mais pourra "certifier" l'origine synthétique d'une image grâce à l'extraction de watermarks.

