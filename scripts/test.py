import json
import os

cur_dir = os.getcwd()
path = f"{cur_dir}/user_query_values.json"

with open(path, "r") as file:
    content = json.load(file)



standardized_order = ["match", "group", "math", "sort", "skip", "limit", "count", "project"]

func_order = content["func_order"]

final_func_order = [elem for elem in standardized_order if elem in func_order]

for k,v in content.items():
    print(k,v)

print(final_func_order)
