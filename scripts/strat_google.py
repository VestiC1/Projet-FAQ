from google import genai
from config import GEMINI_TOKEN

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client(api_key=GEMINI_TOKEN)

response = client.models.generate_content(
    model="gemini-2.5-flash-lite", contents="What is the difference between deepval and RAGAS"
)
print(response.text)