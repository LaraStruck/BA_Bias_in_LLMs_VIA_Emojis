import sqlite3
import pandas as pd
from collections import Counter
from data.variables.models import MODELS
from utils.getUtlis import getDatabasePath
from utils.sort_flags import normalize_flags

def average_score_top_emojis_per_model(db_path, score_col="V6_Scale", run_id="9", top_n=5):
    conn = sqlite3.connect(db_path)
    all_results = []

    for model in MODELS:
        if not model.get("active", False):
            continue
        model_id = model["id"]

        query = f"""
            SELECT 
                results.emoji,
                parties.{score_col} AS score
            FROM results
            JOIN parties ON results.party_id = parties.CPARTYABB
            WHERE results.emoji IS NOT NULL
              AND parties.{score_col} IS NOT NULL
              AND results.model = ?
              AND results.run_id = {run_id}
        """

        df = pd.read_sql_query(query, conn, params=(model_id,))
        df["score"] = pd.to_numeric(df["score"], errors="coerce").round(2)
        df["emoji"] = df["emoji"].apply(normalize_flags)

        # Top-N Emojis
        top_emojis = Counter(df["emoji"]).most_common(top_n)
        top_emoji_set = {e for e, _ in top_emojis}
        filtered = df[df["emoji"].isin(top_emoji_set)]

        # Durchschnitt berechnen
        avg_df = filtered.groupby("emoji")["score"].agg(["mean", "count"]).reset_index()
        avg_df["model"] = model_id
        avg_df.rename(columns={"mean": "average_score"}, inplace=True)

        all_results.append(avg_df)

    conn.close()
    return pd.concat(all_results, ignore_index=True)

if __name__ == "__main__":
    db_path = getDatabasePath()
    df = average_score_top_emojis_per_model(db_path,
                                            score_col="V6_Scale",
                                            run_id=" 9 OR results.run_id = 10 OR results.run_id = 11 OR results.run_id = 12 OR results.run_id = 13",
                                            top_n=5)
    print(df)