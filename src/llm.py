from huggingface_hub import InferenceClient
from config import HF_TOKEN, LLMNAME


from huggingface_hub import InferenceClient

class LLMChatCompletion:
    def __init__(self, system_prompt, max_tokens):

        self.client = InferenceClient(model=LLMNAME, token=HF_TOKEN)

        self.max_tokens = max_tokens

        self.messages = [
            {"role": "system", "content": system_prompt}
        ]

    def reply(self, prompt):

        return self.client.chat_completion(
            messages=self._build_message(prompt=prompt), 
            max_tokens=self.max_tokens
        )


    def _build_message(self, prompt):

        return self.messages + [{
            "role": "user", 
            "content": prompt
        }]
