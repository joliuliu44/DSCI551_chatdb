import os
import pandas as pd
import json
from helper import mongo
from pymongo import MongoClient


def main(db_name, coll_name, csv_name):

    mongo_inst = mongo()
    mongo_inst.create_collection(db_name, coll_name)
    
    cur_dir = os.getcwd()
    data_path = f"{cur_dir}/../data/{csv_name}"
    metadata_path = os.path.join(cur_dir, "collection_metadata.json")
    
    
    data = pd.read_csv(data_path)
    
    input_data = []
    
    for idx, row in data.iterrows():
        ind_data = {}
        for col in data.columns:
            ind_data[col] = row[col]
        input_data.append(ind_data)
    
    mongo_inst.load_to_db(data=input_data)
    
    
    collection_metadata = {
            "collection_name": coll_name,
            "columns": [
                {
                    "name": col,
                    "type": str(data[col].dtype),
                    "vals": data[col].unique()[:3].tolist()
                }
            for col in data.columns
        ]
    }
    
    if os.path.exists(metadata_path):
        try:
            with open(metadata_path, "r") as file:
                metadata = json.load(file)
        except json.JSONDecodeError:
            print("Warning: metadata file is empty or invalid, starting with an empty metadata list.")
            metadata = []
    else:
        metadata = []

    metadata.append(collection_metadata)
       
    with open(metadata_path, "w") as file:
        json.dump(metadata, file, indent=4)
       
    print("Data loaded into MongoDB and metadata updated.")
    mongo_inst.close_client()
   

if __name__ == "__main__":
    csv_name = input("Input the file name of your csv: ")
    db_name = input("Choose a database to input the data: ")
    coll_name = input("Input a name for this collection: ")
    main(db_name, coll_name, csv_name)
    
