import json
import os
import spacy
from helper import contains_comparison_term


def main(user_input):

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(user_input)
    tokens = [(token.text, token.pos_) for token in doc]
    
    # Keywords setup
    keywords = {
        "match": ["named", "called", "where"],
        "limit": {
            "val": ["top", "bottom"]
        },
        "group": ["every", "each", "group", "grouped"],
        "project": ["show", "display", "return"],
        "sort": ["ascending", "descending"], 
        "count": ["count", "number"],
        "skip": ["skip"],
        "math": {
            "sum": ["total", "sum"],
            "avg": ["average", "mean"],
            "max": ["highest", "max", "maximum"],
            "min": ["lowest", "min", "minimum"],
            },
        "conditional": ["greater", "less", "equals"],
        "misc_words": ["than", "but", "in", "only", "for", "of", "the", "get", "a", "is", "or", "to", "find", "and","row", "rows", "object", "objects", "order", "items", "with"]
    }
    
    # Initialize extracted functions
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
    
    function_order = []
    function_on_deck = None
    limit_val = None
    field_val = None
    
    # Parse tokens
    for token, pos in tokens:
    
        if token in keywords["misc_words"]:
            continue
    
        # Handle numeric values
        if pos == "NUM":
            token = int(token)
    
            if function_on_deck in {"limit_top", "limit_bottom"}:
                function["limit"] = {"type": function_on_deck, "limit_val": token}
    
            elif function_on_deck == "match":
                if function[function_on_deck] is None:
                    function[function_on_deck] = {}
                function[function_on_deck]["field"] = field_val
                function[function_on_deck]["match_val"] = token
                function_on_deck = None
    
            elif function_on_deck == "skip":
                function[function_on_deck] = token
            
            elif function_on_deck == "conditional":
                function[function_on_deck]["value"] = token
    
            continue
    
    
        # Handle nouns (fields or group criteria)
        elif pos in {"NOUN", "PROPN", "X"}:
            field_val = token
            if function_on_deck in {"limit_top", "limit_bottom"}:
                if not function["limit"]:
                    function["limit"] = {"type": function_on_deck, "limit_val": None, "field": field_val}
                else:
                    function["limit"]["field"] = field_val
    
            elif token in keywords["count"]:
                function["count"] = True
                function_order.append("count")
    
            elif function_on_deck == "match":
                if not function[function_on_deck]:
                    function[function_on_deck] = {}
                function[function_on_deck]["match_val"] = token
    
            elif function_on_deck == "group":
                function[function_on_deck] = field_val
                function_on_deck = None
    
            elif function_on_deck == "project":
                if not function[function_on_deck]:
                    function[function_on_deck] = [field_val]
                else:
                    function[function_on_deck].append(field_val)
                continue
    
            elif function_on_deck and function_on_deck[:4] == "math":
                if not function["math"]:
                    function["math"] = {"field": field_val, "type": function_on_deck[-3:]}
                else:
                    function["math"]["field"] = field_val
                function_on_deck = None
           
            elif token in keywords["math"]["sum"]:
                function_on_deck = "mathsum"
                function_order.append("math")
                
                if not function["math"]:
                    function["math"] = {"type": function_on_deck[-3:]}
                else:
                    function["math"]["type"] = function_on_deck[-3:]
    
            elif token in keywords["math"]["avg"]:
                function_on_deck = "mathavg"
                function_order.append("math")
    
                if not function["math"]:
                    function["math"] = {"type": function_on_deck[-3:]}
                else:
                    function["math"]["type"] = function_on_deck[-3:]
    
            elif token in keywords["math"]["max"]:
                function_on_deck = "mathmax"
                function_order.append("math")
    
                if not function["math"]:
                    function["math"] = {"type": function_on_deck[-3:]}
                else:
                    function["math"]["type"] = function_on_deck[-3:]
    
            elif token in keywords["math"]["min"]:
                function_on_deck = "mathmin"
                function_order.append("math")
    
                if not function["math"]:
                    function["math"] = {"type": function_on_deck[-3:]}
                else:
                    function["math"]["type"] = function_on_deck[-3:]
    
            elif function_on_deck:
                function[function_on_deck] = token
                function_on_deck = None
    
        # Handle adjectives for ordering or aggregation
        elif pos == "ADJ":
            if token in keywords["limit"]["val"]:
                function_on_deck = f"limit_{token}"
                function_order.append("limit")
    
            elif token in keywords["math"]["avg"]:
                function_on_deck = "mathavg"
                function_order.append("math")
    
            elif token in keywords["math"]["sum"]:
                function_on_deck = "mathsum"
                function_order.append("math")
    
            elif token in keywords["math"]["max"]:
                function_on_deck = "mathmax"
                function_order.append("math")
    
            elif token in keywords["math"]["min"]:
                function_on_deck = "mathmin"
                function_order.append("math")
    
            elif token in keywords["match"]:
                function_on_deck = "match"
                function_order.append("match")
                function["match"] = {}  # Initialize match field
    
            # Set flag for count, sum, or avg if detected
            elif token in keywords["count"]:
                function_on_deck = "count"
                function_order.append("count")
                function["count"] = True
    
            elif token in keywords["conditional"]:
                function_on_deck = "conditional"
                con_val = contains_comparison_term(user_input)
                function[function_on_deck] = {"con_val": con_val}
    
        elif pos == "VERB":
            if token in keywords["project"]:
                function_on_deck = "project"
                function_order.append("project")
    
            elif token in keywords["sort"]:
                if "asc" in token:
                    function_on_deck = "sort_asc"
                if "desc" in token:
                    function_on_deck = "sort_desc"
    
                function_order.append("sort")
    
                sort_val = [1 if function_on_deck == "sort_asc" else -1]
                function["sort"] = {
                        "field": field_val,
                        "sort_val": sort_val 
                        }
    
            elif token in keywords["skip"]:
                function_on_deck = "skip"
                function_order.append("skip")

            elif token in keywords["match"]:
                function_on_deck = "match"
                function["match"] = {"field": field_val}
                if "match" not in function_order:
                    function_order.append("match")
    
        elif pos == "SCONJ":
            if token in keywords["match"]:
                function_on_deck = "match"
                function_order.append("match")
    
    
        # Handle grouping (e.g., "for each category")
        elif pos == "DET" or pos == "PRON":
            if token in keywords["group"]:
                function_on_deck = "group"
                function_order.append("group")
    
    function["func_order"] = function_order
    
    # export user query input values
    cur_dir = os.getcwd()
    
    with open(f"{cur_dir}/user_query_values.json", "w") as file:
        json.dump(function, file, indent=4)


if __name__ == "__main__":
    user_input = input("Type in a query: ")
    main(user_input)







