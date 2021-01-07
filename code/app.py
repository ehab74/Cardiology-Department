from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager, get_raw_jwt
import mysql.connector

# import pymysql
from blacklist import BLACKLIST

from resources.doctor import DoctorRegister, Doctor, DoctorLogin, DoctorLogout, DoctorList
from resources.patient import PatientRegister, Patient, PatientLogin, PatientLogout, PatientList
from resources.admin import AdminRegister, AdmingLogin, AdminLogout
from resources.prescription import PrescriptionRegister, Prescription, PrescriptionList
from resources.refresh import TokenRefresh



# pymysql.install_as_MySQLdb()
app = Flask(__name__)
CORS(app)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+mysqlconnector://root:mysql@localhost/cardio"  # "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
app.secret_key = "my_secret_key"
api = Api(app)

database = "cardio"


@app.before_first_request
def create_tables():
    engine = db.create_engine(
        "mysql+mysqlconnector://root:mysql@localhost", {}
    )  # connect to server
    existing_databases = engine.execute("SHOW DATABASES")
    existing_databases = [d[0] for d in existing_databases]

    if database not in existing_databases:
        engine.execute("CREATE DATABASE {}".format(database))
    db.create_all()


jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    user_claims = get_raw_jwt()["user_claims"]
    if user_claims["type"] == "doctor":
        return {"type": "doctor"}
    elif user_claims["type"] == "patient":
        return {"type": "patient"}
    else:
        pass


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


@jwt.expired_token_loader
def expired_token_callback():
    return (
        jsonify({"description": "The token has expired.", "error": "Token expired"}),
        401,
    )


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify(
            {"description": "Signature verification failed.", "error": "Invalid token"}
        ),
        401,
    )


@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return (
        jsonify(
            {"description": "The token is not fresh.", "error": "fresh token required"}
        ),
        401,
    )


@jwt.revoked_token_loader
def revoked_token_callback():
    return (
        jsonify(
            {"description": "The token has been revoked.", "error": "token_revoked"}
        ),
        401,
    )


# Resources
api.add_resource(DoctorRegister, "/doctor/register")
api.add_resource(Doctor, "/doctor/?id=<int:doctor_id>")
api.add_resource(DoctorLogin, "/doctor/login")
api.add_resource(DoctorLogout, "/doctor/logout")
api.add_resource(DoctorList, "/doctors")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(PatientRegister, "/patient/reg")
api.add_resource(Patient, "/patient/<int:patient_id>")
api.add_resource(PatientLogin, "/patient/login")
api.add_resource(PatientList, "/patients")
api.add_resource(PatientLogout, "/patient/logout")
api.add_resource(AdminRegister, "/admin/register")
api.add_resource(AdmingLogin, "/admin/login")
api.add_resource(AdminLogout, "/admin/logout")
api.add_resource(PrescriptionRegister, "/add_prescription")
api.add_resource(Prescription, "/prescription/<int:prescription_id>")
api.add_resource(PrescriptionList, "/patient/prescriptions")


if __name__ == "__main__":
    from db import db

    db.init_app(app)
    app.run(host="localhost", port=5000, debug=True)
