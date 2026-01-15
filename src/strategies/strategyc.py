from src.rag import TinyRag
from src.qna import QnAExtractor
from config import HF_TOKEN, LLMNAME, DATA_DIR, qna_model_name, embd_model_name, RAG_K

def main():
    
    rag = TinyRag(model_name=embd_model_name, k= RAG_K)

    question = "Quelles sont les démarches pour déclarer une naissance ?"
    contexts = rag.search(text=question)
    context_text = "\n".join([f"{row['answer']}" for _, row in contexts.iterrows()])

    qna = QnAExtractor(model_name=qna_model_name)
    answer = qna.reply(question=question, context=context_text)
    print("Réponse de l'assistant :")
    print(answer)

if __name__ == "__main__":
    main()