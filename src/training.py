import polars as pl
import lightgbm as lgb
from sklearn.model_selection import train_test_split

class ModelTrainer:
    
    def __init__(self) -> None:
        pass
    
    def train_model(self, 
                    dataset: pl.DataFrame,
                    sort_field: str = None,
                    descending: bool = True,
                    train_size: float = 0.8
                    ):
        if sort_field:
            dataset = dataset.sort(sort_field, descending = descending)
        
        train_df, test_df = train_test_split(
            dataset, 
            train_size = train_size,
            shuffle = False
        )
        
        print(train_df.shape)
        print(test_df.shape)