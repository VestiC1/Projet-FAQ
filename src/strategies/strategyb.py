from src.llm import LLMChatCompletion
from src.rag import TinyRag
from config import embd_model_name, RAG_K, system_prompt_template
from src.strategies.abstract import StrategyAbstract

class StrategyB(StrategyAbstract):

    def __init__(self, system_prompt: str, max_tokens: int, model_name: str, top_k: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.llm = LLMChatCompletion(system_prompt=system_prompt, max_tokens=max_tokens)
        self.rag = TinyRag(model_name=model_name, k=top_k)

    def answer(self, question: str) -> str:

        documents = self.rag.search(text=question)
        context_text = self._build_context(documents=documents)

        return self.llm.reply(prompt=question, context=context_text)
    
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

    strat = StrategyB(
        system_prompt=system_prompt_template['B'],
        max_tokens=200,
        model_name=embd_model_name,
        top_k=RAG_K
    )

    question = "Quelles sont les démarches pour déclarer une naissance ?"
    
    answer = strat.answer(question=question)
    
    print(answer)

if __name__ == "__main__":
    main()