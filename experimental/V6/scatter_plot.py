import sqlite3
import pandas as pd
import plotly.express as px

from utils.getUtlis import getDatabasePath
from utils.normalize_scores import normalize_emoji_counts_by_score


def scatter_emojis_as_text(db_path, score_col="V6_Scale",
                           model_id=None,
                           excluded_prompt_ids=None,
                           run_id= "9 OR results.run_id = 10 OR results.run_id = 11 OR results.run_id = 12 OR results.run_id = 13",
                           unicode="'0x1f621' OR results.unicode = '0x1f620' OR results.unicode = '0x1f60a'"):
    """
    Plots emojis as text (without circles) across ideological GPS scores.
    """
    from utils.sort_flags import normalize_flags

    conn = sqlite3.connect(db_path)

    model_filter = f'AND results.model = "{model_id}"' if model_id else ""
    prompt_filter = f'AND results.prompt_id != "{excluded_prompt_ids}"' if excluded_prompt_ids else ""

    query = f"""
        SELECT 
            results.emoji,
            parties.{score_col} AS score,
            results.run_id,
            results.model,
            results.unicode
        FROM results
        JOIN parties ON results.party_id = parties.CPARTYABB
        WHERE results.emoji IS NOT NULL 
              AND parties.{score_col} IS NOT NULL 
              AND results.run_id = {run_id}
              AND results.unicode = {unicode}
              {prompt_filter}
              {model_filter}
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Round scores and normalize flag emojis
    df["score"] = df["score"].round(0).astype(int)
    df["emoji"] = df["emoji"].apply(normalize_flags)

    # Keep top N emojis
    top_emojis = df["emoji"].value_counts().nlargest(3).index
    df = df[df["emoji"].isin(top_emojis)]

    # Group by ideology score and emoji
    df = df.groupby(["score", "emoji"]).size().reset_index(name="count")

    # Plot with Plotly, emojis as text (no circles)
    df["y"] = df["count"]  # vertical positioning = frequency
    fig = px.scatter(
        df,
        x="score",
        y="y",
        text="emoji"
    )

    fig.update_traces(
        marker=dict(size=1, opacity=0),
        textposition='middle center',
        textfont_size=28
    )

    fig.update_layout(
        title="Emoji usage by ideology score",
        xaxis_title="GPS Score",
        yaxis_title="Emoji Frequency",
        showlegend=False,
        margin=dict(l=30, r=30, t=60, b=30)
    )

    fig.show()


if __name__ == "__main__":
    scatter_emojis_as_text(getDatabasePath())
