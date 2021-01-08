from flask_restful import Resource, reqparse
from models.appointment import appointmentModel
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
class appointment(Resource):
    appointment_parser = reqparse.RequestParser()
    appointment_parser.add_argument(
        "doctor_id", type=int, required=True, help="This field cannot be blank."
    )
    appointment_parser.add_argument("patient_id", type=int, required=False)
    appointment_parser.add_argument(
        "date", type=str, required=True, help="This field cannot be blank."
    )

    @jwt_required
    @classmethod
    def post(cls):
        claims = get_jwt_claims()
        if claims["type"] == "doctor":
            return {"message": "Access denied"}

        identity = get_jwt_identity()
        data = cls.appointment_parser.parse_args()
        if  data["date"].isspace():
            return {'message': 'One of the inputs is empty'},400

        data["patient_id"] = identity

        doctor = DoctorModel.find_by_id(data["doctor_id"])
        if not doctor:
            return {"message": "Doctor not found"}, 404

        data["current_time"] = datetime.now().strftime("%Y-%m-%d")
        y1, m1, d1 = [int(x) for x in data["date"].split("-")]
        y2, m2, d2 = [int(x) for x in data["current_time"].split("-")]
        
        appdate = datetime(y1, m1, d1)
        current_date = datetime(y2, m2, d2)

        if appdate < current_date:
            return {"message": "Invalid date"}

        appointmentModel.main(appdate)    

        appointment = appointmentModel(**data)
        appointment.save_to_db()
        return {"message": "Appointment created successfully."}, 201

    @classmethod
    @jwt_required
    def get(cls):
        identity = get_jwt_identity()
        claims = get_jwt_claims()

        if claims["type"] == "doctor":
            doctor_appointments = DoctorModel.find_by_id(identity).appointments

            doctorapp = []
            for appointment in doctor_appointments:
                doctorapp.append(appointment.json())
            return doctorapp

        elif claims["type"] == "patient":
            patient_appointments = PatientModel.find_by_id(identity).appointments

            patientapp = []
            for appointment in patient_appointments:
                patientapp.append(appointment.json())
            return patientapp

        else:
            patents = appointmentModel.find_all()
            patientapp = []
            for appointment in patients:
                patientapp.append(appointment.json())

            return patientapp


class deleteAppointments(Resource):
    @classmethod
    @jwt_required
    def delete(cls, app_id):
        claims = get_jwt_claims()
        if claims["type"] != "admin":
            return {"message": "access denied"}

        app = appointmetModel.find_by_id(app_id)
        if not app:
            return {"message": "Appointment not found"}, 404
        app.delete_from_db()
        return {"message": "Appointment deleted"}
