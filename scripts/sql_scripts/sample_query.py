import os
import sys
import json
import time
import numpy as np
import mysql.connector
from helper import construct_query, extract_table_metadata

# User chooses function
usr_func = input("Choose a language construct: ")

# have the user choose these values or store these values in a txt file
cur_dir = os.getcwd()
with open(f"{cur_dir}/current_db.json", "r") as file:
    content = json.load(file)

table_name = content["table"]
db_name = content["database"]

query_build_table = {
    "table": table_name,
    "count": None,
    "join": None,
    "project": None,
    "agg": None,
    "group": None,
    "order": None,
    "where": None,
    "having": None,
    "limit": None
}

# Extract the numerical and categorical columns from the collection
sample_values, usr_q_vals, categorical, numerical = extract_table_metadata(table_name)

cat_num = np.random.randint(0, len(categorical)-1)
num_num = np.random.randint(0, len(numerical)-1)

cat_field = categorical[cat_num]
num_field = numerical[num_num]

for col, vals in sample_values.items():
    if col == cat_field:
        cat_vals = vals
    if col == num_field:
        num_vals = vals

cat_rand_num = np.random.randint(0, len(cat_vals)-1)
num_rand_num = np.random.randint(0, len(num_vals)-1)

cat_rand_val = cat_vals[cat_rand_num]
num_rand_val = num_vals[num_rand_num]

funcs = list(query_build_table.keys())[1:]

if usr_func == "count":
    query_build_table[usr_func] = True
    query_build_table["where"] = {"field": cat_field, "value": cat_rand_val}
    nl = f"The number of rows where {cat_field} is called {cat_rand_val}"
elif usr_func == "join":
    query_build_table[usr_func] = {"table": "maleWages", "field": "nr"}
    nl = f"Join the maleWages table on nr."
elif usr_func == "project":
    query_build_table[usr_func] = [cat_field, num_field]
    nl = f"Get all rows but only show {cat_field} and {num_field}."
elif usr_func == "agg":
    query_build_table[usr_func] = {"method": "avg", "field": num_field}
    nl = f"Get the average {num_field} value."
elif usr_func == "group":
    query_build_table[usr_func] = {"field": cat_field}
    query_build_table["agg"] = {"method": "max", "field": num_field}
    nl = f"Get the max {num_field} value for each {cat_field}."
elif usr_func == "order":
    query_build_table[usr_func] = {"field": num_field, "method": "desc"}
    nl = f"Sort the {num_field} in descending order."
elif usr_func == "where":
    query_build_table[usr_func] = {"field": cat_field, "value": cat_rand_val}
    nl = f"Get the rows where {cat_field} is called {cat_rand_val}."
elif usr_func == "limit":
    query_build_table[usr_func] = {"method": "top", "value": "10"}
    nl = f"Get the top 10 rows in the table."

query = construct_query(query_build_table)

print("This is an example query for your request:")
print(nl)
print(f"SQL query: {query}\n")
run_choice = input("Would you like to run this query? (y/n) ")

if run_choice[0].lower() == "y":
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="DSCI",
        database=db_name
    )

    cursor = connection.cursor()
    cursor.execute(query)

    results = cursor.fetchall()
    print()
    for row in results:
        print(row)

    if connection.is_connected():
        cursor.close()
        connection.close()

    time.sleep(6)
else:
    sys.exit(1)
