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

# Configuration ChromaDB
DB_PATH = os.path.join(os.getcwd(), "ma_base_rag")
chroma_client = chromadb.PersistentClient(path=DB_PATH)
collection = chroma_client.get_or_create_collection(name="presse_officielle")

API_URL = "https://router.huggingface.co/v1/chat/completions"
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

def safe_json_text(text: str):
    """
    Nettoyage radical pour éviter l'erreur 'Invalid control character'.
    Supprime les sauts de ligne, tabulations et protège les guillemets.
    """
    if not text:
        return ""
    # 1. Remplace les retours à la ligne et tabulations par des espaces
    text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")
    # 2. Remplace les guillemets doubles par des simples pour ne pas casser le JSON
    text = text.replace('"', "'")
    # 3. Supprime les caractères non-imprimables (ceux qui causent ton erreur)
    text = "".join(char for char in text if ord(char) >= 32)
    # 4. Nettoie les espaces multiples
    return re.sub(r'\s+', ' ', text).strip()

def get_ai_prediction(text: str):
    """
    Analyse de fact-checking avec nettoyage strict et gestion de la confiance.
    """
    # Nettoyage immédiat de l'entrée pour éviter les crashs JSON
    clean_input = safe_json_text(text)
    
    # --- RAG : RECHERCHE ---
    results = collection.query(query_texts=[clean_input], n_results=1)
    context_to_send = "AUCUNE SOURCE INTERNE."
    
    # Seuil strict (0.7) pour éviter les mélanges de sujets (ex: Macron/Motards)
    if results['documents'] and len(results['documents'][0]) > 0:
        distance = results['distances'][0][0]
        if distance <= 0.7:
            context_to_send = f"SOURCE OFFICIELLE : {safe_json_text(results['documents'][0][0])}"
            print(f"✅ RAG MATCH (dist: {distance:.4f})")

    # --- PROMPT : EXPERT EN CRÉDIBILITÉ ---
    system_message = (
        "Tu es un expert en fact-checking indépendant. "
        "Le score de 'confiance' doit refléter la probabilité que l'article soit VRAI ou FAUX.\n"
        "DIRECTIVES :\n"
        "- Si l'article est validé par la SOURCE : Confiance 95-100%.\n"
        "- Si l'article est riche en détails (noms, lieux, dates, citations) : Confiance 75-90%, même sans source.\n"
        "- Si l'article est vague ou alarmiste (Fake News) : Confiance élevée dans un verdict 'Faux'.\n"
        "Réponds UNIQUEMENT en JSON."
    )

    user_message = (
        f"[SOURCE] : {context_to_send}\n\n"
        f"[ARTICLE] : {clean_input}\n\n"
        "JSON : {\"verdict\": \"Vrai|Faux|Partiel\", \"confiance\": 0-100, \"categorie\": \"...\", \"justification\": \"...\"}"
    )

    headers = {"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}
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
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            content = response.json()["choices"][0]["message"]["content"].strip()
            # Nettoyage des balises Markdown ```json ... ```
            content = re.sub(r'```json|```', '', content).strip()
            return json.loads(content)
        else:
            return {"verdict": "Erreur API", "confiance": 0, "justification": f"Erreur {response.status_code}"}
            
    except Exception as e:
        # En cas d'erreur de parsing JSON, on renvoie un dictionnaire propre
        return {
            "verdict": "Erreur Format",
            "confiance": 0,
            "justification": f"Erreur de traitement des données : {str(e)}"
        }
