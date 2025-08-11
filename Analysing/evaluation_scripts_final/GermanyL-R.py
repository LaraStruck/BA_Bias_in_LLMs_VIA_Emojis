# Import core modules
import sqlite3
import pandas as pd
from collections import Counter

# Import project-specific utility functions and configuration
from Analysing.utils.plot_emojis import plot_emojis_by_group
from data.variables.models import MODELS
from utils.emoji_parser import count_emojis_by_group
from utils.getUtlis import getDatabasePath
from utils.sort_flags import normalize_flags
from utils.sort_emojis_emotionally import get_top25_nonflag_emoji_emotion_ranking

# Define fixed color mapping for selected German parties (used for plotting)
PARTY_COLORS = {
    "Alliance 90/The Greens": "#64A12D",
    "Alternative for Germany ": "#009EE0",
    "Christian Democratic Union": "#000000",
    "Christian Social Union in Bavaria": "#999999",
    "Free Democratic Party": "#FFED00",
    "Social Democratic Party": "#E3000F",
    "The Left": "#B4006E"
}

# Load database path
database = getDatabasePath()

# Prepare plot DataFrame by selecting and normalizing top emojis per group (party)
def prepare_plot_df(group_counts, top_n=10, model_name=""):
    relevant_emojis = set()
    for group in group_counts:
        relevant_emojis.update([e for e, _ in group_counts[group].most_common(top_n)])

    # Sort emojis based on emotional ranking (e.g. 😊 before 😡)
    sentiment_order = get_top25_nonflag_emoji_emotion_ranking()
    relevant_emojis = sorted(relevant_emojis, key=lambda e: sentiment_order.get(e, 999))

    rows = []
    for group in group_counts:
        total = sum(group_counts[group].values())
        for emoji_char in relevant_emojis:
            count = group_counts[group].get(emoji_char, 0)
            rows.append({
                "Emoji": emoji_char,
                "Percentage (%)": count / total if total > 0 else 0,  # relative frequency
                "Group": group,  # party name
                "Model": model_name
            })

    return pd.DataFrame(rows)

# Load emoji results for a specific model and country, filtered by party name
def load_data_by_party(db_path, model_id=None, run_id="9", country_id=None):
    conn = sqlite3.connect(db_path)

    # Apply optional SQL filters
    model_filter = f'AND results.model = "{model_id}"' if model_id else ""
    country_filter = f'AND results.country = "{country_id}"' if country_id else ""

    # Include only selected German parties
    party_ids = (
        "Alliance 90/The Greens",
        "Alternative for Germany ",
        "Christian Democratic Union",
        "Christian Social Union in Bavaria",
        "Free Democratic Party",
        "Social Democratic Party",
        "The Left"
    )
    party_filter = f"AND parties.Partyname IN ({','.join('?' for _ in party_ids)})"

    # SQL query to load relevant data
    query = f"""
    SELECT 
        results.emoji,
        parties.Partyname AS party,
        results.run_id,
        results.model
    FROM results
    JOIN parties ON results.party_id = parties.CPARTYABB
    WHERE results.emoji IS NOT NULL 
          AND (results.run_id {run_id})
          {model_filter}
          {country_filter}
          {party_filter}
    """

    df = pd.read_sql_query(query, conn, params=party_ids)
    conn.close()

    # Each party becomes a group for aggregation
    df["group"] = df["party"]
    return df

# Plot top emojis per party using consistent colors and normalized frequencies
def plot_by_party(df, model_name="", top_n=10, title_suffix="", country_id=None):
    group_counts = count_emojis_by_group(df, group_col="group", emoji_col="emoji")
    df_plot = prepare_plot_df(group_counts, top_n=top_n, model_name=model_name)

    # Set plot title and labels
    if country_id is None:
        country_id = ""

    plot_emojis_by_group(
        df_plot,
        emoji_col="Emoji",
        group_col="Group",
        top_n=top_n,
        title=f"Top {top_n} Emojis by Party – {model_name} {country_id}",
        color_map=PARTY_COLORS
    )

# Main execution: loop over all active models and create one plot per model
if __name__ == "__main__":
    for model in MODELS:
        if model["active"]:
            df = load_data_by_party(
                database,
                run_id=" BETWEEN 9 AND 18",
                country_id="Germany",
                model_id=model["id"]
            )
            plot_by_party(
                df,
                model_name=model["name"],
                top_n=5,
                title_suffix="(German Parties)",
                country_id="Germany"
            )
