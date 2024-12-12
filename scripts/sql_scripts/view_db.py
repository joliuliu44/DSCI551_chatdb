import os
import time
import sys
import json
import mysql.connector

while True:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='DSCI'
        )    
    cursor = connection.cursor()
    
    print("Databases Available: ")
    cursor.execute("SHOW DATABASES;")
    rows = cursor.fetchall()
    for row in rows:
        print(row[0])

    db_name = input("Choose a database or type 'exit': ")
    if db_name == 'exit':
        sys.exit(1)

    cursor.execute(f"USE {db_name};")

    cursor.execute("SHOW TABLES;")
    rows = cursor.fetchall()
    for row in rows:
        print(row[0])

    while True:
        table_name = input("Choose a table or type 'back': ")
        
        if table_name == "back":
            break
        
        try:
            with open("table_metadata.json", "r") as file:
                table_metadata = json.load(file)
        except:
            print("No tables in mysql.")
            sys.exit(1)
        
        curr_db_info = {}
        curr_db_info["database"] = db_name
        curr_db_info["table"] = table_name
        with open("current_db.json", "w") as file:
            json.dump(curr_db_info, file, indent=4)

        matching_tables = [elem for elem in table_metadata if elem["table_name"] == table_name]
        if not matching_tables:
            print(f"Table '{table_name}' not found in metadata.")
            sys.exit(1)
        
        chosen_table_md = matching_tables[0]
        
        print(f"\n\nYou have chosen the {table_name} table in the {db_name} database:")
        print(f"{table_name} Attributes:")
        for k, v in chosen_table_md["columns"].items():
            print(f"Field: {k:<30} Type: {v}")
        
        print(f"\n\n{table_name} Preview:")
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 10;")
        rows = cursor.fetchall()
        
        if rows:
            for row in rows:
                print(row)
            time.sleep(5)
        else:
            print(f"No data found in table: {table_name}.")
        
        cursor.close()
        connection.close()
        sys.exit(1)
    
    
