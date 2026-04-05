import os
import json
import requests
import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

embed_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

DB_PATH = os.path.join(os.getcwd(), "ma_base_rag")
chroma_client = chromadb.PersistentClient(path=DB_PATH)
collection = chroma_client.get_or_create_collection(name="presse_officielle")

API_URL = "https://router.huggingface.co/v1/chat/completions"
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

def get_ai_prediction(text: str):
    results = collection.query(query_texts=[text], n_results=3)
    
    context = ""
    if results['documents'] and len(results['documents'][0]) > 0:
        context = f"RÉFÉRENCE OFFICIELLE : {results['documents'][0][0]}"
    else:
        context = "Aucune source fiable n'a été trouvée pour comparer."

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "model": "meta-llama/Llama-3.1-8B-Instruct",
        "provider": "cerebras",
        "messages": [
            {"role": "system", "content": "Tu es un expert en fact-checking. Réponds UNIQUEMENT en JSON valide avec les clés : \"verdict\", \"confiance\", \"categorie\", \"justification\". Aucun texte avant ou après le JSON."},
            {"role": "user", "content": f"{context}\n\nARTICLE : {text}"}
        ],
        "max_tokens": 400
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            res_text = response.json()["choices"][0]["message"]["content"]
            
            return json.loads(res_text)
        return {"error": "Problème avec l'API Llama"}
    except Exception as e:
        return {"error": str(e)}
