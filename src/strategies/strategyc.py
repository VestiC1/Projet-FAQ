from src.models import TinyRag, QnAExtractor
from config import qna_model_name, embd_model_name, RAG_K, FAQ_VEC
from pathlib import Path
from .abstract import Strategy

class StrategyC(Strategy):

    def __init__(self, corpus: Path, vec_model_name: str, top_k: int, qna_model_name: str, *args, **kwargs):
        super().__init__(strategy_name='Strategy_C')

        self.rag = TinyRag(model_name=vec_model_name, corpus=corpus, k=top_k)
        self.qna = QnAExtractor(model_name=qna_model_name)

    def _answer(self, question: str) -> str:

        documents = self.rag.search(text=question)
        context_text = self._build_context(documents=documents)

        answer = self.qna.predict(question=question, context=context_text)

        return answer['answer'].strip()
    
    def _build_context(self, documents) -> str:
        context_text = "\n----------".join([f"""
                Document [{row['id']}]
                {row['answer']}
                Mots clés : {row['keywords']}
            """ 
            for _, row in documents.iterrows()
        ])
        return context_text

def main():

    strat = StrategyC(
        corpus=FAQ_VEC,
        vec_model_name=embd_model_name,
        top_k=RAG_K,
        qna_model_name=qna_model_name
    )

    question = "Quelles sont les démarches pour déclarer une naissance ?"

    answer = strat.answer(question=question)
    print("Réponse de l'assistant :")
    print(answer)

if __name__ == "__main__":
    main()