# Import all necessary modules for saving results and parsing responses
from data.sql.save_results_sql import save_results_sql as save_result
from data.variables.prompts import PROMPTS
from data.variables.models import MODELS
from openrouter_api.api_utils import query_model
from utils.emoji_parser import extract_emojis
from utils.extract_text_from_response import extract_text_from_response
from utils.invalid_return import invalid_saved
from utils.load_parties import load_parties
import json
import concurrent.futures
from utils.entry_exists import entry_exists
from utils.getUtlis import getDatabasePath

# Load database path from .env
database = getDatabasePath()

# Load all filtered political parties from CSV
# File must contain at least: CPARTYABB, Partyname, Country
POLITICAL_ENTITIES = load_parties(
    "partie_selection/filtered_parties_with_scores_preStudy.csv")

def run_prompt_cycle(run_id):
    """
    Executes all active prompt-party-model combinations for a given run_id.
    This includes:
    - Filling in the party name and country in the prompt
    - Sending the prompt to each active model via OpenRouter
    - Extracting emoji from the response
    - Storing valid results in the database
    """
    for prompt in PROMPTS:

        if not prompt.get("active", False):
            continue  # Skip inactive prompts

        for party in POLITICAL_ENTITIES:
            # Fill the prompt with party name and country
            filled_prompt = prompt["text"] \
                .replace("PARTYNAME", party["name"]) \
                .replace("COUNTRY", party["country"])

            print(f"\n==> [{prompt['id']}] {party['name']} ({party['country']}) | Prompt: {filled_prompt}")

            for model in MODELS:
                if not model.get("active", False):
                    continue  # Skip inactive models

                print(f"\n--- {model['name']} ---")
                try:
                    # Skip combination if already stored
                    if entry_exists(model["id"], party["id"], prompt["id"], run_id, database):
                        print(f"⏭️ Combination already stored – skipping")
                        continue

                    # Send request to OpenRouter using a thread
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(query_model, filled_prompt, model=model["id"])
                        response = future.result()

                    if not response:
                        print(f"❌ No response from model {model['id']}")
                        continue

                    print("Model response:")
                    print(response)

                    # Extract plain text and emoji
                    text = extract_text_from_response(response)
                    if not text:
                        print("❌ No valid text in response – skipping.")
                        continue

                    emojis = extract_emojis(text)
                    print("Extracted emojis:", emojis)

                    # Store invalid results if multiple/no emojis
                    if len(emojis) != 1:
                        invalid_saved(model, party, prompt, run_id, emojis, text, response)
                        continue
                    # Save result to SQLite
                    save_result(
                        model=model["id"],
                        party_id=party["id"],
                        party_name=party["name"],
                        country=party["country"],
                        prompt_id=prompt["id"],
                        run_id=run_id,
                        emojis=emojis,
                        full_answer=text,
                        json_response=json.dumps(response)
                    )

                except Exception as e:
                    print(f"⚠️ Error in prompt {prompt['id']}: {e}")

if __name__ == "__main__":
    # Currently, the main loop is configured to run prompts 5 times
    # using run_ids 9 to 18. You can easily change this range here.
   # run_id = 8
   # for i in range(10):  # repeat cycle 5 times
   #     run_id += 1
   #     for j in range(20):  # repeat inner logic 20x (can be reduced)
   #         run_prompt_cycle(run_id)
   run_prompt_cycle(19)