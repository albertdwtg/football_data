from src.retriever import DataRetriever

from src.validator import InputValidator
from src.feature_engineering.shots_events import ShotsFeaturesCreator
from src.training import ModelTrainer

import polars as pl

retriever = DataRetriever()
input_validator = InputValidator()
shots_events_cleaner = ShotsFeaturesCreator()
model_trainer = ModelTrainer()

# retriever.get_competitions_events()
# retriever.get_competitions().head()
# filters = {
#     "competition_gender" : "male",
#     "competition_name": "La Liga"
# }
# print(retriever.get_competition_season_duo(filters))
# print(retriever.get_matches(competition_id=9,
#                       season_id=27))
shots_events_df = retriever.get_events(3890561, event_type="shots")
df = shots_events_cleaner.fill_bool_values(shots_events_df)
df = shots_events_cleaner.create_total_seconds(df)
model_trainer.train_model(df[["team_id", "player_id", "shot_technique", "total_seconds"]],
                          sort_field = "total_seconds",
                          descending = False)

# retriever.get_competition_events(competition_id=9,
#                       season_id=27)
