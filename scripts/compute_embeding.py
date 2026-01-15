from scripts.data_loader import load_faq
from sentence_transformers import SentenceTransformer
from config import FAQ_VEC
import pandas as pd
from pathlib import Path

class TinyRag:

    def __init__(self, model_name: str, corpus_data: Path):
        self.model = SentenceTransformer(model_name)
        self.corpus_df = data_extract(json_data=load_faq())
        


def compute_embeddings(model, texts: list[str]) -> list[list[float]]:
    return model.encode(texts)

def data_extract(json_data):

    return pd.DataFrame({
        "id" : [ doc['id'] for doc in json_data['faq']],
        "question" : [ doc['question'] for doc in json_data['faq']],
        "answer" :   [ doc['answer'] for doc in json_data['faq']],
        "keywords" : [ ", ".join(doc['keywords']) for doc in json_data['faq'] ],
    })

def main():
    faq_data = load_faq()
    df = data_extract(faq_data)
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    model = SentenceTransformer(model_name)
    df['embedding'] = df[['question', 'answer', 'keywords']].apply(lambda x : compute_embeddings(model, f"{x['question']} {x['answer']} {x['keywords']}"), axis=1)
    df.to_parquet(FAQ_VEC, index=False)

if __name__ == "__main__":
    main()