
import sqlite3



def entry_exists(model, party_id, prompt_id, run_id, db_path):

    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()
        cursor.execute("""
            SELECT 1 FROM results
            WHERE model = ? AND party_id = ? AND prompt_id = ? AND run_id = ?
            LIMIT 1
        """, (model, party_id, prompt_id, run_id))
        return cursor.fetchone() is not None

