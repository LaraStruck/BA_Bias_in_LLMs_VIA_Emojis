import csv
import os
from datetime import datetime

def save_results_to_csv(model, party_id, party_name, country, prompt_id, emojis, full_response, file_path="data/emoji_results.csv"):
    file_exists = os.path.exists(file_path)

    with open(file_path, "a", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        if not file_exists:
            writer.writerow([
                "Modell", "Partei-ID", "Partei-Name", "Land",
                "Prompt-ID", "Emoji", "Unicode", "Antwort", "Zeitstempel"
            ])

        for emoji_char in emojis:
            unicode_repr = ",".join([hex(ord(c)) for c in emoji_char])
            writer.writerow([
                model,
                party_id,
                party_name,
                country,
                prompt_id,
                emoji_char,
                unicode_repr,
                full_response,
                datetime.now().isoformat()
            ])
