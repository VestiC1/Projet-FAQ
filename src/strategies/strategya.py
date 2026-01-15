from src.llm import LLMChatCompletion
from config import HF_TOKEN, LLMNAME, DATA_DIR
from scripts.data_loader import load_golden
import json
import time


def main():
    system_prompt = """
    Assistant IA de la Communauté de Communes Val de Loire Numérique. Réponds **uniquement** aux questions sur : état civil, urbanisme, déchets, transports, petite-enfance, social, vie associative, élections, logement, culture/sport, fiscalité, eau/assainissement.
    Si la question est dans ce périmètre, réponds en 1-2 phrases max. Si hors-périmètre, réponds **uniquement** : "Ce sujet ne fait pas partie de mon périmètre."
    """

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
        time.sleep(1) 
    with open(DATA_DIR / 'llm_answers.json', 'w', encoding='utf-8') as f:
        json.dump(answers, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
