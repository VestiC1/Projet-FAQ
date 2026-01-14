from ..config import HF_TOKEN
from transformers import AutoModelForCausalLM, AutoTokenizer
import requests

# Configuration de l'API Hugging Face
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-v0.1"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def query_mistral(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Exemple d'utilisation
if __name__ == "__main__":
    payload = {
        "inputs": "Pourquoi le ciel est-il bleu ?",
    }
    result = query_mistral(payload)
    print("Réponse du modèle :", result)
