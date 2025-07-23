import plotly.express as px
import pandas as pd

def plot_emojis_as_text(df, x_col="avg_score", emoji_col="emoji", count_col="count"):
    """
    Plots emojis as text on a horizontal axis based on their average ideology score.

    Parameters:
        df (pd.DataFrame): DataFrame containing at least 'avg_score' and 'emoji' columns.
        x_col (str): Name of the column representing x-axis values (e.g., average ideology score).
        emoji_col (str): Name of the column containing emojis to be displayed.
        count_col (str): Optional column for size or frequency info (not visualized here).
    """
    df = df.copy()
    df["y"] = 0  # place all emojis on the same horizontal level

    fig = px.scatter(
        df,
        x=x_col,
        y="y",
        text=emoji_col,
    )

    fig.update_traces(
        marker=dict(size=1, opacity=0),  # hide markers
        textposition="middle center",
        textfont_size=28
    )

    fig.update_layout(
        title="Emoji mapped to average GPS score",
        showlegend=False,
        yaxis=dict(showticklabels=False, title=None, zeroline=False),
        xaxis_title="Ø GPS Score",
        height=400,
        margin=dict(l=40, r=40, t=60, b=40)
    )

    fig.show()
