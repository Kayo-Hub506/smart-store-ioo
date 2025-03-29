import pandas as pd
from data_scrubber import DataScrubber

# Step 1: Load raw data
df = pd.read_csv("data/raw/products_data.csv")

# Step 2: Clean the data
scrubber = DataScrubber(df)
scrubber.remove_duplicate_records()
scrubber.handle_missing_data(drop=True)
scrubber.filter_column_outliers(column="YearAdded", lower_bound=1990, upper_bound=2025)
scrubber.convert_column_to_new_data_type("YearAdded", int)

# Step 3: Save the cleaned data
scrubber.df.to_csv("data/prepared/products_data_prepared.csv", index=False)

print("✅ Products data cleaned and saved.")