import os
from openai import OpenAI
from config import OPENAI_BASE_URL

_api_key = os.environ.get("OPENROUTER_API_KEY")

def create_openai_client() -> OpenAI:
    if _api_key is None:
        raise RuntimeError("OPENROUTER_API_KEY is not set.")

    return OpenAI(
        base_url=OPENAI_BASE_URL,
        api_key=_api_key,
    )
