import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-3.5-flash-lite"

SYSTEM_PROMPT = "You are a friendly assistant. Keep answers short and clear."

def get_reply(history: list[dict], new_message: str) -> str:

    contents = []
    for m in history:
        contents.append(
            types.Content(role=m["role"], parts=[types.Part(text=m["content"])])
        )
    contents.append(
        types.Content(role="user", parts=[types.Part(text=new_message)])
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=contents,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
    )
    return response.text

# if __name__ == "__main__":
#     history = [
#         {"role": "user", "content": "My name is Samyam."},
#         {"role": "model", "content": "Nice to meet you, Samyam!"},
#     ]
#     print(get_reply(history, "What is my name?"))


