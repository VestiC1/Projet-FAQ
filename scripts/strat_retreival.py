import requests
import json
import sys

MODAL_ENDPOINT = "https://jcaillaux--retrieval-service-retrieve.modal.run"

query = sys.argv[1] if len(sys.argv) > 1 else "Qu'est-ce que le FAQ ?"

response = requests.post(
    MODAL_ENDPOINT,
    json={"query": query, "top_k": 10, "threshold": 0.0},
)

print(f"Status: {response.status_code}\n")

data = response.json()
for i, result in enumerate(data["results"], 1):
    print(f"--- Result {i} (similarity: {result['similarity']:.4f}) ---")
    print(json.dumps(result["content"], indent=2, ensure_ascii=False))
    print()