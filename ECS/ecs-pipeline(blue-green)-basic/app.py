from flask import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('hello this is index page.')

@app.route('/health')
def health():
    return jsonify({'status':'up'})

@app.route('/<username>')
def username(username):
    return render_template_string(f'Hello {username}!')

@app.route('/<username>/<command>')
def username_command(username, command):
    return render_template_string(f'Hello {username}!<br>Your input is {command}!')

app.run(host='0.0.0.0', port=8080)
