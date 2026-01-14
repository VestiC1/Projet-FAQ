from huggingface_hub import InferenceClient
from config import HF_TOKEN, LLMNAME


class LLMChatCompletion:

    def __init__(self, system_prompt, max_tokens):

        # HF client initialisation
        self.client = InferenceClient(
            model=LLMNAME,
            token=HF_TOKEN,
        )

        self.max_tokens = max_tokens

        messages = [{
            "role": "user",
            "content": system_prompt,
        }]

        result = self.client.chat_completion(messages=messages, max_tokens=max_tokens)
        print(result)
    
    def reply(self, prompt):
        return self.client.chat_completion(
            messages=[{
                "role": "user",
                "content": prompt,
            }], 
            max_tokens=self.max_tokens
        )