import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    max_retries=3,
    timeout=30.0
)


def generate_answer(prompt):
    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            input=prompt
        )
        return response.output_text

    except Exception as error:
        print(f"Answer generation failed: {error}")
        raise