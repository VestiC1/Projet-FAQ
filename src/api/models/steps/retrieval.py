from .abstract import Model
import requests
from config import MODAL_ENDPOINT, RAG_K
import requests
import json 

class RetreivalService(Model):

    def __init__(self, endpoint:str, k:int=5, threshold:float=0.0):
        super().__init__(model_name='modal')
        self._endpoint = endpoint
        self._k = k
        self._threshold = threshold
    
    
    def search(self, text):
        query = f"query : {text}"
        response = requests.post(
            self._endpoint,
            json={"query": query, "top_k": 10, "threshold": 0.0},
        )
        response.raise_for_status()
        return [ json.loads(row['content']) for row in response.json()['results'] ]
    
    def predict(self, text):
        return self.search(text=text)
            

def main():
    print('Here')
    rag = RetreivalService(endpoint=MODAL_ENDPOINT, k=RAG_K)
    text = "Comment obtenir un acte de naissance ?"
    results = rag.search(text=text)
    print(results)

if __name__ == "__main__":
    main()