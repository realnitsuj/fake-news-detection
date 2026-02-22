import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://router.huggingface.co/hf-inference/models/hamzab/roberta-fake-news-classification"
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")


def get_ai_prediction(text: str):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": text, "options": {"wait_for_model": True}}

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=20)
        if response.status_code == 200:
            data = response.json()
            # On extrait le dictionnaire de la liste imbriquée [[{...}]]
            return data[0][0] if isinstance(data, list) else data
        else:
            return {"error": f"Erreur API ({response.status_code})"}
    except Exception as e:
        return {"error": str(e)}
