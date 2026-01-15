from config import FAQ_VEC, embd_model_name, RAG_K
from scripts.compute_embeding import compute_embeddings
from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np
from pathlib import Path
from .abstract import Model


class TinyRag(Model):

    def __init__(self, model_name: str, corpus: Path, k=5):
        super().__init__(model_name=model_name)

        self.model = SentenceTransformer(model_name)

        self.corpus_df = self.load_embeddings(corpus)
        self.corpus_vec = np.array(self.corpus_df['embedding'].to_list())

        self.corpus_df.drop(columns=['embedding'], inplace=True)
        self.k = k
    
    def search(self, text):
        vector = compute_embeddings(model=self.model, texts=[text])
        projected = self.corpus_vec @ vector[0].T

        idx = np.argsort(-projected)[:self.k]
        
        return self.corpus_df.iloc[idx][['id', 'question', 'answer', 'keywords']]
    
    def load_embeddings(self, path : Path) -> pd.DataFrame:
        """Charge les embeddings FAQ depuis le fichier parquet."""

        return pd.read_parquet(path)
    
    def predict(self, text):
        return self.search(text=text)
            



def main():
    
    rag = TinyRag(model_name=embd_model_name, corpus=FAQ_VEC, k=RAG_K)
    text = "Comment obtenir un acte de naissance ?"
    results = rag.search(text=text)
    print(results)

if __name__ == "__main__":
    main()