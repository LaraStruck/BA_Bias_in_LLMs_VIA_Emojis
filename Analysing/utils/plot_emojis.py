import pandas as pd
import plotly.express as px

def plot_top_emojis(emoji_counter, top_n=10, title="Top Emojis", output_file=None):
    """
    Plots a bar chart of the top N emojis from a Counter object.

    Parameters:
        emoji_counter (collections.Counter): Counted emojis
        top_n (int): Number of top emojis to plot
        title (str): Chart title
        output_file (str): Optional HTML file to save the plot
    """
    top = emoji_counter.most_common(top_n)
    emojis, counts = zip(*top)
    df = pd.DataFrame({"Emoji": emojis, "Count": counts})

    fig = px.bar(df, x="Emoji", y="Count", color="Emoji", title=title)
    fig.update_layout(font=dict(size=31), xaxis_tickfont_size=70, yaxis_title="Frequency")

    if output_file:
        fig.write_html(output_file)
    fig.show()


def plot_emojis_by_group(
        df,
        emoji_col="Emoji",
        group_col="Spectrum",
        top_n=5,
        title="Emoji Comparison by Group",
        output_file=None,
        color_map=None):

    # Optional: filter top N emojis per group
    top_emojis = set()
    for group in df[group_col].unique():
        top = df[df[group_col] == group].nlargest(top_n, "Percentage (%)")
        top_emojis.update(top[emoji_col])

    df_filtered = df[df[emoji_col].isin(top_emojis)]

    fig = px.bar(df_filtered, x=emoji_col, y="Percentage (%)", color=group_col, barmode="group", title=title, color_discrete_map=color_map)
    fig.update_layout(font=dict(size=20),
                      xaxis_tickfont_size=30,
                        legend=dict(
                            orientation="h",          # horizontal statt vertikal
                            yanchor="top",            # verankert an der Oberkante der Legende
                            y=-0.19,                   # Position unterhalb des Plots
                            xanchor="center",         # zentriert
                            x=0.2                   # horizontal zentriert
                            )
                      )

    if output_file:
        fig.write_html(output_file)
    fig.show()
