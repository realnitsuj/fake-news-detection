import os
import json
import requests
import chromadb
import re
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# 1. INITIALISATION DES COMPOSANTS
load_dotenv()
embed_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Configuration ChromaDB
DB_PATH = os.path.join(os.getcwd(), "ma_base_rag")
chroma_client = chromadb.PersistentClient(path=DB_PATH)
collection = chroma_client.get_or_create_collection(
    name="presse_officielle",
    metadata={"hnsw:space": "cosine"}
)

API_URL = "https://router.huggingface.co/v1/chat/completions"
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

def safe_json_text(text: str):
    """Nettoyage strict pour éviter les erreurs de caractères de contrôle JSON."""
    if not text: return ""
    text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ").replace('"', "'")
    text = "".join(char for char in text if ord(char) >= 32)
    return re.sub(r'\s+', ' ', text).strip()

def get_plaintext_from_url(url: str):
    """Extrait proprement le texte d'une page web."""
    try:
        # Faux User-Agent pour éviter de se faire bloquer par les sites d'actualité
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        res = requests.get(url, headers=headers, timeout=10)
        
        if not 200 <= res.status_code <= 300:
            return "Erreur"

        # Parsing avec BeautifulSoup
        soup = BeautifulSoup(res.text, "html.parser")

        # Nettoyage : on retire le code Javascript et CSS qui polluerait l'IA
        for script_or_style in soup(["script", "style", "nav", "footer"]):
            script_or_style.extract()

        # Extraction du texte en gardant des espaces entre les balises
        text = soup.get_text(separator=" ")
        
        # On passe le résultat dans ton nettoyeur existant pour faire le ménage
        return safe_json_text(text)

    except Exception as e:
        print(f"Erreur d'extraction URL: {e}")
        return "Erreur"

def get_ai_prediction(text: str):
    """
    Analyse de fact-checking avec filtrage strict du RAG pour éviter les hors-sujets.
    """
    clean_input = safe_json_text(text)
    
    # --- ÉTAPE 1 : RECHERCHE RAG AVEC SEUIL STRICT ---
    source_to_send = ""
    try:
        results = collection.query(query_texts=[clean_input], n_results=1)
        if results['documents'] and len(results['documents'][0]) > 0:
            distance = results['distances'][0][0]
            if distance <= 0.85:
                source_to_send = safe_json_text(results['documents'][0][0])
    except Exception as e:
        print(f"Erreur ChromaDB: {e}")

    # --- ÉTAPE 2 : PROMPT SYSTEME (AVEC FEW-SHOT) ---
    system_message = (
        "Tu es un expert en vérification d'information. Ton analyse est destinée à des utilisateurs finaux.\n\n"
        "RÈGLES D'OR :\n"
        "1. PAS DE JARGON : Interdiction d'utiliser 'RAG', 'Base de données', 'IA', ou 'Vecteur'.\n"
        "2. ANALYSE : Si une SOURCE est fournie, compare les faits. Si elle est absente, juge la cohérence globale.\n"
        "3. HORS-SUJET : Si la source parle d'un sujet totalement différent, IGNORE-LA.\n"
        "4. CONFIANCE : 90-100% (Preuve directe), 70-89% (Article crédible), <40% (Douteux/Fake News).\n\n"
        "EXEMPLES D'ANALYSE :\n"
        "---\n"
        "Exemple 1 (Source confirmant l'information) :\n"
        "RÉFÉRENCE OFFICIELLE : Le gouvernement a voté une aide énergétique de 100 euros pour les foyers modestes.\n"
        "ARTICLE : L'État distribue un chèque énergie de 100€.\n"
        "RÉPONSE : {\"verdict\": \"Vrai\", \"confiance\": 95, \"categorie\": \"Économie\", \"justification\": \"L'information correspond aux annonces officielles concernant l'aide énergétique gouvernementale.\"}\n"
        "---\n"
        "Exemple 2 (Source contredisant l'information) :\n"
        "RÉFÉRENCE OFFICIELLE : L'OMS confirme que le virus se transmet uniquement par voie aérienne. Aucun remède alimentaire n'est prouvé.\n"
        "ARTICLE : Boire du thé au citron brûlant tue le virus en 2 heures !\n"
        "RÉPONSE : {\"verdict\": \"Faux\", \"confiance\": 98, \"categorie\": \"Santé\", \"justification\": \"Les autorités sanitaires démentent l'efficacité de ce remède alimentaire et rappellent le mode de transmission exact de la maladie.\"}\n"
        "---\n"
        "Exemple 3 (Aucune source pertinente trouvée) :\n"
        "RÉFÉRENCE OFFICIELLE : Aucune source directe trouvée pour ce sujet.\n"
        "ARTICLE : Un vaisseau extraterrestre a été photographié au-dessus de la Tour Eiffel hier soir.\n"
        "RÉPONSE : {\"verdict\": \"Partiel\", \"confiance\": 20, \"categorie\": \"Insolite\", \"justification\": \"Aucune source factuelle ne confirme cet événement. Sans preuve officielle, cette affirmation reste au stade de rumeur non vérifiée.\"}\n"
    )

    # --- ÉTAPE 3 : PROMPT UTILISATEUR ---
    user_message = (
        f"--- RÉFÉRENCE OFFICIELLE ---\n{source_to_send if source_to_send else 'Aucune source directe trouvée pour ce sujet.'}\n\n"
        f"--- ARTICLE À ANALYSER ---\n{clean_input}\n\n"
        "Tâche : Produis une analyse sobre. Ne dis jamais qu'un article est faux juste parce qu'il manque une source.\n"
        "Réponds UNIQUEMENT avec un objet JSON strict : {\"verdict\": \"Vrai|Faux|Partiel\", \"confiance\": nombre entier, \"categorie\": \"texte\", \"justification\": \"texte\"}"
    )

    # --- ÉTAPE 4 : APPEL API ---
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
            print(f"Erreur API: {response.status_code}")
            return {"verdict": "Erreur", "confiance": 0, "justification": "Service temporairement indisponible."}

        content = response.json()["choices"][0]["message"]["content"].strip()
        content = re.sub(r'```json|```', '', content).strip()
        
        data = json.loads(content)
        if isinstance(data, list): data = data[0]

        # --- POST-TRAITEMENT : SÉCURITÉ ET COHÉRENCE ---
        if "justification" in data:
            # Suppression manuelle du jargon technique au cas où
            data["justification"] = data["justification"].replace("RAG", "base de référence")
            
            # Correction de cohérence : Si la justif est positive, le verdict doit suivre
            j_low = data["justification"].lower()
            positive_words = ["confirmé", "crédible", "vrai", "exact", "correspond"]
            if any(w in j_low for w in positive_words) and data["verdict"] == "Faux":
                data["verdict"] = "Vrai"

        return data

    except Exception as e:
        print(f"Erreur Analyse : {e}")
        return {"verdict": "Erreur", "confiance": 0, "justification": "Une erreur technique est survenue."}
