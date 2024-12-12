from pymongo import MongoClient
import sys
import re
import os
import json
from query_templates import query_pieces, conditionals, math_methods


def render_template(template, **kwargs):
    return template.format(**kwargs)


class mongo:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.collection = None
        print("Mongo client initialized")
    
    def create_collection(self, project, table):
        db = self.client[project]
        self.collection = db[table]
        print(f"{project} db and {table} collection created.")
        return self.collection    
    
    def connect_db(self, project):
        db = self.client[project]
        return db
    
    def load_to_db(self, data=None):
        result = self.collection.insert_many(data)
        print("Data successfully loaded to mongodb")

    def close_client(self):
        self.client.close()
        print("MongoDB client has been closed.")


def contains_comparison_term(text):
    term_map = {
        r"greater than or equal to": "gte",
        r"less than or equal to": "lte",
        r"greater than": "gt",
        r"less than": "lt",
        r"equals": "eq",
        r"equal to": "eq"
    }
    
    pattern = re.compile(r"|".join(term_map.keys()), re.IGNORECASE)
    
    match = pattern.search(text)
    
    if match:
        matched_term = match.group(0).lower()
        for full_term, short_form in term_map.items():
            if re.fullmatch(full_term, matched_term, re.IGNORECASE):
                return short_form
    return None


def construct_query(pieces, func_vals, coll_name):
    # Build final query
    pipeline_pieces = []
    for elem in pieces:
        if elem == "match":
            try:
                feature = func_vals[elem]["field"]
            except:
                feature = func_vals[elem]["match_val"]
            
            if not func_vals["conditional"]:
                if (isinstance(func_vals[elem]["match_val"], int)) or (isinstance(func_vals[elem]["match_val"], float)):
                    value = func_vals[elem]["match_val"]
                    condition = "eq"
                elif func_vals[elem]["match_val"].isdigit():
                    value = int(func_vals[elem]["match_val"])
                    condition = "eq"
                else:
                    value = func_vals[elem]["match_val"]
                    condition = "base"
            else:
                condition = func_vals["conditional"]["con_val"]
                value = int(func_vals["conditional"]["value"])
    
            pipe_piece = render_template(
                query_pieces[elem],
                feature=feature,
                conditional=render_template(
                    conditionals[condition], 
                    value=value
                    )
                )
            pipeline_pieces.append(pipe_piece)
        
        elif elem == "project":
            projections_input = func_vals[elem]
            projections = {'"{attr}"'.format(attr=k): 1 for k in projections_input}
            pipe_piece = render_template(
                query_pieces[elem],
                projections=projections
                )
            pipeline_pieces.append(pipe_piece)
        
        elif elem == "group":
            gb_feature = func_vals[elem]
            math_function = func_vals["math"]["type"]
            g_feature = func_vals["math"]["field"]
    
            math_piece = render_template(
                    math_methods[math_function],
                    feature=g_feature
                    )
    
            pipe_piece = render_template(
                    query_pieces[elem],
                    feature=gb_feature,
                    mathstr=math_function,
                    g_feature=g_feature,
                    math_piece=math_piece
                    )
            pipeline_pieces.append(pipe_piece)
    
        elif elem == "sort":
            feature = func_vals[elem]["field"]
            sort_val = func_vals[elem]["sort_val"][0]
            
            pipe_piece = render_template(
                    query_pieces[elem],
                    feature=feature,
                    value=sort_val
                    )
            pipeline_pieces.append(pipe_piece)
    
        elif elem == "limit":
            lim_type = func_vals["limit"]["type"]
    
            if lim_type in ["limit_top", "limit_bottom"]:
                if lim_type == "limit_top":
                    sort_val = -1
                else:
                    sort_val = 1
    
                # sort first
                pipe_piece = render_template(
                        query_pieces["sort"],
                        feature=func_vals["limit"]["field"],
                        value=sort_val
                        )
                pipeline_pieces.append(pipe_piece)
                lim_val = func_vals[elem]["limit_val"]
                pipe_piece = render_template(
                        query_pieces[elem],
                        value=lim_val
                        )
                pipeline_pieces.append(pipe_piece)
    
        elif elem == "skip":
            skip_val = func_vals[elem]
            pipe_piece = render_template(
                    query_pieces[elem],
                    value=skip_val
                    )
            pipeline_pieces.append(pipe_piece)
    
        elif elem == "count":
            pipe_piece = render_template(
                    query_pieces[elem]
                    )
            pipeline_pieces.append(pipe_piece)
        
        else:
            print(f"{elem} is not supported yet.")
            sys.exit(1)
    
    pipeline_pieces = str(pipeline_pieces).replace("'", "").replace("\\","")
    
    query = render_template(
                query_pieces["base"],
                collection=coll_name,
                pieces=pipeline_pieces
                )
    
    return query


def execute_query(query, coll_name, db_name):
    mongo_inst = mongo()
    db = mongo_inst.connect_db(db_name)

    command = json.loads(query)
    result = db.command(command)

    all_docs = result["cursor"]["firstBatch"]
    cursor_id = result["cursor"]["id"]

    while cursor_id != 0:
        get_more = {"getMore": cursor_id, "collection": coll_name}
        next_batch = db.command(get_more)
        all_docs.extend(next_batch["cursor"]["nextBatch"])
        cursor_id = next_batch["cursor"]["id"]
    
    mongo_inst.close_client()

    return all_docs


def extract_collection_metadata(coll_name):
    cur_dir = os.getcwd()
    coll_md_path = os.path.join(cur_dir, "collection_metadata.json")
    
    with open(coll_md_path, "r") as file:
        content = json.load(file)
    
    for collection in content:
        if collection["collection_name"] == coll_name:
            coll_md = collection
    
    
    # import user query values json
    with open(f"{cur_dir}/user_query_values.json", "r") as file:
        usr_q_vals = json.load(file)
    
    for key in usr_q_vals:
        usr_q_vals[key] = None
    
    # create list of categorical and numerical columns
    columns = coll_md["columns"]
    categorical = [elem["name"] for elem in columns if "object" in elem["type"]]
    numerical = [elem["name"] for elem in columns if "int" in elem["type"] or "float" in elem["type"]]
    return columns, usr_q_vals, categorical, numerical





















