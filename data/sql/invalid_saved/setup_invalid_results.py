
import sqlite3

from utils.getUtlis import getCSVPath, getDatabasePath

DB_PATH = getDatabasePath()

def create_tables():
    with sqlite3.connect(DB_PATH) as con:
        con.execute("DROP TABLE IF EXISTS invalid_results")
        con.execute("""
        CREATE TABLE IF NOT EXISTS invalid_results (
            model TEXT,
            party_id TEXT,
            party_name TEXT,
            country TEXT,
            prompt_id TEXT,
            run_id INTEGER,
            retry_count INTEGER,
            emoji TEXT, 
            unicode TEXT, 
            full_answer TEXT,
            json TEXT,
            timestamp TEXT,
            error_type TEXT,
            PRIMARY KEY (model, party_id, prompt_id, run_id, retry_count)
        );

        """)
        print("✅ Tabelle 'invalid_results' wurde erstellt.")

if __name__ == "__main__":
    create_tables()

