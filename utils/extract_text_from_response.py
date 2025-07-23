from typing import Union


def extract_text_from_response(response: dict) -> Union[str, None]:
    """
    Extrahiert intelligent den Antworttext aus einem unbekannten Modell-Response.
    Funktioniert für OpenAI, Mistral, Targon, DeepSeek etc.
    """
    def find_text(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, str) and len(value.strip()) > 0:
                    # Heuristik: vermeide Felder wie 'id', 'model', etc.
                    if key.lower() in ["content", "text", "completion", "response", "message"]:
                        return value.strip()
                elif isinstance(value, (dict, list)):
                    result = find_text(value)
                    if result:
                        return result
        elif isinstance(obj, list):
            for item in obj:
                result = find_text(item)
                if result:
                    return result
        return None

    return find_text(response)
