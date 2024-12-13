from flask import Flask, render_template, request, app
from werkzeug.utils import quote
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
def worked():
    return render_template('worked.html')
@app.route('/submit', methods=['POST'])
def gibmeyourmoney():
    confession = request.form.get('confession')
    if confession:
        with open('confession.txt', 'a') as file:
            file.write(confession  + '\n')
        return worked(), 200
    return "It didn't work :(", 400
