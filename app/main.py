import sqlite3
import pandas as pd
import os

def log_error(message):
    with open("error_log.txt", "a") as f:
        f.write(message + "\n")

def handle_schema_conflict(table_name, conn):
    print(f"Table '{table_name}' already exists.")
    choice = input("Overwrite (o), Rename (r), or Skip (s)? ").strip().lower()
    
    if choice == "o":
        print("Overwriting table...")
        return table_name
    elif choice == "r":
        new_name = input("Enter new table name: ").strip()
        return new_name
    elif choice == "s":
        print("Skipping table creation.")
        return None
    else:
        print("Invalid choice. Skipping.")
        return None

def read_csv(filename):
    try:
        return pd.read_csv(filename)
    except Exception as e:
        log_error(f"Error reading CSV {filename}: {e}")
        return None

def data_structure(df):
    return list(df.columns), list(df.dtypes)

def create_table(cols, types, table_name, df, conn):
    data_types = {
        'object': 'TEXT', 'int64': 'INTEGER', 'int32': 'INTEGER',
        'float64': 'REAL', 'float32': 'REAL', 'bool': 'NUMERIC', 'datetime64[ns]': 'NUMERIC'
    }

    table_def = f"CREATE TABLE {table_name} ("
    table_def += ", ".join([f"{col} {data_types[str(dtype)]}" for col, dtype in zip(cols, types)])
    table_def += ")"

    cursor = conn.cursor()

    try:
        cursor.execute(table_def)
    except sqlite3.OperationalError as e:
        if "already exists" in str(e):
            log_error(f"Schema conflict on table '{table_name}': {e}")
            return False
        else:
            log_error(f"Other error creating table '{table_name}': {e}")
            return False

    try:
        df.to_sql(table_name, conn, if_exists='replace', index=False)
    except Exception as e:
        log_error(f"Error writing to table '{table_name}': {e}")
        return False

    return True

def chatbot_interface():
    conn = sqlite3.connect("students.db")
    while True:
        print("\nOptions: load, query, list, exit")
        user_input = input("What would you like to do? ").strip().lower()
        
        if user_input == "exit":
            break
        elif user_input == "load":
            filename = input("Enter CSV filename: ").strip()
            df = read_csv(filename)
            if df is not None:
                cols, types = data_structure(df)
                table_name = os.path.splitext(os.path.basename(filename))[0]
                
                # Check for existing table
                tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
                if table_name in tables['name'].values:
                    new_name = handle_schema_conflict(table_name, conn)
                    if new_name:
                        create_table(cols, types, new_name, df, conn)
                else:
                    create_table(cols, types, table_name, df, conn)

        elif user_input == "query":
            sql = input("Enter SQL query: ")
            try:
                result = pd.read_sql_query(sql, conn)
                print(result)
            except Exception as e:
                print("Query failed.")
                log_error(f"Query failed: {e}")

        elif user_input == "list":
            tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
            print("Tables:", tables['name'].tolist())

    conn.close()

chatbot_interface()