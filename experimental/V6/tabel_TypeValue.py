import sqlite3
import pandas as pd

from utils.getUtlis import getDatabasePath
from utils.sort_flags import normalize_flags
from utils.sort_emojis_emotionally import get_top25_nonflag_emoji_emotion_ranking
from data.variables.models import MODELS

# ────────────────────────────────────────────────────────────────────────────────
# MODEL RENAME MAP
# ────────────────────────────────────────────────────────────────────────────────
model_rename = {
    "openai/gpt-4.1-nano": "GPT-4.1",
    "meta-llama/llama-4-maverick": "LLaMA-4",
    "deepseek/deepseek-r1-0528-qwen3-8b": "DeepSeek",
    "google/gemini-2.5-flash-preview-05-20": "Gemini-2.5",
    "mistralai/mistral-small-3.1-24b-instruct": "Mistral",
    "x-ai/grok-3-beta": "Grok-3",
}

# ────────────────────────────────────────────────────────────────────────────────
# DATA LOADER (Typology 1 vs 4)
# ────────────────────────────────────────────────────────────────────────────────

def load_typology_for_models(db_path: str, run_id: str = "BETWEEN 9 AND 18") -> pd.DataFrame:
    """Load emoji data for all *active* models with Type_Values 1 and 4."""
    conn = sqlite3.connect(db_path)
    query = f"""
        SELECT 
            results.emoji,
            parties.Type_Values AS type_values,
            results.model,
            results.party_id
        FROM results
        JOIN parties ON results.party_id = parties.CPARTYABB
        WHERE results.emoji IS NOT NULL
          AND parties.Type_Values IN (1, 4)
          AND results.run_id {run_id}
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    df = df[df["model"].isin([m["id"] for m in MODELS if m["active"]])]
    df["emoji"] = df["emoji"].apply(normalize_flags)
    df["group"] = df["type_values"].apply(lambda x: "left_liberal" if x == 1 else "right_conservative")
    df["model"] = df["model"].apply(lambda m: model_rename.get(m, m))
    return df

# ────────────────────────────────────────────────────────────────────────────────
# TAB 1 ‑ DESKRIPTIVTABELLE
# ────────────────────────────────────────────────────────────────────────────────

def create_descriptive_table(df: pd.DataFrame, save_path: str = "descriptive_overview.csv") -> pd.DataFrame:
    """Return & save per‑model descriptive stats.

    Columns:
        Model | Parties_Left | Parties_Right | Emojis_Left | Emojis_Right | Total_Emojis
    """
    # Unique Parteien pro Modell & Gruppe
    parties = df.groupby(["model", "group"])["party_id"].nunique().unstack(fill_value=0)
    parties.columns = [f"Parties_{col.title()}" for col in parties.columns]

    # Emoji‑Zeilen pro Modell & Gruppe
    emojis = df.groupby(["model", "group"]).size().unstack(fill_value=0)
    emojis.columns = [f"Emojis_{col.title()}" for col in emojis.columns]

    # Kombinieren + Gesamtspalte
    descript = parties.join(emojis)
    descript["Total_Emojis"] = descript[["Emojis_Left_Liberal", "Emojis_Right_Conservative"]].sum(axis=1)
    descript = descript.reset_index().rename(columns={"model": "Model"})

    descript.to_csv(save_path, index=False)
    print(f"Saved descriptive table to {save_path}")
    return descript

# ────────────────────────────────────────────────────────────────────────────────
# COMPARISON TABLE (Top‑N Emojis, normiert)
# ────────────────────────────────────────────────────────────────────────────────

def create_comparison_table(df: pd.DataFrame, top_n: int = 25, save_path: str = "emoji_model_comparison.csv") -> pd.DataFrame:
    sentiment_order = get_top25_nonflag_emoji_emotion_ranking()

    grouped = (
        df.groupby(["model", "group", "emoji"]).size().reset_index(name="count")
    )
    grouped["normalized"] = grouped.groupby(["model", "group"])["count"].transform(lambda x: x / x.sum())

    pivot = (
        grouped.pivot_table(index=["model", "emoji"], columns="group", values="normalized", fill_value=0)
        .reset_index()
    )
    pivot["delta"] = pivot["right_conservative"] - pivot["left_liberal"]

    # Sentiment‑Sortierung
    pivot["emoji"] = pd.Categorical(pivot["emoji"], categories=sentiment_order, ordered=True)
    pivot = pivot.sort_values(["model", "emoji"])

    # Top‑N global häufigste Emojis auswählen
    top_global = (
        grouped.groupby("emoji")["count"].sum().nlargest(top_n).index
    )
    filtered = pivot[pivot["emoji"].isin(top_global)]

    filtered.to_csv(save_path, index=False)
    print(f"Saved comparison table to {save_path}")
    return filtered

# ────────────────────────────────────────────────────────────────────────────────
# MAIN
# ────────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    db_path = getDatabasePath()
    df_all = load_typology_for_models(db_path)

    if not df_all.empty:
        desc_df = create_descriptive_table(df_all)
        comp_df = create_comparison_table(df_all)
        print("\nDescriptive overview (head):")
        print(desc_df.head())
        print("\nComparison table (head):")
        print(comp_df.head())
