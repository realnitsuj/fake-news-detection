from fastapi import APIRouter
from app.api.models import TextSchema
from ..dependencies import get_ai_prediction

router = APIRouter()

@router.post("/check-text")
async def check_text(payload: TextSchema):
    
    result = get_ai_prediction(payload.text)

    if "error" in result:
        return {"status": "error", "message": result["error"]}

    
    return {
        "status": "success",
        "verdict": result.get("verdict"),
        "score": f"{result.get('confiance')}%",
        "categorie": result.get("categorie"),
        "justification": result.get("justification")
    }
