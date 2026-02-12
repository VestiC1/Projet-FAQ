from pathlib import Path
from .steps import LLMChatCompletion, RetreivalService
from config import RAG_K, system_prompt_template, HF_TOKEN, MODAL_ENDPOINT, LLMNAME
from .abstract import Strategy
from pprint import pprint


class RAG(Strategy):

    def __init__(self, hf_token: str, model_name: str, system_prompt: str, max_tokens: int, endpoint:str, top_k: int, *args, **kwargs):
        super().__init__(strategy_name='RAG')

        self.llm = LLMChatCompletion(hf_token=hf_token, model_name=model_name, prompt_template=system_prompt, max_tokens=max_tokens)
        self.rag = RetreivalService(endpoint=endpoint, k=top_k)

    def _answer(self, question: str, stream:bool=False) -> str:

        documents = self.rag.search(text=question)
        context_text = self._build_context(documents=documents)

        return self.llm.predict(query=question, context=context_text, stream=stream)
    
    def _build_context(self, documents) -> str:

        context_text = "\n----------".join([f"""
                Document [{row['id']}]
                {row['answer']}
                Mots clés : {row['keywords']}
            """ 
            for row in documents
        ])
        return context_text

def main():

    strat = RAG(
        hf_token=HF_TOKEN,
        model_name=LLMNAME,
        system_prompt=system_prompt_template['B'],
        max_tokens=200,
        endpoint=MODAL_ENDPOINT,
        top_k=RAG_K
    )

    question = "Quelles sont les démarches pour déclarer une naissance ?"
    
    answer = strat.answer(question=question, stream=False)
    
    print(answer)

if __name__ == "__main__":
    main()
