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

    def reply(self, prompt, context : str = None):

        return self.client.chat_completion(
            messages=self._build_message(prompt=prompt, context=context), 
            max_tokens=self.max_tokens,
            temperature=0.1
        ).choices[0].message['content'].strip()


    def _build_message(self, prompt, context: str = None):
        first_msg  = self.messages
        if context is not None:
            # Then system prompt is a template
            try :
                first_msg[0]["content"] = self.messages[0]['content'].format(context=context)
            except ValueError:
                raise ValueError("System prompt should be a template.")

        return first_msg + [{
            "role": "user", 
            "content": prompt
        }]
