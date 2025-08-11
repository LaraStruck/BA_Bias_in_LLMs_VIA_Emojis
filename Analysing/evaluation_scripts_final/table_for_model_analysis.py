
"""
 Script to generate a summary table of emoji usage per model.
 Loads valid and invalid emoji responses from the SQLite database (filtered by run_id and party type),
 normalizes flags, and computes metrics such as:
 - number of valid/invalid responses
 - number of unique emojis
 - number of frequently used emojis (>= 40 occurrences)
 Results are saved as CSV in the 'Tables' directory.
 Note, that flags are normalized to a base emoji, e.g., '🇺🇸' -> '🏳️' and are not
 included in the unique emoji count.
"""
import sqlite3
import pandas as pd
from collections import Counter

from utils.getUtlis import getDatabasePath
from utils.sort_flags import normalize_flags

model_rename = {
    "openai/gpt-4.1-nano": "GPT-4.1",
    "meta-llama/llama-4-maverick": "LLaMA-4",
    "deepseek/deepseek-r1-0528-qwen3-8b": "DeepSeek",
    "google/gemini-2.5-flash-preview-05-20": "Gemini-2.5",
    "mistralai/mistral-small-3.1-24b-instruct": "Mistral",
    "x-ai/grok-3-beta": "Grok-3",
}

def generate_emoji_summary(db_path, run_id="BETWEEN 9 AND 18"):
    conn = sqlite3.connect(db_path)

    # Load valid emoji responses
    query = f"""
        SELECT results.emoji, results.model, parties.Type_Values AS type_values
        FROM results
        JOIN parties ON results.party_id = parties.CPARTYABB
        WHERE results.emoji IS NOT NULL
          AND results.model IS NOT NULL
          AND results.run_id {run_id}
          AND parties.Type_Values IN (1, 4)
    """
    df = pd.read_sql_query(query, conn)
    df["emoji"] = df["emoji"].apply(normalize_flags)
    df["group"] = df["type_values"].apply(lambda x: "left" if x == 1 else "right")

    # Load invalid responses
    invalid_query = f"""
        SELECT model
        FROM invalid_results
        WHERE model IS NOT NULL
          AND run_id {run_id}
    """
    invalid_df = pd.read_sql_query(invalid_query, conn)
    invalid_counts = Counter(invalid_df["model"])
    conn.close()

    # Prepare summary
    rows = []
    for model in sorted(df["model"].unique()):
        df_model = df[df["model"] == model]
        top5 = df_model["emoji"].value_counts().nlargest(5)
        rare_count = (df_model["emoji"].value_counts() >= 40).sum()
        row = {
            "Model": model_rename.get(model, model),
            "Valid Responses": len(df_model),
            "Invalid Responses": invalid_counts.get(model, 0),
            "Unique Emojis": df_model["emoji"].nunique(),
            "Frequent emojis (>=40)": rare_count,
        }
        rows.append(row)

    result_df = pd.DataFrame(rows)
    result_df.to_csv("Tables/emoji_typology_summary.csv", index=False)
    return result_df

if __name__ == "__main__":
    db_path = getDatabasePath()
    df_summary = generate_emoji_summary(db_path) # run_id can be changed, now 9-18
    print(df_summary)
