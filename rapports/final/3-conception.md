# Conception et architecture

## Frontend

Maquettes, stack technologique et interface utilisateur

- **Stack technologique :** L'interface est développée avec React 19 et TypeScript, bundlée via Vite. Le style est géré par Tailwind CSS et les composants shadcn/ui.
- **Interface utilisateur :** L'application s'articule autour de deux vues principales :
    - **Page d'accueil :** Interface épurée permettant la saisie d'une URL ou d'un texte brut via un système d'onglets. 
    - **Page de résultats :** Affichage immédiat d'un verdict avec code couleur adapté (FAKE, REAL, UNCERTAIN), d'un score de confiance, de métriques détaillées et d'une explication textuelle.
- **Expérience :** Les transitions entre les pages sont fluides, utilisant un "skeleton" de chargement en attente de la réponse du serveur.

## Backend & API

Structure FastAPI et flux de traitement

- **Structure :** Le serveur expose une API REST développée avec FastAPI. Ce framework a été retenu pour sa gestion asynchrone et sa compatibilité native avec Pydantic pour la validation des données. Le backend agit comme intermédiaire sécurisé entre l'utilisateur et les services d'IA.
* **Flux de traitement (5 étapes) :**
    1. **Validation :** Réception et vérification du format et de la longueur du texte.
    2. **Authentification :** Injection sécurisée des clés API.
    3. **Traitement IA :** Transmission des données au modèle d'intelligence artificielle.
    4. **Parsing :** Extraction des valeurs essentielles (label, score, justification) de la réponse brute.
    5. **Post-traitement :** Conversion des données et restitution finale sous la forme d'un objet JSON standardisé pour le frontend.

## Évolution de l'IA

- **Transition vers Llama 3 :** Le système est passé d'un modèle de classification binaire initial (RoBERTa) à un modèle de langage (Llama 3 Instruct). Cette évolution permet au système de fournir un raisonnement détaillé et d'analyser le contexte global de l'information.
- **Architecture RAG (Génération Augmentée par Récupération) :** Le fine-tuning a été écarté au profit du Prompt Engineering combiné à une architecture RAG. Cette approche dote l'IA d'une mémoire factuelle. Le texte à vérifier est comparé à une base de connaissances ; l'article de référence le plus pertinent est alors injecté dans le prompt de Llama 3 pour guider le verdict.
- **Base vectorielle ChromaDB :** Les articles de référence sont transformés en vecteurs sémantiques via le modèle Sentence-Transformers, puis stockés et indexés dans la base de données vectorielle ChromaDB pour permettre une recherche de similarité rapide.
- **Stratégie de collecte de données :** La base de connaissances est alimentée par un script de collecte automatisée. Ce système extrait quotidiennement le contenu des flux RSS de sources de presse reconnues pour leur fiabilité et leur complémentarité (Le Monde et France 24).
