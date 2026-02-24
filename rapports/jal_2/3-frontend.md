# Frontend

## Maquette conceptuelle du produit

Pour notre produit, nous avons cherché à avoir une interface simple et épurée, qui va à l'essentiel. Voici la maquette conceptuelle de notre interface, en deux pages principales, accueil et résultats :

![Maquette conceptuelle de l'accueil de VerifAI](maquette-accueil.png){height=250px}

![Maquette conceptuelle des résultats](maquette-resultats.png){height=250px}

## Stack Frontend

Le frontend a été développé avec **React 19** et **TypeScript**, bundlé via **Vite 7** configuré sur le port `8080`. L'interface utilise **Tailwind CSS v4** pour le style et **shadcn/ui** (style New York) pour les composants de base comme les boutons, les inputs et les textareas. Les icônes proviennent de **Lucide React**.

## Structure

Par souci de simplicité, l'ensemble du code frontend est centralisé dans un seul fichier `src/App.tsx`, sans pages ou composants séparés. Cela facilite la lecture et la maintenance pour un projet de cette taille.

```
src/
|- App.tsx        <- global : types, logique, composants, pages
|- index.css      <- thème + animations
|- assets/
   |- logo.jpg
```

Le fichier `App.tsx` est organisé dans l'ordre suivant :
1. Types TypeScript (`Verdict`, `AnalysisResult`)
2. Fonction `runAnalysis` — appel à l'API backend
3. Configuration des verdicts (FAKE / REAL / UNCERTAIN) avec leurs couleurs et labels
4. Composant `BgDecorations` — décoration de fond partagée entre les deux pages
5. Composant `MetricRow` — barre de progression réutilisable
6. Fonction `HomePage` — page d'accueil
7. Fonction `ResultPage` — page de résultat
8. Export `App` — gestion du routing et de l'état global

## Page d'accueil

La page d'accueil est épurée et centrée. Elle affiche le logo VerifAI avec un effet de glow bleu, un sous-titre, puis une carte principale contenant les éléments de saisie. L'utilisateur peut basculer entre deux modes via des tabs : **URL** pour coller un lien et **Texte** pour coller directement le contenu d'un article. En dessous de la carte, trois statistiques (précision, délai, nombre de sources) donnent de la crédibilité à l'outil. Un lien vers les conditions d'utilisation est placé en pied de page.

![Page d'accueil](accueil.png){height=290px}

## Page de résultat

La page de résultat s'organise en trois zones distinctes. En haut, une **carte verdict pleine largeur** affiche le résultat principal avec une couleur adaptée au verdict (rouge pour FAKE, vert pour REAL, ambre pour UNCERTAIN), le score de confiance en grand et une barre de progression animée.

En dessous, un **layout en deux colonnes** permet de lire les informations en parallèle. La colonne gauche (plus étroite) contient un cercle de score et quatre barres de métriques détaillées. La colonne droite (plus large) affiche l'explication textuelle du résultat ainsi que les sources consultées par le modèle. En bas de page, deux boutons permettent de **sauvegarder** le rapport au format `.txt` ou de **revenir** à l'accueil.

![Page de réponse](reponse.png){height=290px}

## Design

Le design suit l'identité visuelle du logo VerifAI — fond très sombre (`oklch(0.09 0 0)`) et bleu électrique comme couleur primaire (`oklch(0.62 0.19 235)`). Chaque page possède un glow radial en fond dont la couleur change selon le verdict affiché, renforçant visuellement le résultat. Une grille subtile en arrière-plan ajoute de la profondeur sans surcharger l'interface. La police **Inter** est chargée depuis Google Fonts pour une typographie propre et lisible.

## Transitions et chargement

Un soin particulier a été apporté à la fluidité des transitions entre les pages. Au lieu d'attendre la réponse du backend avant de changer de vue — ce qui provoquerait un écran noir ou un blocage visible — le frontend **bascule immédiatement** vers la page de résultat dès que l'utilisateur clique sur Analyser, et affiche un skeleton en attendant la réponse.

```ts
const handleAnalyze = async (input: string) => {
  setResult(null)       // efface le résultat précédent
  setShowResult(true)   // navigue instantanément vers la page résultat
  const data = await runAnalysis(input)
  setResult(data)       // remplit les données quand le backend répond
}
```

Le skeleton comprend un **spinner SVG circulaire animé** à la place du cercle de score, des **barres grises pulsantes** pour les métriques et des **lignes grises de largeurs variées** pour simuler le texte des explications. Dès que la réponse arrive, les données remplacent le skeleton sans transition brusque.

## Liaison Frontend/Backend

### Configuration du port — `vite.config.ts`

Vite est configuré pour démarrer sur le port `8080`, qui est déjà autorisé dans les origines CORS du backend — aucune modification côté backend n'est donc nécessaire pour le CORS.

```ts
server: {
  port: 8080,
}
```

### CORS — `backend/app/main.py`

Le port `8080` étant déjà présent dans la liste des origines autorisées, aucune modification n'a été nécessaire de ce côté.

```python
origins = [
    "http://localhost",
    "http://localhost:8080",  # déjà présent
]
```

### Limite de taille du texte — `backend/app/api/models.py`

La contrainte `max_length` devra être augmentée de 500 à 5000 caractères pour permettre l'analyse d'articles complets, car les textes réels dépassent facilement 500 caractères.

```python
# Avant
text: str = Field(..., min_length=50, max_length=500)

# Après
text: str = Field(..., min_length=50, max_length=5000)
```

### Fonction `runAnalysis` — `App.tsx`

La fonction `runAnalysis` est le point de jonction entre le frontend et le backend. Elle envoie le texte en POST sur `/ai/check-text`, récupère le verdict et le score, puis construit l'objet `AnalysisResult` attendu par la page de résultat. Le score retourné par le backend est une chaîne du type `"87.43%"` — le `replace("%", "")` est nécessaire avant le `parseFloat` pour éviter un `NaN`.

```ts
async function runAnalysis(input: string): Promise<AnalysisResult> {
  const res = await fetch("http://localhost:8000/ai/check-text", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: input }),
  })
  if (!res.ok) throw new Error(`Erreur ${res.status}`)
  const { result } = await res.json()
  const confidence = Math.round(parseFloat(result.score.replace("%", "")))
  const verdict: Verdict = result.prediction === "FAKE" ? "FAKE" : "REAL"
  return {
    verdict,
    confidence,
    inputPreview: input.length > 100 ? input.slice(0, 100) + "…" : input,
    isUrl: input.startsWith("http"),
    metrics: {
      sourceCredibility: verdict === "FAKE" ? 21 : 87,
      factualAccuracy:   confidence,
      linguisticBias:    verdict === "FAKE" ? 14 : 83,
      crossVerification: verdict === "FAKE" ? 11 : 78,
    },
    explanation: verdict === "FAKE"
      ? "Le modèle a détecté des signaux de désinformation."
      : "Aucun signal de désinformation détecté.",
    sources: ["hamzab/roberta-fake-news-classification"],
  }
}
```

## Limitations

Plusieurs limitations ont été identifiées au cours du développement.

Le **mode URL** ne fonctionne pas comme attendu : le frontend envoie l'URL comme une chaîne de texte brute, sans en extraire le contenu. Le modèle reçoit donc l'URL elle-même à analyser, ce qui produit des résultats incohérents. Pour corriger cela, il faudrait ajouter un mécanisme de scraping côté backend (par exemple avec `beautifulsoup4`) pour récupérer le contenu de la page avant de l'envoyer au modèle.

Les **métriques détaillées** sont en partie statiques. Le backend ne retournant qu'un score global et un label, les valeurs de crédibilité de source, neutralité linguistique et vérification croisée sont calculées à partir de valeurs fixes selon le verdict. Seule l'exactitude factuelle reflète le vrai score du modèle.

La contrainte **`min_length=50`** côté backend peut surprendre l'utilisateur si son texte est trop court — une validation côté frontend avant l'envoi éviterait une erreur 422 silencieuse.

Enfin, le modèle HuggingFace peut mettre **10 à 30 secondes** à répondre lors de la première requête après une période d'inactivité (cold start), ce qui peut donner l'impression que l'application est bloquée.
