import os
import sys
import json
import time
import numpy as np
from helper import construct_query, execute_query, mongo, extract_collection_metadata

# User chooses function
usr_func = input("Choose a language construct: ")

# have the user choose these values or store these values in a txt file
cur_dir = os.getcwd()
with open(f"{cur_dir}/current_db.json", "r") as file:
    content = json.load(file)

coll_name = content["collection"]
db_name = content["database"]

# Extract the numerical and categorical columns from the collection
columns, usr_q_vals, categorical, numerical = extract_collection_metadata(coll_name)

# randomly select numerical and categorical values
cat_num = np.random.randint(0, len(categorical)-1) 
num_num = np.random.randint(0, len(numerical)-1)


cat_field = categorical[cat_num]
num_field = numerical[num_num]

for elem in columns:
    if elem["name"] == cat_field:
        cat_vals = elem["vals"]
    if elem["name"] == num_field:
        num_vals = elem["vals"]

cat_rand_num = np.random.randint(0, len(cat_vals)-1)
num_rand_num = np.random.randint(0, len(num_vals)-1)

cat_rand_val = cat_vals[cat_rand_num]
num_rand_val = num_vals[num_rand_num]

func_order = []
if usr_func == "limit":
    usr_q_vals[usr_func] = {
            "type": "limit_top",
            "limit_val": 5,
            "field": num_field
            }
    func_order.append(usr_func)

elif usr_func == "match":
    usr_q_vals[usr_func] = {
            "field": num_field,
            "match_val": num_rand_val
            }
    func_order.append(usr_func)

elif usr_func == "sort":
    usr_q_vals[usr_func] = {
            "field": num_field,
            "sort_val": [-1]
            }
    func_order.append(usr_func)

elif usr_func == "skip":
    usr_q_vals[usr_func] = 2
    func_order.append(usr_func)

    usr_q_vals["limit"] = {
            "type": "limit_top",
            "limit_val": 5,
            "field": num_field
            }
    func_order.append("limit")

elif usr_func == "count":
    usr_q_vals[usr_func] = True
    func_order.append(usr_func)

elif usr_func == "group":
    usr_q_vals[usr_func] = cat_field
    usr_q_vals["math"] = {
            "field": num_field,
            "type": "max"
            }
    func_order.append(usr_func)

elif usr_func == "project":
    usr_q_vals[usr_func] = [cat_field, num_field]
    func_order.append(usr_func) 

else:
    print("language construct not supported.")


with open(f"{cur_dir}/user_query_values.json", "w") as file:
    json.dump(usr_q_vals, file, indent=4)

query = construct_query(func_order, usr_q_vals, coll_name)

print("\n\n\n")
print("This is an example of a query with your chosen language construct:")
print(query)
print("\n\n\n\n")
run_sample = input("Would you like to run this sample query? (y/n): ")
run_sample = run_sample.lower()

if run_sample in ["y", "yes"]:
    query_result = execute_query(query, coll_name, db_name)
    for elem in query_result[:10]:
        print(elem)
        print()
    time.sleep(10)
else:
    sys.exit(1)
