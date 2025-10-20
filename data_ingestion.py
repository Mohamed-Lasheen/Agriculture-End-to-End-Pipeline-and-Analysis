from sqlalchemy import create_engine, text
import logging
import pandas as pd

logger = logging.getLogger('data_ingestion')
 
"""
Database and CSV data access utilities.

This module provides functions for creating database connections, executing SQL queries,
and reading CSV data from web sources with comprehensive error handling and logging.
"""

def create_db_engine(db_path):
    """
    Create a SQLAlchemy database engine and test the connection.

    Args:
        db_path (str): Database connection string in SQLAlchemy format.

    Returns:
        sqlalchemy.engine.Engine: SQLAlchemy engine object if successful.

    Raises:
        ImportError: If SQLAlchemy is not installed.
        Exception: If database engine creation fails.
    """
    try:
        engine = create_engine(db_path)
        # Test connection
        with engine.connect() as conn:
            pass
        # test if the database engine was created successfully
        logger.info("Database engine created successfully.")
        return engine # Return the engine object if it all works well
    except ImportError: #If we get an ImportError, inform the user SQLAlchemy is not installed
        logger.error("SQLAlchemy is required to use this function. Please install it first.")
        raise e
    except Exception as e:# If we fail to create an engine inform the user
        logger.error(f"Failed to create database engine. Error: {e}")
        raise e
    
def query_data(engine, sql_query):
    """
    Execute SQL query and return results as a pandas DataFrame.

    Args:
        engine (sqlalchemy.engine.Engine): Database engine object.
        sql_query (str): SQL query string to execute.

    Returns:
        pandas.DataFrame: Query results as a DataFrame.

    Raises:
        ValueError: If the query returns an empty DataFrame.
        Exception: If query execution fails.
    """
    try:
        with engine.connect() as connection:
            df = pd.read_sql_query(text(sql_query), connection)
        if df.empty:
            # Log a message or handle the empty DataFrame scenario as needed
            msg = "The query returned an empty DataFrame."
            logger.error(msg)
            raise ValueError(msg)
        logger.info("Query executed successfully.")
        return df
    except ValueError as e: 
        logger.error(f"SQL query failed. Error: {e}")
        raise e
    except Exception as e:
        logger.error(f"An error occurred while querying the database. Error: {e}")
        raise e
    
def read_from_web_CSV(URL):
    """
    Read CSV data from a web URL into a pandas DataFrame.

    Args:
        URL (str): Web URL pointing to a CSV file.

    Returns:
        pandas.DataFrame: Data from the CSV file.

    Raises:
        pd.errors.EmptyDataError: If the URL does not point to a valid CSV file.
        Exception: If CSV reading fails.
    """
    try:
        df = pd.read_csv(URL)
        logger.info("CSV file read successfully from the web.")
        return df
    except pd.errors.EmptyDataError as e:
        logger.error("The URL does not point to a valid CSV file. Please check the URL and try again.")
        raise e
    except Exception as e:
        logger.error(f"Failed to read CSV from the web. Error: {e}")
        raise e
    