from config import FAQ_VEC, embd_model_name, RAG_K
from scripts.compute_embeding import compute_embeddings
from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np
from pathlib import Path

def load_embeddings() -> pd.DataFrame:
    """Charge les embeddings FAQ depuis le fichier parquet."""

    return pd.read_parquet(FAQ_VEC)

class TinyRag:

    def __init__(self, model_name: str, k=5):

        self.model = SentenceTransformer(model_name)

        self.corpus_df = load_embeddings()
        self.corpus_vec = np.array(self.corpus_df['embedding'].to_list())

        self.corpus_df.drop(columns=['embedding'], inplace=True)
        self.k = k
    
    def search(self, text):
        vector = compute_embeddings(model=self.model, texts=[text])
        projected = self.corpus_vec @ vector[0].T

        idx = np.argsort(-projected)[:self.k]
        
        return self.corpus_df.iloc[idx][['id', 'question', 'answer', 'keywords']]
        



def main():
    
    rag = TinyRag(model_name=embd_model_name, k=RAG_K)
    text = "Comment obtenir un acte de naissance ?"
    results = rag.search(text=text)
    print(results)

if __name__ == "__main__":
    main()