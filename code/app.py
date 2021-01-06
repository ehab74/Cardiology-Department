from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
import mysql.connector

from resources.doctor import (
    DoctorRegister,
    Doctor,
    DoctorLogin,
    DoctorLogout,
    TokenRefresh,
)
from blacklist import BLACKLIST

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+mysqlconnector://root:12345@localhost:3306/databaseproject"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
app.secret_key = "my_secret_key"
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if (
        identity == 1
    ):  # Instead of hard-coding, you should read from a config file or a database
        return {"is admin": True}
    return {"is admin": False}


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
api.add_resource(DoctorRegister, "/doctor_register")
api.add_resource(Doctor, "/doctor/<int:doctor_id>")
api.add_resource(DoctorLogin, "/doctor_login")
api.add_resource(DoctorLogout, "/doctor_logout")
api.add_resource(TokenRefresh, "/doctor_refresh")

if __name__ == "__main__":
    from db import db

    db.init_app(app)
    app.run(host="localhost", port=5000, debug=True)
