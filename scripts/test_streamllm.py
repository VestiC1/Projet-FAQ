from src.models import LLMChatCompletion
from config import HF_TOKEN, LLMNAME, system_prompt_template

llm = LLMChatCompletion(hf_token=HF_TOKEN, model_name=LLMNAME, prompt_template=system_prompt_template['A'], max_tokens=200)

question = "Quelles sont les démarches pour déclarer une naissance ?"


gen = llm.predict_streamed(question)
for token in gen:
    print(token, end="", flush=True)