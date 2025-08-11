

"""
Counts the number of political parties per specified ideological score (e.g., V6 or V8)
from the `parties` table in the SQLite database. The function retrieves each party once,
rounds scores to the nearest integer, and outputs both a printed table and a DataFrame
of party counts per score.
"""


import sqlite3
import pandas as pd
from utils.getUtlis import getDatabasePath

def parteien_pro_score(db_path, score_col="V6_Scale"):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)

    # Retrieve each party only once, along with the selected score column
    # (no join with the emoji results table to avoid duplicates)
    query = f"""
        SELECT DISTINCT CPARTYABB, {score_col} AS score
        FROM parties
        WHERE {score_col} IS NOT NULL
    """

    # Load query results into a pandas DataFrame
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Convert score to numeric, round to the nearest integer (e.g., 6.3 → 6),
    # and store as nullable integer type (Int64) to allow missing values
    df["score"] = pd.to_numeric(df["score"], errors="coerce").round().astype("Int64")

    # Count how many parties fall into each score value
    score_counts = df["score"].value_counts().sort_index().reset_index()
    score_counts.columns = ["Score", "Number of Parties"]

    # Print the counts in a readable table format
    print(score_counts.to_string(index=False))

    # Return the DataFrame with score counts
    return score_counts

# Example usage: count parties per score for V8 scale
if __name__ == "__main__":
    parteien_pro_score(getDatabasePath(), score_col="V8_Scale")
