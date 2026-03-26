import logging
import os
import requests
import json
import chromadb 
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer 
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()

embed_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

chroma_client = chromadb.PersistentClient(path="./ma_base_rag")
collection = chroma_client.get_or_create_collection(name="presse_officielle")


API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

def get_ai_prediction(text: str):
    
    try:
        results = collection.query(query_texts=[text], n_results=1)
        context = f"CONTEXTE DE RÉFÉRENCE : {results['documents'][0][0]}" if results['documents'][0] else "Aucun contexte trouvé."
    except Exception as e:
        logger.error(f"Erreur RAG: {e}")
        context = "Erreur de récupération du contexte."

    prompt = f"""[INST] Tu es un expert en fact-checking. 
    {context}
    En t'appuyant sur le contexte (si utile) et tes connaissances, analyse l'article ci-dessous.
    Réponds EXCLUSIVEMENT en JSON avec les clés : "verdict", "confiance", "categorie", "justification".
    
    ARTICLE : {text} [/INST]"""

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 400, "temperature": 0.1} 
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            full_text = response.json()[0]['generated_text']
            
            start = full_text.find('{')
            end = full_text.rfind('}') + 1
            return json.loads(full_text[start:end])
        else:
            return {"error": f"Erreur API ({response.status_code})"}
    except Exception as e:
        return {"error": str(e)}

def get_plaintext_from_url(url: str):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        return soup.get_text()
    except:
        return "Erreur"
