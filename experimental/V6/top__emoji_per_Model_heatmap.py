import sqlite3

import pandas as pd
import plotly.express as px
from data.variables.models import MODELS
from utils.getUtlis import getDatabasePath
from utils.sort_emojis_emotionally import \
    get_top25_nonflag_emoji_emotion_ranking


def emoji_score_distribution_percent_plot(db_path, score_col="V6_Scale", model_id=None, excluded_prompt_ids=None, run_id="8", country_id=None):
    """
    Displays a heatmap of the top 15 most frequent emojis used by a given model,
    showing the relative frequency (%) of each emoji across ideological score groups (1–10).
    """

    from utils.sort_flags import normalize_flags

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
              AND (results.run_id = {run_id} )
              {prompt_filter}
              {model_filter}
              {country_filter}
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    df["score"] = pd.to_numeric(df["score"], errors="coerce").round(0).astype("Int64")
    df["emoji"] = df["emoji"].apply(normalize_flags)

    # Bestimme Top-15 Emojis für das Modell (nicht global)
    top_emojis = df["emoji"].value_counts().nlargest(15).index
    df = df[df["emoji"].isin(top_emojis)]

    # Absolute Zählung
    count_df = df.groupby(["score", "emoji"]).size().reset_index(name="count")

    # Gesamtsumme je Score-Gruppe (für Prozentrechnung)
    total_per_score = count_df.groupby("score")["count"].sum().reset_index(name="total")
    merged = count_df.merge(total_per_score, on="score")
    merged["percentage"] = merged["count"] / merged["total"]

    # Pivot zur Darstellung
    pivot_df = merged.pivot(index="score", columns="emoji", values="percentage").fillna(0)

    sentiment_order = get_top25_nonflag_emoji_emotion_ranking()
    valid_emojis = [e for e in sentiment_order if e in pivot_df.columns]

    # Pivot für Heatmap

    pivot_df = pivot_df[sorted(valid_emojis, key=lambda e: sentiment_order[e])]

    # Plot
    fig = px.imshow(
        pivot_df,
        labels=dict(x="Emoji", y="Ideology Score", color="percentage"),
        text_auto=".2f",
        color_continuous_scale="OrRd"
    )

    title_model = model_id if model_id else "All Models"
    fig.update_layout(
        title=f"Emoji-Verteilung nach Score (prozentual, Modell: {title_model})",
        xaxis_title="Emoji",
        yaxis_title="GPS Score",
        font=dict(size=30),
        xaxis_tickfont_size=50,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.19,
            xanchor="center",
            x=0.2
        )
    )

    fig.show()


if __name__ == "__main__":
    for model in MODELS:
        if model["active"]:
            emoji_score_distribution_percent_plot(getDatabasePath(), model_id=model["id"],  score_col="V6_Scale", run_id=" 9 OR results.run_id = 10 OR results.run_id = 11 OR results.run_id = 12 OR results.run_id = 13 OR results.run_id = 14 OR results.run_id = 15 OR results.run_id = 16 OR results.run_id = 17 OR results.run_id = 18")