import sqlite3

create_table = """CREATE TABLE students (
                name TEXT,
                age INTEGER,
                id INTEGER
                )"""

students_information = [
    ('Bhoovi', 21, 17),
    ('Vanshika', 20, 23),
    ('Rachel', 21, 27),
    ('Kaaviri', 20, 7),
    ('Dhanvi', 20, 21),
    ('Sharanya', 19, 15),
    ('Shravs', 21, 30),
    ('Joey', 5, 12),
    ('Sam', 6, 13),
    ('Gary', 1, 19),
    ('Anu', 52, 6),
    ('Ashish', 54, 3)
]

try:
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute(create_table)
    cursor.executemany("INSERT INTO students VALUES (?, ?, ?)", students_information)
    conn.commit()
    conn.close()
    print("Tables were successfully created")

except sqlite3.OperationalError as e:
    print("Failed to create tables:", e)


