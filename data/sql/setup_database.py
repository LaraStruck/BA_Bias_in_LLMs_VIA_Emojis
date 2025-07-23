# setup_database.py
import sqlite3
import pandas as pd
from pathlib import Path

from utils.getUtlis import  getDatabasePath, getPartiesCSV

DB_PATH = getDatabasePath()


def create_tables():
    with sqlite3.connect(DB_PATH) as con:
        con.execute("DROP TABLE IF EXISTS results")
        con.execute("""
        CREATE TABLE IF NOT EXISTS results (
            model       TEXT,
            party_id    TEXT,
            party_name  TEXT,
            country     TEXT,
            prompt_id   TEXT,
            run_id      INTEGER,
            emoji       TEXT,
            unicode     TEXT,
            full_answer TEXT,
            json    TEXT,
            timestamp   TEXT,
            PRIMARY KEY (model, party_id, prompt_id, run_id)
        )
        """)
        print("✅ Tabelle 'results' wurde erstellt.")

def import_parties(csv_path):
    df = pd.read_csv(csv_path)
    with sqlite3.connect(DB_PATH) as con:
        df.to_sql("parties", con, if_exists="replace", index=False)
        print("✅ Parteitabelle wurde importiert.")

if __name__ == "__main__":
    create_tables()
    import_parties(getPartiesCSV())  # Pfad anpassen
