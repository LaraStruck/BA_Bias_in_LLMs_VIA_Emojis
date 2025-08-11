# Import core libraries
import sqlite3
import pandas as pd
import plotly.express as px

# Import project-specific modules
from data.variables.models import MODELS
from utils.getUtlis import getDatabasePath
from utils.sort_emojis_emotionally import get_top25_nonflag_emoji_emotion_ranking
from utils.sort_flags import normalize_flags

# New normalization function: Score distribution per emoji
def normalize_score_counts_by_emoji(df):
    grouped = df.groupby(["emoji", "score"]).size().reset_index(name="count")
    totals = grouped.groupby("emoji")["count"].transform("sum")
    grouped["normalized_count"] = grouped["count"] / totals
    return grouped

# Function to generate an interactive heatmap: Score distribution per emoji
def heatMapScorePerEmoji_plotly(
        db_path,
        score_col="V8_Scale",
        model_id=None,
        excluded_prompt_ids=None,
        run_id="BETWEEN 9 AND 18",
        country_id=None,
        model_name=None
):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)

    # Optional SQL filters
    model_filter = f'AND results.model = "{model_id}"' if model_id else ""
    prompt_filter = f'AND results.prompt_id != "{excluded_prompt_ids}"' if excluded_prompt_ids else ""
    country_filter = f'AND results.country = "{country_id}"' if country_id else ""

    # Query: get emoji + score per result
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
              AND (results.run_id {run_id} )
              {prompt_filter}
              {model_filter}
              {country_filter}
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    # Round scores to whole numbers for clearer axis
    df["score"] = pd.to_numeric(df["score"], errors="coerce").round(0).astype("Int64")

    # Normalize flags (e.g. unify all flag variants to white flag or similar)
    df["emoji"] = df["emoji"].apply(normalize_flags)

    # Normalize: per emoji
    norm_df = normalize_score_counts_by_emoji(df)

    # Optional: Limit to top 10 emojis overall
    top_emojis_raw = df["emoji"].value_counts().nlargest(10).index
    norm_df = norm_df[norm_df["emoji"].isin(top_emojis_raw)]

    # Pivot: score as rows, emoji as columns
    pivot_df = norm_df.pivot(index="score", columns="emoji", values="normalized_count").fillna(0)

    # Sort emoji columns by predefined emotional order
    sentiment_order = get_top25_nonflag_emoji_emotion_ranking()
    valid_emojis = [e for e in sentiment_order if e in pivot_df.columns]
    pivot_df = pivot_df[sorted(valid_emojis, key=lambda e: sentiment_order[e])]

    # Plot: emoji on x-axis, score on y-axis
    fig = px.imshow(
        pivot_df,
        labels=dict(x="Emoji", y="GPS Score", color="Proportion"),
        text_auto=".2f",
        color_continuous_scale="OrRd"
    )

    if model_id is None:
        model_name = "All Models"

    fig.update_layout(
        title=f"Score distribution per Emoji ({model_name})",
        xaxis_title="Emoji",
        yaxis_title="GPS Score",
        font=dict(size=25),
        xaxis_tickfont_size=25,
        yaxis_tickfont_size=25,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )

    fig.show()

# Optional run
if __name__ == "__main__":
    heatMapScorePerEmoji_plotly(
        getDatabasePath(),
        score_col="V8_Scale",
        run_id="BETWEEN 9 AND 18"
    )
