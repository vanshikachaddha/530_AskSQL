#https://datacarpentry.github.io/python-ecology-lesson/instructor/09-working-with-sql.html
import sqlite3
import pandas as pd

try:
    conn = sqlite3.connect('students.db')
    # Load the data into a DataFrame
    students_df = pd.read_sql_query("SELECT * from students", conn)
    print(students_df)

    # Select people younger than 21
    under_21 = pd.read_sql_query("SELECT * from students WHERE age < 21", conn)
    print(under_21)

    # Add anoter list of people to DataBase
    data = {'name': ['Preens', 'Rohan', 'Sumi'], 'age': [21, 21, 22], 'id': [4, 5, 8]}
    new_data_df = pd.DataFrame(data)
    new_data_df.to_sql('students', conn, if_exists='append', index=False)
    updated_students_df = pd.read_sql_query("SELECT * from students", conn)
    print(updated_students_df)
    conn.close()
    

except sqlite3.OperationalError as e:
    print("Failed to create tables:", e)
    