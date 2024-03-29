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
from models import db, User, Medical_History
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('FLASK_APP_KEY')
jwt = JWTManager(app)
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

@app.route('/<string:nature>', methods=['GET'])
def handle_user(nature):
    response = []
    if nature == 'user':
        users = User.query.all()
        if users:
            for user in users:
                response.append(user.serialize())
            return jsonify(response), 200
        else:
            return jsonify([]), 500
        return jsonify({"message":"Bad request"}), 400 

    if nature == 'medical_history':
        histories = Medical_History.query.all()
        if histories:
            for history in histories:
                response.append(history.serialize())
            return jsonify(response), 200
        else:
            return jsonify([]), 500
        return jsonify({"message":"Bad request"}), 400


@app.route('/id_medical_history', methods=['GET'])
@jwt_required()
def handle_medical_history_id():
    user_id = get_jwt_identity()
    try:
        medical_information = Medical_History.query.filter_by(user_id= user_id).one_or_none()
        return jsonify(medical_information.serialize()), 200
    except Exception as error:
        return({"message":"Does not exist"}), 404


@app.route('/id_user', methods=['GET'])
@jwt_required()
def handle_user_id():
    user_id = get_jwt_identity()
    try:
        user_information = User.query.filter_by(id= user_id).one_or_none()
        return jsonify(user_information.serialize()), 200
    except Exception as error:
        return({"message":"Does not exist"}), 404


@app.route("/logup", methods=['POST'])
def handle_nature():
    body = request.json
    new_user = User.register(body)
    if new_user is not None:
        try:
            token = create_access_token(identity = new_user.id)
            return jsonify({"token": token, "user_id": new_user.id, "email": new_user.email, "name": new_user.name}), 201
        except Exception as error:
            return jsonify({"message": "oh oh, can't create token"}), 500
    else:
        return jsonify({"message": "Oops, check if you don't have empty fields"}), 500      


@app.route('/login', methods=['POST'])
def handle_log_in():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(email = email, password = password).one_or_none()
    if user is not None:
        token = create_access_token(identity = user.id)
        return jsonify({"token": token, "user_id": user.id, "email": user.email, "name": user.name}), 200
    else:
        return jsonify({"message":"Put your correct credentials"}), 401

@app.route('/delete_acount', methods=['DELETE'])   
@jwt_required()   
def handle_delete_user():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id = user_id).one_or_none()
    if user is not None:
        user_delete = user.delete()
        if user_delete == True:
            return jsonify([]), 204
        else:
            return jsonify({"message": "oops, method does not work, please try again"}), 500
    else:
        return jsonify({"message": "oops, not found"}), 404   

@app.route('/medical_history', methods=['POST','PUT'])
@jwt_required()
def handle_medical_history():
    height = request.json["height"]
    weight = request.json["weight"]
    diabetes = request.json["diabetes"]
    uric_acid = request.json["uric_acid"]
    gastric_ulcers = request.json["gastric_ulcers"]
    gastritis = request.json["gastritis"]
    cholesterol = request.json["cholesterol"]
    triglycerides = request.json["triglycerides"]
    dairy_intolerance = request.json["dairy_intolerance"]
    celiac = request.json["celiac"]
    obesity = request.json["obesity"]
    kidney_stones = request.json["kidney_stones"]
    inflammation_of_the_colon = request.json["inflammation_of_the_colon"]
    heart_problems = request.json["heart_problems"]  

    if request.method == 'POST':
        new_history = Medical_History(
            user_id = get_jwt_identity(),
            height =  height,
            weight = weight,
            diabetes = diabetes,
            uric_acid = uric_acid,
            gastric_ulcers = gastric_ulcers,
            gastritis = gastritis,
            cholesterol = cholesterol,
            triglycerides = triglycerides,
            dairy_intolerance = dairy_intolerance,
            celiac = celiac,
            obesity = obesity,
            kidney_stones = kidney_stones,
            inflammation_of_the_colon = inflammation_of_the_colon,
            heart_problems = heart_problems  
        )
        db.session.add(new_history)
        try:
            db.session.commit()
            return jsonify(new_history.serialize()), 201
        except Exception as error:
            db.session.rollback()
            return jsonify(error.args), 500 
    if request.method == 'PUT':
        user_id = get_jwt_identity()
        old_history = Medical_History.query.filter_by(user_id= user_id).one_or_none()
        modified = old_history.put(request.json)
        if modified:
            return jsonify(old_history.serialize()), 201
        else:
            return jsonify({"message":"Try again"}), 500        


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)