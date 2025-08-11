# Emoji-Based Political Bias Detection in Large Language Models

This repository contains the full pipeline for collecting and analyzing emoji associations made by large language models (LLMs) when asked about political parties. The goal is to measure consistency, emotional framing, and potential ideological bias across models, using entropy and frequency analysis.
## AI Assistance Disclosure
Most parts of the code in this repository were generated or adapted using ChatGPT, based on my own design and instructions. All code was reviewed, tested, and validated by me before inclusion.

---
## Installation and Requirements

To run the project locally, I recommend creating a virtual environment and installing all required packages listed in requirements.txt:
```bash
python -m venv .venv
source .venv/bin/activate      # On macOS/Linux
.venv\Scripts\activate         # On Windows

pip install -r requirements.txt
```

The `requirements.txt` file contains all libraries needed to run the project. Most importantly, it includes:

* `pandas` for data handling and analysis
* `plotly` and `matplotlib`/`seaborn` for visualization
* `sqlite3` for querying the results database
* `emoji` for handling and normalizing emoji output
* `spacy` and `en_core_web_sm` (optional, for prompt logic)
* `python-dotenv` to load API keys and configuration

The environment ensures that results are reproducible across systems. The `en_core_web_sm` spaCy model is installed via a direct URL included in `requirements.txt`.


##  Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd your-repo
```

### 2. Create a `.env` file in the root directory

This file must include:

```dotenv
OPENROUTER_API_KEY=your_openrouter_key
CSV_PATH=path/to/Global_Party_Survey.csv
DATABASE_EMOJI_RESULTS=path/to/all_SQL_TABLES.db
PARTIES_CSV=path/to/filtered_parties_with_scores.csv
```

> The required database files (`all_SQL_TABLES.db` and `filtered_parties_with_scores.csv`) are included in the `data/exports/` folder of this repository.  
> If you want to regenerate them manually, follow the steps in `party_selection/` and `setup_database.py`.



##  Project Structure

### `main.py`

Runs the entire data collection pipeline. For each combination of party, prompt, and model:
- Sends a prompt to the model via OpenRouter
- Extracts one emoji from the response
- Saves valid responses in the `results` table of the database
- Saves invalid responses (multiple or no emojis) to `invalid_results`
- Uses multiple `run_id`s to allow repeated querying for entropy calculation

Valid outputs are stored in the `results` table; invalid ones in `invalid_results`.

### `data/variables/`

Contains static configuration files:
- `models.py`: List of models with OpenRouter IDs and `active: True/False` flag
- `prompts.py`: All standardized prompt templates used for model queries

**Note:** Only models and prompts with `active: True` will be used.

### `party_selection/`

Handles filtering of parties from the Global Party Survey:
- `find_parties_inCSV.py`: Allows you to filter by country or score
- Output is saved as `filtered_parties_with_scores_preStudy.csv`
- This file is used both in the main run and database setup

### `data/sql/`

Contains logic for setting up and writing to the SQLite database:
- `setup_database.py`: Initializes tables and inserts party metadata
- `save_results_sql.py`: Saves valid emoji responses to the `results` table

### `openrouter_api/`

Handles all communication with OpenRouter using your API key.

- Sends HTTP POST requests
- Includes authorization, payload formatting, and model selection

### `utils/`

Small helper functions used throughout the project:
- emoji parsing (`emoji_parser.py`)
- response extraction and filtering
- checking if entries already exist
- working with paths and files

---

##  Workflow Summary

1. **Prepare filtered parties:**
   - Edit `find_parties_inCSV.py` to select countries or scores
   - Run the script to create `filtered_parties_with_scores_preStudy.csv`

2. **Configure active models and prompts:**
   - Activate models in `models.py` (OpenRouter ID + `active: True`)
   - Activate prompts in `prompts.py`

3. **Run the main script:**

```bash
python main.py
```

## Analyzing the Results

All analysis scripts are located in the `Analysing/` folder and its subdirectories. The final evaluation scripts are loaded in `evaluation_scripts_final` 
They evaluate how LLMs use emojis to represent political parties based on different dimensions (model, party, ideology, etc.).

---

###  General Analysis 

- `count_per_model.py`:  
  Creates an interactive bar chart (via Plotly) showing the top 5 most common emojis per model.

- `entropy.py`:  
  Calculates the Shannon entropy for each model, party, prompt, and ideological category (left–progressive vs. right–conservative).  
  ➤ Saves results as CSV files:  
  `entropy_by_model.csv`, `entropy_left_vs_right.csv`, `entropy_by_party_overall.csv.

- `table_for_model_analysis.py`:  
  Generates a summary table of emoji usage per model:
    - valid and invalid responses,
    - number of unique emojis,
    - frequently used emojis (≥40 occurrences).  
      ➤ Output: `emoji_typology_summary.csv`.

---

###  Score-Based Visualization Scripts 

These scripts generate interactive Plotly plots based on ideological scores from the Global Party Survey (e.g., Type_Value/V6/V8):

- `heatMap.py`:  
  Generates an interactive heatmap to visualize how frequently specific emojis are used across the V8 scale from the Global Party Survey, which captures populist rhetoric (1 = pluralist, 10 = strongly populist).
  The script can:
  - Aggregate emoji frequencies across all models (default)
  - Or produce separate heatmaps for each model individually
  - And optionally adapt it to other ideological scales (e.g., V6)
    
  The plotted values are normalized emoji proportions per score level.
  Gerne – hier ist die überarbeitete, ausführlichere Beschreibung deiner beiden Scripts:



* `TypeValueBarChart.py`:
  Compares emotional emoji distributions between left–progressive and right–conservative parties, based on their `TYPE_VALUES` from the Global Party Survey (1 = left–progressive, 4 = right–conservative).
  The frequencies are normalized within each ideological group, so that results are comparable despite different group sizes.
  Currently, the categorization is based on U.S. parties. The bar chart can be generated model wise or across all models.

* `GermanyL-R.py`:
  Provides a focused analysis of emoji usage across major German parties, grouped into ideological camps based on their official party identity (e.g. SPD, CDU/CSU, Greens, AfD, etc.).
  The data is normalized by party and model, ensuring that the results reflect relative emotional tone rather than raw frequency. The bar chart can be generated model wise or across all models.
  
---

###  Utility Functions are in: 
`Analysing/utils/plot_emojis.py`
- `plot_emojis_by_group()`:  
  Reusable Plotly function to generate grouped bar charts by category (e.g., model, party type, ideology).  
  Supports flexible plot sizing, color schemes, and axis scaling.

---

 **Note**:  
All visualizations are created dynamically using Plotly and are not stored as image files by default.  
To save figures manually, use the Plotly export options or extend the code accordingly.



This collects emoji outputs from all active model–party–prompt combinations and stores them in the SQLite database.

---
## Optional Parameters and Configuration

Most scripts support flexible configuration via optional arguments, such as:

- `run_id`: defines the runs that should be analyzed 
- `model_id`: filters outputs by a specific language model (e.g., `"openai/gpt-4.1-nano"`)
- `country_id`: restricts the analysis to parties from a given country (e.g., `"Germany"` or `"United States"`)
- `score_col`: chooses the ideological scale (e.g., `"V6_Scale"` for economic policy or `"V8_Scale"` for populism or `Type_Value` for left–progressive vs. right–conservative)
- `prompt_id` or `excluded_prompt_ids`: allows to include or ignore specific prompts

All options can be adjusted either inside the functions or via the `__main__` block in each script. The names may differ slightly.


##  Output

- Graphs not stored but shown wit plotly
- Tables stored in predefined `.csv` files, different for every table
- Valid emoji responses → `results` table (via `save_results_sql.py`)
- Invalid responses → `invalid_results` table
- Party metadata → `parties` table

All stored in the SQLite database defined as `emoji_results`.

---


##  Notes

- The OpenRouter API must be available and functional during querying
- Each party–prompt–model combination is executed across multiple runs (e.g. 5×)
- You can swap models, countries, and prompt styles flexibly by editing the config files

---

##  Credits & Sources

- Emoji prompting via [OpenRouter.ai](https://openrouter.ai)
- Ideological data from the [Global Party Survey (2019)](https://www.globalpartysurvey.org/)
- Developed as part of a Bachelor's thesis in Computer Science (2025)

---
##  License

This project is licensed under the MIT License.

You are free to use, modify, and distribute the code (including analysis scripts and model logic), provided that you include attribution to the original author.

Note: Some modules are experimental and provided “as is”, without any warranty or guarantee of correctness or fitness for a particular purpose.

Gerne! Hier ist der Textabschnitt für deine `README.md`, klar formuliert und ohne Tabelle – bereit zum Kopieren:

---

## Installation and Requirements

To run the project, first create a virtual environment and install all necessary packages:

```bash
python -m venv .venv
source .venv/bin/activate      # On macOS/Linux
.venv\Scripts\activate         # On Windows

pip install -r requirements.txt
```

The `requirements.txt` file contains all libraries needed to run the project. Most importantly, it includes:

* `pandas` for data handling and analysis
* `plotly` and `matplotlib`/`seaborn` for visualization
* `sqlite3` for querying the results database
* `emoji` for handling and normalizing emoji output
* `spacy` and `en_core_web_sm` (optional, for prompt logic)
* `python-dotenv` to load API keys and configuration

The environment ensures that results are reproducible across systems. The `en_core_web_sm` spaCy model is installed via a direct URL included in `requirements.txt`.

