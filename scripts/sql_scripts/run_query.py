import json
import time
import mysql.connector
from helper import construct_query

with open("current_db.json", "r") as file:
    content = json.load(file)
db_name = content["database"]

with open("user_query_values.json", "r") as file:
    query_dict = json.load(file)

query = construct_query(query_dict)
print("\n" * 40)
print("Your SQL Query:\n")
print(query)

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="DSCI",
    database=db_name
)

cursor = connection.cursor()
cursor.execute(query)

results = cursor.fetchall()
print()
for row in results:
    print(row)

if connection.is_connected():
    cursor.close()
    connection.close()

time.sleep(6)


