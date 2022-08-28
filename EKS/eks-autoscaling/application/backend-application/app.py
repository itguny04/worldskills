from flask import *
import math
app = Flask(__name__)
v1 = Blueprint('v1', __name__, url_prefix='/v1')

@v1.route('/')
def index():
    return render_template_string('hello this is index page.')

@v1.route('/health')
def health():
    return jsonify({'status':'up'})

@v1.route('/<username>')
def username(username):
    return jsonify({'username':f'{username}', 'message':f'hello! {username}'})

@v1.route('/<username>/<command>')
def username_command(username, command):
    return jsonify({'username':f'{username}', 'message':f'hello! {username}'})

@v1.route('/ip')
def ip():
    return jsonify({'user-ip':request.remote_addr})

@v1.route('/stress')
def stress():
    x = 0.0001
    for i in range(100000000):
        x += math.sqrt(x)
    return jsonify({'status':'ok'})

app.register_blueprint(v1)
app.run(host='0.0.0.0', port=8080)
