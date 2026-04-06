from fastapi import APIRouter
from app.api.models import TextSchema
from ..dependencies import get_ai_prediction, get_plaintext_from_url

router = APIRouter()

@router.post("/check-text")
async def check_text(payload: TextSchema):
    
    input_text = payload.text

    # 1. On vérifie si l'utilisateur a envoyé une URL
    if input_text.startswith("http://") or input_text.startswith("https://"):
        print(f"URL détectée : {input_text}")
        input_text = get_plaintext_from_url(input_text)
        
        # Gestion d'erreur si le site bloque l'extraction
        if input_text == "Erreur":
            return {"status": "error", "message": "Impossible d'extraire le texte de cette URL. Le site la bloque peut-être."}

    # 2. On passe le texte (ou le contenu extrait de l'URL) à l'IA
    result = get_ai_prediction(input_text)

    # 3. Retour classique
    if "error" in result:
        return {"status": "error", "message": result["error"]}

    return {
        "status": "success",
        "verdict": result.get("verdict"),
        "score": f"{result.get('confiance')}%",
        "categorie": result.get("categorie"),
        "justification": result.get("justification")
    }