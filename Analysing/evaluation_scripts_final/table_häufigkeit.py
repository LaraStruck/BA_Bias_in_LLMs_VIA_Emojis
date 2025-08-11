import sqlite3
import pandas as pd
from utils.getUtlis import getDatabasePath

def parteien_pro_score(db_path, score_col="V6_Scale"):
    conn = sqlite3.connect(db_path)

    # Hole jede Partei genau einmal mit zugehörigem Score (ohne Join mit Emoji-Tabelle!)
    query = f"""
        SELECT DISTINCT CPARTYABB, {score_col} AS score
        FROM parties
        WHERE {score_col} IS NOT NULL
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    # Score runden auf ganze Werte (z. B. 6.3 → 6)
    df["score"] = pd.to_numeric(df["score"], errors="coerce").round().astype("Int64")

    # Zähle Anzahl der Parteien pro Score
    score_counts = df["score"].value_counts().sort_index().reset_index()
    score_counts.columns = ["Score", "Anzahl Parteien"]

    # Ausgabe
    print(score_counts.to_string(index=False))
    return score_counts

# Beispiel-Aufruf
if __name__ == "__main__":
    parteien_pro_score(getDatabasePath(), score_col="V8_Scale")
