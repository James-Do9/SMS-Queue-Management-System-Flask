"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
from sms import send
from datastructures import Queue
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

queue=Queue()

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_all_users():
    response_body = {
        "msg": "Hello, this is all of the users",
        "resp": queue.get_queue()
    }

    return jsonify(response_body), 200

@app.route('/user', methods=['GET'])
def get_one_user():
    guest = queue.dequeue()
    #Extract phone # from guest and call the send method from sms with that phone #
    #Once the user sends the text, return a message back to the host. Guest has been texted as such #
    send(body='', to=guest['phone'])
    response_body = {
        "msg": "Hello, this is the phone number and user that the text message was sent!",
        "resp": guest
    }

    return jsonify(response_body), 200

@app.route('/users', methods=['POST'])
def add_new_user():
    item = request.get_json() #works!
    queue.enqueue(item)
    response_body = {
        "msg": "Hello, this is the new list of users! ",
        "resp": queue.get_queue()
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
