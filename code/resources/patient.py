from flask_restful import Resource, reqparse
from werkzeug.security import check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_raw_jwt,
    get_jwt_identity,
    get_jwt_claims,
    jwt_required,
)
from models.patient import PatientModel
from blacklist import BLACKLIST
from datetime import datetime, timedelta


class PatientRegister(Resource):
    patient_parser = reqparse.RequestParser()
    patient_parser.add_argument(
        "username", type=str, required=True, help="This field cannot be blank."
    )
    patient_parser.add_argument(
        "password", type=str, required=True, help="This field cannot be blank."
    )
    patient_parser.add_argument(
        "first_name", type=str, required=True, help="This field cannot be blank."
    )
    patient_parser.add_argument(
        "last_name", type=str, required=True, help="This field cannot be blank."
    )
    patient_parser.add_argument(
        "email", type=str, required=True, help="This field cannot be blank."
    )
    patient_parser.add_argument(
        "gender", type=str, required=True, help="This field cannot be blank."
    )
    patient_parser.add_argument(
        "mobile", type=str, required=True, help="This field cannot be blank."
    )
    patient_parser.add_argument(
        "address", type=str, required=True, help="This field cannot be blank."
    )
    patient_parser.add_argument(
        "birthdate", type=str, required=True, help="This field cannot be blank"
    )

    def post(self):
        data = PatientRegister.patient_parser.parse_args()

        if (
            data["username"].isspace()
            or data["password"].isspace()
            or data["address"].isspace()
            or data["mobile"].isspace()
            or data["email"].isspace()
            or data["first_name"].isspace()
            or data["last_name"].isspace()
        ):
            return {"message": "One of the inputs is empty"}, 400

        if len(data["username"]) < 5:
            return {"message": "Username is too short"}, 400

        if PatientModel.find_by_username(data["username"]):
            return {"message": "A user with that username already exists"}, 400

        if PatientModel.find_by_email(data["email"]):
            return {"message": "A user with that email already exists"}, 400

        data["gender"] = int(data["gender"])
        if data["gender"] != 0 and data["gender"] != 1:
            return {
                "message": "Invalid request: gender is only '0' if male or '1' if female"
            }

        patient = PatientModel(**data)
        patient.save_to_db()

        return {"message": "User created successfully."}, 201


class Patient(Resource):
    @classmethod
    @jwt_required
    def get(cls, patient_id):
        if get_jwt_claims()["type"] == "admin":
            patient = PatientModel.find_by_id(patient_id)
            if patient:
                return patient.json_with_appointments()
            return {"message": "User not found"}, 404
        return {"message": "You have to be an admin"}

    @classmethod
    @jwt_required
    def delete(cls, patient_id):
        if get_jwt_claims()["type"] == "admin":
            patient = PatientModel.find_by_id(patient_id)
            if patient:
                patient.delete_from_db()
                return {"message": "User deleted"}, 200
            return {"message": "User not found"}, 404
        return {"message": "Admin authorization required."}


class PatientLogin(Resource):

    patient_parser = reqparse.RequestParser()
    patient_parser.add_argument(
        "username", type=str, required=True, help="This field cannot be blank."
    )
    patient_parser.add_argument(
        "password", type=str, required=True, help="This field cannot be blank."
    )

    @classmethod
    def post(cls):
        data = cls.patient_parser.parse_args()

        patient = PatientModel.find_by_username(data["username"])

        if patient and check_password_hash(patient.password, data["password"]):
            access_token = create_access_token(
                identity=patient.id,
                fresh=True,
                user_claims={"type": "patient"},
                expires_delta=timedelta(1),
            )
            refresh_token = create_refresh_token(
                identity=patient.id, user_claims={"type": "patient"}
            )
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        return {"message": "Invaild credentials"}, 401


# class pTokenRefresh(Resource):
#    @jwt_refresh_token_required
#    def post(self):
#        current_patient = get_jwt_identity()
#        new_token = create_access_token (identity = current_patient,fresh = False)
#        return {"access_token":new_token},200


class PatientLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()["jti"]  # jti is a "JWT ID", a unique identifier for a JWT
        BLACKLIST.add(jti)
        return {"message": "Sucessfully logged out"}, 200


class PatientList(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        if get_jwt_claims()["type"] == "admin":
            patients = PatientModel.find_all()
            patients_list = [patient.json() for patient in patients]
            return patients_list, 200
        return {"message": "Authorization required."}
