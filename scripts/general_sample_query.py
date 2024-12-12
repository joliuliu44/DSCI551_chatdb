import os
import sys
import json
import time
import numpy as np
from helper import extract_collection_metadata, construct_query


print("********** SAMPLE QUERIES **********")
print("\n")

cur_dir = os.getcwd()
with open(f"{cur_dir}/current_db.json", "r") as file:
    content = json.load(file)

coll_name = content["collection"]

function = {
    "match": None,
    "limit": None,
    "group": None,
    "project": None,
    "sort": None,
    "skip": None,
    "conditional": None,
    "count": None,
    "math": None,
}
 

columns, usr_q_vals, categorical, numerical = extract_collection_metadata(coll_name)

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

funcs = list(function.keys())[:-3]

dict_list = []
func_order = []
nl_list = []
for elem in funcs:
    if elem == "limit":
        function[elem] = {
                "type": "limit_top",
                "limit_val": 5,
                "field": num_field
                }
        nl = f"The top 5 {num_field} values."
        func_order.append(elem)

    elif elem == "match":
        function[elem] = {
                "field": num_field,
                "match_val": num_rand_val
                }
        nl = f"The items where {num_field} is equal to {num_rand_val}."
        func_order.append(elem)
    
    elif elem == "sort":
        function[elem] = {
                "field": num_field,
                "sort_val": [-1]
                }
        nl = f"Return the items with {num_field} in descending order"
        func_order.append(elem)
    
    elif elem == "skip":
        function[elem] = 2
        func_order.append(elem)
    
        function["limit"] = {
                "type": "limit_top",
                "limit_val": 5,
                "field": num_field
                }
        nl = f"Get the top 5 {num_field} values but skip the first 2 values."
        func_order.append("limit")
    
    elif elem == "count":
        function[elem] = True
        nl = f"Get the count of all items in the collection."
        func_order.append(elem)
    
    elif elem == "group":
        function[elem] = cat_field
        function["math"] = {
                "field": num_field,
                "type": "max"
                }
        nl = f"Get the maximum {num_field} value for each {cat_field}."
        func_order.append(elem)
    
    elif elem == "project":
        function[elem] = [cat_field, num_field]
        nl = f"Get all of the items in the collection but only display {cat_field} and {num_field} fields."
        func_order.append(elem) 
    
    else:
        print("language construct not supported.")

    function["func_order"] = func_order
    dict_list.append(function)
    function = {k: None for k in function.keys()}
    func_order = []
    nl_list.append(nl)



query_list = [construct_query(elem["func_order"], elem, coll_name) for elem in dict_list]
#
for words, query_str in zip(nl_list, query_list):
    print(words)
    print(query_str)
    print("\n\n")

time.sleep(6)







