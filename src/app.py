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
from models import db, User, People, Planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/people')
def get_people():
    
    people = People.query.all()
    people_serialize = [person.serialize() for person in people]

    return jsonify(people_serialize), 200

@app.route('/people/<int:people_id>')
def get_person(people_id):
    
    person = People.query.get(people_id)
    if person: 
        person_serialize = person.serialize()

        return jsonify(person_serialize)
    else: 
        return jsonify({"msg": "Person not found"}), 400
    
@app.route('/planets')
def get_planets():
    
    planets = Planets.query.all()
    planets_serialize = [planet.serialize() for planet in planets]

    return jsonify(planets_serialize), 200

@app.route('/planets/<int:planets_id>')
def get_planet(planets_id):
    
    planet = Planets.query.get(planets_id)
    if planet: 
        planet_serialize = planet.serialize()

        return jsonify(planet_serialize)
    else: 
        return jsonify({"msg": "Planet not found"}), 400

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
