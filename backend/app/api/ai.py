from fastapi import APIRouter

from app.api.models import TextSchema

from ..dependencies import get_ai_prediction

router = APIRouter()


def ai_check_text(text_input: str):
    # Get AI prediction
    result = get_ai_prediction(text_input)
    res = {}

    # Check for errors
    if "error" in result:
        res = {"error", f"Erreur : {result['error']}"}
    else:
        label = result.get("label", "").upper()
        score = result.get("score", 0) * 100

        if label in ["LABEL_0", "FAKE", "fake"]:
            res["prediction"] = "FAKE"
        else:
            res["prediction"] = "GOOD"

        res["score"] = f"{score:.2f}%"

    return res


@router.post("/check-text")
async def check_text(payload: TextSchema):
    return {"result": ai_check_text(payload.text)}


@router.post("/check-file")
async def check_file(payload: TextSchema):
    return {"result": "Not implemented yet"}
