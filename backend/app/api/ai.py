from fastapi import APIRouter
from app.api.models import FileSchema, TextSchema
from ..dependencies import get_ai_prediction

router = APIRouter()

def format_prediction_response(result: dict) -> dict:
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
    result = get_ai_prediction(payload.text)
    return format_prediction_response(result)

@router.post("/check-file")
async def check_file(payload: FileSchema):
    # TODO: Implémenter l'extraction de texte avec une nouvelle librairie (ex: pypdf, python-docx)
    return {"status": "error", "message": "L'extraction de texte à partir de fichiers est en cours de développement."}
