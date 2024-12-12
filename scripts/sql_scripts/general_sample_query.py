import json
import time
import numpy as np
from helper import construct_query, extract_table_metadata


print("********** SAMPLE QUERIES **********")
print("\n")

with open("current_db.json", "r") as file:
    content = json.load(file)

table_name = content["table"]

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

dict_list = []
nl_list = []
for elem in funcs:
    query_build_table["table"] = table_name
    if elem == "count":
        query_build_table[elem] = True
        query_build_table["where"] = {"field": cat_field, "value": cat_rand_val}
        nl = f"The number of rows where {cat_field} is called {cat_rand_val}"
    elif elem == "join":
        query_build_table[elem] = {"table": "maleWages", "field": "nr"}
        nl = f"Join the maleWages table on nr."
    elif elem == "project":
        query_build_table[elem] = [cat_field, num_field]
        nl = f"Get all rows but only show {cat_field} and {num_field}."
    elif elem == "agg":
        query_build_table[elem] = {"method": "avg", "field": num_field}
        nl = f"Get the average {num_field} value."
    elif elem == "group":
        query_build_table[elem] = {"field": cat_field}
        query_build_table["agg"] = {"method": "max", "field": num_field}
        nl = f"Get the max {num_field} value for each {cat_field}."
    elif elem == "order":
        query_build_table[elem] = {"field": num_field, "method": "desc"}
        nl = f"Sort the {num_field} in descending order."
    elif elem == "where":
        query_build_table[elem] = {"field": cat_field, "value": cat_rand_val}
        nl = f"Get the rows where {cat_field} is called {cat_rand_val}."
    elif elem == "limit":
        query_build_table[elem] = {"method": "top", "value": "10"}
        nl = f"Get the top 10 rows in the table."
        
    dict_list.append(query_build_table)
    query_build_table = {k: None for k in query_build_table.keys()}
    nl_list.append(nl)

query_list = [construct_query(elem) for elem in dict_list]

for words, query_str in zip(nl_list, query_list):
    print(words)
    print(query_str)
    print("\n\n")

time.sleep(6)


print()























