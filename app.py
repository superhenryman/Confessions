from flask import Flask, render_template, request, logging
import psycopg2
import os
from psycopg2 import sql
import logging
app = Flask(__name__)

database_url = os.getenv('DATABASE_URL')

if not database_url:
    app.logger.error("Database URL is not set up properly.")
    raise Exception("Database URL is not set up properly, please fix.")


def get_db_connection():
    database_url = os.getenv('DATABASE_URL')
    retry_count = 5
    for attempt in range(retry_count):
        try:
            conn = psycopg2.connect(database_url)
            return conn
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2 ** attempt)
    raise Exception("Failed to connect to the database after multiple attempts.")
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS confessions (
            id SERIAL PRIMARY KEY,
            confession TEXT NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

init_db()

if not app.debug:
    app.logger.setLevel(logging.DEBUG)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def gibmeyourmoney():
    confession = request.form.get('confession')
    if confession:
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO confessions (confession) VALUES (%s)", (confession,))
            conn.commit()
            cur.close()
            conn.close()

            return render_template('worked.html'), 200
        except Exception as e:
            app.logger.error(f"Error inserting confession: {e}")
            return render_template('error.html'), 500
    return "It didn't work :(", 400

if __name__ == '__main__':
    app.run(debug=True)
#ana jo3an kteer
