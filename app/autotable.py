import sqlite3
import pandas as pd

# Read CSV File
def read_csv(filename):
    return pd.read_csv(filename)

# Structure of Data
def data_structure(df):
    cols = list(df.columns)
    types = list(df.dtypes)
    return cols, types

def create_table(cols, types, table_name, df):

    #Making SQL Table
    data_types = {'object': 'TEXT',
    'int64': 'INTEGER',
    'int32': 'INTEGER',
    'float64': 'REAL',
    'float32': 'REAL',
    'bool': 'NUMERIC',
    'datetime64[ns]': 'NUMERIC'}

    zipped = zip(cols, types)

    table = f"CREATE TABLE {table_name} ("

    for column, dtypes in zipped:
        table += column + data_types[str(dtypes)] + ","
    
    table = table[:-1]
    table += ")"

    conn = sqlite3.connect(table_name)
    cursor = conn.cursor()
    cursor.execute(table)

    # Including Data
    data = df.to_dict('list')
    data_df = pd.DataFrame(data)
    data_df.to_sql(table_name, conn, if_exists='replace', index=False)

    print("Table successfully created")


# Trial
df = read_csv('students.csv')
c, t = data_structure(df)
create_table(c, t, 'updated_students', df)

conn = sqlite3.connect('updated_students')
students_df = pd.read_sql_query("SELECT * from updated_students", conn)
print(students_df)











        



