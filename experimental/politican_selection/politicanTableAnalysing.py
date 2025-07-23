import pandas as pd
import spacy

# Lade das englische spaCy-Modell
nlp = spacy.load("en_core_web_sm")

def extract_first_person(text: str) -> str:
    doc = nlp(str(text))
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text.strip()
    return "UNKNOWN"  # fallback wenn nichts erkannt


def run_analysis():
    df = pd.read_csv("politician_results.csv")
    df.columns = ["Model", "Country", "Alignment", "Politician", "Rank"]

    # ✨ spaCy-basierte Bereinigung: erste erkannte Person pro Zelle extrahieren
    df["Politician"] = df["Politician"].apply(extract_first_person)

    most_common_politicians = (
        df.groupby(["Country", "Alignment", "Politician"])
        .size()
        .reset_index(name="Count")
    )

    most_common_politicians = most_common_politicians.sort_values(
        by=["Country", "Alignment", "Count"], ascending=[True, True, False]
    )

    top_n = (
        most_common_politicians.groupby(["Country", "Alignment"])
        .head(5)
        .reset_index(drop=True)
    )

    top_n.to_csv("top_politicians_by_country_and_alignment.csv", index=False)
    print(top_n)


if __name__ == "__main__":
    run_analysis()
