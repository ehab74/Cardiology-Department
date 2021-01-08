from db import db

class appointmentModel(db.Model):
    __tablename__ = 'Appointments'

    id = db.Column(db.Integer,primary_key = True)
    date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime)

    doctor_id = db.Column (db.Integer,db.ForeignKey('Doctors.id'))
    patient_id = db.Column (db.Integer,db.ForeignKey('Patients.id'))

    doctor = db.relationship('DoctorModel') 
    patient = db.relationship('PatientModel')

    def __init__ (self,date,doctor_id,patient_id,created_at):
        self.date = date
        self.doctor_id = doctor_id
        self.patient_id = patient_id
        self.created_at = created_at

    def json (self):
        return {
            '_id': self.id,
            'date' : str(self.date),
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'date_of_reservation': str(self.created_at)
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
    def find_all(cls):
        return cls.query.all()

        


