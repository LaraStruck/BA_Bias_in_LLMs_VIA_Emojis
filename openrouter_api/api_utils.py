import requests
from typing import Union, Dict, Any

from utils.getUtlis import getApiKey



def query_model(prompt: str, model: str) -> dict[str, dict[
    str, str | int]] | Any:
    headers = {
        "Authorization": f"Bearer {getApiKey()}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
    }
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        return response.json()
    except requests.HTTPError:
        return {
            "error": {
                "message": response.text,
                "status_code": response.status_code,
            }
        }
    except requests.RequestException as e:
        return {"error": {"message": str(e), "status_code": 500}}