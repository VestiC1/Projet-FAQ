from config import CHAT_TOKEN, BENCHMARK_RESULTS, RAGAS_METRICS
import pandas as pd
from ragas.metrics import Faithfulness, AnswerRelevancy, AnswerCorrectness
from ragas import evaluate
from ragas.run_config import RunConfig
from ragas.embeddings import LangchainEmbeddingsWrapper
from datasets import Dataset
from openai import AsyncOpenAI
from ragas.llms import llm_factory
from langchain_openai import OpenAIEmbeddings as LangchainOpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from pprint import pprint
import re


strategy_name = re.compile(r'^Strategy_(\w)$')

# Client async
client = AsyncOpenAI(
    api_key=CHAT_TOKEN,
    base_url="https://api.mistral.ai/v1"
)

llm = llm_factory(
    "mistral-small-latest",
    provider="openai",
    client=client,
)

# Embeddings
#embeddings = LangchainEmbeddingsWrapper(
#    LangchainOpenAIEmbeddings(
#        model="mistral-embed",
#        openai_api_key=CHAT_TOKEN,
#        openai_api_base="https://api.mistral.ai/v1"
#    )
#)
embeddings = LangchainEmbeddingsWrapper(
    HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
)
# Run config pour limiter le rate
run_config = RunConfig(
    max_workers=1,
    max_wait=120,
    max_retries=5,
)


def count_strategies(df):
    cols = [col for col in df.columns if re.match(strategy_name, col)]
    return cols


def build_ground_truth(row) -> str:
    return f"{row['expected_answer_summary']}\n\nMots-clés importants : {row['expected_keywords']}"


def build_ragas_datasets(df, strategies):
    datasets = {
        strategy: {
            "user_input": [],
            "response": [],
            "retrieved_contexts": [],
            "reference": []
        } for strategy in strategies
    }

    for i, row in df.loc.iterrows():
        for strategy in strategies:
            datasets[strategy]["user_input"].append(row['question'])
            datasets[strategy]["response"].append(row[strategy])
            datasets[strategy]["retrieved_contexts"].append([row[f"{strategy}_context"]])
            datasets[strategy]["reference"].append(build_ground_truth(row))

    return datasets


def run_evaluation(datasets):
    results = {
        'strategy' : [],
        'faithfulness' : [],
        'answer_relevancy' : [],
        'answer_correctness' : []
    }

    for key, data in datasets.items():
        print(f"Evaluating {key}...")
        
        metrics = [
            Faithfulness(llm=llm),
            AnswerRelevancy(llm=llm, embeddings=embeddings, strictness=1),
            AnswerCorrectness(llm=llm, embeddings=embeddings)
        ]

        result = evaluate(
            dataset=Dataset.from_dict(data),
            metrics=metrics,
            run_config=run_config,
        )
        results['strategy'].append(key)
        results['faithfulness'].append(result['faithfulness'][0])
        results['answer_relevancy'].append(result['answer_relevancy'][0])
        results['answer_correctness'].append(result['answer_correctness'][0])


    df = pd.DataFrame.from_dict(results)
    df = df.set_index('strategy')  
    #df = df.drop(columns='strategy')
 

    return df


def main():
    df = pd.read_parquet(BENCHMARK_RESULTS)
    strategy_names = count_strategies(df)

    print("Building datasets...")
    datasets = build_ragas_datasets(df, strategy_names)

    print("Running evaluation...")
    df = run_evaluation(datasets)

    print(df)

    print("Exporting results ...")

    df.to_parquet(RAGAS_METRICS)


if __name__ == "__main__":
    main()