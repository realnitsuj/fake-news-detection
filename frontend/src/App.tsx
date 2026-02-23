import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Input } from "@/components/ui/input"
import logo from "@/assets/logo.jpg"

function App() {
  const [mode, setMode] = useState<"url" | "texte">("url")

  return (
    <div className="relative flex min-h-svh flex-col items-center justify-center p-4 bg-background">
      
      {/* Conteneur principal centré */}
      <main className="flex w-full max-w-sm flex-col items-center gap-6">
        
        {/* Logo */}
        <div className="flex items-center justify-center">
          <img 
            src={logo} 
            alt="Logo de VerifAI" 
            className="h-12 w-auto"
          />
        </div>

        <div className="flex w-full justify-evenly">
            <Button
                aria-pressed={mode === "url"}
                variant={mode === "url" ? "default" : "outline"} 
                onClick={() => setMode("url")}
            >
                URL
            </Button>
            <Button
                aria-pressed={mode === "texte"}
                variant={mode === "texte" ? "default" : "outline"} 
                onClick={() => setMode("texte")}
            >
                Texte
            </Button>
        </div>

        {/* Affichage conditionnel de l'entrée */}
        <div className="w-full">
          {mode === "url" ? (
            <Input type="url" placeholder="Saisissez l'URL..." />
          ) : (
            <Textarea placeholder="Saisissez le texte..." rows={6} />
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="absolute bottom-6 text-sm text-muted-foreground">
        <a href="/conditions" className="hover:underline underline-offset-4">
          Conditions d'utilisation
        </a>
      </footer>

    </div>
  )
}

export default App
