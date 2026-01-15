from src.rag import TinyRag
from src.qna import QnAExtractor
from config import qna_model_name, embd_model_name, RAG_K

class StrategyC:

    def __init__(self, vec_model_name: str, top_k: int, qna_model_name: str, *args, **kwargs):

        self.rag = TinyRag(model_name=vec_model_name, k=top_k)
        self.qna = QnAExtractor(model_name=qna_model_name)

    def answer(self, question: str) -> str:

        documents = self.rag.search(text=question)
        context_text = self._build_context(documents=documents)

        answer = self.qna.reply(question=question, context=context_text)

        return answer['answer']
    
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