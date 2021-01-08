from db import db
from werkzeug.security import generate_password_hash
from models.doctor import DoctorModel
from models.examination import ExaminationModel
from models.appointment import AppointmentModel
from sqlalchemy import Enum
from datetime import datetime


class GenderEnum(Enum):
    male = 0
    female = 1


class PatientModel(db.Model):
    __tablename__ = "Patients"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True)
    mobile = db.Column(db.String(80))
    address = db.Column(db.String(80))
    gender = db.Column(db.Integer)
    birthdate = db.Column(db.DateTime)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(128))

    appointments = db.relationship("AppointmentModel")

    def __init__(
        self,
        first_name,
        last_name,
        email,
        mobile,
        gender,
        birthdate,
        username,
        password,
        address,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.mobile = mobile
        self.gender = gender
        self.birthdate = birthdate
        self.username = username
        self.password = generate_password_hash(password)
        self.address = address

    def json(self):
        return {
            "_id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "mobile": self.mobile,
            "gender": "male" if self.gender == 0 else "female",
            "birthdate": str(self.birthdate),
            "age": (datetime.now() - self.birthdate).days // 365,
            "username": self.username,
            "address":self.address
            # 'appointments': [appointment.json() for appointment in self.appointments.all()],
        }

    def json_with_appointments(self):
        return {
            "_id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "mobile": self.mobile,
            "gender": "male" if self.gender == 0 else "female",
            "birthdate": str(self.birthdate),
            "age":(datetime.now() - self.birthdate).days // 365,
            "username": self.username,
            "appointments": [appointment.json() for appointment in self.appointments],
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(PatientModel, patient_id):
        patientAppointments = (
            PatientModel.query.filter(PatientModel.id == patient_id)
            .join(AppointmentModel, PatientModel.id == AppointmentModel.patient_id)
            .first()
        )
        return patientAppointments

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_doctor(PatientModel, doctor_id):
        patientList = PatientModel.query.join(
            AppointmentModel, PatientModel.id == AppointmentModel.patient_id
        ).filter(AppointmentModel.doctor_id == doctor_id)
        return patientList
