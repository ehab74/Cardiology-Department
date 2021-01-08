from models.examination import ExaminationModel
from flask_restful import Resource, reqparse
from datetime import datetime
from models.doctor import DoctorModel
from models.patient import PatientModel
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    jwt_required,
    get_raw_jwt,
    get_jwt_identity,
    get_jwt_claims,
)
BLANK = "This field cannot be left blank"

class ExaminationRegister(Resource):
    examination_parser = reqparse.RequestParser()
    examination_parser.add_argument("patient_id", type=int, required=True, help=BLANK)
    examination_parser.add_argument("doctor_id", type=int, required=False)
    examination_parser.add_argument("check_in_date", type=str, required=False)
    examination_parser.add_argument("diagnosis", type=str, required=True, help=BLANK)
    examination_parser.add_argument("patient_name", type=str, required=True, help=BLANK)
    examination_parser.add_argument("doctor_name", type=str, required=True, help=BLANK)
    @classmethod
    @jwt_required
    def post(cls):
        data = cls.examination_parser.parse_args()
         if (
            data["diagnosis"].isspace()
            or data["patient_name"].isspace()
            or data["doctor_name"].isspace()
        ):
            return {'message': 'One of the inputs is empty'},400
        if get_jwt_claims()['type'] == "doctor":
            patient = PatientModel.find_by_id(data['patient_id'])
            if patient:
                data['doctor_id'] = get_jwt_identity()
                data['check_in_date'] = datetime.now().strftime("%d/%m/%Y")
                examination = ExaminationModel(**data)
                examination.save_to_db()
                return {'message': 'Added Successfully.'}
            return {'message': 'Patient not found'}
        return {'message': 'Authorization required: You must be a doctor.'}
    
class PatientExaminations(Resource):
    @classmethod
    @jwt_required
    def get(cls, patient_id):
        if get_jwt_claims()['type'] == 'doctor':
            examinations = ExaminationModel.find_all_filtered(patient_id)
            examination_list = [examination.json() for examination in examinations]
            return examination_list, 200
        return {'message': 'Unauthorized: You must be a doctor'}

class Examination(Resource):
    @classmethod
    @jwt_required
    def get(cls, examination_id):
        if get_jwt_claims()['type'] == 'doctor' or get_jwt_claims()['type'] == 'admin':
            examination = ExaminationModel.find_by_id(examination_id)
            return examination.json()
        return {'message': 'Invalid authorization'}

    @classmethod
    @jwt_required
    def delete(cls, examination_id):
        if get_jwt_claims()['type'] == 'admin':
            examination = ExaminationModel.find_by_id(examination_id)
            examination.delete_from_db()
            return {'message': 'Deleted Successfully.'}
        return {'message': 'Unauthorized: Admin authorization required.'}

class ExaminationList(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        if get_jwt_claims()['type'] == 'admin':
            examinations = ExaminationModel.find_all()
            examinations_list = [examination.json() for examination in examinations]
            return examinations_list, 200
        return {'message': 'Unauthorized: Admin authorization required.'}







