import json
from pathlib import Path


def load_faq(faq_path:Path):
    if not faq_path.exists():
        raise FileNotFoundError("FAQ introuvable")
    with open(faq_path, "r") as f:
        return json.load(f)
    
def get_document(faq_json, id):

    results = []

    for doc in faq_json["faq"] :
        if doc["id"]==id :
            results.append(doc)
            break

    return results