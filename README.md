# ChatDB: A SQL and NoSQL Query Automation Tool

ChatDB is a robust query automation tool designed to simplify the interaction with both SQL (MySQL) and NoSQL (MongoDB) databases. It allows users to ingest, view, and query data using scripts and natural language processing (NLP). The application features automated metadata management, sample query generation, and support for both SQL and NoSQL query execution.

---

## Features

### MySQL Integration

- **DATA Directory**: Contains the CSV files to be uploaded to the MySQL database.
- **run_chatdb.sh**: A bash script that orchestrates the ChatDB application workflow.
- **input_data.py**:
  - Uploads CSV data to the MySQL database.
  - Generates and updates `table_metadata.json` with column names, data types, and sample values.
- **table_metadata.json**:
  - Stores metadata for all tables, including column names, data types, and sample values.
- **view_db.py**:
  - Allows users to select a database and table.
  - Displays a preview of the table schema and the first 10 rows of data.
  - Updates the `current_db.json` file with the selected database and table.
- **current_db.json**:
  - Tracks the currently selected database and table.
  - Used by other scripts for context-specific operations.
- **query_logic.sh**:
  - Orchestrates user interactions and triggers specific query scripts.
- **general_sample_query.py**:
  - Generates random sample SQL queries based on table metadata.
  - Randomly selects categorical and numerical columns for query examples.
- **sample_query.py**:
  - Creates sample queries based on user-defined SQL constructs.
  - Prompts users to execute the generated queries.
- **nlp.py**:
  - Converts natural language inputs into SQL queries using:
    - A dictionary of keywords for SQL functions.
    - Spacy for part-of-speech tagging.
  - Populates `user_query_values.json` with parsed query components.
- **user_query_values.json**:
  - Stores parsed query information as a JSON object.
- **run_query.py**:
  - Builds and executes SQL queries based on `user_query_values.json`.
  - Uses a helper function, `construct_query`, to assemble query strings from metadata.

### NoSQL Integration (MongoDB)

- **collection_metadata.json**:
  - Stores metadata for MongoDB collections, analogous to `table_metadata.json` in MySQL.
- **query_templates.py**:
  - Contains query templates for MongoDB operations (e.g., project, group).
- **Construct Query Function**:
  - Uses templates to generate MongoDB query strings based on user input.
  - Concatenates individual components into a complete MongoDB query.

### Key Differences Between SQL and NoSQL Implementations

- Metadata is stored in `collection_metadata.json` for MongoDB.
- Query templates for MongoDB are defined in a dedicated file (`query_templates.py`).

---

## How It Works

1. **Data Ingestion**:
   - Use `input_data.py` to upload CSV data to MySQL and automatically generate metadata files.
   - For MongoDB, metadata is managed in `collection_metadata.json`.
2. **Database and Table Selection**:
   - Run `view_db.py` to select the database and table.
   - Update the context with `current_db.json`.
3. **Query Generation**:
   - For SQL:
     - Use `general_sample_query.py` for random query examples.
     - Use `sample_query.py` to generate and execute queries based on user-defined constructs.
   - For MongoDB:
     - Queries are built using `query_templates.py` and executed with a MongoDB equivalent of `run_query.py`.
4. **NLP Query Support**:
   - Run `nlp.py` to input queries in natural language.
   - NLP parses user input, identifies key SQL/NoSQL constructs, and populates `user_query_values.json`.
5. **Query Execution**:
   - Execute queries using `run_query.py` for SQL and a corresponding MongoDB execution script.

---

## Prerequisites

- **MySQL Server**
- **MongoDB**
- **Python 3.8** with the following libraries:
  - `spacy`
  - `mysql-connector-python` (for MySQL connectivity)
  - `pymongo` (for MongoDB connectivity)
  - `pandas`
  - `numpy`
- **Spacy English Model**:
  - Install using: `python -m spacy download en_core_web_sm`

---

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/joliuliu44/DSCI551_chatdb.git
   cd DSCI551_chatdb/scripts/
   ```
2. Run the main orchestration script:
   ```bash
   ./run_chatdb.sh
   ```
3. Follow the on-screen prompts to interact with the application.

---

## License
This project is licensed under the MIT License.

---

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any bugs or feature requests.

---

## Acknowledgments
Special thanks to the open-source community for providing the tools and libraries used in this project.


