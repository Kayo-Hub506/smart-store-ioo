import pandas as pd
import sqlite3
import pathlib
import sys

# For local imports, temporarily add project root to sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Constants
DW_DIR = pathlib.Path("data").joinpath("dw")
DB_PATH = DW_DIR.joinpath("smart_sales.db")
PREPARED_DATA_DIR = pathlib.Path("data").joinpath("prepared")

def create_schema(cursor: sqlite3.Cursor) -> None:
    """Create tables in the data warehouse if they don't exist."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customer (
            customer_id INTEGER PRIMARY KEY,
            name TEXT,
            region TEXT,
            join_date DATE,
            loyalty_points INTEGER,
            preferred_contact_method TEXT       
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT,
            category TEXT,
            unit_price REAL,
            year_added INTEGER,
            supplier TEXT       
        )
    """)

    # Drop and recreate the sale table
    cursor.execute("DROP TABLE IF EXISTS sale")
    cursor.execute("""
        CREATE TABLE sale (
            transaction_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            product_id INTEGER,
            sale_date TEXT,
            sale_amount REAL,
            bonus_points INTEGER,
            payment_type TEXT,
            FOREIGN KEY (customer_id) REFERENCES customer (customer_id),
            FOREIGN KEY (product_id) REFERENCES product (product_id)
        )
    """)



def delete_existing_records(cursor: sqlite3.Cursor) -> None:
    """Delete all existing records from the customer, product, and sale tables."""
    cursor.execute("DELETE FROM customer")
    cursor.execute("DELETE FROM product")
    cursor.execute("DELETE FROM sale")

def insert_customers(customers_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """Insert customer data into the customer table."""
    print("DataFrame columns:", customers_df.columns.tolist())

    # Rename columns to match SQLite schema
    customers_df = customers_df.rename(columns={
        "CustomerID": "customer_id",
        "Name": "name",
        "Region": "region",
        "JoinDate": "join_date",
        "LoyaltyPoints": "loyalty_points",
        "PreferredContactMethod": "preferred_contact_method"
    })

    customers_df.to_sql("customer", cursor.connection, if_exists="append", index=False)


def insert_products(products_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """Insert product data into the product table."""
    print("Product DataFrame columns:", products_df.columns.tolist())

    products_df = products_df.rename(columns={
        "ProductID": "product_id",
        "ProductName": "product_name",
        "Category": "category",
        "UnitPrice": "unit_price",
        "YearAdded": "year_added",
        "Supplier": "supplier"
    })

    products_df.to_sql("product", cursor.connection, if_exists="append", index=False)


def insert_sales(sales_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """Insert sales data into the sale table."""
    print("Sales DataFrame columns:", sales_df.columns.tolist())

    sales_df = sales_df.rename(columns={
        "TransactionID": "transaction_id",
        "CustomerID": "customer_id",
        "ProductID": "product_id",
        "SaleDate": "sale_date",
        "SaleAmount": "sale_amount",
        "BonusPoints": "bonus_points",
        "PaymentType": "payment_type",
    })

    # Drop columns not present in the 'sale' table schema
    sales_df = sales_df[[
        "transaction_id", "customer_id", "product_id",
        "sale_date", "sale_amount", "bonus_points", "payment_type"
    ]]

    sales_df.to_sql("sale", cursor.connection, if_exists="append", index=False)



def load_data_to_db() -> None:
    try:
        # Connect to SQLite – will create the file if it doesn't exist
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Create schema and clear existing records
        create_schema(cursor)
        delete_existing_records(cursor)

        # Load prepared data using pandas
        customers_df = pd.read_csv(PREPARED_DATA_DIR.joinpath("customers_data_prepared.csv"))
        products_df = pd.read_csv(PREPARED_DATA_DIR.joinpath("products_data_prepared.csv"))
        sales_df = pd.read_csv(PREPARED_DATA_DIR.joinpath("sales_data_prepared.csv"))

        # Insert data into the database
        insert_customers(customers_df, cursor)
        insert_products(products_df, cursor)
        insert_sales(sales_df, cursor)

        conn.commit()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    load_data_to_db()