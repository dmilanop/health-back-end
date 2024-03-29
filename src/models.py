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
    exercises = db.Column(db.String(60), nullable=False, unique=False)
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
            "exercises": self.exercises
            # do not serialize the password, its a security breach
        }

    def delete(self):
        delete_acount = Medical_History.query.filter_by(user_id=self.id).one_or_none()
        delete_acount.delete()
        db.session.delete(self)
        try:
            db.session.commit()
            return True
        except Exception as error:
            db.session.rollback()
            return False    

class Medical_History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    height = db.Column(db.Float, nullable=False, unique=False)
    weight = db.Column(db.Integer, nullable=False, unique=False)
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
    inflammation_of_the_colon = db.Column(db.String(10), nullable=False, unique=False)
    heart_problems = db.Column(db.String(10), nullable=False, unique=False)

    def serialize(self):
        return {
            "user_id": self.user_id,
            "height": self.height,
            "weight": self.weight,
            "diabetes": self.diabetes,
            "uric_acid": self.uric_acid, 
            "gastric_ulcers": self.gastric_ulcers,
            "gastritis": self.gastritis,
            "cholesterol": self.cholesterol,
            "triglycerides": self.triglycerides,
            "dairy_intolerance": self.dairy_intolerance,
            "celiac": self.celiac,
            "obesity": self.obesity,
            "kidney_stones": self.kidney_stones,
            "inflammation_of_the_colon": self.inflammation_of_the_colon,
            "heart_problems": self.heart_problems
        }
    
    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
            return True
        except Exception as error:
            db.session.rollback()
            return False  
    
    def put(self, attribute):
        for key, value in attribute.items():
            setattr(self, key, value)
        try:
            db.session.commit()
            return True
        except Exception as error:
            db.session.rollback()
            return False
