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
    text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ").replace('"', "'")
    text = "".join(char for char in text if ord(char) >= 32)
    return re.sub(r'\s+', ' ', text).strip()

def get_ai_prediction(text: str):
    clean_input = safe_json_text(text)
    
    # --- RECHERCHE DE SOURCE ---
    results = collection.query(query_texts=[clean_input], n_results=1)
    source_found = ""
    if results['documents'] and len(results['documents'][0]) > 0:
        if results['distances'][0][0] <= 1.1:
            source_found = safe_json_text(results['documents'][0][0])

    # --- PROMPT CLIENT (SANS JARGON) ---
    system_message = (
        "Tu es un expert en vérification d'information pour une application grand public.\n\n"
        "CONSIGNES DE RÉDACTION (DESTINATION CLIENT) :\n"
        "1. INTERDICTION : Ne mentionne JAMAIS les termes techniques comme 'RAG', 'Base de données', 'Vecteur', 'IA' ou 'Modèle' dans tes justifications.\n"
        "2. Vocabulaire autorisé : 'Source officielle', 'Presse spécialisée', 'Détails factuels', 'Cohérence de l'information'.\n"
        "3. Si tu ne trouves pas de document correspondant, dis simplement : 'Aucune source officielle directe n'a été identifiée pour confirmer ce fait précis'.\n"
        "4. Un verdict 'Vrai' est possible sans source si l'information est de notoriété publique ou très cohérente avec l'actualité réelle."
    )

    user_message = (
        f"CONTEXTE DE RÉFÉRENCE : {source_found if source_found else 'Aucune source disponible.'}\n\n"
        f"ARTICLE À ANALYSER : {clean_input}\n\n"
        "Tâche : Analyse l'article pour un client. Sois sobre et professionnel.\n"
        "Format JSON : {\"verdict\": \"Vrai|Faux|Partiel\", \"confiance\": 0-100, \"categorie\": \"...\", \"justification\": \"...\"}"
    )

    payload = {
        "model": "meta-llama/Llama-3.1-8B-Instruct",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 500,
        "temperature": 0.1
    }

    try:
        response = requests.post(
            API_URL, 
            headers={"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}, 
            json=payload, 
            timeout=30
        )
        
        if response.status_code != 200:
            return {"verdict": "Indisponible", "confiance": 0, "justification": "Service momentanément indisponible."}

        content = response.json()["choices"][0]["message"]["content"].strip()
        content = re.sub(r'```json|```', '', content).strip()
        data = json.loads(content)
        
        # Sécurité pour transformer une liste en dictionnaire
        if isinstance(data, list): data = data[0]

        # Nettoyage final de la justification pour supprimer le jargon "RAG" au cas où l'IA désobéit
        if "justification" in data:
            data["justification"] = data["justification"].replace("RAG", "source officielle").replace("rag", "source officielle")

        return data
            
    except Exception as e:
        return {"verdict": "Erreur", "confiance": 0, "justification": "Erreur lors du traitement de l'information."}
