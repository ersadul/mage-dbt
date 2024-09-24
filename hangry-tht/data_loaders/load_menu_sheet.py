from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_sheets import GoogleSheets
from os import path
import pandas as pd
import numpy as np


if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

menu_schema = {
    'menu_id': np.int64,
    'brand': object,
    'name': object,
    'price': np.int64,
    'cogs': np.int64,
    'effective_date': np.dtype("datetime64[ns]")
}

@data_loader
def load_from_google_sheet(*args, **kwargs):
    """
    Load menu data from google sheets

    document name: Copy of [Hangry] Data Engineer Analyst - Take Home Test
    sheet: Menu

    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    header_rows = 1
    sheet_url = 'https://docs.google.com/spreadsheets/d/1__4FSI0iqrmj8cv3Shupq3wgOV7Iz2X8RKeNQMdqvmo/edit?usp=sharing'
    sheet_name = 'Menu'

    df = GoogleSheets.with_config(ConfigFileLoader(config_path, config_profile)).load(
        sheet_url=sheet_url,
        header_rows=header_rows
    )

    df.columns = (
        df.columns
        .str.replace(' ', '_')
        .str.lower()
        )

    df['effective_date'] = pd.to_datetime(df['effective_date'])

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
    assert set(menu_schema.keys()).issubset(set(df.columns)), "DataFrame does not have all required columns"
    assert len(set(menu_schema)) == len(set(df.columns)), "DataFrame has extra columns"
    
    # Check if the data types match the expected types
    for column, dtype in menu_schema.items():
        assert df[column].dtype == dtype, f"Column {column} should be of type {dtype}, but got {df[column].dtype}"