from flask import Flask, render_template, request, logging, send_file
import psycopg2
import os
from io import BytesIO
import logging
import requests
import time
import pandas as pd
app = Flask(__name__)
SECRET_KEY = os.getenv('SECRET_KEY')

def Get_Data():
    with get_db_connection() as conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM confessions")
            data = cursor.fetchall()
            allids = []
            alldata = []
            for row in data:
                allids.append(row[0])
                alldata.append(row[1])
            result = {
                "id": allids,
                "confessions": alldata
            }
        #result = [{"id": row[0],  "confession": row[1]} for row in data]
        except Exception as e:
            raise Exception(f"Unhandled Exception when getting data: {e}")
    return result

def TurnIntoCSV(data):
    try:
        df = pd.DataFrame(data)
        csv = df.to_csv(index=False)
    except Exception as e:
        raise Exception(f"Unhandled Exception at turning data to CSV format.: {e}")
    return csv

def Send_Data():
    try:
        data = Get_Data()
        csv = TurnIntoCSV(data)
        filestream = BytesIO(csv.encode())
        return send_file(filestream, None, as_attachment=True, download_name="confessions.csv")
    except Exception as e:
        print(f"Unhandled Exception when sending data {e}") # to not lead to another exception with the route

def verify_recaptcha(response_token):
    url = 'https://www.google.com/recaptcha/api/siteverify'
    data = {
        'secret': SECRET_KEY,
        'response': response_token
    }
    response = requests.post(url, data=data)
    result = response.json()
    return result.get('success')
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
    response_token = request.form.get('g-recaptcha-response')
    if verify_recaptcha(response_token):
        # Continue processing form
        confession = request.form.get('confession')
        if confession:
            try:
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute("INSERT INTO confessions (confession) VALUES (%s)", (confession,))
                conn.commit()
                return render_template('worked.html'), 200
            except Exception as e:
                app.logger.error(f"Error inserting confession: {e}")
                return render_template('error.html', errorcode = "Database didn't work.")
            finally:
                cur.close()
                conn.close()
        return "It didn't work :(", 400
    else:
        return render_template("error.html", errorcode = "Captcha verification bad.")
    
@app.route("/getdata")
def get_data():
    try:
        return Send_Data() # AHA!
    except Exception as e:
        raise Exception(f"Error while handling Send_Data() route. {e}")

if __name__ == '__main__':
    app.run(debug=True)
#ana jo3an kteer
