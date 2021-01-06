from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import(
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_raw_jwt,
    get_jwt_identity,
    jwt_required
)
from models.patient import PatientModel
from blacklist import BLACKLIST


class PatientRegister(Resource):
    patient_parser = reqparse.RequestParser()
    patient_parser.add_argument('username',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
    patient_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
    patient_parser.add_argument('first_name',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
    patient_parser.add_argument('last_name',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
    patient_parser.add_argument('age',
                          type=int,
                          required=True,
                          help="This field cannot be blank."
                          )                          
    patient_parser.add_argument('email',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
    patient_parser.add_argument('gender',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
    patient_parser.add_argument('mobile',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
    patient_parser.add_argument('address',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )                            
    def post(self):
        data = PatientRegister.patient_parser.parse_args()

        if PatientModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        if PatientModel.find_by_email(data['email']):
            return {"message": "A user with that email already exists"}, 400

        patient = PatientModel(**data)
        patient.save_to_db()

        return {"message": "User created successfully."}, 201


class Patient(Resource):

    @classmethod
    def get(cls,patient_id):
        patient = PatientModel.find_by_id(patient_id)
        if patient:
            return patient.json()
        return {'message':'User not found'}, 404    

    @classmethod
    def delete(cls,user_id):
        patient = PatientModel.find_by_id(user_id)
        if patient:
            patient.delete_from_db()
            return {'message':'User deleted'},200
        return {'message': 'User not found'},404    


class PatientLogin(Resource):

    patient_parser = reqparse.RequestParser()
    patient_parser.add_argument('username',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
    patient_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
    @classmethod
    def post(cls):
        data = cls.patient_parser.parse_args()

        patient = PatientModel.find_by_username(data['username'])

        if patient and safe_str_cmp(patient.password,data['password']):
            access_token = create_access_token(identity = patient.id, fresh = True, user_claims={'type': 'patient'})
            refresh_token = create_refresh_token(identity=patient.id, user_claims={'type': 'patient'})
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            },200
        return {'message': 'Invaild credentials'},401                        


#class pTokenRefresh(Resource):
#    @jwt_refresh_token_required
#    def post(self):
#        current_patient = get_jwt_identity()
#        new_token = create_access_token (identity = current_patient,fresh = False)
#        return {"access_token":new_token},200        


class PatientLogout(Resource):  
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti'] #jti is a "JWT ID", a unique identifier for a JWT
        BLACKLIST.add(jti)
        return {'message': 'Sucessfully logged out'},200           
