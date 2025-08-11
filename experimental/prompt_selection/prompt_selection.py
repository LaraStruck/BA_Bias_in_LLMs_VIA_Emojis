from Analysing.utils.plot_emojis_count import plot_emojis_by_group_count
import sqlite3
from utils.emoji_parser import count_emojis_by_group
from utils.getUtlis import getDatabasePath
from utils.sort_emojis_emotionally import \
    get_top25_nonflag_emoji_emotion_ranking

database = getDatabasePath()

def prepare_plot_df(group_counts, top_n=5):
    relevant_emojis = set()
    for group in group_counts:
        relevant_emojis.update([e for e, _ in group_counts[group].most_common(top_n)])

    sentiment_order = get_top25_nonflag_emoji_emotion_ranking()
    relevant_emojis = sorted(relevant_emojis, key=lambda e: sentiment_order.get(e, 999))

    rows = []
    for group in group_counts:
        for emoji_char in relevant_emojis:
            count = group_counts[group].get(emoji_char, 0)
            rows.append({
                "Emoji": emoji_char,
                "Count": count,
                "Group": group
            })

    return pd.DataFrame(rows)

def load_results_with_prompts(db_path):
    conn = sqlite3.connect(db_path)
    query = """
    SELECT emoji, prompt_id, run_id
    FROM results
    WHERE emoji IS NOT NULL AND run_id BETWEEN 9 and 18 AND prompt_id != 'SimpleShort_05' AND prompt_id != 'SimpleShort_Switched_06' AND prompt_id != 'based_on_frequency_patterns_unicode_01'

    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

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


if __name__ == "__main__":
    df = load_results_with_prompts(database)
    group_counts = count_emojis_by_group(df, group_col="prompt_id", emoji_col="emoji")
    df_plot = prepare_plot_df(group_counts, top_n=5)
    print (df_plot)
    count_emoji_stats(
            df_plot,
            emoji_col="Emoji",
            group_col="Group")
    plot_emojis_by_group_count(
            df_plot,
            emoji_col="Emoji",
            group_col="Group",
            top_n=5,
            title="Top 5 Emojis by Prompt"
        )
