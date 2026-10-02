from google import genai
from google.genai import types

from app.config import settings


class GeminiServiceError(RuntimeError):
    pass


def generate_text(
    prompt: str,
    model: str,
    temperature: float = 0.7
) -> str:

    if settings.mock_ai:

        return ""


    if not settings.gemini_api_key:

        raise GeminiServiceError(
            "GEMINI_API_KEY is not configured. "
            "Add it to .env or use MOCK_AI=true."
        )


    try:

        client = genai.Client(
            api_key=settings.gemini_api_key
        )


        response = client.models.generate_content(

            model=model,

            contents=prompt,

            config=types.GenerateContentConfig(

                temperature=temperature,

                max_output_tokens=5000,

                candidate_count=1
            )
        )


        text = getattr(
            response,
            "text",
            None
        )


        if not text:

            raise GeminiServiceError(
                "Gemini returned an empty response."
            )


        return text.strip()


    except GeminiServiceError:

        raise


    except Exception as exc:

        raise GeminiServiceError(
            f"Gemini request failed: {exc}"
        ) from exc