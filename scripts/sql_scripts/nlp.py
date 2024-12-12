import os
import sys
import json
import spacy
from helper import contains_comparison_term

user_input = input("Input your query: ")

nlp = spacy.load("en_core_web_sm")
doc = nlp(user_input)
tokens = [(token.text, token.pos_) for token in doc]

# Get which db and table that the user is using currently
with open("current_db.json", "r") as file:
    current_db_info = json.load(file)
table_name = current_db_info["table"]

# Get the column metadata for the table being used
with open("table_metadata.json", "r") as file:
    current_table_info = json.load(file)

column_data = [elem["columns"] for elem in current_table_info if elem["table_name"] == table_name]
column_data = column_data[0]
column_list = list(column_data.keys())
list_of_tables = [elem["table_name"] for elem in current_table_info]

keywords = {
    "where": ["named", "called", "where"], 
    "limit": ["top", "bottom"], 
    "join": ["combine", "join"], 
    "group": ["every", "each", "group", "grouped"],
    "project": ["show", "display", "return"],
    "order": ["ascending", "descending", "order", "sort"], 
    "count": ["count", "number"],
    "agg": {
        "union": ["total", "sum", "average", "mean", "highest", "max", "maximum", "lowest", "min", "minimum"],
        "sum": ["total", "sum"],
        "avg": ["average", "mean"],
        "max": ["highest", "max", "maximum"],
        "min": ["lowest", "min", "minimum"],
        },
    "conditional": ["greater", "less", "equals"], 
    "misc_words": ["table", "Get", "than", "but", "in", "only", "for", "of", "the", "get", "a", "is", "or", "to", "find", "and","row", "rows", "object", "objects", "order", "items", "with"]
    }

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


function_on_deck = None
for token,pos in tokens:

    # quick break out of loop for misc words
    if token in keywords["misc_words"]:
        continue
    #---------------------------------------
    # Check if token in column list and set to field_val if so.
    if token in column_list:
        field_val = token

        if function_on_deck == "agg":
            query_build_table[function_on_deck]["field"] = field_val
            function_on_deck = None
        elif function_on_deck == "group":
            query_build_table[function_on_deck]["field"] = field_val
            function_on_deck = None
        elif function_on_deck == "where":
            query_build_table[function_on_deck]["field"] = field_val
            #function_on_deck = None
        elif function_on_deck == "project":
            query_build_table[function_on_deck].append(field_val)
        elif function_on_deck == "order":
            query_build_table[function_on_deck]["field"] = field_val
        elif function_on_deck == "join":
            query_build_table[function_on_deck]["field"] = field_val
    #---------------------------------------
    # Check if token is another table name
    elif token in list_of_tables:
        if function_on_deck == "join":
            query_build_table[function_on_deck]["table"] = token
    #----------------------------------------
    # Check if token in keywords
    elif token in keywords["group"]:
        function_on_deck = "group"
        if not query_build_table["group"]:
            query_build_table["group"] = {}

    elif token in keywords["agg"]["union"]:
        function_on_deck = "agg"
        if not query_build_table[function_on_deck]:
            query_build_table[function_on_deck] = {}

        for elem in list(keywords[function_on_deck].keys())[1:]:
            if token in keywords[function_on_deck][elem]:
                query_build_table[function_on_deck]["method"] = elem

    elif token in keywords["where"]:
        function_on_deck = "where"
        if not query_build_table[function_on_deck]:
            query_build_table[function_on_deck] = {}

    elif token in keywords["project"]:
        function_on_deck = "project"
        if not query_build_table[function_on_deck]:
            query_build_table[function_on_deck] = []

    elif token in keywords["order"]:
        function_on_deck = "order"
        if not query_build_table[function_on_deck]:
            query_build_table[function_on_deck] = {}
        if token == "ascending":
            query_build_table[function_on_deck]["method"] = "asc"
        elif token == "descending":
            query_build_table[function_on_deck]["method"] = "desc"

    elif token in keywords["conditional"]:
        conditional_term = contains_comparison_term(user_input)
        if function_on_deck == "where":
            query_build_table[function_on_deck]["conditional"] = conditional_term

    elif token in keywords["limit"]:
        function_on_deck = "limit"
        if not query_build_table[function_on_deck]:
            query_build_table[function_on_deck] = {"method": token}

    elif token in keywords["join"]:
        function_on_deck = "join"
        if not query_build_table[function_on_deck]:
            query_build_table[function_on_deck] = {}

    elif token in keywords["count"]:
        query_build_table["count"] = True

    #--------------------------------------------------
    # Part of speech section
    elif pos in {"NOUN", "PROPN", "X"}:
        if function_on_deck == "where":
            query_build_table[function_on_deck]["value"] = token
    elif pos == "NUM":
        if function_on_deck == "where":
            query_build_table[function_on_deck]["value"] = int(token)
        elif function_on_deck == "limit":
            query_build_table[function_on_deck]["value"] = token



with open("user_query_values.json", "w") as file:
    json.dump(query_build_table, file, indent=4)





































