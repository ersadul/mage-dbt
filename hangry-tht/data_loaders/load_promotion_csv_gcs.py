from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from os import path
import pandas as pd
import numpy as np

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

promotion_schema = {
    'id': np.int64,
    'start_date': np.dtype("datetime64[ns]"),
    'end_date': np.dtype("datetime64[ns]"),
    'disc_value': np.float64,
    'max_disc': np.int64
}

@data_loader
def load_from_google_cloud_storage(*args, **kwargs):
    """
    Load promotion data from google cloud storage

    project name: hangrytht-435208
    bucket name: hangrytht-435208-bucket
    file name: promotion.csv
    format: csv

    Docs: https://docs.mage.ai/design/data-loading#googlecloudstorage
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    bucket_name = 'hangrytht-435208-bucket'
    object_key = 'promotion.csv'

    df = GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).load(
        bucket_name,
        object_key,
    )
    
    df.columns = (
        df.columns
        .str.replace(' ', '_')
        .str.lower()
        )

    df['start_date'] = pd.to_datetime(df['start_date'])
    df['end_date'] = pd.to_datetime(df['end_date'])

    return df 


@test
def check_is_load_success(df) -> None:
    """
    Checks if the data loading process was successful.

    Args:
        df: The loaded DataFrame.

    Raises:
        AssertionError: If the DataFrame is None.
    """
    assert df is not None, "Data loading failed: output DataFrame is undefined"


@test
def check_uniqueness(df, *args) -> None:
    """ 
    Checks if the DataFrame `df` has no duplicate rows.

    Args:
        df: The DataFrame to check.

    Raises:
        AssertionError: If the DataFrame has duplicate rows.
    """
    assert df.duplicated().sum() == 0, 'Duplicate rows found in the DataFrame'

@test
def check_completeness(df, *args) -> None:
    """ 
    Checks if the DataFrame `df` has no null values.

    Args:
        df: The DataFrame to check.

    Raises:
        AssertionError: If the DataFrame has null value/s.
    """
    assert df.isnull().sum().any() == 0, 'Duplicate rows found in the DataFrame'

@test
def check_column_correctness(df, *args) -> None: 
    """
    Checks if the DataFrame `df` has the correct columns and data types.

    Args:
        df: The DataFrame to check.

    Raises:
        AssertionError: If the DataFrame does not have all the expected columns or if the data types are incorrect.
    """
    # Check if the DataFrame has all the required columns
    assert set(promotion_schema.keys()).issubset(set(df.columns)), "DataFrame does not have all required columns"
    assert len(set(promotion_schema)) == len(set(df.columns)), "DataFrame has extra columns"
    
    # Check if the data types match the expected types
    for column, dtype in promotion_schema.items():
        assert df[column].dtype == dtype, f"Column {column} should be of type {dtype}, but got {df[column].dtype}"