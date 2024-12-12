import json
import time
import mysql.connector
import pandas as pd

def detect_data_types(df):
    """Detect MySQL-compatible data types for a DataFrame."""
    dtype_map = {
        'int64': 'BIGINT',
        'float64': 'FLOAT',
        'object': 'VARCHAR(255)',
        'bool': 'BOOLEAN',
        'datetime64[ns]': 'DATETIME'
    }
    column_types = {}
    column_sample_vals = {}
    for col in df.columns:
        dtype = str(df[col].dtype)
        column_types[col] = dtype_map.get(dtype, 'TEXT')

        samples = df[col].unique()[:5].tolist()
        column_sample_vals[col] = samples

    return column_types, column_sample_vals

def create_table_from_csv(cursor, table_name, column_types):
    """Generate and execute a CREATE TABLE query."""
    columns = [f"`{col}` {dtype}" for col, dtype in column_types.items()]
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS `{table_name}` (
        {', '.join(columns)}
    );
    """
    cursor.execute(create_table_query)

def insert_data_from_csv(cursor, table_name, df):
    """Generate and execute an INSERT query for the data."""
    df = df.where(pd.notnull(df), None)
    columns = ", ".join([f"`{col}`" for col in df.columns])
    placeholders = ", ".join(["%s"] * len(df.columns))
    insert_query = f"INSERT INTO `{table_name}` ({columns}) VALUES ({placeholders});"
    data = [tuple(row) for row in df.itertuples(index=False)]
    cursor.executemany(insert_query, data)

def main():
    dataset_name = input("Input filename of dataset: ")
    file_path = f"../../data/{dataset_name}"
    df = pd.read_csv(file_path)
    
    try:
        with open("table_metadata.json", "r") as file:
            table_metadata = json.load(file) 
    except:
        table_metadata = [] 

    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='DSCI',
    )

    cursor = connection.cursor()
    
    db_name = input("Database name: ")
    cursor.execute(f"DROP DATABASE IF EXISTS {db_name};")
    cursor.execute(f"CREATE DATABASE {db_name};")
    cursor.execute(f"USE {db_name};")

    specific_table_metadata = {}
    table_name = input("Enter the name of the table to create: ")
    specific_table_metadata["table_name"] = table_name

    column_types, column_sample_vals = detect_data_types(df)
    specific_table_metadata["columns"] = column_types
    specific_table_metadata["sample_values"] = column_sample_vals
    
    create_table_from_csv(cursor, table_name, column_types)
    insert_data_from_csv(cursor, table_name, df)

    table_metadata.append(specific_table_metadata)

    with open("table_metadata.json", "w") as file:
        json.dump(table_metadata, file, indent=4)

    connection.commit()
    cursor.close()
    connection.close()
    print(f"Data from {dataset_name} has been successfully inserted into the {table_name} table.")

if __name__ == "__main__":
    main()
    time.sleep(3)

