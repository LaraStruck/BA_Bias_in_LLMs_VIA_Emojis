import csv
import os
import json
import spacy  # neu
from data.variables.models import MODELS
from openrouter_api.api_utils import query_model

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

def run_selection():
    spectrums = {
        "progressive": "as progressive",
        "conservative": "as conservative",
        "centrist": "as centrist"
    }

    countries = ["Germany", "USA", "Russia", "China"]
    output_file = "politician_results.csv"

    file_exists = os.path.exists(output_file)

    with open(output_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["Model", "Country", "Spectrum", "PoliticianName", "Position"])

        for model in MODELS:
            if not model.get("active", False):
                continue

            model_id = model["id"]
            model_name = model["name"]

            for country in countries:
                for key, label in spectrums.items():
                    prompt_text = f"Name five well-known politicians from {country} associated {label}. Only list the politicians' names and nothing else!"
                    print(f"\n→ [{model_name}] {prompt_text}")

                    try:
                        response = query_model(prompt_text, model=model_id)

                        if isinstance(response, str):
                            response = json.loads(response)

                        if "choices" in response:
                            content = response["choices"][0]["message"]["content"]
                        elif "error" in response:
                            raise ValueError(f"API Error: {response['error']['message']}")
                        else:
                            raise ValueError("Unexpected response format from API.")

                        print("Response:")
                        print(content)

                        # ✨ spaCy: Politiker extrahieren
                        politician_names = extract_politicians(content)

                        for i, name in enumerate(politician_names):
                            writer.writerow([model_name, country, key, name, i + 1])

                    except Exception as e:
                        print(f"❌ Error for model {model_name} | {country} ({key}): {e}")

if __name__ == "__main__":
    run_selection()
    print("\nDone! Results saved to 'politician_results.csv'")
