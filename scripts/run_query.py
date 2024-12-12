import sys
import os
import json
import time
from helper import mongo, render_template, construct_query, execute_query
from query_templates import query_pieces, conditionals, math_methods

# get the current db and collection names
cur_dir = os.getcwd()
with open(f"{cur_dir}/current_db.json", "r") as file:
    content = json.load(file)

coll_name = content["collection"]
db_name = content["database"]

# Initialize mongodb instance
mongo_inst = mongo()
db = mongo_inst.connect_db(db_name)


# acquire user inputs
query_val_path = f"{cur_dir}/user_query_values.json"

with open(query_val_path, "r") as file:
    func_vals = json.load(file)

standard_order = ["match", "group", "sort", "skip", "limit", "count", "project"]
unordered = func_vals["func_order"]

pieces = [elem for elem in standard_order if elem in unordered]

# construct the query from the pipeline pieces in the correct order.
query = construct_query(pieces, func_vals, coll_name)
print(query)
print()
print()
print()

all_docs = execute_query(query, coll_name, db_name)

print()
for doc in all_docs:
    print(doc)
    print()


time.sleep(6)
mongo_inst.close_client()



