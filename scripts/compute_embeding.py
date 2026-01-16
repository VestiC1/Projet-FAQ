from src.utils import load_faq
from sentence_transformers import SentenceTransformer
from config import FAQ_VEC, embd_model_name
import pandas as pd
from pathlib import Path


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
    model_name = embd_model_name
    model = SentenceTransformer(model_name)
    df['embedding'] = df[['question', 'answer', 'keywords']].apply(lambda x : compute_embeddings(model, f"passage: {x['question']} {x['answer']} {x['keywords']}"), axis=1)
    df.to_parquet(FAQ_VEC, index=False)

if __name__ == "__main__":
    main()