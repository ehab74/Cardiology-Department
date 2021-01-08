from db import db

class ExaminationModel(db.Model):
    __tablename__ = 'Examinations'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('Patients.id'))
    patient = db.relationship("PatientModel")
    doctor_id = db.Column(db.Integer, db.ForeignKey('Doctors.id'))
    doctor = db.relationship("DoctorModel")
    check_in_date = db.Column(db.String(80))
    diagnosis = db.Column(db.String(500))
    doctor_name = db.Column(db.String(80))
    patient_name = db.Column(db.String(80))

    def __init__(self, patient_id: int, doctor_id: int, check_in_date: str, diagnosis: str, doctor_name:str, patient_name:str):
        
        self.patient_id = patient_id
        self.diagnosis = diagnosis
        self.doctor_name = doctor_name
        self.patient_name = patient_name
        self.doctor_id = doctor_id
        self.check_in_date = check_in_date

    def json(self):
        return{
            "_id": self.id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "check_in_date": self.check_in_date,
            "diagnosis": self.diagnosis,
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
    
    @classmethod
    def find_all_filtered(cls, patient_id):
        return cls.query.filter_by(patient_id=patient_id).all()
    
    @classmethod
    def find_all(cls):
        return cls.query.all()
    @classmethod
    def find_by_examinations(cls, doctor_id):
        q = cls.query.all() 
        examinations_list = []
        for examination in q:
            if examination.doctor_id == doctor_id:
                examinations_list.append({'patient_id': examination.patient_id, 'patient_name': examination.patient_name})
        return examinations_list