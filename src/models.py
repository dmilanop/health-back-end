from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=False, nullable=False)
    name = db.Column(db.String(100), nullable=False, unique=False)
    last_name = db.Column(db.String(150), nullable=False, unique=False)
    gender = db.Column(db.String(80), nullable=False, unique=False)
    date_of_birth = db.Column(db.String(25), nullable=False, unique=False)
    ailments = db.Column(db.String(60), nullable=False, unique=False)
    exercises = db.Column(db.String(60), nullable=False, unique=False)
    user_recipes = db.relationship('User_recipes', backref='user', lazy=True)
    medical_history = db.relationship('Medical_History', backref='user', lazy=True)

    @classmethod
    def register(cls, new_user):
        new_user = cls(**new_user)
        db.session.add(new_user)
        try:
            db.session.commit()
            return new_user
        except Exception as error:
            db.session.rollback()
            print(error.args)
            return None

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "last_name": self.last_name,
            "gender": self.gender,
            "date_of_birth": self.date_of_birth,
            "ailments": self.ailments,
            "exercises": self.exercises
            # do not serialize the password, its a security breach
        }

class User_recipes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipes = db.relationship('Recipes', backref='user_recipes', lazy=True)
    active = db.Column(db.Boolean, nullable=False, unique=False, default=True)

class Recipes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_recipes_id = db.Column(db.Integer, db.ForeignKey('user_recipes.id'), nullable=False)
    recipes_name = db.Column(db.String(150), nullable=False, unique=True)
    description = db.Column(db.String(250), nullable=False, unique=True)

class Medical_History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    height = db.Column(db.Float, nullable=False, unique=False)
    weight = db.Column(db.Float, nullable=False, unique=False)
    diabetes = db.Column(db.String(10), nullable=False, unique=False)
    uric_acid = db.Column(db.String(10), nullable=False, unique=False)
    gastric_ulcers = db.Column(db.String(10), nullable=False, unique=False)
    gastritis = db.Column(db.String(10), nullable=False, unique=False)
    cholesterol = db.Column(db.String(10), nullable=False, unique=False)
    triglycerides = db.Column(db.String(10), nullable=False, unique=False)
    dairy_intolerance = db.Column(db.String(10), nullable=False, unique=False)
    celiac = db.Column(db.String(10), nullable=False, unique=False)
    obesity = db.Column(db.String(10), nullable=False, unique=False)
    kidney_stones = db.Column(db.String(10), nullable=False, unique=False)
    inflametion_of_the_colon = db.Column(db.String(10), nullable=False, unique=False)
    heart_problems = db.Column(db.String(10), nullable=False, unique=False)

        @classmethod
        def register(cls, new_history):
            new_history = cls(**new_history)
            db.session.add(new_history)
            try:
                db.session.commit()
                return new_history
            except Exception as error:
                db.session.rollback()    
                print(error.args)
                return None

        def serialize(self):
            return {
                "user_id" : self.user_id,
                "height": self.height,
                "weight": self.weight,
                "diabetes": self.diabetes,
                "uric_acid": self.uric_acid,
                "gastric_ulcers": self.gastric_ulcers,
                "gastritis": self.gastric_ulcers,
                "cholesterol": self.cholesterol,
                "triglycerides": self.triglycerides,
                "dairy_intolerance": self.dairy_intolerance,
                "celiac": self.celiac,
                "obesity": self.obesity,
                "kidney_stones": self.kidney_stones,
                "inflametion_of_the_colon": self.inflametion_of_the_colon,
                "heart_problems": self.heart_problems
            }