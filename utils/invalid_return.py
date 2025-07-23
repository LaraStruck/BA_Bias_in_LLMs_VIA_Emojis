import json
import sqlite3

from utils.getUtlis import getDatabasePath


def get_retry_count(model, party_id, prompt_id, run_id):
    with sqlite3.connect(getDatabasePath()) as con:
        cursor = con.cursor()
        cursor.execute("""
            SELECT MAX(retry_count)
            FROM unvalid_results
            WHERE model = ? AND party_id = ? AND prompt_id = ? AND run_id = ?
        """, (model, party_id, prompt_id, run_id))
        result = cursor.fetchone()
        if result[0] is None:
            return 0  # erster Versuch
        return result[0]

def invalid_saved(model, party, prompt, run_id, emojis, text, response):

    if len(emojis) == 0 :
        error = "No emojis found"
    else:
        error = "Too many emojis found"

    from data.sql.invalid_saved.save_invalid_results import \
        save_invalid_results_sql
    save_invalid_results_sql(
        model=model["id"],
        party_id=party["id"],
        party_name=party["name"],
        country=party["country"],
        prompt_id=prompt["id"],
        run_id=run_id,
        emoji=emojis,
        full_answer=text,
        json_response=json.dumps(response),
        error_type= error
    )
    raise Exception("None or too many emojis found")

