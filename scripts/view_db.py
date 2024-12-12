import os
import sys
import json
import time
from helper import mongo

cur_dir = os.getcwd()
db_path = f"{cur_dir}/current_db.json"

mongo_inst = mongo()

while True:
    databases = mongo_inst.client.list_database_names()
    print("\n" * 40)
    print("Databases Available:")
    
    for elem in databases:
        print(elem)
   
    db_choice = input("Input a database to view or type 'exit': ")
    
    if db_choice == "exit":
        sys.exit(1)
    elif db_choice in databases:
        db = mongo_inst.connect_db(db_choice)
        collections = db.list_collection_names()
        
        print("\n" * 40)
        print("Collections available: ")
        for elem in collections:
            print(elem)

        while True:
            coll_choice = input("Choose a collection to interact with or type 'back': ")
            if coll_choice == "back":
                break

            elif coll_choice in collections:
                result = {
                        "database": db_choice,
                        "collection": coll_choice
                        }
                with open(f"{cur_dir}/collection_metadata.json", "r") as file:
                    content = json.load(file)
                coll_metadata = [elem["columns"] for elem in content if elem["collection_name"] == coll_choice]
                coll_metadata = coll_metadata[0]

                with open(db_path, "w") as file:
                    json.dump(result, file, indent=4)

                print("\n" * 40)
                print(f"You have chosen {db_choice} database and the {coll_choice} collection.")
                print("\nAttributes:")
                for elem in coll_metadata:
                    print(f"Field: {elem['name']:<30} Type: {elem['type']}")

                print(f"\n{coll_choice} Preview:")
                query = {
                    "aggregate": coll_choice,
                    "pipeline": [
                        {"$limit": 10}
                            ],
                    "cursor": {}
                    }
                preview = db.command(query)
                for doc in preview["cursor"]["firstBatch"]:
                    print(doc, '\n')
                time.sleep(5)
                sys.exit(1)

            else:
                print("Invalid Collection. Please try again.")



    






