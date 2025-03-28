import pathlib
import sys
import pandas as pd

# For local imports, temporarily add project root to Python sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Now we can import local modules
from utils.logger import logger  # noqa: E402

# Constants
DATA_DIR: pathlib.Path = PROJECT_ROOT.joinpath("data")
RAW_DATA_DIR: pathlib.Path = DATA_DIR.joinpath("raw")
PREPARED_DATA_DIR: pathlib.Path = DATA_DIR.joinpath("prepared")

def read_raw_data(file_name: str) -> pd.DataFrame:
    logger.info(f"Reading data from {RAW_DATA_DIR.joinpath(file_name)}")
    df = pd.read_csv(RAW_DATA_DIR.joinpath(file_name))
    return df

def save_prepared_data(df: pd.DataFrame, file_name: str) -> None:
    logger.info(f"Saving cleaned data to {PREPARED_DATA_DIR.joinpath(file_name)}")
    df.to_csv(PREPARED_DATA_DIR.joinpath(file_name), index=False)

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Removing duplicates based on 'Name'")
    df = df.drop_duplicates(subset=['Name'])
    return df

def remove_customer_id(df: pd.DataFrame, customer_id: int) -> pd.DataFrame:
    logger.info(f"Removing CustomerID {customer_id}")
    df = df[df['CustomerID'] != customer_id]
    return df

def remove_outliers(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    logger.info(f"Removing outliers from '{column_name}' using IQR")
    Q1 = df[column_name].quantile(0.25)
    Q3 = df[column_name].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df = df[(df[column_name] >= lower_bound) & (df[column_name] <= upper_bound)]
    return df

def main() -> None:
    logger.info("Starting data preparation script")
    input_file = "customers_data.csv"
    output_file = "customers_data_prepared.csv"
    
    df = read_raw_data(input_file)
    df = remove_customer_id(df, 1011)
    df = remove_outliers(df, 'LoyaltyPoints')
    save_prepared_data(df, output_file)
    
    logger.info("Data preparation complete.")

if __name__ == "__main__":
    main()

