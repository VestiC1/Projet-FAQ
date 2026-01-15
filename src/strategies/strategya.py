from src.llm import LLMChatCompletion
from config import HF_TOKEN, LLMNAME, DATA_DIR, system_prompt_template
from src.strategies.abstract import StrategyAbstract

class StrategyA(StrategyAbstract):

    def __init__(self, system_prompt: str, max_tokens: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.llm = LLMChatCompletion(system_prompt=system_prompt, max_tokens=max_tokens)

    def answer(self, question: str) -> str:

        return self.llm.reply(prompt=question)

def main():
    system_prompt = system_prompt_template['A']

    strat = StrategyA(system_prompt=system_prompt, max_tokens=200)

    question = "Quelles sont les démarches pour déclarer une naissance ?"
    print("Q:", question)
    result = strat.answer(question=question)
    print("A:", result)
        

if __name__ == "__main__":
    main()
