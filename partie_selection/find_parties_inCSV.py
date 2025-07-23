import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def find_parties_in_csv(csv_path, selected_countries):
    df = pd.read_csv(csv_path)

    # Filter by selected countries
    filtered_df = df[df["Country"].isin(selected_countries)]
    filtered_df = filtered_df[df["Type_Partysize_vote"].isin(["2", "3"])]



    # Drop rows without complete scores
    required_columns = [
        "CPARTYABB",
        "Country",
        "Partyname",
        "V6_Scale",
        "V6_Ord",
        "V4_Scale",
        "V8_Scale",
        "V8_Ord",
        "Type_Values",
        "Type_Populism",
        "Type_Populist_Values",
        "Type_Partysize_vote"
    ]




    filtered_df_complete = filtered_df.dropna(subset=required_columns)

    # Keep only relevant columns with exact names for joining
    output_df = filtered_df_complete[[
        "CPARTYABB",
        "Country",
        "Partyname",
        "V6_Scale",
        "V6_Ord",
        "V4_Scale",
        "V8_Scale",
        "V8_Ord",
        "Type_Values",
        "Type_Populism",
        "Type_Populist_Values",
        "Type_Partysize_vote"

    ]].copy()

    output_df.to_csv("filtered_parties_with_scores_preStudy.csv", index=False)
    print("✅ Exported filtered CSV with aligned column names for joining.")

if __name__ == "__main__":
    csv_path = os.getenv("CSV_PATH")
    selected_countries = [ "Germany", "France", "United States", "United Kingdom" ,"Canada", "Italy", "Spain", "Chile", "Australia", "Poland", "Austria", "Japan"] #  "Brazil" ,
    find_parties_in_csv(csv_path, selected_countries)