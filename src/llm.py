from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

client = OpenAI()

CHAT_MODEL = "gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-small"


def get_chat_completion(messages, temperature=0.2):
    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=messages,
        temperature=temperature,
    )

    return response.choices[0].message.content


def get_embedding(text: str):
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text,
    )

    return response.data[0].embedding