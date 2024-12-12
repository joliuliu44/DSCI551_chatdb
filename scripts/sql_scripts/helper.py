import os
import sys
import json
import mysql.connector
import re


def contains_comparison_term(text):
    term_map = {
        r"greater than or equal to": ">=",
        r"less than or equal to": "<=",
        r"greater than": ">",
        r"less than": "<",
        r"equals": "=",
        r"equal to": "=",
        r"named": "=",
        r"called": "="
    }

    pattern = re.compile(r"|".join(term_map.keys()), re.IGNORECASE)

    match = pattern.search(text)

    if match:
        matched_term = match.group(0).lower()
        for full_term, short_form in term_map.items():
            if re.fullmatch(full_term, matched_term, re.IGNORECASE):
                return short_form
    return None


def construct_query(query_dict):
    # Base elements
    table = query_dict.get('table')
    count = query_dict.get('count')
    join = query_dict.get('join')
    project = query_dict.get('project')
    agg = query_dict.get('agg')
    group = query_dict.get('group')
    order = query_dict.get('order')
    where = query_dict.get('where')
    having = query_dict.get('having')
    limit = query_dict.get('limit')

    if not table:
        raise ValueError("The 'table' key is required.")

    # SELECT clause
    if count:
        select_clause = "SELECT COUNT(*)"
    elif agg:
        select_clause = f"SELECT {agg['method'].upper()}({agg['field']})"
        if project:
            select_clause += ", " + ", ".join(project)
    elif project:
        select_clause = "SELECT " + ", ".join(project)
    else:
        select_clause = "SELECT *"

    # FROM clause
    from_clause = f"FROM {table}"

    # JOIN clause
    join_clause = ""
    if join:
        join_clause = f"JOIN {join['table']} ON {table}.{join['field']} = {join['table']}.{join['field']}"

    # WHERE clause
    where_clause = ""
    if where:
        conditional = where.get('conditional', '=')
        value = f"'{where['value']}'" if isinstance(where['value'], str) else where['value']
        where_clause = f"WHERE {where['field']} {conditional} {value}"

    # GROUP BY clause
    group_clause = ""
    if group:
        group_clause = f"GROUP BY {group['field']}"

    # HAVING clause
    having_clause = ""
    if having:
        conditional = having.get('conditional', '=')
        value = f"'{having['value']}'" if isinstance(having['value'], str) else having['value']
        having_clause = f"HAVING {having['field']} {conditional} {value}"

    # ORDER BY clause
    order_clause = ""
    if order:
        method = order.get('method', 'ASC').upper()
        order_clause = f"ORDER BY {order['field']} {method}"

    # LIMIT clause
    limit_clause = ""
    if limit:
        if limit['method'] == 'top':
            limit_clause = f"LIMIT {limit['value']}"
        elif limit['method'] == 'bottom':
            order_clause = f"ORDER BY {order['field']} DESC"
            limit_clause = f"LIMIT {limit['value']}"

    # Construct the full query
    query = " ".join(
        filter(
            None, [
                select_clause,
                from_clause,
                join_clause,
                where_clause,
                group_clause,
                having_clause,
                order_clause,
                limit_clause,
            ]
        )
    )

    return query

def extract_table_metadata(table_name):
    table_md_path = "table_metadata.json"
    user_query_path = "user_query_values.json"

    with open(table_md_path, "r") as file:
        content = json.load(file)

    table_md = None
    for table in content:
        if table["table_name"] == table_name:
            table_md = table

    if not table_md:
        print("Table could not be found.")
        sys.exit(1)

    # import user query values
    with open(user_query_path, "r") as file:
        usr_q_vals = json.load(file)

    for key in usr_q_vals:
        usr_q_vals[key] = None

    # Create list of categorical and numerical columns
    columns = table_md["columns"]
    categorical = [k for k, v in columns.items() if "VARCHAR" in v or "TEXT" in v]
    numerical = [k for k, v in columns.items() if "INT" in v or "FLOAT" in v]
    return table_md["sample_values"], usr_q_vals, categorical, numerical


