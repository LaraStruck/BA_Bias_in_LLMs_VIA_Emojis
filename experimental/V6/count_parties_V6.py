import sqlite3
from utils.getUtlis import getDatabasePath

def count():
    db_path = getDatabasePath()

    # SQL-Abfrage zur Gruppenzählung
    query = """
    SELECT
        SUM(CASE WHEN V6_Scale < 5 THEN 1 ELSE 0 END) AS progressive_count,
        SUM(CASE WHEN V6_Scale >= 5 THEN 1 ELSE 0 END) AS conservative_count,
        COUNT(*) AS total
    FROM parties
    WHERE V6_Scale IS NOT NULL;
    """

    # DB-Verbindung und Abfrage
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()

    # Ergebnisse anzeigen
    progressive, conservative, total = result
    print(f"Progressive Parteien (<5):   {progressive}")
    print(f"Conservative Parteien (≥5): {conservative}")
    print(f"Gesamtanzahl:               {total}")

import pandas as pd

def count_parties_per_v6_group(df, v6_column="V6_Scale"):
    # In Float umwandeln, falls nötig
    df[v6_column] = df[v6_column].astype(float)

    # Runde Score auf ganze Zahl (1–10)
    df["v6_group"] = df[v6_column].apply(lambda x: round(x))

    # Zähle eindeutige Parteien pro Gruppe
    party_counts = df.groupby("v6_group")["party_id"].nunique().reset_index()
    party_counts.columns = ["V6_Group", "Number_of_Parties"]

    return party_counts

if __name__ == "__main__":
    count()