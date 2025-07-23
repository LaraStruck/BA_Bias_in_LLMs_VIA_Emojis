from collections import Counter
from Analysing.utils.data_loader import load_data
from Analysing.utils.plot_emojis import plot_top_emojis
from data.variables.models import MODELS
from utils.emoji_parser import extract_emojis
from utils.getUtlis import getDatabasePath
from utils.sort_flags import normalize_flags

database = getDatabasePath()
def count_emojis(responses):
    all_emojis = []
    for response in responses:
        all_emojis.extend(extract_emojis(response))
    return Counter(all_emojis)


def total_emoji_count(model):

            model_id = model["id"]
            df = load_data(
                db_path=database,
                table="results",
                columns=["emoji"],
                where_clauses=["emoji IS NOT NULL AND run_id BETWEEN 9 AND 18 AND model =" + "'" + model_id + "'"],
            )

            # Emojis extrahieren und zählen
            df["emoji"] = df["emoji"].apply(normalize_flags)
            responses = df["emoji"].astype(str).tolist()
            emoji_counter = count_emojis(responses)

            # Ausgabe in Konsole
            print("Top 10 häufigste Emojis:")
            for emoji_char, freq in emoji_counter.most_common(10):
                print(f"{emoji_char} : {freq} mal")

            # Plot anzeigen
            plot_top_emojis(emoji_counter, top_n=10, title=f"Top 10 Emojis " + model["name"])
