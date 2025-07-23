import sqlite3
import pandas as pd

from Analysing.utils.plot_emojis import plot_emojis_by_group
from data.variables.models import MODELS
from utils.emoji_parser import count_emojis_by_group
from utils.getUtlis import getDatabasePath
from utils.sort_flags import normalize_flags

database = getDatabasePath()



def prepare_plot_df(group_counts, top_n=5):
    relevant_emojis = set()
    for group in group_counts:
        relevant_emojis.update([e for e, _ in group_counts[group].most_common(top_n)])

    rows = []
    for group in group_counts:
        for emoji_char in relevant_emojis:
            count = group_counts[group].get(emoji_char, 0)
            rows.append({
                "Emoji": emoji_char,
                "Count": count,
                "Group": group.capitalize()
            })

    return pd.DataFrame(rows)

def load_data_with_score_grouping(db_path, score_col="V6_Scale", threshold=None, model_id=None, run_id = "9", country_id = "United States"):
    conn = sqlite3.connect(db_path)

    # Lade Scores zum Median-Berechnen
    score_df = pd.read_sql_query(f"SELECT {score_col} FROM parties WHERE {score_col} IS NOT NULL", conn)
    if threshold is None:
        threshold = score_df[score_col].median()
    model_filter = f'AND results.model = "{model_id}"' if model_id else ""
    query = f"""
    SELECT 
        results.emoji,
        parties.{score_col} AS score,
        results.run_id,
        results.model
    FROM results
    JOIN parties ON results.party_id = parties.CPARTYABB
    WHERE results.emoji IS NOT NULL 
            AND parties.{score_col} IS NOT NULL 
            AND (results.run_id = {run_id})
            {model_filter}
            AND results.country = "{country_id}"
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Score in Gruppen einteilen
    df["score_group"] = df["score"].apply(lambda x: "progressive" if x < threshold else "conservative")
    return df



def compare_spectrum(model_id = None,
                     run_id=" 9 OR results.run_id = 10 OR results.run_id = 11 OR results.run_id = 12 OR results.run_id = 13",
                     score_col = "V6_Scale",
                     top_n = 10,
                     country_id = "United States"):

        df = load_data_with_score_grouping(database, score_col=score_col, model_id = model_id, run_id = run_id, country_id=country_id)  # oder "v2x_polyarchy" etc.
        df["emoji"] = df["emoji"].apply(normalize_flags)
        group_counts = count_emojis_by_group(df, group_col="score_group", emoji_col="emoji")
        df_plot = prepare_plot_df(group_counts, top_n=top_n)

        plot_emojis_by_group(
            df_plot,
            emoji_col="Emoji",
            group_col="Group",
            top_n=top_n,
            title="Top " + str(top_n) + " Emojis by "  + score_col + str(model_id)
        )

if __name__ == "__main__":
    for model in MODELS:
        if model["active"]:
            compare_spectrum( model_id=model["id"], score_col="V6_Scale")
