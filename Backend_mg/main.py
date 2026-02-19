from services.ia_service import get_ai_prediction
import sys

def run_cli():
    print("\n")

    while True:
        
        user_input = input("Texte à analyser : ")

        if user_input.lower() in ['quitter', 'exit', 'q']:
            print("Au revoir !")
            break

        if len(user_input.strip()) < 10:
            print("Texte trop court (10 caractères min).\n")
            continue

        print("Analyse en cours...")

       
        result = get_ai_prediction(user_input)

       
        if "error" in result:
            print(f"Erreur : {result['error']}\n")
        else:
            label = result.get('label', '').upper()
            score = result.get('score', 0) * 100
            
            
            if label in ["LABEL_0", "FAKE", "fake"]:
                print(f" RÉSULTAT : FAKE NEWS détectée !")
            else:
                print(f" RÉSULTAT : Information fiable.")
            
            print(f"Confiance : {score:.2f}%")
            print(f"  Label IA : {label}")

if __name__ == "__main__":
    run_cli()
