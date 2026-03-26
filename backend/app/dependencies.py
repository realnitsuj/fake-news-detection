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

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

def get_ai_prediction(text: str):
    results = collection.query(query_texts=[text], n_results=1)
    
    context = ""
    if results['documents'] and len(results['documents'][0]) > 0:
        context = f"RÉFÉRENCE OFFICIELLE : {results['documents'][0][0]}"
    else:
        context = "Aucune source fiable n'a été trouvée pour comparer."

    prompt = f"""[INST] Tu es un expert en fact-checking. 
    {context}
    Analyse l'article suivant et réponds UNIQUEMENT en JSON avec : "verdict", "confiance", "categorie", "justification".
    ARTICLE : {text} [/INST]"""

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 400}}

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            res_text = response.json()[0]['generated_text']
            
            return json.loads(res_text[res_text.find("{"):res_text.rfind("}")+1])
        return {"error": "Problème avec l'API Mistral"}
    except Exception as e:
        return {"error": str(e)}
