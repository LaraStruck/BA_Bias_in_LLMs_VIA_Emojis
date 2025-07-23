import sqlite3
import pandas as pd
import plotly.express as px
from data.variables.models import MODELS
from utils.getUtlis import getDatabasePath
from utils.normalize_scores import normalize_emoji_counts_by_score
from utils.sort_emojis_emotionally import get_top25_nonflag_emoji_emotion_ranking
from utils.sort_flags import normalize_flags
import webbrowser
import plotly.io as pio

def delta_heatmap_by_model(db_path, score_col="V6_Scale", run_id="8", top_n_emojis=15, country_id= None):
    conn = sqlite3.connect(db_path)
    TypeValuesFilter = ""
    if score_col == "Type_Values":
        TypeValuesFilter = "AND (parties.Type_Values IS NOT 2 OR parties.Type_Values IS NOT 3)"


    country_filter = f'AND results.country = "{country_id}"' if country_id else ""
    query = f"""
        SELECT 
            results.emoji,
            parties.{score_col} AS score,
            results.model,
            results.run_id
        FROM results
        JOIN parties ON results.party_id = parties.CPARTYABB
        WHERE results.emoji IS NOT NULL 
              AND parties.{score_col} IS NOT NULL 
              AND ({run_id})
              {TypeValuesFilter}
              {country_filter}
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    df["score"] = pd.to_numeric(df["score"], errors="coerce").round(2)
    df["emoji"] = df["emoji"].apply(normalize_flags)

    norm_df = normalize_emoji_counts_by_score(df)

    # Modell-Information aus Original-DataFrame wieder mergen
    norm_df = norm_df.merge(df[["emoji", "score", "model"]], on=["emoji", "score"], how="left")

    # Optional: Top N Emojis auswählen
    top_emojis = (
        norm_df.groupby("emoji")["normalized_count"]
        .sum()
        .nlargest(top_n_emojis)
        .index
    )
    norm_df = norm_df[norm_df["emoji"].isin(top_emojis)]

    # Pivot nach Modell und Emoji (umgedreht für horizontale Darstellung)
    pivot_df = norm_df.pivot_table(index="model", columns="emoji", values="normalized_count", aggfunc="mean", fill_value=0)

    # Mittelwert aller Modelle je Emoji
    mean_emoji_use = pivot_df.mean(axis=0)

    # Delta berechnen: Modellnutzung minus Durchschnitt
    delta_df = pivot_df.subtract(mean_emoji_use, axis=1)

    # Optional sortieren
    sentiment_order = get_top25_nonflag_emoji_emotion_ranking()
    valid_emojis = [e for e in sentiment_order if e in delta_df.columns]
    delta_df = delta_df[sorted(valid_emojis, key=lambda e: sentiment_order[e])]

    # Optional: Modellnamen kürzen für bessere Darstellung
    model_rename = {
        "openai/gpt-4.1-nano": "GPT-4.1",
        "meta-llama/llama-4-maverick": "LLaMA-4",
        "deepseek/deepseek-r1-0528-qwen3-8b": "DeepSeek",
        "google/gemini-2.5-flash-preview-05-20": "Gemini-2.5",
        "mistralai/mistral-small-3.1-24b-instruct": "Mistral",
        "x-ai/grok-3-beta": "Grok-3",
    }

    delta_df.index = delta_df.index.to_series().replace(model_rename)

    # Responsive Darstellung im Browser mit automatischer Größe
    fig = px.imshow(
        delta_df,
        labels=dict(x="Emoji", y="Model", color="Δ to avg."),
        text_auto=".2f",
        color_continuous_scale="RdBu",
        zmin=-0.06,
        zmax=0.06
    )

    fig.update_layout(
        title="Emoji Delta per Model",
        xaxis_title="Emoji",
        yaxis_title="Model",
        autosize=True,
        font=dict(size=24),
        xaxis_tickfont=dict(size=32),
        yaxis_tickfont=dict(size=18),
        margin=dict(t=50, b=80, l=100, r=40)
    )

    # In Browser öffnen mit automatischer Fenstergröße
    html_file = "delta_heatmap.html"
    pio.write_html(fig, file=html_file, auto_open=True, full_html=True)

if __name__ == "__main__":
    delta_heatmap_by_model(getDatabasePath(), run_id="results.run_id BETWEEN 9 AND 18", score_col="Type_Values", country_id = "United States")
