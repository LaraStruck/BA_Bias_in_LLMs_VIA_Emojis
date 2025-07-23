import sqlite3
import pandas as pd
import plotly.express as px
from utils.getUtlis import getDatabasePath
from utils.sort_flags import normalize_flags
from utils.sort_emojis_emotionally import get_top25_nonflag_emoji_emotion_ranking


def emoji_focus_by_score_share(db_path, score_col="V6_Scale", model_id=None, excluded_prompt_ids=None, run_id="8", country_id=None, model_name=None):
    conn = sqlite3.connect(db_path)

    model_filter = f'AND results.model = "{model_id}"' if model_id else ""
    prompt_filter = f'AND results.prompt_id != "{excluded_prompt_ids}"' if excluded_prompt_ids else ""
    country_filter = f'AND results.country = "{country_id}"' if country_id else ""

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
              AND (results.run_id {run_id})
              {prompt_filter}
              {model_filter}
              {country_filter}
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    # Round score to whole numbers for block grouping (e.g. 2, 4, 6...)
    df["score"] = pd.to_numeric(df["score"], errors="coerce").round().astype("Int64")
    df["emoji"] = df["emoji"].apply(normalize_flags)

    # Count how often each emoji appears at each rounded score
    emoji_counts = df.groupby(["emoji", "score"]).size().reset_index(name="count")

    # Total count per emoji
    emoji_totals = emoji_counts.groupby("emoji")["count"].sum().reset_index(name="total")

    # Merge and calculate relative share per emoji across scores
    merged = pd.merge(emoji_counts, emoji_totals, on="emoji")
    # Häufigkeit jedes Scores im Gesamt-Datensatz (nicht pro Emoji!)
    score_freq = df["score"].value_counts(normalize=True).to_dict()  # relative Häufigkeit

    # Anteil pro Emoji (wie bisher)
    merged["share_per_emoji"] = merged["count"] / merged["total"]

    # Gewichtung je Score: seltene Scores = stärker gewichtet
    merged["score_weight"] = merged["score"].map(lambda s: 1 / score_freq.get(s, 1))

    # Gewichtete Emoji-Verteilung
    merged["weighted_share"] = merged["share_per_emoji"] * merged["score_weight"]
    # Top 10 emojis by raw total (not normalized)
    top_emojis = (
        df["emoji"].value_counts()
        .nlargest(10)
        .index
    )
    merged = merged[merged["emoji"].isin(top_emojis)]

    # Pivot table: scores (y), emojis (x)
    pivot_df = merged.pivot(index="score", columns="emoji", values="weighted_share").fillna(0)

    # Sort emojis emotionally
    sentiment_order = get_top25_nonflag_emoji_emotion_ranking()
    valid_emojis = [e for e in sentiment_order if e in pivot_df.columns]
    pivot_df = pivot_df[sorted(valid_emojis, key=lambda e: sentiment_order[e])]

    # Plot
    fig = px.imshow(
        pivot_df,
        labels=dict(x="Emoji", y="GPS Score", color="Emoji Share"),
        text_auto=".2f",
        color_continuous_scale="OrRd",
        aspect="auto"
    )

    if not model_name:
        model_name = model_id or "All Models"

    fig.update_layout(
        title=f"Emoji usage distribution over – {model_name}  {score_col}",
        xaxis_title="Emoji",
        yaxis_title="GPS Score",
        font=dict(size=28),
        xaxis_tickfont_size=36,
        yaxis_tickfont_size=20,
        margin=dict(t=50, b=80, l=100, r=40)
    )

    fig.show()


if __name__ == "__main__":
    from data.variables.models import MODELS
    for model in MODELS:
        if model["active"]:
            emoji_focus_by_score_share(
                getDatabasePath(),
                model_name=model["name"],
                model_id=model["id"],
                score_col="Type_Values",
                run_id="BETWEEN 9 AND 18"
            )
