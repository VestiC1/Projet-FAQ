from huggingface_hub import InferenceClient
from config import HF_TOKEN


messages = [
    {
        "role": "user",
        "content": "quel language est principalement utilisé en machine learning ?",
    }
]
client = InferenceClient(
    provider="featherless-ai",
    model="mistralai/Mistral-7B-Instruct-v0.2",
    token=HF_TOKEN,
)

result = client.chat_completion(messages=messages, max_tokens=100)
print(result)
