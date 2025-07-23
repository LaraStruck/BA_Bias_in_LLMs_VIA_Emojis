from data.variables import models
from main import prompt
from openrouter_api.api_utils import query_model
import spacy


def safe_query_model(prompt, model_id):
    response = query_model(prompt, model_id)
    try:
        return response["choices"][0]["message"]["content"]
    except KeyError:
        if "error" in response:
            return f"❌ Fehler ({response['error'].get('type', 'unknown')}): {response['error']['message']}"
        else:
            return "❌ Unbekannter Fehler, Antwort enthält kein 'choices' und keine 'error'-Info."

# Verwendung:
content = safe_query_model(prompt, models["id"])
print(content)

# Lade englisches spaCy-Modell (für Politiker aus USA, Russland etc. geeignet)
nlp = spacy.load("en_core_web_sm")

def extract_politicians(text):
    doc = nlp(text)
    names = [ent.text.strip() for ent in doc.ents if ent.label_ == "PERSON"]
    # Optional: Duplikate und leere Strings filtern
    seen = set()
    clean_names = []
    for name in names:
        lower = name.lower()
        if lower not in seen and name:
            clean_names.append(name)
            seen.add(lower)
    return clean_names
