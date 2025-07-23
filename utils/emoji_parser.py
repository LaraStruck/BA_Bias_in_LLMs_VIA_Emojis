# openrouter_api/emoji_parser.py
import json
from collections import Counter

import emoji

def extract_emojis(text: str) -> list:
    return [e["emoji"] for e in emoji.emoji_list(text)]

def is_emoticon(c):
    return len(c) == 1 and 0x1F600 <= ord(c) <= 0x1F637

def extract_emojis_text(text):
    return [char for char in text if char in emoji.EMOJI_DATA]

def count_emojis_by_group(df, group_col="score_group", emoji_col="emoji"):

    grouped = df.groupby(group_col)
    group_counts = {}

    for group, group_df in grouped:
        all_emojis = []
        for response in group_df[emoji_col].dropna().astype(str):
            all_emojis.extend(extract_emojis(response))
        group_counts[group] = Counter(all_emojis)

    return group_counts
