from src.models import LLMChatCompletion
from config import HF_TOKEN, LLMNAME, system_prompt_template
from .abstract import Strategy

class StrategyA(Strategy):

    def __init__(self, hf_token: str, model_name: str, system_prompt: str, max_tokens: int, *args, **kwargs):
        super().__init__(strategy_name='Strategy_A')

        self.llm = LLMChatCompletion(hf_token=hf_token, model_name=model_name, system_prompt=system_prompt, max_tokens=max_tokens)

    def _answer(self, question: str) -> str:
        
        return self.llm.predict(prompt=question)
    
def main():
    system_prompt = system_prompt_template['A']

    strat = StrategyA(hf_token=HF_TOKEN, model_name=LLMNAME, system_prompt=system_prompt, max_tokens=200)
    question = "Quelles sont les démarches pour déclarer une naissance ?"
    print("Q:", question)
    result = strat.answer(question=question)
    print("A:", result)
        

if __name__ == "__main__":
    main()
