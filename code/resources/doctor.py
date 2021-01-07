from flask import jsonify
from flask_restful import Resource, reqparse
from models.doctor import DoctorModel
from models.patient import PatientModel
from models.examination import ExaminationModel
from werkzeug.security import check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    jwt_required,
    get_raw_jwt,
    get_jwt_identity,
    get_jwt_claims,
)
from blacklist import BLACKLIST

BLANK = "This field cannot be left blank."


BLANK_ERROR = "'{}' cannot be blank."
DOCTOR_ALREADY_EXISTS = "A doctor with that username already exists."
DOCTOR_ALREADY_EXISTS2 = "A doctor with that email already exists."
CREATED_SUCCESSFULLY = "Doctor created successfully."
USER_NOT_FOUND = "Doctor not found."
USER_DELETED = "Doctor deleted."
INVALID_CREDENTIALS = "Invalid credentials!"
USER_LOGGED_OUT = "Doctor <id={doctor_id}> successfully logged out."


class DoctorRegister(Resource):
    @classmethod
    def post(cls):
        _doctor_parser = reqparse.RequestParser()
        _doctor_parser.add_argument("username", type=str, required=True, help=BLANK)

        _doctor_parser.add_argument("password", type=str, required=True, help=BLANK)

        _doctor_parser.add_argument("first_name", type=str, required=True, help=BLANK)

        _doctor_parser.add_argument("last_name", type=str, required=True, help=BLANK)

        _doctor_parser.add_argument("email", type=str, required=True, help=BLANK)

        _doctor_parser.add_argument("mobile", type=str, required=True, help=BLANK)

        _doctor_parser.add_argument("gender", type=str, required=True, help=BLANK)

        _doctor_parser.add_argument("address", type=str, required=True, help=BLANK)

        _doctor_parser.add_argument("age", type=int, required=True, help=BLANK)

        data = _doctor_parser.parse_args()
        if (
            data["username"].isspace()
            or data["password"].isspace()
            or data["age"].isspace()
            or data["gender"].isspace()
            or data["address"].isspace()
            or data["mobile"].isspace()
            or data["email"].isspace()
            or data["first_name"].isspace()
            or data["last_name"].isspace()
        ):
            return {'message': 'One of the inputs is empty'},400

        if len(data['username']) <5:
            return {'message' : 'Username is too short'},400

        if data["age"] <= 0:
            return {"message": "Age must be greater than 0"}, 400

        if DoctorModel.find_by_username(data["username"]):
            return {"message": DOCTOR_ALREADY_EXISTS}, 400

        if DoctorModel.find_by_email(data["email"]):
            return {"message": DOCTOR_ALREADY_EXISTS2}, 400

        user = DoctorModel(**data)
        user.save_to_db()

        return {"message": CREATED_SUCCESSFULLY}


class Doctor(Resource):
    @classmethod
    def get(cls, doctor_id: int):
        user = DoctorModel.find_by_id(doctor_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404
        return user.json()

    @classmethod
    @jwt_required
    def delete(cls, doctor_id: int):
        if get_jwt_claims()["type"] == "admin":
            doctor = DoctorModel.find_by_id(doctor_id)
            if not doctor:
                return {"message": USER_NOT_FOUND}, 404
            doctor.delete_from_db()
            return {"message": USER_DELETED}
        return {"message": "Admin authorization required."}


class DoctorLogin(Resource):
    @classmethod
    def post(cls):

        _doctor_parser = reqparse.RequestParser()
        _doctor_parser.add_argument("username", type=str, required=True, help=BLANK)

        _doctor_parser.add_argument("password", type=str, required=True, help=BLANK)
        data = _doctor_parser.parse_args()
        doctor = DoctorModel.find_by_username(data["username"])
        if doctor and check_password_hash(doctor.password, data["password"]):
            access_token = create_access_token(
                identity=doctor.id, fresh=True, user_claims={"type": "doctor"}
            )
            refresh_token = create_refresh_token(
                identity=doctor.id, user_claims={"type": "doctor"}
            )
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        return {"message": INVALID_CREDENTIALS}, 401


class DoctorLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        BLACKLIST.add(jti)
        doctor_id = get_jwt_identity()
        return {"message": USER_LOGGED_OUT.format(doctor_id=doctor_id)}


class DoctorList(Resource):
    @classmethod
    def get(cls):
        doctors = DoctorModel.find_all()
        doctors_list = []
        for doctor in doctors:
            doctors_list.append(
                {
                    "first_name": doctor[0],
                    "last_name": doctor[1],
                    "mobile": doctor[2],
                    "age": doctor[3],
                    "_id": doctor[4],
                }
            )

        return doctors_list, 200

class DoctorPatient(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        if get_jwt_claims()['type'] == 'doctor':
            identity = get_jwt_identity()
            patients = ExaminationModel.find_by_examinations(identity)
            return patients, 200
        return {'message': 'You must have a doctor authorization.'}



# class TokenRefresh(Resource):
#     @classmethod
#     @jwt_refresh_token_required
#     def post(cls):
#         current_user = get_jwt_identity()
#         new_token = create_access_token(identity=current_user, fresh=False)
#         return {"access_token": new_token}, 200
