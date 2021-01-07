from db import db

class PrescriptionModel(db.Model):
    __tablename__ = 'Prescriptions'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('Patients.id'))
    patient = db.relationship("PatientModel")
    text = db.Column(db.String(500))
    patient_name = db.Column(db.String(80))
    doctor_name = db.Column(db.String(80))

    def __init__(self, patient_id: int, text: str, patient_name: str, doctor_name: str):
        self.patient_id = patient_id
        self.text = text
        self.patient_name = patient_name
        self.doctor_name = doctor_name
    def json(self):
        return{
            "_id": self.id,
            "patient_id": self.patient_id,
            "text": self.text,
            "doctor_name": self.doctor_name,
            "patient_name": self.patient_name

        }
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
    