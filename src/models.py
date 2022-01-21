from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=False, nullable=False)

    # def serialize(self):
    #     return {
    #         "id": self.id,
    #         "email": self.email,
    #         # do not serialize the password, its a security breach
    #     }

class User_recipes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # recipes_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)

class Recipes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipes_name = db.Column(db.String(150), nullable=False, unique=True)
    description = db.Column(db.String(250), nullable=False, unique=True)

class User_information(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False, unique=False)
    last_name = db.Column(db.String(150), nullable=False, unique=False)
    gender = db.Column(db.String(80), nullable=False, unique=False)
    date_of_birth =db.Column(db.Integer, nullable=False, unique=False)
    height = db.Column(db.Float, nullable=False, unique=False)
    weight = db.Column(db.Float, nullable=False, unique=False)
    ailments = db.Column(db.Boolean, nullable=False, unique=False)
    exercises = db.Column(db.Boolean, nullable=False, unique=False)

class Medical_history(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    diabetes = db.Column(db.Boolean, nullable=False, unique=False)
    uric_acid = db.Column(db.Boolean, nullable=False, unique=False)
    gastric_ulcers = db.Column(db.Boolean, nullable=False, unique=False)
    gastritis = db.Column(db.Boolean, nullable=False, unique=False)
    cholesterol = db.Column(db.Boolean, nullable=False, unique=False)
    triglycerides = db.Column(db.Boolean, nullable=False, unique=False)
    dairy_intolerance = db.Column(db.Boolean, nullable=False, unique=False)
    celiac = db.Column(db.Boolean, nullable=False, unique=False)
    obesity = db.Column(db.Boolean, nullable=False, unique=False)
    kidney_stones = db.Column(db.Boolean, nullable=False, unique=False)
    inflametion_of_the_colon = db.Column(db.Boolean, nullable=False, unique=False)
    heart_problems = db.Column(db.Boolean, nullable=False, unique=False)