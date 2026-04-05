import os
import json
import requests
import chromadb
import re
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# 1. INITIALISATION
load_dotenv()
embed_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

DB_PATH = os.path.join(os.getcwd(), "ma_base_rag")
chroma_client = chromadb.PersistentClient(path=DB_PATH)
collection = chroma_client.get_or_create_collection(
    name="presse_officielle",
    metadata={"hnsw:space": "cosine"}
)

API_URL = "https://router.huggingface.co/v1/chat/completions"
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

def safe_json_text(text: str):
    if not text: return ""
    text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")
    text = text.replace('"', "'")
    text = "".join(char for char in text if ord(char) >= 32)
    return re.sub(r'\s+', ' ', text).strip()

def get_ai_prediction(text: str):
    clean_input = safe_json_text(text)
    
    # --- RAG ---
    results = collection.query(query_texts=[clean_input], n_results=1)
    context_to_send = ""
    if results['documents'] and len(results['documents'][0]) > 0:
        if results['distances'][0][0] <= 1.1:
            context_to_send = f"SOURCE DE RÉFÉRENCE : {safe_json_text(results['documents'][0][0])}"

    # --- PROMPT ---
    system_message = (
        "Tu es un expert en fact-checking. Réponds UNIQUEMENT en JSON.\n"
        "Barème de confiance : 95-100% (Preuve RAG), 75-94% (Détails précis), 0-39% (Douteux)."
    )

    user_message = (
        f"SOURCE : {context_to_send if context_to_send else 'Aucune.'}\n\n"
        f"ARTICLE : {clean_input}\n\n"
        "JSON attendu : {\"verdict\": \"...\", \"confiance\": 0-100, \"categorie\": \"...\", \"justification\": \"...\"}"
    )

    payload = {
        "model": "meta-llama/Llama-3.1-8B-Instruct",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 500,
        "temperature": 0.2
    }

    try:
        response = requests.post(
            API_URL, 
            headers={"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}, 
            json=payload, 
            timeout=30
        )
        
        # Vérification si la réponse est vide ou invalide
        if not response.text or response.status_code != 200:
            return {
                "verdict": "Erreur",
                "confiance": 0,
                "justification": f"L'API ne répond pas correctement (Code {response.status_code})."
            }

        # Nettoyage du contenu avant de parser
        content = response.json()["choices"][0]["message"]["content"].strip()
        content = re.sub(r'```json|```', '', content).strip()
        
        # Tentative de décodage JSON sécurisée
        try:
            data = json.loads(content)
            if isinstance(data, list): data = data[0]
            return data
        except json.JSONDecodeError:
            return {
                "verdict": "Erreur Format",
                "confiance": 0,
                "justification": "L'IA a renvoyé du texte au lieu d'un objet JSON. Réessayez."
            }
            
    except Exception as e:
        return {
            "verdict": "Erreur Système",
            "confiance": 0,
            "justification": f"Une erreur est survenue : {str(e)}"
        }
