import pandas as pd

def count_emoji_stats(df, group_col="prompt_id", emoji_col="emoji"):
    stats = []

    for group, group_df in df.groupby(group_col):
        total = len(group_df)
        valid = group_df[emoji_col].apply(lambda e: isinstance(e, str) and len(e.strip()) > 0).sum()
        unique = group_df[emoji_col].nunique()
        avg_count = group_df[emoji_col].apply(lambda x: len(x.strip()) if isinstance(x, str) else 0).mean()

        stats.append({
            "Prompt ID": group,
            "Total Responses": total,
            "Valid Emojis": valid,
            "Unique Emojis": unique,
            "Avg. Emoji Count per Response": round(avg_count, 2)
        })

    return pd.DataFrame(stats)

    df_stats = count_emoji_stats(df)
    print(df_stats)
