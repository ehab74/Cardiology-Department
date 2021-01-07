from db import db
from werkzeug.security import generate_password_hash


class PatientModel(db.Model):
    __tablename__ = "Patients"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True)
    mobile = db.Column(db.String(80))
    address = db.Column(db.String(80))
    gender = db.Column(db.String(80))
    age = db.Column(db.Integer)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(128))
    prescriptions = db.relationship("PrescriptionModel", lazy="dynamic")

    def __init__(
        self,
        first_name,
        last_name,
        email,
        mobile,
        gender,
        age,
        username,
        password,
        address,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.mobile = mobile
        self.gender = gender
        self.age = age
        self.username = username
        self.password = generate_password_hash(password)
        self.address = address
        

    def json(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "mobile": self.mobile,
            "gender": self.gender,
            "age": self.age,
            "username": self.username,
            "prescriptions": [Prescriptions.json() for item in self.items.all()]
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def find_all(cls):
        return cls.query.all()
