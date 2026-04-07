import pandas as pd
import requests
import time
import os
import random

# Configuration
API_URL = "http://127.0.0.1:8000/ai/check-text"
DATASET_FILE = "dataset_test.csv"
ITERATIONS = 5
SAMPLE_SIZE = 30 
FINAL_REPORT_CSV = "rapport_final_5_sessions.csv"

def run_robustness_audit_with_csv():
    print(f"🛡️ AUDIT DE ROBUSTESSE ET GÉNÉRATION CSV ({ITERATIONS} sessions)")
    print("="*60)
    
    if not os.path.exists(DATASET_FILE):
        print(f"❌ Erreur : Fichier {DATASET_FILE} introuvable.")
        return

    df_full = pd.read_csv(DATASET_FILE)
    tous_les_resultats = []
    stats_sessions = []

    for i in range(1, ITERATIONS + 1):
        df_session = df_full.sample(n=SAMPLE_SIZE).reset_index(drop=True)
        print(f"▶️ Session {i}/{ITERATIONS} en cours...")
        
        success_count = 0
        valid_responses = 0

        for _, row in df_session.iterrows():
            texte_clean = str(row['texte'])
            label_attendu = str(row['label_attendu']).strip().upper()
            
            try:
                res = requests.post(API_URL, json={"text": texte_clean}, timeout=15)
                if res.status_code == 200:
                    data = res.json()
                    prediction = str(data.get("verdict", "ERREUR")).upper()
                    confiance = data.get("score", "0%")
                    
                    succes = (prediction == label_attendu)
                    if succes: success_count += 1
                    valid_responses += 1

                    # On garde tout en mémoire pour le CSV final
                    tous_les_resultats.append({
                        "Session": i,
                        "Texte": texte_clean[:100] + "...", # Tronqué pour lisibilité CSV
                        "Label_Attendu": label_attendu,
                        "Prediction_IA": prediction,
                        "Confiance": confiance,
                        "Succes": succes
                    })
            except:
                continue
            time.sleep(5)

        if valid_responses > 0:
            acc = (success_count / valid_responses) * 100
            stats_sessions.append(acc)
            print(f"📊 Fin Session {i} : {acc:.1f}% d'exactitude")

    # --- GÉNÉRATION DU FICHIER CSV ---
    df_final = pd.DataFrame(tous_les_resultats)
    df_final.to_csv(FINAL_REPORT_CSV, index=False, encoding='utf-8-sig')
    
    # --- BILAN FINAL ---
    avg_acc = sum(stats_sessions) / len(stats_sessions)
    print("="*60)
    print(f"🏆 AUDIT TERMINÉ")
    print(f"Moyenne sur 5 sessions : {avg_acc:.1f}%")
    print(f"📁 Rapport détaillé généré : {FINAL_REPORT_CSV}")
    print("="*60)

if __name__ == "__main__":
    run_robustness_audit_with_csv()