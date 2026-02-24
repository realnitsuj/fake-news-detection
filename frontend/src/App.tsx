import { useState, useCallback, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import {
  ArrowRight, Link2, FileText, Loader2,
  Download, RotateCcw, CheckCircle2, XCircle, AlertTriangle,
  ExternalLink,
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
  metrics: {
    sourceCredibility: number
    factualAccuracy: number
    linguisticBias: number
    crossVerification: number
  }
  explanation: string
  sources: string[]
}

// ─────────────────────────────────────────────────────────────────────────────
// Mock IA — remplacer par le vrai endpoint
// ─────────────────────────────────────────────────────────────────────────────

async function runAnalysis(input: string): Promise<AnalysisResult> {
  const res = await fetch("http://localhost:8000/ai/check-text", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: input }),
  })
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
      factualAccuracy: confidence,
      linguisticBias: verdict === "FAKE" ? 14 : 83,
      crossVerification: verdict === "FAKE" ? 11 : 78,
    },
    explanation: verdict === "FAKE"
      ? "Le modèle a détecté des signaux de désinformation."
      : "Aucun signal de désinformation détecté.",
    sources: ["hamzab/roberta-fake-news-classification"],
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

const METRIC_LABELS: Record<string, string> = {
  sourceCredibility: "Crédibilité de la source",
  factualAccuracy:   "Exactitude factuelle",
  linguisticBias:    "Neutralité linguistique",
  crossVerification: "Vérification croisée",
}

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
// MetricRow
// ─────────────────────────────────────────────────────────────────────────────

function MetricRow({ label, value, bar, delay }: { label: string; value: number; bar: string; delay: string }) {
  return (
    <div className={`space-y-1.5 animate-fade-up ${delay}`}>
      <div className="flex justify-between text-xs">
        <span className="text-muted-foreground">{label}</span>
        <span className="font-semibold tabular-nums text-foreground">{value}%</span>
      </div>
      <div className="h-1 w-full rounded-full bg-secondary overflow-hidden">
        <div className={`h-full rounded-full ${bar} animate-bar-grow ${delay}`} style={{ width: `${value}%` }} />
      </div>
    </div>
  )
}

// ─────────────────────────────────────────────────────────────────────────────
// HomePage
// ─────────────────────────────────────────────────────────────────────────────

function HomePage({ onAnalyze }: { onAnalyze: (v: string) => void }) {
  const [mode, setMode] = useState<"url" | "texte">("url")
  const [value, setValue] = useState("")
  const inputRef = useRef<HTMLInputElement>(null)

  const handleSubmit = () => { if (value.trim()) onAnalyze(value.trim()) }
  const handleKey = (e: React.KeyboardEvent) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); handleSubmit() } }

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
            {(["url", "texte"] as const).map(m => (
              <button
                key={m}
                onClick={() => { setMode(m); setValue("") }}
                className={`flex flex-1 items-center justify-center gap-2 rounded-lg py-2 text-sm font-medium transition-all duration-200
                  ${mode === m ? "bg-primary text-primary-foreground shadow-sm" : "text-muted-foreground hover:text-foreground"}`}
              >
                {m === "url" ? <><Link2 className="size-3.5" />URL</> : <><FileText className="size-3.5" />Texte</>}
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
            ) : (
              <Textarea
                value={value}
                onChange={e => setValue(e.target.value)}
                onKeyDown={handleKey}
                placeholder="Collez le texte de l'article à vérifier…"
                rows={5}
                className="rounded-xl border-border bg-input/40 text-sm placeholder:text-muted-foreground/60 focus-visible:ring-primary/40 focus-visible:border-primary/60 resize-none transition-all"
              />
            )}

            <Button
              onClick={handleSubmit}
              disabled={!value.trim()}
              className="w-full h-11 rounded-xl bg-primary hover:bg-primary/90 text-primary-foreground font-semibold gap-2 transition-all duration-200 disabled:opacity-40 shadow-[0_0_20px_oklch(0.62_0.19_235_/_25%)] hover:shadow-[0_0_28px_oklch(0.62_0.19_235_/_40%)]"
            >
              <>Analyser<ArrowRight className="size-4" /></>
            </Button>
          </div>

        </div>

        {/* Stats */}
        <div className="animate-fade-up delay-200 flex items-center gap-6 text-xs text-muted-foreground">
          {[{ val: "94%", label: "Précision" }, { val: "< 3s", label: "Délai" }, { val: "12k+", label: "Sources" }].map(s => (
            <div key={s.label} className="flex flex-col items-center gap-0.5">
              <span className="text-base font-bold text-foreground">{s.val}</span>
              <span>{s.label}</span>
            </div>
          ))}
        </div>
      </main>

      <footer className="absolute bottom-5 text-xs text-muted-foreground/60">
        <a href="#" className="hover:text-muted-foreground transition-colors underline-offset-4 hover:underline">Conditions d'utilisation</a>
      </footer>

    </div>
  )
}

// ─────────────────────────────────────────────────────────────────────────────
// ResultPage
// ─────────────────────────────────────────────────────────────────────────────

function ResultPage({ result, onClear, leaving }: { result: AnalysisResult | null; onClear: () => void; leaving: boolean }) {
  const isLoading = result === null
  const cfg = isLoading ? VERDICTS.UNCERTAIN : VERDICTS[result.verdict]
  const { Icon } = cfg

  const handleSave = () => {
    if (!result) return
    const lines = [
      "VerifAI — Rapport d'analyse", "═".repeat(36),
      `Verdict   : ${cfg.label}`, `Confiance : ${result.confidence}%`, "",
      `Entrée    : ${result.inputPreview}`, "",
      "MÉTRIQUES", ...Object.entries(result.metrics).map(([k, v]) => `  ${METRIC_LABELS[k]}: ${v}%`), "",
      "EXPLICATION", result.explanation, "",
      "SOURCES", ...result.sources.map(s => `  · ${s}`),
    ]
    const a = document.createElement("a")
    a.href = URL.createObjectURL(new Blob([lines.join("\n")], { type: "text/plain" }))
    a.download = "verifai-rapport.txt"; a.click()
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
                <div className="flex items-start justify-between gap-4">
                  <div className="flex items-start gap-3">
                    <div className={`mt-0.5 rounded-full p-2 bg-card border ${cfg.border}`}>
                      <Icon className={`size-5 ${cfg.color}`} />
                    </div>
                    <div>
                      <p className={`font-bold text-xl leading-tight ${cfg.color}`}>{cfg.label}</p>
                      <p className="text-xs text-muted-foreground mt-0.5">{cfg.sub}</p>
                    </div>
                  </div>
                  <div className="text-right shrink-0">
                    <p className={`text-4xl font-black tabular-nums leading-none ${cfg.color}`}>
                      {result!.confidence}<span className="text-xl font-semibold">%</span>
                    </p>
                    <p className="text-xs text-muted-foreground mt-1">de confiance</p>
                  </div>
                </div>
                <div className="mt-5 h-1.5 w-full rounded-full bg-black/20 overflow-hidden">
                  <div className={`h-full rounded-full ${cfg.bar} animate-bar-grow delay-200`} style={{ width: `${result!.confidence}%` }} />
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
                  <div
                    className={`relative flex items-center justify-center rounded-full w-28 h-28 border-4 ${cfg.border}`}
                    style={{ boxShadow: `0 0 32px -4px ${cfg.glow}` }}
                  >
                    <div className="text-center">
                      <p className={`text-3xl font-black tabular-nums leading-none ${cfg.color}`}>{result!.confidence}</p>
                      <p className={`text-sm font-semibold ${cfg.color}`}>%</p>
                    </div>
                  </div>
                )}
                <p className="text-xs text-muted-foreground">Score de confiance</p>
              </div>

              <div className="h-px bg-border/60" />

              {/* Métriques */}
              <div className="space-y-3 flex-1">
                <h2 className="text-xs font-semibold uppercase tracking-widest text-muted-foreground">Métriques</h2>
                {isLoading ? (
                  <div className="space-y-4">
                    {[80, 60, 70, 50].map((w, i) => (
                      <div key={i} className="space-y-1.5">
                        <div className="flex justify-between">
                          <div className="h-3 rounded bg-secondary animate-pulse" style={{ width: `${w}%` }} />
                          <div className="h-3 w-8 rounded bg-secondary animate-pulse" />
                        </div>
                        <div className="h-1 w-full rounded-full bg-secondary overflow-hidden">
                          <div className="h-full rounded-full bg-secondary/80 animate-pulse" style={{ width: "60%" }} />
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="space-y-3">
                    {Object.entries(result!.metrics).map(([key, val], i) => (
                      <MetricRow key={key} label={METRIC_LABELS[key]} value={val} bar={cfg.bar} delay={`delay-${250 + i * 50}`} />
                    ))}
                  </div>
                )}
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
                  {result!.sources.length > 0 && (
                    <div className="pt-4 border-t border-border space-y-2">
                      <p className="text-xs font-medium text-muted-foreground/70 uppercase tracking-wider">Sources consultées</p>
                      <ul className="space-y-1.5">
                        {result!.sources.map((s, i) => (
                          <li key={i} className="flex items-center gap-2 text-xs text-muted-foreground">
                            <span className={`size-1.5 rounded-full shrink-0 ${cfg.dot}`} />{s}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
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
        <a href="#" className="hover:text-muted-foreground transition-colors underline-offset-4 hover:underline">Conditions d'utilisation</a>
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
  const [leaving, setLeaving]       = useState(false)

  const handleAnalyze = useCallback(async (input: string) => {
    setResult(null)       // clear previous
    setShowResult(true)   // navigate instantly — skeleton shown
    const data = await runAnalysis(input)
    setResult(data)       // fill in results
  }, [])

  const handleClear = useCallback(() => {
    setLeaving(true)
    setTimeout(() => { setResult(null); setShowResult(false); setLeaving(false) }, 280)
  }, [])

  if (showResult) {
    return <ResultPage result={result} onClear={handleClear} leaving={leaving} />
  }
  return <HomePage onAnalyze={handleAnalyze} />
}
