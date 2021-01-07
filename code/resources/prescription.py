from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    fresh_jwt_required,
    jwt_optional,
    jwt_required,
    get_jwt_claims,
    get_jwt_identity,
)
from models.prescription import PrescriptionModel

class PrescriptionRegister(Resource):
    _prescription_parser = reqparse.RequestParser()
    _prescription_parser.add_argument("text", type=str, required=True)
    _prescription_parser.add_argument("patient_id", type=int, required=True)
    _prescription_parser.add_argument("patient_name", type=str, required=True)
    _prescription_parser.add_argument("doctor_name", type=str, required=True)

    @jwt_required
    def post(cls):
        if get_jwt_claims()['type'] == 'doctor':
            data = PrescriptionRegister._prescription_parser.parse_args()
            prescription = PrescriptionModel(**data)
            prescription.save_to_db()
            return {'message': 'Prescription Added.'}
        return {'message': 'Only a doctor can add prescriptions.'}, 401

class Prescription(Resource):
    @classmethod
    @jwt_required
    def get(cls, prescription_id):
        prescription = PrescriptionModel.find_by_id(prescription_id)
        if prescription:
            return prescription.json()
        return {'message': 'prescription with that id does not exist'}, 404

class PatientPrescriptionList(Resource):
    @classmethod
    @jwt_required
    def get (cls):
        identity = get_jwt_identity()
        prescriptions = PrescriptionModel.query.filter_by(patient_id=identity).all()
        prescription_list = [prescription.json() for prescription in prescriptions]
        return prescription_list, 200

class PrescriptionsList(Resource):
    @classmethod
    @jwt_required
    def get (cls):
        if get_jwt_claims()['type'] == 'admin':
            prescriptions = PrescriptionModel.query.all()
            Prescription_list = [prescription.json() for prescription in prescriptions]
            return Prescription_list
        return {'message': 'Admin authorization required'}


