# Marketing : Stratégie de Commercialisation et d'Acquisition

Conformément aux exigences du plan de cours, ce rapport décrit la stratégie marketing complète du produit VerifAI. Cette stratégie vise à préparer le passage critique d'un prototype fonctionnel actuel à un produit technologique réellement adopté par ses utilisateurs cibles lors des phases de déploiement et d'expansion à venir.

Notre application répond à un besoin sociétal croissant et urgent : vérifier rapidement la fiabilité d’un contenu dans un contexte où la désinformation circule massivement. Lors des élections québécoises de 2022, près du tiers des électeurs ont affirmé avoir été exposés à de la désinformation, un fléau qui prend une ampleur inquiétante sur le web.

L’objectif de cette section est structuré autour de cinq axes majeurs :

1. Identifier précisément les utilisateurs cibles grâce à une analyse Persona.
2. Définir le positionnement face à la concurrence.
3. Présenter la vitrine numérique (Page web).
4. Établir une présence sur les plateformes sociales.
5. Poser les bases d’une stratégie de collaborations et de publicités.

Le positionnement marketing de VerifAI repose sur une promesse simple et actionnable : **“vérifier avant de partager”**, soutenue par une expérience fluide, un retour rapide et un score compréhensible généré par notre architecture hybride.

## 1. Analyse Persona des utilisateurs cibles

Afin d’orienter la communication, le développement des fonctionnalités prioritaires et le choix des canaux d’acquisition, nous avons structuré notre ciblage autour de deux segments complémentaires : **B2C** (grand public) et **B2B** (organisations et professionnels de l'information).

### 1.1 Persona B2C — Étudiant universitaire connecté {.unnumbered .unlisted}

**Profil démographique et comportemental**

- Âge : 19 à 25 ans.
- Habitudes numériques : Utilise quotidiennement Instagram, TikTok, X (Twitter) et YouTube.
- Consommation de l'information : Consulte quasi exclusivement l’actualité via les algorithmes de recommandation des réseaux sociaux plutôt que via les médias traditionnels ou la presse écrite.

**Besoins primaires**

- Vérifier rapidement une information ou une rumeur avant de la repartager à son cercle social.
- Comprendre en quelques secondes si un contenu viral semble crédible ou manipulateur.
- Disposer d’un outil simple, pensé pour le mobile (mobile-friendly) et nécessitant zéro friction à l'inscription.

**Points de douleur (Pain points)**

- Surcharge informationnelle constante entraînant une fatigue cognitive.
- Difficulté croissante à distinguer une source fiable d’un contenu généré pour faire du clic (putaclic) ou tromper l'opinion publique.
- Manque de temps et de méthodologie pour faire une vérification manuelle approfondie.

**Valeur apportée par VerifAI et Parcours Utilisateur (Vision en production)**

- **Valeur :** Analyse instantanée d'un texte ou d'un lien avec un verdict clair, accompagné d'un score de confiance. L'interface sera intuitive et adaptée à un usage quotidien compulsif.
- **Parcours type attendu (Phase 2 - Déploiement):** L'étudiant voit un post suspect sur TikTok $\rightarrow$ Il copie le texte $\rightarrow$ Il ouvre l'application web VerifAI sur son téléphone (après déploiement public) $\rightarrow$ Il obtient un diagnostic clair $\rightarrow$ Il décide de ne pas relayer la fausse nouvelle, réduisant ainsi la chaîne de désinformation.

### 1.2 Persona B2B — Responsable communication / Journaliste junior {.unnumbered .unlisted}

**Profil démographique et comportemental**

- Âge : 25 à 40 ans.
- Secteur : Travaille en rédaction, média étudiant, communication institutionnelle, ONG, ou agence de relations publiques.
- Rôle : Publie régulièrement de l’information pour un public large et engage la responsabilité de sa structure. Ce phénomène préoccupe d'ailleurs la grande majorité des journalistes professionnels (42% affirment que le phénomène les préoccupe beaucoup).

**Besoins primaires**

- Obtenir un premier niveau de vérification automatisée avant la validation d'une publication.
- Réduire le temps de pré-validation des contenus (dépêches, communiqués, tweets).
- Appuyer les décisions éditoriales avec des indicateurs compréhensibles pour sa hiérarchie.
- Disposer d’un outil léger, capable de s'intégrer dans un flux de travail (workflow) existant.

**Points de douleur (Pain points)**

- Pression temporelle extrême et volume massif de contenus bruts à traiter lors des "breaking news".
- Risque réputationnel et légal majeur en cas de diffusion d’une information erronée au nom de son organisation.
- Multiplication des sources non vérifiées sur le web.
- Besoin constant de justifier les choix éditoriaux en interne face à des délais très courts.

**Valeur apportée par VerifAI et Parcours Utilisateur (Vision en production)**

- **Valeur :** Outil d'aide à la décision ultra-rapide. Les résultats explicites (générés par le LLM) justifient une vigilance éditoriale accrue. C'est un complément moderne aux processus de fact-checking traditionnels.
- **Parcours type attendu (Phase 3 - Intégrations B2B):** Le journaliste reçoit une alerte suspecte sur X $\rightarrow$ Il soumet le texte à l'API VerifAI via son interface ou son flux de travail existant (après intégration CMS) $\rightarrow$ Le backend basé sur FastAPI analyse le contenu et le LLM retourne une explication détaillée de la classification $\rightarrow$ Le journaliste utilise cette explication pour écarter la dépêche.

### 1.3 Synthèse des personas et alignement stratégique {.unnumbered .unlisted}

L’analyse Persona démontre que VerifAI cible deux marchés distincts mais fondamentalement alignés sur un même besoin de confiance :

1. **B2C :** Les utilisateurs individuels exposés à des contenus viraux, qui veulent vérifier avant de partager. (Proposition de valeur : Simple, rapide, accessible).
2. **B2B :** Les équipes de communication et de publication, qui doivent décider vite tout en réduisant le risque réputationnel. (Proposition de valeur : Fiable, explicable, intégrable).

Les canaux prioritaires découlent directement de cette synthèse : réseaux sociaux visuels pour le B2C, et plateformes professionnelles (LinkedIn, intégrations techniques) pour le B2B. Le ton de communication global de la marque sera pédagogique, concret et orienté sur l'usage.

## 2. Différenciation par rapport à la concurrence

Le marché des outils de vérification d'information est déjà occupé par plusieurs approches : plateformes de fact-checking éditorial, extensions de navigateur, moteurs de recherche enrichis et assistants IA généralistes. VerifAI ne cherche pas à remplacer ces solutions expertes ; son positionnement est celui d'un **outil de pré-vérification rapide**, accessible au quotidien et doté d'une forte dimension éducative.

Notre avantage concurrentiel absolu repose sur trois axes complémentaires visant à obtenir une meilleure performance de détection tout en expliquant le résultat au public.

### 2.1 Explicabilité du résultat (La lutte contre l'effet "Boîte Noire") {.unnumbered .unlisted}

Contrairement à une réponse binaire opaque proposée par de nombreux détecteurs, VerifAI présente un verdict accompagné d'un score de confiance, d'indicateurs lisibles et surtout d'une explication synthétique. Notre projet inclut une méthode automatisée pour expliquer les décisions de classification de l'information.

Cette approche facilite grandement l'appropriation du résultat par des utilisateurs non spécialistes et répond directement aux besoins du Persona B2B, où les décisions de publication doivent pouvoir être justifiées. La valeur marketing est forte : l'utilisateur ne reçoit pas seulement un résultat froid, il comprend **pourquoi** le système algorithmique propose ce résultat, remplissant ainsi notre mission d'éducation de la population.

### 2.2 Simplicité d'usage et architecture optimisée {.unnumbered .unlisted}

La proposition produit est pensée pour réduire au maximum la friction cognitive et technique : coller un texte ou un lien, lancer l'analyse, obtenir une synthèse claire. Notre interface, développée avec Vite, privilégie une lisibilité extrême, un parcours court et des actions immédiates.

Par rapport à des outils d'investigation numérique complets mais très complexes à maîtriser, VerifAI se distingue par une courbe d'apprentissage quasi nulle. Cette simplicité logicielle et visuelle améliore l'adoption, notamment auprès du public étudiant hyper-connecté et des équipes de communication qui travaillent sous contrainte de temps permanente.

### 2.3 Rapidité d'usage (Le premier filtre) {.unnumbered .unlisted}

La rapidité est un avantage concurrentiel décisif dans un contexte de flux informationnel continu et instantané. Grâce à une architecture backend asynchrone performante (FastAPI), VerifAI est conçu pour fournir un premier niveau d'analyse en quelques secondes. 

Cela correspond au moment critique (le "Zero Moment of Truth") où l'utilisateur hésite à partager ou publier un contenu. Cette logique "vite et utile" complète les démarches de vérification approfondie : VerifAI agit comme un premier filtre de sécurité sanitaire de l'information, alors que les solutions expertes (humaines) interviennent ensuite pour l'analyse détaillée.

### 2.4 Positionnement concurrentiel synthétique {.unnumbered .unlisted}

En synthèse, VerifAI se positionne comme une solution de rupture intermédiaire entre les outils grand public souvent trop simplifiés et les approches journalistiques institutionnelles, souvent trop lourdes et lentes.

- **Face aux fact-checkers traditionnels :** VerifAI apporte la rapidité d'un pré-diagnostic algorithmique.
- **Face aux assistants IA généralistes :** VerifAI propose un cadre strictement orienté sur la vérification, avec une restitution structurée et factuelle.
- **Face aux extensions techniques basiques :** VerifAI privilégie une expérience utilisateur claire, directe et, surtout, pédagogique.

Ce positionnement assumé permet de défendre une promesse concrète et hautement différenciante sur le marché : **une vérification explicable, simple et rapide, parfaitement adaptée aux usages réels et frénétiques du partage d'information en ligne.**

## 3. Page web de l'application (Vitrine Numérique) — Prototype & Roadmap

La page web de VerifAI constitue actuellement un prototype fonctionnel local, fondation technique et conceptuelle pour le principal point de contact avec l'utilisateur en production. Dans notre stratégie marketing de lancement, elle jouera un double rôle fondamental : convertir la curiosité initiale en usage réel et installer un sentiment de confiance absolue dès les premières secondes d'interaction.

L'interface prototype est strictement orientée produit. Elle est pensée pour un usage immédiat, caractérisé par un parcours utilisateur ultra-court, une lisibilité élevée et une restitution visuellement compréhensible du verdict de l'intelligence artificielle. Cette fondation sera déployée publiquement lors de la Phase 2.

### 3.1 Identité visuelle et Psychologie du design {.unnumbered .unlisted}

La page introduit une identité visuelle claire et professionnelle (le branding VerifAI), utilisant des codes couleurs (comme le bleu ardoise) qui inspirent naturellement la fiabilité technologique, le sérieux et la cybersécurité.

L'architecture de l'information est hiérarchisée pour éliminer les distractions. L'utilisateur est immédiatement invité à saisir un texte ou une URL dans un champ de saisie central. Une fois l'analyse lancée, le système communique de manière fluide avec l'API backend, et l'utilisateur comprend le verdict sans aucune ambiguïté grâce à une restitution structurée en trois blocs : 

1. Le score de confiance global.
2. Les métriques techniques simplifiées.
3. L'explication textuelle synthétique générée par le modèle.

### 3.2 Alignement avec les objectifs d'acquisition {.unnumbered .unlisted}

Cette page web soutient de manière directe et mesurable nos deux cibles marketing, dès le déploiement public (Phase 2).

- **Côté B2C :** L'absence de création de compte obligatoire pour les premières analyses et la simplicité globale de l'UI réduiront la friction. Cela favorisera un usage spontané, augmentant les chances que l'étudiant revienne utiliser l'outil de manière habituelle.
- **Côté B2B :** La clarté de la restitution, l'apparence professionnelle et l'explication algorithmique faciliteront la prise de décision. Cela améliorera considérablement la crédibilité perçue de l'outil dans un contexte professionnel de publication et d'édition.

En résumé, la page web transformera l'effort technique de VerifAI — du prototype backend actuel — en un véritable produit crédible, commercialisable, compréhensible et parfaitement aligné avec notre promesse marketing : vérifier avant de partager, de façon simple, rapide et explicable.

*(Les captures d'écran ci-dessous illustrent le prototype actuel et serviront de fondation visuelle pour le déploiement public).*

![Prototype - Page d'accueil de VerifAI](homepage.png){height=250px}

![Prototype - Page de résultats de VerifAI](result.png){height=250px}

**Note de déploiement :** Le prototype actuel fonctionne en local (localhost). La Phase 2 inclura le déploiement public sur un domaine VerifAI officiel avec infrastructure cloud, HTTPS, et optimisation mobile.

## 4. Présence sur les plateformes sociales

La présence sociale de VerifAI a pour objectif stratégique de transformer un besoin aujourd'hui diffus et passif ("Je veux éviter de partager de la désinformation") en un réflexe actif et concret d'utilisation du produit. 

Puisque les réseaux sociaux sont paradoxalement les principaux conduits du désordre de l'information, VerifAI doit y être présent pour combattre le feu à sa source. La ligne éditoriale retenue repose sur deux leviers complémentaires : des formats de **démonstration produit** pour prouver la valeur immédiate, et des formats de **vulgarisation** pour remplir notre mission d'éducation à l'information sans complexifier le propos.

### 4.1 Positionnement éditorial et Tonalité {.unnumbered .unlisted}

La communication adopte un ton clair, profondément pédagogique et systématiquement orienté sur l'usage. Le message central qui guide chaque publication reste constant : **"Vérifier avant de partager"**. 

Chaque publication, quel que soit le réseau, doit répondre à une question simple et pragmatique de l'utilisateur : *"Qu'est-ce que VerifAI m'apporte maintenant, en pratique ?"* Cette cohérence cognitive permet de renforcer la mémorisation de la marque à long terme et de créer une continuité parfaite entre le contenu social consommé en scrollant, la page web, et l'expérience produit finale.

### 4.2 Les Formats de Démonstration (Acquisition B2C) {.unnumbered .unlisted}

Les contenus de démonstration ont pour but de montrer l'application en situation réelle, en prouvant que le parcours est extrêmement court, de bout en bout : copie d'un texte suspect, lancement de l'analyse, et lecture du verdict en quelques secondes.

- Vidéos très courtes d'avant/après analyse (Shorts/Reels).
- Captures d'écran commentées montrant l'interface graphique minimaliste et le score de probabilité.
- Mini-cas d'usage intitulés "Vu sur les réseaux", où une rumeur du jour est traitée et débunkée en moins d'une minute d'animation.
- Démonstrations comparatives mettant en parallèle l'analyse d'une information sourcée et fiable face à l'analyse d'une information trompeuse ou générée par IA.

Ces formats dynamiques servent principalement l'acquisition directe de notre cible B2C. Ils rendent la proposition de valeur immédiatement visible et hautement virale.

### 4.3 Les Formats de Vulgarisation (Crédibilité B2B et Éducation) {.unnumbered .unlisted}

La stratégie de vulgarisation complète la démonstration pure en expliquant les bons réflexes informationnels et la mécanique de lecture des résultats algorithmiques. L'objectif n'est pas de transformer les utilisateurs en ingénieurs IA, mais de les rendre critiques et autonomes dans leurs décisions quotidiennes de partage.

- Carrousels éducatifs (format LinkedIn/Instagram) : "Comment repérer un signal faible de désinformation dans un article".
- Infographies "Mythe vs Réalité" sur la fiabilité des différentes sources d'information.
- Capsules vidéo explicatives : "Comment notre IA calcule-t-elle un score de confiance ?" (Transparence).
- Publications pédagogiques liées à l'actualité numérique et à la cybersécurité.

Ces formats de fond favorisent la crédibilité globale de la marque VerifAI. Ils soutiennent particulièrement l'acquisition de la cible B2B, intrinsèquement sensible à la qualité, à la neutralité et à la robustesse du cadre explicatif de l'outil.

### 4.4 Déploiement et Plateformes prioritaires {.unnumbered .unlisted}

Le déploiement social est tactiquement adapté aux lieux de consommation de nos deux segments. 

- **Pour le B2C :** Les plateformes hautement visuelles, algorithmiques et rapides (Instagram, TikTok, X) sont privilégiées, avec une cadence élevée de contenus courts et démonstratifs.
- **Pour le B2B :** LinkedIn, ainsi que les communautés professionnelles ou forums campus, sont nettement plus pertinents. Les contenus y seront plus longs, orientés sur la méthode scientifique, la fiabilité du Deep Learning et les études de cas professionnels.

L'enjeu marketing n'est pas de diluer notre budget en étant présent partout, mais d'être chirurgical et régulier là où nos personas consomment déjà de l'information politique ou sociale.

*(Effet attendu : Augmenter la notoriété spontanée de VerifAI, générer de la confiance envers la startup, et convertir l'attention sociale en visites qualifiées vers l'application web).*

## 5. Stratégie de collaborations et de publicités (Acquisition)

Pour accélérer l'adoption de VerifAI sur le marché, la stratégie de croissance commerciale combine habilement des collaborations organiques très ciblées et des actions publicitaires digitales légères. L'objectif de la startup n'est pas de brûler du capital pour maximiser le volume de trafic à court terme, mais d'obtenir une acquisition d'utilisateurs hautement qualifiée, cohérente avec la promesse technologique du produit : vérifier rapidement, et comprendre clairement un résultat grâce à l'IA.

### 5.1 Collaborations prioritaires (Levier Organique) {.unnumbered .unlisted}

Les collaborations sont pensées et structurées comme des relais de confiance indispensables. Dans sa phase initiale de lancement (Go-To-Market), VerifAI s'appuiera prioritairement sur des partenaires physiquement et socialement proches des personas identifiés : les associations étudiantes, les médias liés aux campus universitaires, les clubs de journalisme, les enseignants impliqués dans l'éducation aux médias, ainsi que les structures locales de communication.

Le principe d'exécution est direct : proposer des démonstrations technologiques concrètes de notre architecture FastAPI/Vite, animer des ateliers courts de sensibilisation à la cyberinfluence et créer des formats de contenu co-brandés. Ce type de partenariat communautaire favorise un bouche-à-oreille extrêmement crédible et permet de tester le produit en boucle de rétroaction rapide (feedback loop) dans des contextes réels d'usage intensif.

### 5.2 Logiques d'activation B2C vs B2B {.unnumbered .unlisted}

- **Logique d'activation B2C (Phase 2 — Déploiement public) :** Les collaborations doivent créer de la proximité émotionnelle et une preuve d'utilité immédiate face à la surcharge des réseaux. Les actions tactiques les plus pertinentes incluent les démonstrations interactives en milieu étudiant (utilisant le prototype ou la version publique), les contenus co-créés avec des créateurs de contenu (influenceurs) orientés sur la vulgarisation scientifique, et le lancement de challenges communautaires autour du mot-dièse "VérifierAvantDePartager".
- **Logique d'activation B2B (Phase 3 — Intégrations et API) :** La priorité absolue est la démonstration de la fiabilité opérationnelle et de la sécurité des données. Les partenariats visent des médias web indépendants, des organismes de sensibilisation à la cybersécurité et des équipes de communication d'entreprise. L'offre de valeur consiste à leur permettre d'intégrer techniquement l'API VerifAI (documentée et sécurisée en Phase 3) comme outil de pré-vérification standardisé, directement connecté dans leur flux de publication ou leur CMS.

### 5.3 Publicité digitale à budget maîtrisé (Levier Payant) {.unnumbered .unlisted}

La publicité payante (Ads) intervient strictement en soutien et en complément des collaborations organiques. Elle se caractérise par un ciblage d'intention extrêmement précis et des budgets maîtrisés, essentiels pour une startup en phase d'amorçage. Les campagnes publicitaires sont principalement orientées vers la diffusion de nos contenus de démonstration (vidéos courtes, captures d'interface commentées, cas d'usage concrets) afin de prouver la valeur de l'outil en moins de cinq secondes.

**Canaux d'acquisition payante retenus :**

- Campagnes vidéos sur **Instagram, TikTok, et X** pour l'acquisition en masse de la cible B2C (étudiants).
- Publications sponsorisées sur **LinkedIn**, ciblant spécifiquement des intitulés de postes (ex: "Rédacteur en chef", "Directeur de la communication") pour la notoriété et la génération de leads qualifiés B2B.
- Campagnes d'intention **Google Ads** (Search), basées sur l'achat de mots-clés liés au doute informationnel (ex: "vérifier rumeur", "fact checking outil"). L'objectif est de capter l'utilisateur au moment même de sa requête avec une redirection immédiate vers la page web pour lui faire tester le produit sans délai.

Le message publicitaire reste invariable d'une plateforme à l'autre : "Vérifier avant de partager", avec une emphase visuelle constante sur l'explicabilité du résultat (l'argument clé face aux modèles concurrents).

### 5.4 Indicateurs de performance marketing (KPIs) {.unnumbered .unlisted}

La rigueur de l'évaluation de nos actions de collaborations et de publicités reposera sur le suivi hebdomadaire d'indicateurs de performance (KPIs) stricts et quantifiables, ajustés par phase :

**Phase 1 (Prototype) — Validation interne :**

- Taux d'essai du prototype local (partenaires, testeurs internes).
- Feedback qualitatif sur la clarté du verdict et l'explication algorithmique.
- Performance technique (temps de réponse, taux d'erreur).

**Phase 2 (Déploiement public) et au-delà :**

- Taux de clic (CTR) sur nos publicités d'intention.
- Coût d'Acquisition Client (CAC) global et segmenté par plateforme.
- Taux d'essai de la plateforme publique (pourcentage de visiteurs lançant au moins une analyse).
- Taux de rétention (part d'utilisateurs revenant utiliser l'outil une seconde fois dans le même mois).
- Retours qualitatifs (Net Promoter Score) des partenaires institutionnels B2B et des utilisateurs B2C.

Cette mesure analytique et continue permettra d'identifier rapidement les canaux les plus rentables et efficaces, et d'ajuster l'allocation budgétaire des actions marketing de manière agile, sans jamais perdre de vue la cohérence globale de notre stratégie produit.

### Synthèse Globale & Phases de déploiement {.unnumbered .unlisted}

La stratégie combinée de collaborations et de publicités de VerifAI privilégie la confiance institutionnelle, la preuve d'usage pragmatique et la régularité d'exposition. Les collaborations organiques apportent la crédibilité nécessaire et un fort ancrage sur le terrain académique et journalistique ; la publicité digitale ciblée apporte, quant à elle, l'amplification nécessaire pour atteindre une masse critique d'utilisateurs.

**Phases de déploiement marketing :**

1. **Phase 1 (Prototype actuel) :** Validation avec testeurs internes, partenaires académiques et journalistiques. Collecte de feedback. Lancement de collaborations communautaires ciblées.
2. **Phase 2 (Déploiement public — Q3-Q4 2026) :** Lancement de la plateforme web publique. Intensification des collaborations B2C. Début des campagnes payantes ciblées (Instagram, TikTok, Google Ads).
3. **Phase 3 (API & Intégrations — 2027) :** Ouverture de l'API documentée et sécurisée. Campagnes B2B (LinkedIn). Partenariats d'intégration CMS avec médias et entreprises.

Ensemble, ces leviers structurent et soutiennent une croissance marketing à la fois progressive, réaliste et financièrement soutenable, parfaitement alignée pour résoudre un enjeu majeur de cybersécurité et de société.