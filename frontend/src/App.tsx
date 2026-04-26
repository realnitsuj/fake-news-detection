import { useState, useCallback, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import {
  ArrowRight, Link2, FileText, Loader2,
  Download, RotateCcw, CheckCircle2, XCircle, AlertTriangle,
  ExternalLink, UploadCloud
} from "lucide-react"
import logo from "@/assets/logo.jpg"

// ─────────────────────────────────────────────────────────────────────────────
// Types
// ─────────────────────────────────────────────────────────────────────────────

type Verdict = "FAKE" | "REAL" | "UNCERTAIN"

interface AnalysisResult {
  verdict: Verdict
  confidence: number
  inputPreview: string
  isUrl: boolean
  explanation: string
  sources: string[]
}

// ─────────────────────────────────────────────────────────────────────────────────────────────

async function runAnalysis(input: string | File): Promise<AnalysisResult> {
  let res;
  
  if (input instanceof File) {
    const formData = new FormData()
    formData.append("file", input)
    res = await fetch("http://localhost:8000/ai/check-file", {
      method: "POST",
      body: formData,
    })
  } else {
    res = await fetch("http://localhost:8000/ai/check-text", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: input }),
    })
  }

  const data = await res.json()
  const result = (data.result ?? data) as any

  if (result.status === "error") {
    throw new Error(result.message || "Erreur d'analyse API")
  }

  const rawScoreValue = result.score ?? result.confiance
  if (rawScoreValue === undefined) {
    throw new Error("Réponse API invalide : score/confiance manquant")
  }

  const rawScore = typeof rawScoreValue === "number" ? rawScoreValue : String(rawScoreValue)
  const confidence = Math.round(parseFloat(rawScore.toString().replace("%", "")))

  const rawVerdict = (result.prediction ?? result.verdict ?? "UNCERTAIN").toUpperCase()
  
  let verdict: Verdict = "UNCERTAIN"
  if (rawVerdict === "FAKE" || rawVerdict === "FAUX") {
    verdict = "FAKE"
  } else if (rawVerdict === "REAL" || rawVerdict === "VRAI") {
    verdict = "REAL"
  }

  return {
    verdict,
    confidence,
    inputPreview: input instanceof File ? `Fichier : ${input.name}` : (input.length > 100 ? input.slice(0, 100) + "…" : input),
    isUrl: typeof input === "string" && input.startsWith("http"),
    explanation: result.justification
      ? `${result.justification}${result.categorie ? ` (Catégorie: ${result.categorie})` : ''}`
      : (verdict === "FAKE"
        ? "Le modèle a détecté des signaux de désinformation."
        : "Aucun signal de désinformation détecté."),
    sources: result.sources ?? ["hamzab/roberta-fake-news-classification"],
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// Verdict config
// ─────────────────────────────────────────────────────────────────────────────

const VERDICTS = {
  FAKE: {
    label: "Fake news",
    sub: "Signaux de désinformation détectés",
    Icon: XCircle,
    color: "text-red-400",
    glow: "oklch(0.65 0.22 25 / 20%)",
    bar: "bg-red-500",
    bg: "bg-red-500/8",
    border: "border-red-500/20",
    dot: "bg-red-400",
  },
  REAL: {
    label: "Information fiable",
    sub: "Aucun signal de désinformation",
    Icon: CheckCircle2,
    color: "text-emerald-400",
    glow: "oklch(0.7 0.15 160 / 20%)",
    bar: "bg-emerald-500",
    bg: "bg-emerald-500/8",
    border: "border-emerald-500/20",
    dot: "bg-emerald-400",
  },
  UNCERTAIN: {
    label: "Résultat incertain",
    sub: "Vérification complémentaire recommandée",
    Icon: AlertTriangle,
    color: "text-amber-400",
    glow: "oklch(0.8 0.17 80 / 20%)",
    bar: "bg-amber-500",
    bg: "bg-amber-500/8",
    border: "border-amber-500/20",
    dot: "bg-amber-400",
  },
} as const


// ─────────────────────────────────────────────────────────────────────────────
// Shared background decorations
// ─────────────────────────────────────────────────────────────────────────────

function BgDecorations({ glow }: { glow?: string }) {
  return (
    <>
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 -z-10 transition-all duration-700"
        style={{
          background: glow
            ? `radial-gradient(ellipse 55% 40% at 50% 0%, ${glow} 0%, transparent 70%)`
            : "radial-gradient(ellipse 60% 50% at 50% 40%, oklch(0.62 0.19 235 / 7%) 0%, transparent 70%)",
        }}
      />
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 -z-10 opacity-[0.028]"
        style={{
          backgroundImage:
            "linear-gradient(oklch(1 0 0) 1px, transparent 1px), linear-gradient(90deg, oklch(1 0 0) 1px, transparent 1px)",
          backgroundSize: "40px 40px",
        }}
      />
    </>
  )
}


// ─────────────────────────────────────────────────────────────────────────────
// HomePage
// ─────────────────────────────────────────────────────────────────────────────

function HomePage({ onAnalyze, onOpenTerms }: { onAnalyze: (v: string | File) => void; onOpenTerms: () => void}) {
  const [mode, setMode] = useState<"url" | "texte" | "fichier">("url")
  const [value, setValue] = useState("")
  const [file, setFile] = useState<File | null>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  const handleSubmit = () => {
    if (mode === "fichier" && file) onAnalyze(file)
    else if (value.trim()) onAnalyze(value.trim())
  }
  
  const handleKey = (e: React.KeyboardEvent) => { 
    if (e.key === "Enter" && !e.shiftKey) { 
      e.preventDefault(); 
      handleSubmit() 
    } 
  }

  const isSubmitDisabled = mode === "fichier" ? !file : !value.trim()

  return (
    <div className="relative flex min-h-svh flex-col items-center justify-center p-6 overflow-hidden animate-page-in">
      <BgDecorations />

      <main className="flex w-full max-w-md flex-col items-center gap-8">
        {/* Logo */}
        <div className="animate-fade-up flex flex-col items-center gap-3">
          <img
            src={logo}
            alt="VerifAI"
            className="h-20 w-auto drop-shadow-[0_0_28px_oklch(0.62_0.19_235_/_35%)]"
          />
          <p className="text-sm text-muted-foreground tracking-wide">Détection de désinformation par IA</p>
        </div>

        {/* Card */}
        <div
          className="animate-fade-up delay-100 w-full rounded-2xl border border-border bg-card p-6 space-y-5"
          style={{ boxShadow: "0 0 0 1px oklch(1 0 0 / 6%), 0 24px 48px -12px oklch(0 0 0 / 60%)" }}
        >
          {/* Tabs */}
          <div className="flex w-full gap-2 rounded-xl bg-secondary/60 p-1">
            {(["url", "texte", "fichier"] as const).map(m => (
              <button
                key={m}
                onClick={() => { setMode(m); setValue(""); setFile(null) }}
                className={`flex flex-1 items-center justify-center gap-2 rounded-lg py-2 text-sm font-medium transition-all duration-200
                  ${mode === m ? "bg-primary text-primary-foreground shadow-sm" : "text-muted-foreground hover:text-foreground"}`}
              >
                {m === "url" ? <><Link2 className="size-3.5" />URL</> : m === "texte" ? <><FileText className="size-3.5" />Texte</> : <><UploadCloud className="size-3.5" />Fichier</>}
              </button>
            ))}
          </div>

          {/* Input area */}
          <div className="space-y-3">
            {mode === "url" ? (
              <Input
                ref={inputRef}
                type="url"
                value={value}
                onChange={e => setValue(e.target.value)}
                onKeyDown={handleKey}
                placeholder="https://exemple.com/article…"
                className="h-11 rounded-xl border-border bg-input/40 text-sm placeholder:text-muted-foreground/60 focus-visible:ring-primary/40 focus-visible:border-primary/60 transition-all"
              />
            ) : mode === "texte" ? (
              <Textarea
                value={value}
                onChange={e => setValue(e.target.value)}
                onKeyDown={handleKey}
                placeholder="Collez le texte de l'article à vérifier…"
                rows={5}
                className="rounded-xl border-border bg-input/40 text-sm placeholder:text-muted-foreground/60 focus-visible:ring-primary/40 focus-visible:border-primary/60 resize-none transition-all"
              />
            ) : (
              <Input
                type="file"
                accept=".txt,.pdf"
                onChange={e => setFile(e.target.files?.[0] || null)}
                className="h-11 pt-2.5 rounded-xl border-border bg-input/40 text-sm file:mr-4 file:py-1 file:px-3 file:rounded-full file:border-0 file:text-xs file:font-semibold file:bg-primary/10 file:text-primary hover:file:bg-primary/20 cursor-pointer transition-all"
              />
            )}

            <Button
              onClick={handleSubmit}
              disabled={isSubmitDisabled}
              className="w-full h-11 rounded-xl bg-primary hover:bg-primary/90 text-primary-foreground font-semibold gap-2 transition-all duration-200 disabled:opacity-40 shadow-[0_0_20px_oklch(0.62_0.19_235_/_25%)] hover:shadow-[0_0_28px_oklch(0.62_0.19_235_/_40%)]"
            >
              <>Analyser<ArrowRight className="size-4" /></>
            </Button>
          </div>

        </div>

      </main>

      <footer className="absolute bottom-5 text-xs text-muted-foreground/60">
        <button 
            onClick={onOpenTerms} 
            className="hover:text-muted-foreground transition-colors underline-offset-4 hover:underline"
          >
            Conditions d'utilisation
          </button>
        </footer>

    </div>
  )
}

// --------------------------------------------------------------------------------
// Terms
// --------------------------------------------------------------------------------
function TermsModal({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-background/80 backdrop-blur-sm animate-in fade-in duration-200">
      <div 
        className="relative w-full max-w-lg max-h-[80vh] overflow-y-auto rounded-2xl border border-border bg-card p-8 shadow-2xl animate-in zoom-in-95 duration-200"
      >
        <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
          <AlertTriangle className="size-5 text-amber-400" />
          Conditions d'utilisation
        </h2>
        
        <div className="space-y-4 text-sm text-muted-foreground leading-relaxed">
          <section>
            <h3 className="font-semibold text-foreground">1. Objectif du service</h3>
            <p>VerifAI est un outil expérimental développé dans le cadre du module Cybersécurité II. Il utilise une intelligence artificielle pour aider à identifier des signaux de désinformation potentiels.</p>
          </section>

          <section>
            <h3 className="font-semibold text-foreground">2. Absence de garantie</h3>
            <p>L'analyse fournie est purement indicative. L'IA peut produire des résultats erronés ("hallucinations"). Ce service ne remplace en aucun cas un jugement critique ou une vérification par des journalistes professionnels.</p>
          </section>

          <section>
            <h3 className="font-semibold text-foreground">3. Protection des données</h3>
            <p>Conformément au principe de confidentialité, aucun texte, URL ou fichier soumis n'est conservé de manière persistante sur nos serveurs après la fin de l'analyse en cours.</p>
          </section>

          <section>
            <h3 className="font-semibold text-foreground">4. Responsabilité</h3>
            <p>Les auteurs du projet déclinent toute responsabilité quant à l'utilisation des résultats fournis par l'application ou aux conséquences d'une mauvaise interprétation des verdicts rendus.</p>
          </section>
        </div>

        <Button onClick={onClose} className="w-full mt-8 rounded-xl">
          J'ai compris
        </Button>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// ResultPage
// ─────────────────────────────────────────────────────────────────────────────

function ResultPage({ result, onClear, leaving, error, onOpenTerms }: { result: AnalysisResult | null; onClear: () => void; leaving: boolean; error?: string | null; onOpenTerms: () => void}) {
  const isLoading = result === null && !error
  const cfg = isLoading || error ? VERDICTS.UNCERTAIN : VERDICTS[result!.verdict]
  const { Icon } = cfg

  const handleSave = () => {
    if (!result) return
    const lines = [
      "VerifAI — Rapport d'analyse", "═".repeat(36),
      `Verdict   : ${cfg.label}`, `Confiance : ${result.confidence}%`, "",
      `Entrée    : ${result.inputPreview}`, "",
      "EXPLICATION", result.explanation, "",
      "SOURCES", ...result.sources.map(s => `  · ${s}`),
    ]
    const a = document.createElement("a")
    a.href = URL.createObjectURL(new Blob([lines.join("\n")], { type: "text/plain" }))
    a.download = "verifai-rapport.txt"; a.click()
  }

  if (error) {
    return (
      <div className={`relative min-h-svh flex flex-col items-center justify-center p-6 overflow-hidden ${leaving ? "animate-page-out" : "animate-page-in"}`}>
        <BgDecorations glow="oklch(0.65 0.22 25 / 20%)" />
        <div className="w-full max-w-md rounded-2xl border border-red-500/20 bg-red-500/10 p-6 text-center space-y-4 shadow-[0_0_40px_-10px_oklch(0.65_0.22_25_/_20%)]">
          <XCircle className="size-10 text-red-400 mx-auto" />
          <div>
            <h2 className="text-lg font-bold text-red-400">Analyse impossible</h2>
            <p className="text-sm text-foreground/80 mt-1">{error}</p>
          </div>
          <Button onClick={onClear} className="w-full h-11 rounded-xl bg-card border border-border hover:bg-secondary transition-all">
            Réessayer
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div className={`relative min-h-svh flex flex-col overflow-hidden ${leaving ? "animate-page-out" : "animate-page-in"}`}>
      <BgDecorations glow={cfg.glow} />

      {/* Header */}
      <header className="animate-fade-in sticky top-0 z-10 border-b border-border/60 bg-background/80 backdrop-blur-md">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-5 py-3">
          <img src={logo} alt="VerifAI" className="h-8 w-auto" />
          <button onClick={onClear} className="flex items-center gap-2 rounded-lg border border-white/20 bg-white/10 px-3 py-1.5 text-xs font-medium text-white hover:bg-white/20 transition-all duration-200">
            <RotateCcw className="size-3.5" />Nouvelle analyse
          </button>
        </div>
      </header>

      {/* Content */}
      <main className="flex-1 overflow-y-auto">
        <div className="mx-auto max-w-5xl px-5 py-8 space-y-4">

          {/* Input preview */}
          {result && (
            <div className="animate-fade-up flex items-center gap-2 text-xs text-muted-foreground">
              {result.isUrl ? <ExternalLink className="size-3 shrink-0" /> : <FileText className="size-3 shrink-0" />}
              <span className="truncate">{result.inputPreview}</span>
            </div>
          )}

          {/* Verdict card — full width */}
          <div
            className={`animate-fade-up delay-100 rounded-2xl border p-5 ${isLoading ? "bg-secondary/30 border-border" : `${cfg.bg} ${cfg.border}`}`}
            style={{ boxShadow: isLoading ? "none" : `0 0 40px -10px ${cfg.glow}` }}
          >
            {isLoading ? (
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-3 flex-1">
                  <div className="rounded-full p-2 bg-secondary border border-border">
                    <Loader2 className="size-5 text-muted-foreground animate-spin" />
                  </div>
                  <div className="space-y-2">
                    <div className="h-4 w-32 rounded-md bg-secondary animate-pulse" />
                    <div className="h-3 w-48 rounded-md bg-secondary/60 animate-pulse" />
                  </div>
                </div>
                <div className="text-right">
                  <div className="h-10 w-16 rounded-md bg-secondary animate-pulse ml-auto" />
                  <div className="h-3 w-20 rounded-md bg-secondary/60 animate-pulse mt-1 ml-auto" />
                </div>
              </div>
            ) : (
              <>
                <div className="flex items-start gap-4">
                  <div className="flex items-start gap-3">
                    <div className={`mt-0.5 rounded-full p-2 bg-card border ${cfg.border}`}>
                      <Icon className={`size-5 ${cfg.color}`} />
                    </div>
                    <div>
                      <p className={`font-bold text-xl leading-tight ${cfg.color}`}>{cfg.label}</p>
                      <p className="text-xs text-muted-foreground mt-0.5">{cfg.sub}</p>
                    </div>
                  </div>
                </div>
              </>
            )}
          </div>

          {/* ── Two-column layout ── */}
          <div className="animate-fade-up delay-200 grid grid-cols-1 lg:grid-cols-[2fr_3fr] gap-4 items-stretch">

            {/* LEFT — Score + Métriques */}
            <div
              className="rounded-2xl border border-border bg-card p-5 space-y-5 flex flex-col"
              style={{ boxShadow: "0 0 0 1px oklch(1 0 0 / 4%), 0 8px 32px -8px oklch(0 0 0 / 40%)" }}
            >
              {/* Score circle */}
              <div className="flex flex-col items-center gap-2 py-3">
                {isLoading ? (
                  <div className="relative flex items-center justify-center w-28 h-28">
                    <svg className="absolute inset-0 w-full h-full -rotate-90" viewBox="0 0 100 100">
                      <circle cx="50" cy="50" r="44" fill="none" stroke="oklch(1 0 0 / 8%)" strokeWidth="6" />
                      <circle cx="50" cy="50" r="44" fill="none" stroke="oklch(0.62 0.19 235)" strokeWidth="6"
                        strokeDasharray="276" strokeDashoffset="276"
                        style={{ animation: "dash-spin 1.4s ease-in-out infinite" }}
                      />
                    </svg>
                    <Loader2 className="size-7 text-primary animate-spin" />
                  </div>
                ) : (
                  <div className="relative flex items-center justify-center w-28 h-28">
                    <svg className="absolute inset-0 w-full h-full -rotate-90" viewBox="0 0 100 100">
                      <circle cx="50" cy="50" r="44" fill="none" stroke="oklch(1 0 0 / 8%)" strokeWidth="6" />
                      <circle 
                        cx="50" 
                        cy="50" 
                        r="44" 
                        fill="none" 
                        stroke={cfg.color === "text-red-400" ? "rgb(248 113 113)" : cfg.color === "text-emerald-400" ? "rgb(52 211 153)" : "rgb(251 191 36)"}
                        strokeWidth="6"
                        strokeDasharray="276"
                        strokeDashoffset={276 * (1 - result!.confidence / 100)}
                        style={{ transition: "stroke-dashoffset 0.6s ease-in-out" }}
                      />
                    </svg>
                    <div className="text-center">
                      <p className={`text-3xl font-black tabular-nums leading-none ${cfg.color}`}>{result!.confidence}</p>
                    </div>
                  </div>
                )}
                <p className="text-xs text-muted-foreground">Score de confiance</p>
              </div>

              
            </div>

            {/* RIGHT — Explications */}
            <div
              className="rounded-2xl border border-border bg-card p-6 flex flex-col gap-4"
              style={{ boxShadow: "0 0 0 1px oklch(1 0 0 / 4%), 0 8px 32px -8px oklch(0 0 0 / 40%)" }}
            >
              <h2 className="text-xs font-semibold uppercase tracking-widest text-muted-foreground">Explications</h2>
              {isLoading ? (
                <div className="space-y-2 flex-1">
                  {[100, 90, 95, 70, 85].map((w, i) => (
                    <div key={i} className="h-3.5 rounded bg-secondary animate-pulse" style={{ width: `${w}%`, animationDelay: `${i * 80}ms` }} />
                  ))}
                </div>
              ) : (
                <>
                  <p className="text-sm text-foreground/80 leading-relaxed flex-1">{result!.explanation}</p>
                </>
              )}
            </div>
          </div>

          {/* Actions */}
          <div className="animate-fade-up delay-400 flex gap-3 pb-8">
            <Button
              onClick={handleSave}
              variant="outline"
              className="flex-1 h-11 rounded-xl border-border/60 bg-card text-sm font-medium gap-2 hover:bg-secondary hover:border-border transition-all"
            >
              <Download className="size-4" />Sauvegarder
            </Button>
            <Button
              onClick={onClear}
              className="flex-1 h-11 rounded-xl bg-primary hover:bg-primary/90 text-primary-foreground text-sm font-semibold gap-2 transition-all shadow-[0_0_20px_oklch(0.62_0.19_235_/_20%)] hover:shadow-[0_0_28px_oklch(0.62_0.19_235_/_35%)]"
            >
              <RotateCcw className="size-4" />Clear
            </Button>
          </div>
        </div>
      </main>

      <style>{`@keyframes dash-spin { 0% { stroke-dashoffset: 276; } 60% { stroke-dashoffset: 0; } 100% { stroke-dashoffset: -276; } }`}</style>
      <footer className="border-t border-border/40 py-4 text-center text-xs text-muted-foreground/50">
        <button 
            onClick={onOpenTerms} 
            className="hover:text-muted-foreground transition-colors underline-offset-4 hover:underline"
        >
            Conditions d'utilisation
        </button>
      </footer>
    </div>
  )
}

// ─────────────────────────────────────────────────────────────────────────────
// App — routing + state
// ─────────────────────────────────────────────────────────────────────────────

export default function App() {
  const [showResult, setShowResult] = useState(false)
  const [result, setResult]         = useState<AnalysisResult | null>(null)
  const [error, setError]           = useState<string | null>(null)
  const [leaving, setLeaving]       = useState(false)
  const [isTermsOpen, setIsTermsOpen] = useState(false)

  const handleAnalyze = useCallback(async (input: string | File) => {
    setResult(null)
    setError(null)
    setShowResult(true)
    
    try {
      const data = await runAnalysis(input)
      setResult(data)
    } catch (e: any) {
      setError(e.message)
    }
  }, [])

  const handleClear = useCallback(() => {
    setLeaving(true)
    setTimeout(() => { 
      setResult(null)
      setError(null)
      setShowResult(false)
      setLeaving(false) 
    }, 280)
  }, [])

  
  return (
    <>
      <TermsModal isOpen={isTermsOpen} onClose={() => setIsTermsOpen(false)} />
      
      {showResult ? (
        <ResultPage 
          result={result} 
          error={error} 
          onClear={handleClear} 
          leaving={leaving} 
          onOpenTerms={() => setIsTermsOpen(true)}
        />
      ) : (
        <HomePage 
          onAnalyze={handleAnalyze} 
          onOpenTerms={() => setIsTermsOpen(true)}
        />
      )}
    </>
  )
}
