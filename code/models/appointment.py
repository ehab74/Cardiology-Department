from db import db

class appointmentModel(db.Model):
    __tablename__ = 'Appointments'

    id = db.Column(db.Integer,primary_key = True)
    date = db.Column(db.String(80))
    current_date = db.Column(db.String(80))

    doctor_id = db.Column (db.Integer,db.ForeignKey('Doctors.id'))
    patient_id = db.Column (db.Integer,db.ForeignKey('Patients.id'))

    doctor = db.relationship('DoctorModel') 
    patient = db.relationship('PatientModel')

    def __init__ (self,date,doctor_id,patient_id,current_date):
        self.date = date
        self.doctor_id = doctor_id
        self.patient_id = patient_id
        self.current_date = current_date

    def json (self):
        return {
            '_id': self.id,
            'date' : self.date,
            'patient username': self.patient_id,
            'doctor username': self.doctor_id,
            'date of reservation': self.current_date
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

    def find_all(cls):
        apps = cls.query().all()

        patientsapp = [app.json() for app in apps]
        return patientsapp 

    def main(start_time):
  
     creds = None
   
     if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
   
     if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret2.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

     service = build('calendar', 'v3', credentials=creds)

     event = {
      'summary': 'Doctor Appointment',
      'location': 'Cairo',
      'description': '',
      'start': {
      'dateTime': start_time,
      'timeZone': 'Africa/Cairo',
       },
     #'end': {
     #'dateTime': end_time,
     #'timeZone': 'Africa/Cairo',
     #},
      'reminders': {
      'useDefault': False,
     #'overrides': [
      #{'method': 'email', 'minutes': 24 * 60},
      #{'method': 'popup', 'minutes': 10},
      #],
      },
     }
  
     service.events().insert(calendarId='primary', body=event).execute()    



