<template>
    <doctor-nav-bar></doctor-nav-bar>
    <base-card>
    <div class="alert alert-success" v-if="isSuccess">You wrote prescription successfully</div>
        <form @submit.prevent="writePrescription">
                    <div class="form-group col-md-6">
                            <label for="exampleFormControlSelect1">Doctor's Name</label>
                            <select class="form-control" id="exampleFormControlSelect1" v-model="doctor_name">
                                <option v-for="doctors in doctorDetails" :key="doctors.id">{{doctors._id }} {{ doctors.first_name}} {{ doctors.last_name}}</option>
                            </select>
                    </div>
                    <div class="form-group col-md-6">
                            <label for="exampleFormControlSelect1">Patient's Name</label>
                            <select class="form-control" id="exampleFormControlSelect1" v-model="patient_name">
                                <option v-for="patients in patientDetails" :key="patients.id">{{ patients._id}} {{ patients.first_name}} {{ patients.last_name}}</option>
                            </select>
                    </div>
                    <div class="form-group col-md-6">
                            <label for="inputPassword2" class="sr-only">Patient's Id</label>
                            <input type="number" class="form-control" id="inputPassword2" placeholder="Patient's Id" v-model="patient_id">
                    </div>
                    <div class="form-group col-md-6">
                            <label for="inputPassword2" class="sr-only">Appointment's Id</label>
                            <input type="number" class="form-control" id="inputPassword2" placeholder="Appointment's Id" v-model="appointment_id">
                    </div>
                    <div class="form-row" style="max-width: 40rem">
                        <div class="form-group col-md-6">
                        <label for="description">Write Diagnosis</label>
                        <textarea id="description" rows="5" cols="45" v-model="diagnosis"></textarea>
                        </div>
                    </div>
                     <div class="form-row" style="max-width: 40rem">
                        <div class="form-group col-md-6">
                        <label for="description">Write Prescription</label>
                        <textarea id="description" rows="5" cols="45" v-model="prescription" style="max-width: 40rem;"></textarea>
                        </div>
                    </div>        
                    <button type="submit" class="btn btn-primary">Write Examination</button>
            </form>
                    
    </base-card>
</template>
<script>
import axios from 'axios';
import BaseCard from '../../ui/BaseCard.vue';
export default {
  components: { BaseCard },
    data() {
        return {
            patient_name: '',
            doctor_name: '',
            diagnosis: '',
            prescription: '',
            isSuccess: '',
             doctorDetails: [],
             patientDetails: [],
             patient_id: null,
             appointment_id: null,

        };
    },
    mounted() {
      this.getDoctorDetails();
      this.getPatientDetails();
  },
    methods: {
        writePrescription() {
            axios
            .post(
                `http://localhost:5000/appointments/${this.appointment_id}/examinations`,
                {diagnosis: this.diagnosis, prescription: this.prescription}, {
                    headers: {
                         Authorization: 'Bearer ' + localStorage.getItem('token')
                    }
                }
                )
            .then((response) => {
                this.isSuccess = true;
                this.$router.push('/doctorhome');
                console.log(response);
            });


        },
         getDoctorDetails() {
         axios.get(
              `http://localhost:5000/doctors`, {
                  headers: {
                      'Content-Type' : 'application/json',
                  }
              }
          ).then((response) => {
              this.formatDoctorDetails(response.data);
          });
      },
      formatDoctorDetails(doctors) {
          for (let key in doctors) {
              this.doctorDetails.push({...doctors[key], id:key});
          }
          console.log(this.doctorDetails);
      },
       getPatientDetails() {
          axios.get(
              `http://localhost:5000/doctor/patients`, {
                  headers: {
                      Authorization: 'Bearer ' + localStorage.getItem('token')
                  }
              }
          ).then((response) => {
              this.formatPatientDetails(response.data);
          });
      },
      formatPatientDetails(patients) {
          for (let key in patients) {
              this.patientDetails.push({...patients[key], id:key});
          }
          console.log(this.patientDetails);
      }
    },
}
</script>