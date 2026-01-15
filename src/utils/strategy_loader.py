from config import HF_TOKEN, LLMNAME, system_prompt_template, embd_model_name, RAG_K, FAQ_VEC, qna_model_name


def make_strategy_a():
    from src.strategies import StrategyA

    system_prompt = system_prompt_template['A']

    return StrategyA(
        hf_token   = HF_TOKEN,
        model_name = LLMNAME,
        system_prompt = system_prompt,
        max_tokens = 200
    )

def make_strategy_b():
    from src.strategies import StrategyB

    system_prompt = system_prompt_template['B']

    return StrategyB(
        hf_token=HF_TOKEN,
        model_name=LLMNAME,
        system_prompt=system_prompt,
        max_tokens=200,
        corpus=FAQ_VEC,
        vec_name=embd_model_name,
        top_k=RAG_K
    )
def make_strategy_c():
    from src.strategies import StrategyC

    return StrategyC(
        corpus=FAQ_VEC,
        vec_model_name=embd_model_name,
        top_k=RAG_K,
        qna_model_name=qna_model_name
    )
