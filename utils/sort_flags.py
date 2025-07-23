import re

def normalize_flags(emoji: str, replacement: str = "🏳️") -> str:
    """
    Ersetzt Flaggen-Emojis durch ein einheitliches Symbol.
    """
    # Flaggen bestehen aus zwei regional indicator symbols: 🇦🇹, 🇺🇸, etc.
    if re.match(r'^[\U0001F1E6-\U0001F1FF]{2}$', emoji):
        return replacement
    return emoji
