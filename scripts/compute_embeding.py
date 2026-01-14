from scripts.data_loader import load_faq
from sentence_transformers import SentenceTransformer

import pandas as pd


def compute_embeddings(model, texts: list[str]) -> list[list[float]]:
    return model.encode(texts)

def data_extract(json_data):

    return pd.DataFrame(
        {
            "id" : [ doc['id'] for doc in json_data['faq']],
            "question" : [ doc['question'] for doc in json_data['faq']],
            "answer" : [ doc['answer'] for doc in json_data['faq']],
        }
    )

def main():
    faq_data = load_faq()
    df = data_extract(faq_data)
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    model = SentenceTransformer(model_name)
    df['embedding'] = df[['question', 'answer']].apply(lambda x : compute_embeddings(model, f"Question : {x['answer']} Réponse : {x['question']}"), axis=1)
    print(df.head())
if __name__ == "__main__":
    main()