import sqlite3
import pandas as pd
from collections import Counter

from Analysing.utils.plot_emojis import plot_emojis_by_group
from data.variables.models import MODELS
from utils.emoji_parser import count_emojis_by_group
from utils.getUtlis import getDatabasePath
from utils.sort_flags import normalize_flags
from utils.sort_emojis_emotionally import get_top25_nonflag_emoji_emotion_ranking

# Load database path
database = getDatabasePath()

# Prepare the DataFrame for plotting: filters, groups, normalizes and labels data
def prepare_plot_df(group_counts, top_n=10, model_name=""):
    # Collect the most common emojis from each group
    relevant_emojis = set()
    for group in group_counts:
        relevant_emojis.update([e for e, _ in group_counts[group].most_common(top_n)])

    # Sort selected emojis based on a predefined emotional ranking
    sentiment_order = get_top25_nonflag_emoji_emotion_ranking()
    relevant_emojis = sorted(relevant_emojis, key=lambda e: sentiment_order.get(e, 999))

    rows = []
    for group in group_counts:
        total = sum(group_counts[group].values())  # Total emoji count for normalization
        for emoji_char in relevant_emojis:
            count = group_counts[group].get(emoji_char, 0)
            rows.append({
                "Emoji": emoji_char,
                "Count": count / total if total > 0 else 0,  # Normalize per group
                "Group": group.capitalize(),
                "Model": model_name
            })

    return pd.DataFrame(rows)

# Load emoji data and assign ideological labels using Type_Values
def load_data_with_value_typology(db_path, model_id=None, run_id="9", country_id=None):
    conn = sqlite3.connect(db_path)
    model_filter = f'AND results.model = "{model_id}"' if model_id else ""
    country_filter = f'AND results.country = "{country_id}"' if country_id else ""

    # Type_Values is a discrete classification (e.g., 1 = left, 4 = right)
    query = f"""
    SELECT 
        results.emoji,
        parties.Type_Values AS type_values,
        results.run_id,
        results.model
    FROM results
    JOIN parties ON results.party_id = parties.CPARTYABB
    WHERE results.emoji IS NOT NULL 
          AND parties.Type_Values IS NOT NULL 
          AND (results.run_id {run_id})
          {model_filter}
          {country_filter}
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Assign simplified group labels (this could be renamed depending on country)
    df["score_group"] = df["type_values"].apply(
        lambda x: "Democrats" if x == 1 else ("Republicans" if x == 4 else None)
    )
    return df.dropna(subset=["score_group"])

# Load data and split into groups based on score blocks (e.g. V8: 1–10)
def load_data_with_score_blocks(db_path, model_id=None, run_id="9", country_id=None):
    conn = sqlite3.connect(db_path)
    model_filter = f'AND results.model = "{model_id}"' if model_id else ""
    country_filter = f'AND results.country = "{country_id}"' if country_id else ""

    query = f"""
    SELECT 
        results.emoji,
        parties.V4_Scale AS score,
        results.run_id,
        results.model
    FROM results
    JOIN parties ON results.party_id = parties.CPARTYABB
    WHERE results.emoji IS NOT NULL 
          AND parties.V8_Scale IS NOT NULL 
          AND (results.run_id {run_id})
          {model_filter}
          {country_filter}
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Normalize flags for consistent emoji representation
    df["emoji"] = df["emoji"].apply(normalize_flags)

    # Convert numerical score into broad ideological grouping
    df["score_group"] = df["score"].apply(
        lambda x: "normal" if x <= 5 else "populistic"
    )
    return df

# Wrapper function for plotting bar charts from grouped emoji data
def plot_typology(df, model_name="", top_n=10, title_suffix="", country_id=None):
    group_counts = count_emojis_by_group(df, group_col="score_group", emoji_col="emoji")
    df_plot = prepare_plot_df(group_counts, top_n=top_n, model_name=model_name)
    if country_id is None:
        country_id = ""
    plot_emojis_by_group(
        df_plot,
        emoji_col="Emoji",
        group_col="Group",
        top_n=top_n,
        title=f"Top {top_n} Emojis by {title_suffix} {model_name} {country_id}"
    )

# Example execution for U.S. parties
if __name__ == "__main__":
    # To run the script for ALL models, uncomment the following block:
    # for model in MODELS:
    #     if model["active"]:
    #         df_typology = load_data_with_value_typology(database, model_id=model["id"], run_id="BETWEEN 9 AND 18")
    #         plot_typology(df_typology, model_name=model["name"], top_n=10, title_suffix="Typology")

    # This example only plots the grouped emoji distribution for U.S. parties
    df_typology = load_data_with_value_typology(database, country_id="United States", run_id="BETWEEN 9 AND 18")
    plot_typology(df_typology, top_n=10, title_suffix="Typology", country_id="United States")

    # Alternatively, you can plot score-based groupings like V6 or V8:
    # df_score_blocks = load_data_with_score_blocks(database, country_id="United States", run_id="BETWEEN 9 AND 18")
    # plot_typology(df_score_blocks, country_id="United States", top_n=10, title_suffix="V8 Left vs Right (no center)")
