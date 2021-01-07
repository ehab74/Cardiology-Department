from flask import jsonify
from flask_restful import Resource, reqparse
from models.doctor import DoctorModel
from werkzeug.security import safe_str_cmp
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
    def delete(cls, doctor_id: int):
        doctor = DoctorModel.find_by_id(doctor_id)
        if not doctor:
            return {"message": USER_NOT_FOUND}, 404
        doctor.delete_from_db()
        return {"message": USER_DELETED}


class DoctorLogin(Resource):
    @classmethod
    def post(cls):

        _doctor_parser = reqparse.RequestParser()
        _doctor_parser.add_argument("username", type=str, required=True, help=BLANK)

        _doctor_parser.add_argument("password", type=str, required=True, help=BLANK)
        data = _doctor_parser.parse_args()
        doctor = DoctorModel.find_by_username(data["username"])
        if doctor and safe_str_cmp(doctor.password, data["password"]):
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


# class TokenRefresh(Resource):
#     @classmethod
#     @jwt_refresh_token_required
#     def post(cls):
#         current_user = get_jwt_identity()
#         new_token = create_access_token(identity=current_user, fresh=False)
#         return {"access_token": new_token}, 200

 


