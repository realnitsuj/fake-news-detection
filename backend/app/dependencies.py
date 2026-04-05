import os
import json
import requests
import chromadb
import re
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# 1. Initialisation
load_dotenv()
embed_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

DB_PATH = os.path.join(os.getcwd(), "ma_base_rag")
chroma_client = chromadb.PersistentClient(path=DB_PATH)
collection = chroma_client.get_or_create_collection(name="presse_officielle")

API_URL = "https://router.huggingface.co/v1/chat/completions"
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

def safe_json_text(text: str):
    if not text: return ""
    text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ").replace('"', "'")
    text = "".join(char for char in text if ord(char) >= 32)
    return re.sub(r'\s+', ' ', text).strip()

def get_ai_prediction(text: str):
    clean_input = safe_json_text(text)
    
    # --- RAG : RECHERCHE ---
    results = collection.query(query_texts=[clean_input], n_results=1)
    context_to_send = ""
    
    if results['documents'] and len(results['documents'][0]) > 0:
        distance = results['distances'][0][0]
        if distance <= 1.2: # Légèrement plus large pour être sûr de trouver la base de comparaison
            context_to_send = safe_json_text(results['documents'][0][0])
            print(f"✅ RAG MATCH : Base de comparaison trouvée (dist: {distance:.4f})")

    # --- PROMPT : INSPECTION DES DÉTAILS ---
    system_message = (
        "Tu es un expert en vérification de faits (Fact-Checker) impitoyable. "
        "Ta priorité absolue est de détecter les CONTRADICTIONS entre l'article et la source.\n\n"
        "PROCÉDURE DE VÉRIFICATION :\n"
        "1. Compare les DATES, les LIEUX et les CHIFFRES un par un.\n"
        "2. Si un seul détail diverge (ex: une date différente, un nom modifié), le verdict doit être 'Faux' ou 'Partiel'.\n"
        "3. Si une date est modifiée, la confiance doit être de 100% dans le verdict 'FAUX' car c'est une altération volontaire de l'info.\n"
        "4. Ne sois pas indulgent : une info 'presque vraie' est une fausse information."
    )

    user_message = (
        f"SOURCE DE RÉFÉRENCE :\n{context_to_send if context_to_send else 'Aucune source'}\n\n"
        f"ARTICLE À VÉRIFIER :\n{clean_input}\n\n"
        "CONSIGNE : Si l'article dit 'Dimanche 5 avril' et que la source dit 'Lundi 6 avril', c'est FAUX. "
        "Réponds en JSON : {\"verdict\": \"...\", \"confiance\": 0-100, \"categorie\": \"...\", \"justification\": \"...\"}"
    )

    payload = {
        "model": "meta-llama/Llama-3.1-8B-Instruct",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 500,
        "temperature": 0.0 # Strictement déterministe
    }

    try:
        response = requests.post(API_URL, headers={"Authorization": f"Bearer {HF_TOKEN}"}, json=payload, timeout=30)
        if response.status_code == 200:
            content = response.json()["choices"][0]["message"]["content"].strip()
            content = re.sub(r'```json|```', '', content).strip()
            data = json.loads(content)
            
            if isinstance(data, list): data = data[0]
            return data
        return {"verdict": "Erreur API", "confiance": 0, "justification": "API Error"}
    except Exception as e:
        return {"verdict": "Erreur", "confiance": 0, "justification": str(e)}
