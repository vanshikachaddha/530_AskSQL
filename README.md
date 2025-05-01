# Chat-SQL-AI 📊

This project is a lightweight natural language SQL assistant powered by OpenAI's GPT-4 and backed by a local SQLite database. You can interact with your data by simply asking questions like “show me all students over age 20” and get back structured results.

## Features

- Load CSV data into SQLite  
- Automatically infer schema and create tables  
- Query your data using natural language (via GPT-4)  
- Dockerized for easy setup and testing  
- GitHub Actions CI to test Docker build  

## Project Structure

app/  
  llm_sql_assistant.py       ← main assistant script (natural language to SQL)  
  students.db                ← example SQLite database  
  students.csv               ← original CSV file  
  autotable.py               ← generates tables from CSV  
  database.py                ← manual table creation  
  main.py                    ← CLI chatbot (optional)  
  mapSQL.py                  ← raw query examples  

docker/  
  Dockerfile                 ← Docker build instructions  

.github/workflows/  
  docker-build-test.yml      ← GitHub Actions workflow  

requirements.txt             ← Python dependencies

## Usage (Locally)

1. Install dependencies:  
   pip install -r requirements.txt

2. Create a `.env` file and add your OpenAI key:  
   OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx

3. Run the assistant:  
   python app/llm_sql_assistant.py

## Usage (Docker)

1. Build the image:  
   docker build -f docker/Dockerfile -t chat-sql-ai .

2. Run the container:  
   docker run --rm -it \
     --env-file docker/.env \
     -v "$(pwd)/app/students.db:/app/students.db" \
     chat-sql-ai

## GitHub Actions

- Every push to `main` runs the workflow in `.github/workflows/docker-build-test.yml`  
- It builds the Docker image and verifies that SQL queries run correctly inside the container

## Notes

- Requires OpenAI GPT-4 API key  
- Uses only Python standard libraries + `openai` and `pandas`  
- SQLite is used for simplicity and portability  

## License

MIT
