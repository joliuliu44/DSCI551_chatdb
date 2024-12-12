# Templates for nosql queries

query_pieces = {
        "base": '{{"aggregate": "{collection}", "pipeline": {pieces}, "cursor": {{}}}}',
        "match": '{{"$match": {{"{feature}": {conditional}}}}}',
        "project":'{{"$project": {projections}}}',
        "group": '{{"$group": {{"_id": "${feature}", "{g_feature}": {math_piece}}}}}',
        "sort": '{{"$sort": {{"{feature}": {value}}}}}',
        "limit": '{{"$limit": {value}}}',
        "skip": '{{"$skip": {value}}}',
        "count": '{{"$count": "total"}}'
        }


conditionals = {
    "base": '"{value}"',
    "gt": '{{"$gt": {value}}}',
    "gte": '{{"$gte": {value}}}',
    "lt": '{{"$lt": {value}}}',
    "lte": '{{"$lte": {value}}}',
    "eq": '{{"$eq": {value}}}'
    }


math_methods = {
        "sum": '{{"$sum": "${feature}"}}',
        "avg": '{{"$avg": "${feature}"}}',
        "min": '{{"$min": "${feature}"}}',
        "max": '{{"$max": "${feature}"}}'
        }






