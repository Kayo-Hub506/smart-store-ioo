# smart-store-ioo
-----

## Project Setup Guide (1-Mac/Linux)

Run all commands from a terminal in the root project folder. 

### Step 1A - Create a Local Project Virtual Environment

```shell
python3 -m venv .venv
```

### Step 1B - Activate the Virtual Environment

```shell
source .venv/bin/activate
```

### Step 1C - Install Packages

```shell
python3 -m pip install --upgrade -r requirements.txt
```

### Step 1D - Optional: Verify .venv Setup

```shell
python3 -m datafun_venv_checker.venv_checker
```

### Step 1E - Run the initial project script

```shell
python3 scripts/data_prep.py
```

### Step 1F - Run the Data Preparation Scripts to cleanup the data

```shell
python3 scripts/data_preparation/prepare_customers_data.py
python3 scripts/data_preparation/prepare_products_data.py
python3 scripts/data_preparation/prepare_sales_data.py
```

Customer Data Cleanup- removed duplicate custer ID 1011, same name as customer 1010
Products Data Cleanup - updated spelling of nintendo
Sales Data Cleanup - removed aplha chara on row 9 BonusPoints 

### Run the Data Preparation Scripts to cleanup the data with data scrubber
```shell
python3 scripts/data_prep_customers.py
python3 scripts/data_prep_products.py
python3 scripts/data_prep_sales.py
```

Customer Data Cleanup- removed duplicates and LoyalityPoints range (0, 1000)
Products Data Cleanup - removed duplicates, YearAdded range (1990,2025)
Sales Data Cleanup - checked for duplicates

### Create Database

Created the create_dw.py script that create the database.  Using the etl_to_dw.py script, tables where created based on the schemas.  


-----

## Commands Used (Frequently) to update GitHub 

```
# to check the status
git status
# to stage the files
git add .
# to commit with message
git commit -m "<<message to commit>>"
# to push into remote branch
git push -u origin main
```