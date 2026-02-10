from pathlib import Path
from src.models import LLMChatCompletion, TinyRag
from config import embd_model_name, RAG_K, system_prompt_template, LLMNAME, HF_TOKEN, FAQ_VEC
from .abstract import Strategy

class StrategyB(Strategy):

    def __init__(self, hf_token: str, model_name: str, system_prompt: str, max_tokens: int, corpus:Path, vec_name: str, top_k: int, *args, **kwargs):
        super().__init__(strategy_name='Strategy_B')

        self.llm = LLMChatCompletion(hf_token=hf_token, model_name=model_name, prompt_template=system_prompt, max_tokens=max_tokens)
        self.rag = TinyRag(model_name=vec_name, corpus=corpus, k=top_k)

    def _answer(self, question: str) -> str:

        documents = self.rag.search(text=question)
        context_text = self._build_context(documents=documents)

        return self.llm.predict(query=question, context=context_text)
    
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
        hf_token=HF_TOKEN,
        model_name=LLMNAME,
        system_prompt=system_prompt_template['B'],
        max_tokens=200,
        corpus=FAQ_VEC,
        vec_name=embd_model_name,
        top_k=RAG_K
    )

    question = "Quelles sont les démarches pour déclarer une naissance ?"
    
    answer = strat.answer(question=question)
    
    print(answer)

if __name__ == "__main__":
    main()