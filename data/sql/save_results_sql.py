# storage_sql.py
import sqlite3
from pathlib import Path
from datetime import datetime

from utils.getUtlis import getDatabasePath


def save_results_sql(model, party_id, party_name, country,
                     prompt_id,run_id, emojis, full_answer , json_response):
    print("💾 Speichern aufgerufen:", model, party_id, prompt_id, emojis)
    with sqlite3.connect(getDatabasePath()) as con:

        for emoji in emojis:
            unicode_repr = ",".join(hex(ord(c)) for c in emoji)
            try:
                con.execute("""
                INSERT INTO results (
                    model, party_id, party_name, country,
                    prompt_id,run_id, emoji, unicode, full_answer, json, timestamp
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
                """, (
                    model, party_id, party_name, country,
                    prompt_id, run_id, emoji, unicode_repr, full_answer, json_response,
                    datetime.now().isoformat()
                ))
            except sqlite3.IntegrityError:
                print("""⚠️ Did not save, probably already exists: Modell: {}, Partei-ID: {}, Prompt-ID: {}, Emoji: {}""".format(model, party_id, prompt_id, emoji))
                pass
            except Exception as e:
                print(f"❌ Fehler beim Speichern: {e}")


