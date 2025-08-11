# Core imports for math, database access, and counting
import math
import sqlite3
import os
from collections import Counter

# Data handling
import pandas as pd

# Local project imports
from utils.getUtlis import getDatabasePath
from data.variables.models import MODELS

"""

 Class for calculating Shannon entropy of emoji outputs from LLM responses.
 Used to measure diversity and unpredictability of emoji usage per run,
 and export these statistics as CSV files for further analysis.
"""
class EmojiEntropyAnalyzer:
    def __init__(self, run_range="BETWEEN 9 AND 18"):
        # Path to the SQLite database
        self.db_path = getDatabasePath()
        self.run_range = run_range

        # Placeholders for loaded and computed data
        self.df = None
        self.entropy_by_party = None
        self.entropy_by_model = None
        self.entropy_by_type = None
        self.entropy_party_overall = None

        # Only include models that are marked as active
        self.active_models = {m["id"] for m in MODELS if m.get("active", False)}

        # Create output directory if it doesn't exist
        self.output_dir = os.path.join( "Tables")
        os.makedirs(self.output_dir, exist_ok=True)

    def load_data(self):
        # Connect to the database and retrieve relevant emoji responses and metadata
        conn = sqlite3.connect(self.db_path)
        query = f"""
        SELECT 
            results.model,
            results.emoji,
            results.run_id,
            results.prompt_id,
            results.party_id,
            results.country,
            parties.Partyname AS party,
            parties.Type_Values
        FROM results
        JOIN parties ON results.party_id = parties.CPARTYABB
        WHERE results.emoji IS NOT NULL
          AND results.run_id {self.run_range}
          AND parties.Type_Values IN (1, 4)
        """
        df = pd.read_sql_query(query, conn)
        conn.close()

        # Filter to include only results from active models
        df = df[df["model"].isin(self.active_models)].copy()
        self.df = df
        print(f"[✓] {len(self.df)} emoji responses from active models loaded.")

    @staticmethod
    def calculate_entropy(emojis):
        # Calculate Shannon entropy of a list of emojis
        total = len(emojis)
        if total == 0:
            return 0.0
        counts = Counter(emojis)
        probs = [c / total for c in counts.values()]
        entropy = -sum(p * math.log2(p) for p in probs if p > 0)
        return round(entropy, 4)

    def compute_entropy(self):
        # Compute entropy per model, party, and prompt
        grouped = self.df.groupby(["model", "party", "prompt_id", "Type_Values"])["emoji"].apply(list).reset_index()
        grouped["entropy"] = grouped["emoji"].apply(self.calculate_entropy)
        self.entropy_by_party = grouped

        # Average entropy per model
        self.entropy_by_model = grouped.groupby("model")["entropy"].mean().reset_index(name="avg_entropy")

        # Average entropy per model, split by party type (left-progressive = 1, right-conservative = 4)
        self.entropy_by_type = grouped.groupby(["model", "Type_Values"])["entropy"].mean().reset_index()
        self.entropy_by_type["type_label"] = self.entropy_by_type["Type_Values"].map({
            1: "Left–Progressive", 4: "Right–Conservative"
        })

        # Overall entropy per party (aggregated across models)
        grouped_all = self.df.groupby(["party"])["emoji"].apply(list).reset_index()
        grouped_all["entropy"] = grouped_all["emoji"].apply(self.calculate_entropy)
        grouped_all = grouped_all.sort_values(by="entropy", ascending=False)
        self.entropy_party_overall = grouped_all

    def export(self, prefix="entropy"):
        # Export all computed tables to CSV inside 'Analysing/Tables'
        if self.entropy_by_party is not None:
            self.entropy_by_party.to_csv(os.path.join(self.output_dir, f"{prefix}_by_party_prompt.csv"), index=False)
        if self.entropy_by_model is not None:
            self.entropy_by_model.to_csv(os.path.join(self.output_dir, f"{prefix}_by_model.csv"), index=False)
        if self.entropy_by_type is not None:
            self.entropy_by_type.to_csv(os.path.join(self.output_dir, f"{prefix}_left_vs_right.csv"), index=False)
        if self.entropy_party_overall is not None:
            self.entropy_party_overall.to_csv(os.path.join(self.output_dir, f"{prefix}_by_party_overall.csv"), index=False)
        print("[✓] Results exported.")

    def run_full_analysis(self):
        # Full execution: load → compute → export
        self.load_data()
        self.compute_entropy()
        self.export()

# Main entry point to run the analysis when the file is executed directly
if __name__ == "__main__":
    analyzer = EmojiEntropyAnalyzer()
    analyzer.run_full_analysis()
