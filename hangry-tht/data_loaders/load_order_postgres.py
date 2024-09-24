from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from os import path
from pandas import DataFrame
from datetime import datetime, timedelta
import pandas as pd
import numpy as np


if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


def remove_duplicate(df:DataFrame) -> DataFrame:
    return df.drop_duplicates()


def remove_null(df:DataFrame) -> DataFrame:
    return df.dropna()


order_schema = {
    'order_id': np.int64,
    'menu_id': np.int64,
    'quantity': np.int64,
    'sales_date': np.dtype("datetime64[ns]")
}


@data_loader
def load_data_from_postgres(*args, **kwargs):
    """
    Load order data from postgres db

    host: localhost
    db: postgres
    schema: public
    table: order
    
    Docs: https://docs.mage.ai/design/data-loading#postgresql
    """

    # Runtime parameters
    execution_date = kwargs.get("execution_date").date()
    start_date = (execution_date - timedelta(days=kwargs.get('days'))) if eval(kwargs.get("is_backfill")) else datetime.strptime(kwargs.get('start_date'), '%Y-%m-%d').date()
    print('execution_date / end_date:', execution_date)
    print('start_date:', start_date)

    query = f"""
    SELECT * 
    FROM public."order"
    WHERE sales_date BETWEEN '{start_date}' AND '{execution_date}';
    """
    
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        df = loader.load(query)

        df.columns = (
            df.columns
            .str.replace(' ', '_')
            .str.lower()
            )

        df = remove_duplicate(df)
        df = remove_null(df)
        print(df.head(20))
        return df




@test
def test_is_load_success(df) -> None:
    """
    Tests if the data loading process was successful.

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
    assert set(order_schema.keys()).issubset(set(df.columns)), "DataFrame does not have all required columns"
    assert len(set(order_schema)) == len(set(df.columns)), "DataFrame has extra columns"
    
    # Check if the data types match the expected types
    for column, dtype in order_schema.items():
        assert df[column].dtype == dtype, f"Column {column} should be of type {dtype}, but got {df[column].dtype}"