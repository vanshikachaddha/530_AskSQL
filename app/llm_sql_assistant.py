import sqlite3
import pandas as pd
import openai
import os

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_schema(conn):
    schema = ""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        schema += f"Table: {table_name}\n"
        cursor.execute(f"PRAGMA table_info({table_name})")
        for col in cursor.fetchall():
            schema += f"  - {col[1]} ({col[2]})\n"
        schema += "\n"
    return schema

def generate_sql_from_prompt(prompt, schema):
    full_prompt = f"""
You are an AI assistant converting user queries into SQL.
Use SQLite syntax. The database schema is:

{schema}

User request: "{prompt}"

Output ONLY the SQL query, no explanation.
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": full_prompt}],
        temperature=0
    )

    return response.choices[0].message.content.strip()

def run_assistant():
    conn = sqlite3.connect("students.db")
    schema = get_schema(conn)

    while True:
        prompt = input("\nAsk a question (or type 'exit'): ")
        if prompt.lower() == "exit":
            break
        try:
            sql_query = generate_sql_from_prompt(prompt, schema)
            print("\nGenerated SQL Query:")
            print(sql_query)

            result = pd.read_sql_query(sql_query, conn)
            print("\nResult:")
            print(result)
        except Exception as e:
            print("Error:", e)

    conn.close()

if __name__ == "__main__":
    run_assistant()