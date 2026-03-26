import os
import json
import requests
import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()


embed_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
chroma_client = chromadb.PersistentClient(path="./ma_base_rag")
collection = chroma_client.get_or_create_collection(name="presse_officielle")


API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

def get_ai_prediction(text: str):
    
    results = collection.query(query_texts=[text], n_results=1)
    context = ""
    if results['documents'] and len(results['documents'][0]) > 0:
        context = f"RÉFÉRENCE FIABLE : {results['documents'][0][0]}"
    else:
        context = "Aucune source de référence trouvée."

    # 2. Construction du Prompt pour Mistral
    prompt = f"[INST] Tu es un expert en fact-checking. {context} Analyse l'article suivant et réponds UNIQUEMENT en JSON (verdict, confiance, categorie, justification). Article : {text} [/INST]"
    
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": prompt, 
        "parameters": {"max_new_tokens": 300, "temperature": 0.1}
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            raw_output = response.json()[0]['generated_text']
            
            json_start = raw_output.find('{')
            json_end = raw_output.rfind('}') + 1
            return json.loads(raw_output[json_start:json_end])
        else:
            return {"error": f"Erreur API ({response.status_code})"}
    except Exception as e:
        return {"error": f"Erreur de traitement : {str(e)}"}
