from src.llm import LLMChatCompletion
from config import HF_TOKEN, LLMNAME, DATA_DIR, system_prompt_template
from scripts.data_loader import load_golden
import json
import time


def main():
    system_prompt = system_prompt_template['A']

    llm = LLMChatCompletion(system_prompt=system_prompt, max_tokens=200)

    #result = llm.reply(prompt="Quelles sont les démarches pour déclarer une naissance ?")
    print()
    #print(result)

    answers = []
    golden_data = load_golden()['golden_set']
    for item in golden_data:
        q = item['question']
        print("Q:", q)
        result = llm.reply(prompt=q)
        print("A:", result)
        answers.append({
            'question': q,
            'answer': str(result)
        })
        time.sleep(2) 
    with open(DATA_DIR / 'llm_answers.json', 'w', encoding='utf-8') as f:
        json.dump(answers, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
