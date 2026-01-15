from src.strategies import StrategyA, StrategyB, StrategyC
from scripts.data_loader import load_golden
from config import DATA_DIR, system_prompt_template, RAG_K, embd_model_name, qna_model_name
import time
import json
from pprint import pprint

def main():
    
    print("Configuration des stratégies...")

    strat_a = StrategyA(
        system_prompt=system_prompt_template['A'],
        max_tokens=200
    )
    strat_b = StrategyB(
        system_prompt=system_prompt_template['B'], 
        max_tokens=200, 
        model_name=embd_model_name,
        top_k=RAG_K
    )
    strat_c = StrategyC(
        vec_model_name=embd_model_name,
        top_k=RAG_K,
        qna_model_name=qna_model_name
    )
    print("Évaluation des stratégies sur le golden set...")

    questions = []

    golden_data = load_golden()['golden_set']

    for i, item in enumerate(golden_data):
        q = item['question']
        print(f"Q{i}:", q)

        answers = {}

        for strat, name in zip([strat_a, strat_b, strat_c], ['A', 'B', 'C']):
            
            answers[name] = strat.answer(question=q)

        print("A:", end="")
        pprint(answers)
        questions.append({
            'question': q,
            'answers': answers
        })
        time.sleep(3)

    print(f"Sauvegarde des réponses dans {DATA_DIR/'llm_answers.json'}...")

    with open(DATA_DIR / 'llm_answers.json', 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()