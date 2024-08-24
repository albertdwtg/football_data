from src.exceptions import BadInput
from src.constants import (
    POSSIBLE_COMPETITION_ID,
    POSSIBLE_EVENTS_TYPE,
    POSSIBLE_PERIOD,
    POSSIBLE_SEASON_ID
)


class InputValidator:

    def __init__(self) -> None:
        pass

    def check_match_id(self, match_id: int):
        if (not isinstance(match_id, int)) or (not len(str(match_id)) == 7) or (match_id <= 0):
            raise BadInput(
                parameter_name="match_id",
                parameter_value=match_id
            )

    def check_season_id(self, season_id: int):
        if season_id not in POSSIBLE_SEASON_ID:
            raise BadInput(
                parameter_name="season_id",
                parameter_value=season_id
            )

    def check_competition_id(self, competition_id: int):
        if competition_id not in POSSIBLE_COMPETITION_ID:
            raise BadInput(
                parameter_name="competition_id",
                parameter_value=competition_id
            )

    def check_events_type(self, events_type: str):
        if events_type not in POSSIBLE_EVENTS_TYPE:
            raise BadInput(
                parameter_name="events_type",
                parameter_value=events_type
            )

    def check_period(self, period: int):
        if period not in POSSIBLE_PERIOD:
            raise BadInput(
                parameter_name="period",
                parameter_value=period
            )

    def check_season_name(self, season_name: str):
        season_name_splitted = season_name.split("/")
        if len(season_name_splitted) == 2:
            if (len(season_name_splitted[0] == 4) 
                and len(season_name_splitted[1] == 4) 
                and season_name_splitted[0].isdigit() 
                and season_name_splitted[1].isdigit()):
                # Good scenario
                pass
            else:
                raise BadInput(
                    parameter_name="season_name",
                    parameter_value=season_name
                )
        else:
            raise BadInput(
                parameter_name="season_name",
                parameter_value=season_name
            )
