import sqlite3
import pandas as pd
import os

def load_data(
        db_path,
        table = "results",
        columns=None,
        where_clauses=None
):
    columns_str = ", ".join(columns) if columns else "*"
    query = f"SELECT {columns_str} FROM {table}"

    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)

    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
