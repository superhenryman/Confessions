from flask import Flask, render_template, request, app
import logging
app = Flask(__name__)
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
            with open('confession.txt', 'a') as file:
                file.write(confession + '\n')
            app.logger.debug(f"Confession saved: {confession}")
            return render_template('worked.html'), 200
        except Exception as e:
            return render_template('error.html')
            return f"Error: {str(e)}", 500
    return "It didn't work :(", 400

