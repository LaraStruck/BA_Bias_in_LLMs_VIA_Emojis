# storage_sql.py
import json
import sqlite3
from pathlib import Path
from datetime import datetime

from utils.entry_exists import entry_exists
from utils.getUtlis import getDatabasePath


def save_invalid_results_sql(model, party_id, party_name, country,
                     prompt_id, run_id, emoji, full_answer, json_response,
                     error_type=None):
    print(f"💾 Saving attempt  for {model} | {party_id} | {prompt_id}")
    emoji = emoji or []
    emoji_str = json.dumps(emoji, ensure_ascii=False)  # für später auswertbar
    unicode_repr = json.dumps([hex(ord(c)) for emoji in emoji for c in emoji])

    with sqlite3.connect(getDatabasePath()) as con:
        if entry_exists(model, party_id, prompt_id, run_id, getDatabasePath()):
            from utils.invalid_return import get_retry_count
            retry_count = get_retry_count(model, party_id, prompt_id, run_id) + 1
        else:
            retry_count = 0
        try:
            con.execute("""
            INSERT INTO invalid_results (
                model, party_id, party_name, country,
                prompt_id, run_id, retry_count, emoji, unicode,
                full_answer, json, timestamp, error_type
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                model, party_id, party_name, country,
                prompt_id, run_id, retry_count, emoji_str, unicode_repr,
                full_answer, json_response, datetime.now().isoformat(), error_type
            ))
        except sqlite3.IntegrityError:
            print(f"⚠️ Retry {retry_count} already exists → skipping")
        except Exception as e:
            print(f"❌ Error saving to DB: {e}")
