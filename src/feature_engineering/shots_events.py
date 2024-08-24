import polars as pl

class ShotsFeaturesCreator:
    
    def __init__(self) -> None:
        pass
    
    def fill_bool_values(self, df: pl.DataFrame) -> pl.DataFrame:
        columns = [
            "under_pressure",
            "shot_aerial_won",
            "shot_one_on_one",
            "shot_first_time"
        ]
        df_modified = df.with_columns(
            pl.col(col).fill_null(False)
            for col in columns
        )
        return df_modified
        
    def create_total_seconds(self, df: pl.DataFrame) -> pl.DataFrame:
        df_modified = df.with_columns((
            60*pl.col("minute") + pl.col("second")
        ).alias("total_seconds"))
        return df_modified