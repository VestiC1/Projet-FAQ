from transformers import AutoTokenizer
from config import LLMNAME

def main():
    model_name = LLMNAME
    #model_name = "bofenghuang/vigostral-7b-chat"
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
    print(tokenizer.chat_template)

    messages = [
        #{"role": "system", "content": "Tu es in assitant IA français."},
        {"role": "user", "content": "Bonjour, Comment ça va?"}
    ]
    formatted = tokenizer.apply_chat_template(messages, tokenize=False)
    print("Formatted messages:")
    print(formatted)

if __name__ == "__main__":
    main()