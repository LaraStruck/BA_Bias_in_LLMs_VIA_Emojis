import pandas as pd

def normalize_emoji_counts_by_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalisiert Emoji-Häufigkeiten pro gerundetem Score-Wert (in df["score"]).
    Gibt für jede Emoji–Score-Kombination den relativen Anteil an allen Emojis dieser Gruppe zurück.

    Voraussetzungen:
        - df muss die Spalten "emoji" und "score" enthalten
        - score ist numerisch (z. B. aus V6_Scale)

    Returns:
        pd.DataFrame mit Spalten: score (int), emoji, normalized_count
    """

    # Stelle sicher, dass score numerisch und gerundet ist
    df["score"] = pd.to_numeric(df["score"], errors="coerce").round().astype("Int64")

    # 1. Emoji-Zählung pro Score
    emoji_counts = df.groupby(["score", "emoji"]).size().reset_index(name="count")

    # 2. Gesamtanzahl Emojis pro Score
    total_counts = df.groupby("score").size().reset_index(name="total")

    # 3. Merge + Normalisierung
    merged = pd.merge(emoji_counts, total_counts, on="score")
    merged["normalized_count"] = merged["count"] / merged["total"]

    # 4. Sortierung nach Score-Wert (aufsteigend)
    merged = merged.sort_values("score")

    # 5. Rückgabe
    return merged[["score", "emoji", "normalized_count"]]


def normalize_by_model(df):
    emoji_counts = df.groupby(["model", "emoji"]).size().reset_index(name="count")
    total_counts = df.groupby("model").size().reset_index(name="total")
    merged = pd.merge(emoji_counts, total_counts, on="model")
    merged["normalized_count"] = merged["count"] / merged["total"]
    return merged[["model", "emoji", "normalized_count"]]
