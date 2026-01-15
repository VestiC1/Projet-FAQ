from src.llm import LLMChatCompletion
from src.rag import TinyRag
from config import HF_TOKEN, LLMNAME, DATA_DIR, embd_model_name, RAG_K, system_prompt_template

def main():
    
    rag = TinyRag(model_name=embd_model_name, k= RAG_K)

    question = "Quelles sont les démarches pour déclarer une naissance ?"
    contexts = rag.search(text=question)
    context_text = "\n----------".join([f"Document [{row['id']}]\n{row['answer']}\n Mots clés : {row['keywords']}" for _, row in contexts.iterrows()])

    system_prompt = system_prompt_template['B'].format(context=context_text)

    llm = LLMChatCompletion(system_prompt=system_prompt, max_tokens=200)
    
    prompt = question
    answer = llm.reply(prompt=prompt)
    print(answer)

if __name__ == "__main__":
    main()