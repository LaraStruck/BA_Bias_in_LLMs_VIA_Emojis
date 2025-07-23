from experimental.V6.differenciate_Heatmap import emoji_focus_by_score_share
from Analysing.evaluation_scripts_final.heatMap import heatMapV8_plotly
from experimental.V6.total_emoji_count import total_emoji_count
from data.variables.models import MODELS
from utils.getUtlis import getDatabasePath

model_id = "x-ai/grok-2-vision-1212"
run_id = 8
score_col = "V6_Scale"

if __name__ == "__main__":
    for model in MODELS:
        if model["active"]:
            total_emoji_count(model)
            emoji_focus_by_score_share(
                getDatabasePath(),
                model_name=model["name"],
                model_id=model["id"],
                score_col="V6_Scale",
                run_id="BETWEEN 9 AND 18"
            )
            emoji_focus_by_score_share(
                getDatabasePath(),
                model_name=model["name"],
                model_id=model["id"],
                score_col="V4_Scale",
                run_id="BETWEEN 9 AND 18"
            )
            emoji_focus_by_score_share(
                getDatabasePath(),
                model_name=model["name"],
                model_id=model["id"],
                score_col="V8_Scale",
                run_id="BETWEEN 9 AND 18"
            )
            heatMapV8_plotly(getDatabasePath(),
                             model_name=model["name"],
                             model_id=model["id"],
                             score_col="V6_Scale",
                             run_id=" BETWEEN 9 AND 18")
