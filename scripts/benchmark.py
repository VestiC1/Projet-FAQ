from src.utils import load_golden, make_strategy_a, make_strategy_b, make_strategy_c

from config import BENCHMARK_RESULTS    
import pandas as pd
from pprint import pprint

import pyarrow as pa

import time

def main():

    print("Configuration des stratégies...")

    strat_a = make_strategy_a()
    strat_b = make_strategy_b()
    strat_c = make_strategy_c()

    strategies = [strat_a, strat_b, strat_c]

    print("Évaluation des stratégies sur le golden set...\n")

    df = {
        'question': [],
        "faq_id_reference": [],
        "expected_keywords": [],
        "expected_answer_summary": [],
        **{
            key: []
            for s in strategies
            for key in (s.strategy_name, f"{s.strategy_name}_time")
        }
    }

    schema = pa.schema({
        'question': pa.string(),
        "faq_id_reference": pa.list_(pa.string()),
        "expected_keywords": pa.list_(pa.string()),
        "expected_answer_summary": pa.string(),
        **{
            key: pa.float64() if 'time' in key else pa.string()
            for s in strategies
            for key in (s.strategy_name, f"{s.strategy_name}_time")
        }
    })

    golden_data = load_golden()['golden_set']

    for i, item in enumerate(golden_data):
        q = item['question']

        df['question'].append(q)
        df['faq_id_reference'].append([item['faq_id_reference']] if isinstance(item['faq_id_reference'], str) else item['faq_id_reference'])
        df['expected_keywords'].append(item['expected_keywords'])
        df['expected_answer_summary'].append(item['expected_answer_summary'])

        print(f"Q{i}:", q)

        answers = {}# For display purposes

        for strategy in [strat_a, strat_b, strat_c]:

            answers[strategy.strategy_name] = strategy.answer(question=q)

            df[strategy.strategy_name].append(answers[strategy.strategy_name])
            df[f"{strategy.strategy_name}_time"].append(strategy.last_ellapsed_time)

        print("A:", end="")
        pprint(answers)
        print("\n" + "-"*50 + "\n")

        # Slow pace to avoid rate limits
        time.sleep(3)

        

    print(f"Sauvegarde des réponses dans {BENCHMARK_RESULTS}...")

    pd.DataFrame(df).to_parquet(BENCHMARK_RESULTS, index=False, schema=schema)

if __name__ == "__main__":
    main()