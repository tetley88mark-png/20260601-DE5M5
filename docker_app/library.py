import os
import pandas as pd
import pyodbc
import sys

from loguru import logger
from pathlib import Path
from sqlalchemy import create_engine

# Variables
engine = create_engine(
"mssql+pyodbc://@localhost/library?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server"
)

customer = {"Int":["Customer ID"]}
books = {"Int":["Id", "Customer ID"],
        "Date":["Book checkout", "Book Returned"]}

folder = "data_in"
output_dir = Path("/data/data_out")
output_dir.mkdir(parents=True, exist_ok=True)

# Functions
def list_files_in_folder(folder_path, include_subfolders=False):
    """
    Lists all files in the given folder.
    
    :param folder_path: Path to the folder to scan.
    :param include_subfolders: If True, will also scan subfolders.
    """
   
    try:
        folder = Path(folder_path)
        files = []

        if not folder.exists():
            logger.info(f"Error: The folder '{folder_path}' does not exist.")
            return

        if include_subfolders:
            # Recursively list all files
            for file_path in folder.rglob("*"):
                if file_path.is_file():
                    files.append(file_path)
        else:
            # Only list files in the top-level folder
            for file_path in folder.iterdir():
                if file_path.is_file():
                    files.append(file_path)
        return files

    except PermissionError:
        logger.info("Error: Permission denied while accessing the folder.")
    except Exception as e:
        logger.info(f"Unexpected error: {e}")

def drop_na(df):
    """Function to Drop any NA rows and return the number dropped"""
    size = len(df)
    df.dropna(how='all', inplace=True)
    logger.info(f"{size - len(df)} row(s) dropped")
    return df

def clear_whitespace(df):
    """Function to clear whitespace from string columns in dataframe"""
    for i in df.columns:
        if df[i].dtype == 'object':
            df[i] = df[i].map(str.strip)
        else:
            pass
    return df

def float_to_int(df, columns):
    """Function to convert floats to rounded integers"""
    df[columns] = df[columns].apply(pd.to_numeric, errors='coerce').round().astype('Int64')
    return df

def dates(df, columns):
    """Function to convert string dates to date values"""
    for col in columns:
        df[col] = (df[col].astype("string")
            .str.strip()
            .str.strip('"')
            .str.strip("'"))

    df[columns] = df[columns].apply(pd.to_datetime, dayfirst=True,
            errors="coerce",format="mixed",)
    return df

def df_to_sql(df,table):
    """Function to load Dataframe values into a local SQL Database"""
    try:
        df.to_sql(
            name=table,       
            con=engine,
            if_exists="replace",
            index=False
        )
        logger.info("DataFrame successfully written to database.")
    except Exception as e:
        logger.info(f"Error writing to database: {e}")

def dataEnrich(df):
    """Function to calculate days between dates"""
    df["days_between"] = (df["Book Returned"] - df["Book checkout"]).dt.days
    df = float_to_int(df,["days_between"])
    return df

def duplicates(df):
    """Function to identify and log duplicates before dropping them from the file"""
    duplicates = df[df.duplicated()]
    if len(duplicates) > 0:
        logger.info("Duplicates Identified and dropped")
        logger.info(f"{duplicates}")
        df.drop_duplicates(inplace=True, ignore_index=True)
    else:
        logger.info("No Duplcation")
    return df

def main():
    files = list_files_in_folder(folder, include_subfolders=False)
    for file in files:
        if "book" in str(file).lower():
            mapping = books
            output = f"{output_dir}/books.csv"
            table = "books"
        else:
            mapping = customer
            output = f"{output_dir}/customer.csv"
            table = "customer"

        df = pd.read_csv(file)
        df = drop_na(df)
        df = duplicates(df)
        if "Int" in mapping.keys():
            df = float_to_int(df,mapping["Int"])
        df = clear_whitespace(df)
        if "Date" in mapping.keys():
            df = dates(df, mapping["Date"])
            df = dataEnrich(df)
        try:
            df.to_csv(output, index=False, encoding="utf-8")
            logger.info(f"{output} written successfully")
        except Exception as e:
            logger.info(f"Unable to write due to {e}")
        sql_mode = len(sys.argv) > 1 and sys.argv[1].lower() == "sql"
        if sql_mode:
            df_to_sql(df, table)
        else:
            logger.info("Local Data Save only")

if __name__ == "__main__":
    main()