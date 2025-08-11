import pandas as pd
import plotly.express as px

# Same function as plot_emojis_by_group but with raw emoji counts for prompt selection
def plot_emojis_by_group_count(
        df,
        emoji_col="Emoji",
        group_col="Group",
        top_n=5,
        title="Emoji Frequency by Group",
        output_file=None,
        color_map=None):
    """
    Plots grouped bar chart using raw emoji counts (not percentages).

    Parameters:
        df (pd.DataFrame): DataFrame with emoji counts.
        emoji_col (str): Column name for emoji symbols.
        group_col (str): Column name for group labels (e.g., prompt_id).
        top_n (int): Number of top emojis per group to show.
        title (str): Plot title.
        output_file (str): Optional path to save as HTML.
        color_map (dict): Optional dict for custom group colors.
    """
    # Select top-N emojis per group
    top_emojis = set()
    for group in df[group_col].unique():
        top = df[df[group_col] == group].nlargest(top_n, "Count")
        top_emojis.update(top[emoji_col])

    df_filtered = df[df[emoji_col].isin(top_emojis)]
    # Plot
    fig = px.bar(
        df_filtered,
        x=emoji_col,
        y="Count",
        color=group_col,
        barmode="group",
        title=title,
        color_discrete_map=color_map
    )

    fig.update_layout(
        font=dict(size=18),
        xaxis_tickfont_size=30,
        yaxis_title="Emoji Count",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )

    if output_file:
        fig.write_html(output_file)
    fig.show()
