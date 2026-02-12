from huggingface_hub import InferenceClient
from .abstract import Model

class LLMChatCompletion(Model):
    def __init__(self, hf_token: str, model_name: str, prompt_template: str, max_tokens: int):
        super().__init__(model_name=model_name)

        self.client = InferenceClient(model=model_name, token=hf_token)
        self.max_tokens = max_tokens
        self.prompt_template = prompt_template  # Contains {context} and {query} placeholders

    def predict(self, query: str, context: str = "", stream:bool=False):
        
        
        prompt = self.prompt_template.format(context=context, query=query)
        
        messages = [
            {"role": "user", "content": prompt}
        ]

        if stream == True: 
            token_stream= self.client.chat_completion(
                messages=messages, 
                max_tokens=self.max_tokens,
                temperature=0.05,
                stream=True
            )

            def generate():
                for chunk in token_stream:
                    token = chunk.choices[0].delta.content
                    if token:
                        yield token
            return generate()
        
        return self.client.chat_completion(
            messages=messages, 
            max_tokens=self.max_tokens,
            temperature=0.05
        ).choices[0].message['content'].strip()