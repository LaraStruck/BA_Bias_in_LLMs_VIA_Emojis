import pandas as pd

def load_parties(csv_path):
    """
    Load filtered party data and convert to a list of dictionaries
    with keys: id (CPARTYABB), name (Partyname), country (Country)
    """
    df = pd.read_csv(csv_path)
    required_cols = {"CPARTYABB", "Partyname", "Country"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"CSV is missing one of the required columns: {required_cols}")

    return [
        {
            "id": row["CPARTYABB"],
            "name": row["Partyname"],
            "country": row["Country"]
        }
        for _, row in df.iterrows()
    ]
