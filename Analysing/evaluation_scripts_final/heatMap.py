
"""
 Script to generate interactive heatmaps of emoji usage by ideological score (e.g., V6/V8)
 using data from the SQLite database. Supports filtering by model, country, and prompt,
 normalizes emoji counts per score, and sorts emojis based on emotional ranking.
"""


# Import core libraries
import sqlite3
import pandas as pd
import plotly.express as px

# Import project-specific modules
from data.variables.models import MODELS
from utils.getUtlis import getDatabasePath
from utils.normalize_scores import normalize_emoji_counts_by_score
from utils.sort_emojis_emotionally import get_top25_nonflag_emoji_emotion_ranking
from utils.sort_flags import normalize_flags

# Function to generate an interactive heatmap of emoji frequencies by ideological score (e.g., V6 or V8)
def heatMapV8_plotly(
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

    # Optional SQL filters for model, prompt, and country
    model_filter = f'AND results.model = "{model_id}"' if model_id else ""
    prompt_filter = f'AND results.prompt_id != "{excluded_prompt_ids}"' if excluded_prompt_ids else ""
    country_filter = f'AND results.country = "{country_id}"' if country_id else ""

    # SQL query: join emoji responses with ideological scores
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

    # Load data into DataFrame and process score column
    df = pd.read_sql_query(query, conn)
    df["score"] = pd.to_numeric(df["score"], errors="coerce").round(2)
    conn.close()

    # Standardize flag emojis to one white flag
    df["emoji"] = df["emoji"].apply(normalize_flags)

    # Normalize emoji frequency distributions per score level
    norm_df = normalize_emoji_counts_by_score(df)
    norm_df["normalized_count"] = (norm_df["normalized_count"] * 100).round(0)# Scale to percentage with rounding


    # Limit to the top 10 most frequently used emojis (overall, unnormalized)
    top_emojis_raw = df["emoji"].value_counts().nlargest(10).index
    norm_df = norm_df[norm_df["emoji"].isin(top_emojis_raw)]

    # Reshape data: scores as rows, emojis as columns
    pivot_df = norm_df.pivot(index="score", columns="emoji", values="normalized_count").fillna(0)

    # Sort emoji columns based on predefined emotional ordering
    sentiment_order = get_top25_nonflag_emoji_emotion_ranking()
    valid_emojis = [e for e in sentiment_order if e in pivot_df.columns]
    pivot_df = pivot_df[sorted(valid_emojis, key=lambda e: sentiment_order[e])]

    # Create interactive heatmap using Plotly
    fig = px.imshow(
        pivot_df,
        labels=dict(x="Emoji", y="Ideology Score", color="pct(%)"),
        text_auto=".0f",
        color_continuous_scale="OrRd"
    )

    # Add plot title
    if model_id is None:
        model_name = "All Models"

    fig.update_layout(
        title=f"Emoji usage by {score_col} ({model_name})",
        xaxis_title="Emoji",
        yaxis_title="GPS Score",
        font=dict(size=25),
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

# Optional execution block to generate plots for all models or for a combined view
if __name__ == "__main__":
    # Uncomment to generate separate heatmaps per active model:
    # for model in MODELS:
    #     if model["active"]:
    #         heatMapV8_plotly(
    #             getDatabasePath(),
    #             model_name=model["name"],
    #             model_id=model["id"],
    #             score_col="V8_Scale",
    #             run_id="BETWEEN 9 AND 18"
    #         )

    # Default: generate one combined heatmap for all models
    heatMapV8_plotly(
        getDatabasePath(),
        score_col="V8_Scale",
        run_id="BETWEEN 9 AND 18"
    )
