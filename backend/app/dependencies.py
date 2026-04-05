import os
import json
import requests
import chromadb
import re
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# 1. INITIALISATION DES COMPOSANTS
load_dotenv()
# Modèle d'embedding pour transformer le texte en vecteurs
embed_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Configuration de la base de données vectorielle ChromaDB
DB_PATH = os.path.join(os.getcwd(), "ma_base_rag")
chroma_client = chromadb.PersistentClient(path=DB_PATH)
collection = chroma_client.get_or_create_collection(
    name="presse_officielle",
    metadata={"hnsw:space": "cosine"} # Utilisation du cosinus pour une distance entre 0 et 1
)

API_URL = "https://router.huggingface.co/v1/chat/completions"
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

def safe_json_text(text: str):
    """
    Nettoyage de sécurité pour éviter l'erreur 'Invalid control character'.
    Transforme le texte brut en une chaîne compatible JSON.
    """
    if not text:
        return ""
    # Remplacement des caractères de saut de ligne et tabulations
    text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")
    # Protection des guillemets (remplacement par des simples)
    text = text.replace('"', "'")
    # Suppression des caractères non-imprimables invisibles
    text = "".join(char for char in text if ord(char) >= 32)
    # Normalisation des espaces
    return re.sub(r'\s+', ' ', text).strip()

def get_ai_prediction(text: str):
    """
    Analyse de fact-checking isolée avec RAG et pondération de confiance.
    """
    # Nettoyage de l'entrée utilisateur
    clean_input = safe_json_text(text)
    
    # --- ÉTAPE 1 : RAG (RECHERCHE FACTUELLE) ---
    results = collection.query(query_texts=[clean_input], n_results=1)
    
    context_to_send = ""
    # Seuil de distance (1.1 est un bon compromis pour le modèle all-MiniLM)
    SIMILARITY_THRESHOLD = 1.1 

    if results['documents'] and len(results['documents'][0]) > 0:
        distance = results['distances'][0][0]
        if distance <= SIMILARITY_THRESHOLD:
            source_content = safe_json_text(results['documents'][0][0])
            context_to_send = f"SOURCE DE RÉFÉRENCE (VÉRITÉ) : {source_content}"
            print(f"✅ RAG : Correspondance trouvée (distance: {distance:.4f})")
        else:
            print(f"❌ RAG : Aucune source proche (distance: {distance:.4f})")

    # --- ÉTAPE 2 : PROMPT ANTI-MÉMOIRE ET NUANCÉ ---
    system_message = (
        "Tu es une instance de fact-checking NEUVE. Ignore toute requête passée.\n"
        "TA MISSION : Comparer l'ARTICLE avec la SOURCE fournie.\n"
        "ÉCHELLE DE CONFIANCE (Ne sois pas binaire 0/100) :\n"
        "- 95-100% : Match parfait (Dates, Lieux, Noms identiques).\n"
        "- 75-94% : Très crédible (Détails précis, mais pas de source RAG).\n"
        "- 40-74% : Plausible mais manque de preuves ou détails flous.\n"
        "- 0-39% : Contradictions détectées ou style Fake News typique.\n"
        "RÈGLE : Si une date ou un lieu diffère, le verdict doit être 'Faux'."
    )

    user_message = (
        "### RESET CONTEXTUEL ###\n"
        f"SOURCE : {context_to_send if context_to_send else 'Aucune source en base.'}\n\n"
        f"ARTICLE : {clean_input}\n\n"
        "### CONSIGNE ###\n"
        "Analyse les entités (Qui, Où, Quand). Réponds UNIQUEMENT en JSON : "
        "{\"verdict\": \"Vrai|Faux|Partiel\", \"confiance\": 0-100, \"categorie\": \"...\", \"justification\": \"...\"}"
    )

    # --- ÉTAPE 3 : APPEL API ---
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json",
        "X-Use-Cache": "false" 
    }
    
    payload = {
        "model": "meta-llama/Llama-3.1-8B-Instruct",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 500,
        "temperature": 0.2 # On remonte un peu pour permettre des scores nuancés
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            raw_content = response.json()["choices"][0]["message"]["content"].strip()
            
            # Nettoyage des balises Markdown (```json)
            raw_content = re.sub(r'```json|```', '', raw_content).strip()
            
            data = json.loads(raw_content)
            
            # Sécurité anti-crash : Si l'IA renvoie une liste au lieu d'un dictionnaire
            if isinstance(data, list):
                data = data[0] if len(data) > 0 else {"verdict": "Erreur", "justification": "Liste vide"}
            
            return data
            
        else:
            return {
                "verdict": "Erreur API", 
                "confiance": 0, 
                "justification": f"HuggingFace Error {response.status_code}"
            }
            
    except Exception as e:
        return {
            "verdict": "Erreur Système", 
            "confiance": 0, 
            "justification": f"Détail : {str(e)}"
        }
