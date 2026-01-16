import marimo

__generated_with = "0.19.2"
app = marimo.App(width="medium")


@app.cell
def _():
    from pathlib import Path
    import sys
    import os
    import os
    import time
    ROOT = Path(__file__).parent.parent
    sys.path.insert(0, str(ROOT))
    return os, time


@app.cell
def _():
    from sentence_transformers import SentenceTransformer
    from config import embd_model_name
    from src.utils import load_faq
    import numpy as np
    import pandas as pd
    return SentenceTransformer, embd_model_name, load_faq, np, pd


@app.cell
def _(embd_model_name):
    models = [embd_model_name, "intfloat/multilingual-e5-small", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"]
    model_name =  embd_model_name #"intfloat/multilingual-e5-small" # embd_model_name
    return (models,)


@app.cell
def _(np, pd):
    def evaluate_embedding_model(model, corpus):
        # What you actually embed in your RAG
        chunks = [
            f"{doc['question']} {doc['answer']} {' '.join(doc['keywords'])}"
            for doc in corpus
        ]
    
        # What users will query with (question-like)
        questions = [doc['question'] for doc in corpus]
    
        emb_chunks = model.encode(chunks)
        emb_questions = model.encode(questions)
    
        # Normalize
        emb_chunks = emb_chunks / np.linalg.norm(emb_chunks, axis=1, keepdims=True)
        emb_questions = emb_questions / np.linalg.norm(emb_questions, axis=1, keepdims=True)
    
        # Alignment: user question → corresponding chunk
        alignment = np.mean(np.sum((emb_questions - emb_chunks) ** 2, axis=1))
    
        # Uniformity: chunks should spread well
        sq_dists = np.sum((emb_chunks[:, None] - emb_chunks[None, :]) ** 2, axis=2)
        uniformity = np.log(np.mean(np.exp(-2 * sq_dists)))
    
        return pd.DataFrame({
            'alignment': [alignment],  # lower = better
            'uniformity': [uniformity]  # lower (more negative) = better
        }, index=[model.model_card_data.base_model])
    return (evaluate_embedding_model,)


@app.cell
def _(np, pd, time):
    def mrr(model, corpus, e5_prefix=False):
        """Where does the correct chunk rank? Higher = better."""
        chunks = [
            f"{doc['answer']} {' '.join(doc['keywords'])}"
            for doc in corpus
        ]
        questions = [doc['question'] for doc in corpus]
    
        if e5_prefix:
            questions = [f"query: {q}" for q in questions]
            chunks = [f"passage: {c}" for c in chunks]
    
        emb_q = model.encode(questions)
        emb_c = model.encode(chunks)
    
        emb_q = emb_q / np.linalg.norm(emb_q, axis=1, keepdims=True)
        emb_c = emb_c / np.linalg.norm(emb_c, axis=1, keepdims=True)
    
        similarities = emb_c @ emb_q.T
    
        reciprocal_ranks = []
        for i, row in enumerate(similarities):
            rank = np.where(np.argsort(row)[::-1] == i)[0][0] + 1
            reciprocal_ranks.append(1 / rank)
    
        return pd.DataFrame({
            'mrr' : [float(np.mean(reciprocal_ranks))]
        }, index=[model.model_card_data.base_model])

    def benchmark_speed(model, corpus, n_runs=10):
        questions = [doc['question'] for doc in corpus]
    
        start = time.perf_counter()
        for _ in range(n_runs):
            model.encode(questions)
        elapsed = time.perf_counter() - start
    
        return pd.DataFrame({
            'time' : [elapsed / n_runs]
        }, index=[model.model_card_data.base_model])
    return benchmark_speed, mrr


@app.cell
def _(load_faq):
    corpus = load_faq()['faq']
    return (corpus,)


@app.cell
def _(
    SentenceTransformer,
    benchmark_speed,
    corpus,
    evaluate_embedding_model,
    models,
    mrr,
    os,
    pd,
):
    os.environ["HF_HUB_OFFLINE"] = "1"

    metrics = None
    for name in models:
        print(name)
        model = SentenceTransformer(name)
        result = evaluate_embedding_model(model=model, corpus=corpus)
        result_mrr = mrr(model, corpus)
        result_speed = benchmark_speed(model, corpus)
        result = pd.concat([result, result_mrr, result_speed], axis=1)
        try :
            metrics.loc[name] = result.iloc[0,:]
        except:
            metrics = result.copy()
    return (metrics,)


@app.cell
def _(metrics):
    metrics
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
