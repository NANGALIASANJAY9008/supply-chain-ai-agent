import os

from dotenv import load_dotenv


load_dotenv()


def test_groq_api_key_exists():

    api_key = os.getenv(
        "GROQ_API_KEY"
    )

    assert api_key is not None

    assert len(api_key) > 0