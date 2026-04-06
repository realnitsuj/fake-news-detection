import chromadb
import pandas as pd
from sentence_transformers import SentenceTransformer
import os

# chhargement des données

CSV_FILE = "articles_vrais.csv"

if not os.path.exists(CSV_FILE):
    print(f" fichier {CSV_FILE} est introuvable.")
    exit()

df = pd.read_csv(CSV_FILE)

# initialisation de ChromaDB 
chroma_client = chromadb.PersistentClient(path="./ma_base_rag")
collection = chroma_client.get_or_create_collection(name="presse_officielle")

# préparation du modèl
print(" Chargement du modèle de vectorisation...")
embed_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

print(f" Importation de {len(df)} articles dans la base vectorielle...")

documents = []
metadatas = []
ids = []

for index, row in df.iterrows():
    #  texte pour la recherche
    documents.append(row['text'])
    
    # titre et source 
    metadatas.append({
        "titre": str(row.get('title', 'Sans titre')),
        "source": str(row.get('source', 'Inconnue'))
    })
    
    # ID unique obligatoire pour ChromaDB
    ids.append(f"id_{index}")


collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)

print(" Base de données RAG prête et enregistrée dans ./ma_base_rag")