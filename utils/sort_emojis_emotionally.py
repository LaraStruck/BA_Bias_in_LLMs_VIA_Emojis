def get_top25_nonflag_emoji_emotion_ranking():
    """
    Returns a dictionary mapping emojis to a combined valence–arousal category.
    Categories:
    1 = highly positive, high arousal (e.g. joyful, euphoric)
    2 = positive, calm (e.g. satisfied)
    3 = symbolic affection (e.g. hearts)
    4 = neutral / thoughtful
    5 = slightly negative, sad
    6 = annoyed / frustrated
    7 = angry
    8 = extremely angry / hostile
    9 = gestures (hands, arms)
    10 = green/environmental
    11 = other symbolic/political or neutral
    """
    return {
        "🥳": 1,
        "😄": 1,
        "😂": 1,
        "😎": 1,
        "😊": 2,
        "🙂": 2,
        "😇": 2,
        "❤️": 3,
        "💙": 3,
        "🧡": 3,
        "💚": 3,
        "❤️‍🔥": 3,
        "🤔": 4,
        "🧐": 4,
        "😐": 4,
        "😢": 5,
        "😞": 5,
        "😔": 5,
        "☹️": 5,
        "😭": 5,
        "😤": 6,
        "😠": 7,
        "😡": 8,
        "🤬": 8,
        "💪": 9,
        "✊": 9,
        "🤝": 9,
        "🤞": 9,
        "👍": 9,
        "🌱": 10,
        "🌿": 10,
        "🌳": 10,
        "🍁": 10,
        "🌎": 10,
        "🏳️": 11,
        "🏴": 11,
        "🗳️": 11,
        "🚀": 11,
        "🔥": 11,
        "🔴": 11,
        "⚫": 11

    }
