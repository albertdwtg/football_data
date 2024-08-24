from statsbombpy import sb
import polars as pl
from pathlib import Path
from datetime import datetime
from src.validator import InputValidator
from typing import List

from src import logging_config
import logging

logger = logging.getLogger(__name__)

input_validator = InputValidator()

class DataRetriever:

    def __init__(self) -> None:
        pass

    def get_matches(
        self,
        competition_id: int,
        season_id: int,
        save_df_output: bool = False,
        output_format: str = None,
    ) -> pl.DataFrame:
        logging.debug(
            f"Start to retrieve matches, competition_id={competition_id}, season_id={season_id}"
        )
        
        #Check input variables
        input_validator.check_season_id(season_id)
        input_validator.check_competition_id(competition_id)
        
        df = pl.from_pandas(
            sb.matches(competition_id=competition_id, season_id=season_id)
        )
        logging.debug(f"Output dataframe shape : {df.shape}")
        if save_df_output:
            destination_directory = Path("outputs", "matches")
            self._save_df_output(
                df=df,
                destination_filename=f"matches_{competition_id}_{season_id}_{datetime.today().strftime('%Y%m%d')}",
                destination_directory=destination_directory,
                output_format=output_format,
            )
        return df

    def get_competitions(
        self, save_df_output: bool = False, output_format: str = None
    ) -> pl.DataFrame:
        logging.debug("Start to retrieve competitions")
        df = pl.from_pandas(sb.competitions())
        print(df["country_name"].unique().to_list())
        logging.debug(f"Output dataframe shape : {df.shape}")
        if save_df_output:
            destination_directory = Path("outputs", "competitions")
            self._save_df_output(
                df=df,
                destination_filename=f"competition_df_{datetime.today().strftime('%Y%m%d')}",
                destination_directory=destination_directory,
                output_format=output_format,
            )
        return df

    def get_events(
        self,
        match_id: str,
        event_type: str = None,
        flatten_attrs: bool = True,
        save_df_output: bool = False,
        output_format: str = None,
    ) -> pl.DataFrame:
        logging.debug(f"Start to retrieve events for match_id={match_id}")
        
        input_validator.check_match_id(match_id)
        
        if event_type is None:
            df = pl.from_pandas(
                sb.events(match_id=match_id, split=False, flatten_attrs=flatten_attrs)
            )
        else:
            input_validator.check_events_type(event_type)    
            df = pl.from_pandas(
                sb.events(match_id=match_id, split=True, flatten_attrs=flatten_attrs)[event_type]
            )
        
        logging.debug(f"Output dataframe shape : {df.shape}")
        if save_df_output:
            destination_directory = Path("outputs", "events")
            self._save_df_output(
                df=df,
                destination_filename=f"events_{match_id}_{datetime.today().strftime('%Y%m%d')}",
                destination_directory=destination_directory,
                output_format=output_format,
            )
        
        return df

    def get_competition_match_ids(
        self, competition_id: int, season_id: int
    ) -> List[int]:
        logging.debug(
            f"Start to retrieve all match_ids for competition_id={competition_id}"
        )
        matches = self.get_matches(competition_id=competition_id, season_id=season_id)
        return matches["match_id"].unique().to_list()

    def _save_df_output(
        self,
        df: pl.DataFrame,
        destination_directory: Path,
        destination_filename: str,
        output_format: str = None,
    ) -> None:

        if output_format is None:
            output_format = "PARQUET"

        destination_directory.mkdir(parents=True, exist_ok=True)
        destination_path = destination_directory / (
            destination_filename + f".{output_format.lower()}"
        )
        logging.debug(f"Start to save df in path={destination_path}")

        if output_format.upper() == "JSON":
            df.write_json(destination_path)
        elif output_format.upper() == "CSV":
            df.write_csv(destination_path)
        elif output_format.upper() == "PARQUET":
            df.write_parquet(destination_path)
        else:
            logging.error(
                f"Select correct output format, format > {output_format} is not valid"
            )

    def get_competition_season_duo(self, filters: dict) -> List[dict]:
        logging.debug(f"Start to retrieve competition_id-season_id duo for filters: {filters}")
        df = self.get_competitions().filter(
                    pl.col(filter_column) == filter_value
                    for filter_column, filter_value in filters.items()
                )
        list_of_duos = df[["competition_id", "season_id"]].unique().to_dicts()
        logging.debug(f"Found {len(list_of_duos)} competition-season")
        return list_of_duos
        
    # def get_competition_events(self, competition_id: int, season_id: int, event_type: str):
    #     match_ids = self.get_competition_match_ids(
    #         competition_id = competition_id,
    #         season_id = season_id
    #     )
    #     print(len(match_ids))
    #     all_events = []
    #     for id in match_ids:
    #         events = self.get_events(
    #             match_id = id,
    #             event_type = event_type
    #         )
    #         all_events.append(events)
    #     all_events_df = pl.concat(all_events)
    #     return all_events
