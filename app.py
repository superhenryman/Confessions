from flask import Flask, render_template, request, app
import logging
import psycopg2 as psy
import os
app = Flask(__name__)
database = os.getenv('postgresql://postgres:ObdGQvQZEHOaxnKQtyXLbUZCoXTEFDmv@postgres.railway.internal:5432/railway')
conn == psy.connect(database)
cur = conn.cursor()
cur.execute("""
        CREATE TABLE IF NOT EXISTS confessions (
            id SERIAL PRIMARY KEY,
            confession TEXT NOT NULL
        );
    """)
conn.commit()

logging.basicConfig(level=logging.DEBUG)
@app.route('/')
def index():
    return render_template('index.html')
def worked():
    return render_template('worked.html')
@app.route('/submit', methods=['POST'])
def gibmeyourmoney():
    confession = request.form.get('confession')
    if confession:
        try:
            cur.execute("INSERT INTO confessions (confessions) VALUE (%s)", (confession,))
            conn.commit()
            app.logger.debug(f"Confession saved: {confession}")
            return render_template('worked.html'), 200
        except Exception as e:
            return render_template('error.html')
            return f"Error: {str(e)}", 500
    return "It didn't work :(", 400

