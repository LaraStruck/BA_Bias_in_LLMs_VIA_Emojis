import sqlite3
import pandas as pd
import plotly.express as px
from data.variables.models import MODELS
from utils.getUtlis import getDatabasePath
from utils.sort_emojis_emotionally import get_top25_nonflag_emoji_emotion_ranking
from utils.sort_flags import normalize_flags
import plotly.io as pio

def delta_absolute_count_heatmap(db_path, run_id="8", sort_by="sum"):
    top_n_emojis = 10
    conn = sqlite3.connect(db_path)

    query = f"""
        SELECT 
            results.emoji,
            results.model,
            results.run_id
        FROM results
        WHERE results.emoji IS NOT NULL
              AND {run_id}
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    df["emoji"] = df["emoji"].apply(normalize_flags)

    # Absolute Emoji-Zählung pro Modell
    count_df = df.groupby(["model", "emoji"]).size().reset_index(name="count")

    # Emoji-Auswahl: Top-N nach Gesamthäufigkeit
    if sort_by == "sum":
        top_emojis = (
            count_df.groupby("emoji")["count"]
            .sum()
            .nlargest(top_n_emojis)
            .index
        )
        count_df = count_df[count_df["emoji"].isin(top_emojis)]

    # Pivot: Modelle = Zeilen, Emojis = Spalten, Werte = Häufigkeit
    pivot_df = count_df.pivot(index="model", columns="emoji", values="count").fillna(0)

    # Mittelwert aller Modelle je Emoji berechnen
    mean_emoji_use = pivot_df.mean(axis=0)

    # Delta = Abweichung von Emoji-Mittelwert
    delta_df = pivot_df.subtract(mean_emoji_use, axis=1)

    # Emoji-Auswahl nach Varianz (optional)
    if sort_by == "var":
        emoji_selector = delta_df.var(axis=0).nlargest(top_n_emojis).index
        delta_df = delta_df[emoji_selector]

    # Sortiere Emojis nach emotionaler Reihenfolge
    sentiment_order = get_top25_nonflag_emoji_emotion_ranking()
    valid_emojis = [e for e in sentiment_order if e in delta_df.columns]
    delta_df = delta_df[sorted(valid_emojis, key=lambda e: sentiment_order[e])]

    # Optional: Modellnamen kürzen
    model_rename = {
        "openai/gpt-4.1-nano": "GPT-4.1",
        "meta-llama/llama-4-maverick": "LLaMA-4",
        "deepseek/deepseek-r1-0528-qwen3-8b": "DeepSeek",
        "google/gemini-2.5-flash-preview-05-20": "Gemini-2.5",
        "mistralai/mistral-small-3.1-24b-instruct": "Mistral",
        "x-ai/grok-3-beta": "Grok-3",
    }
    delta_df.index = delta_df.index.to_series().replace(model_rename)

    # Plot
    fig = px.imshow(
        delta_df,
        labels=dict(x="Emoji", y="Model", color="Δ to avg."),
        text_auto=".0f",  # ganze Zahlen anzeigen
        color_continuous_scale="RdBu",
        color_continuous_midpoint=0,
        aspect="auto"
    )

    fig.update_layout(
        title="Emoji Count Δ per Model (absolute usage)",
        xaxis_title="Emoji",
        yaxis_title="Model",
        font=dict(size=24),
        xaxis_tickfont=dict(size=32),
        yaxis_tickfont=dict(size=18),
        margin=dict(t=50, b=80, l=100, r=40)
    )

    html_file = "delta_heatmap_absolute.html"
    pio.write_html(fig, file=html_file, auto_open=True, full_html=True)

if __name__ == "__main__":
    delta_absolute_count_heatmap(getDatabasePath(), run_id="results.run_id BETWEEN 9 AND 18", sort_by="sum")
