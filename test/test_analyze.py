import os
import requests
import json
import time

def test_question_analysis():
    API_URL = "http://localhost:3000/analyze_question/"
    TEST_FILE = os.path.join(os.path.dirname(__file__), "questions.txt")
    DELAY = 3.0

    try:
        with open(TEST_FILE, 'r', encoding='utf-8') as f:
            questions = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: Archivo {TEST_FILE} no encontrado")
        return

    for i, question in enumerate(questions, 1):
        try:
            response = requests.post(
                API_URL,
                json={"question": question},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            print(question)
            print(json.dumps(data, ensure_ascii=False, indent=2))

            print("\n")


            if i < len(questions):
                time.sleep(DELAY)

        except Exception as e:
            print(f"Error en pregunta {i} ('{question}'): {e}")

if __name__ == "__main__":
    test_question_analysis()


    
