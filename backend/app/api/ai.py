import io
import pypdf
from fastapi import APIRouter, UploadFile, File
from app.api.models import TextSchema
from ..dependencies import get_ai_prediction, get_plaintext_from_url

router = APIRouter()

def format_prediction_response(result: dict) -> dict:
    """Standardise la réponse JSON."""
    if "error" in result:
        return {"status": "error", "message": result["error"]}

    return {
        "status": "success",
        "verdict": result.get("verdict"),
        "score": f"{result.get('confiance')}%",
        "categorie": result.get("categorie"),
        "justification": result.get("justification")
    }

@router.post("/check-text")
async def check_text(payload: TextSchema):
    input_text = payload.text

    # Vérification URL
    if input_text.startswith("http://") or input_text.startswith("https://"):
        print(f"URL détectée : {input_text}")
        input_text = get_plaintext_from_url(input_text)
        if input_text == "Erreur":
            return {"status": "error", "message": "Impossible d'extraire le texte de cette URL. Le site la bloque peut-être."}

    result = get_ai_prediction(input_text)
    return format_prediction_response(result)

@router.post("/check-file")
async def check_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        extracted_text = ""
        
        # Extraction selon l'extension
        if file.filename.lower().endswith(".pdf"):
            pdf_reader = pypdf.PdfReader(io.BytesIO(content))
            extracted_text = " ".join(
                page.extract_text() for page in pdf_reader.pages if page.extract_text()
            )
        elif file.filename.lower().endswith(".txt"):
            extracted_text = content.decode("utf-8", errors="ignore")
        else:
            return {"status": "error", "message": "Format non supporté (PDF et TXT uniquement)."}
            
        if not extracted_text.strip():
            return {"status": "error", "message": "Le fichier est vide ou le texte est illisible."}
            
        result = get_ai_prediction(extracted_text)
        return format_prediction_response(result)
        
    except Exception as e:
        return {"status": "error", "message": f"Erreur lors du traitement du fichier : {str(e)}"}
