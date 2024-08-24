from src.retriever import DataRetriever
from src.validator import InputValidator
import polars as pl

retriever = DataRetriever()
input_validator = InputValidator()

# retriever.get_competitions_events()
# retriever.get_competitions().head()
# filters = {
#     "competition_gender" : "male",
#     "competition_name": "La Liga"
# }
# print(retriever.get_competition_season_duo(filters))
# print(retriever.get_matches(competition_id=9,
#                       season_id=27))
retriever.get_events(3890561, event_type="shots").head()
# retriever.get_competition_events(competition_id=9,
#                       season_id=27)
