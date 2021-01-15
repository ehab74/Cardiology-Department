<template>
    <patient-nav-bar></patient-nav-bar>
    <base-card>
    <div class="alert alert-success" v-if="isSuccess">You Booked successfully</div>
        <form @submit.prevent="addAppointment">
                    <div class="form-row">
                        <div class="col">
                            <label>First Name</label>
                            <input type="text" class="form-control" placeholder="First name" v-model="first_name">
                            </div>
                            <div class="col">
                                <label>Last Name</label>
                                <input type="text" class="form-control" placeholder="Last name" v-model="last_name">
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="col">
                        <label for="inputEmail4">Email</label>
                        <input type="email" class="form-control" id="inputEmail4" placeholder="xxx@email.com" v-model="email">
                        </div>
                        <div class="col">
                        <label for="inputmobile">Mobile Number</label>
                        <input type="text" class="form-control" id="inputmobile" placeholder="+20 01.." v-model="mobile">
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="col">
                            <label for="exampleFormControlSelect1">Doctor's Name</label>
                            <select class="form-control" id="exampleFormControlSelect1" v-model="doctor_name">
                                <option v-for="doctors in doctorDetails" :key="doctors.id">{{ doctors._id}} {{ doctors.first_name}} {{ doctors.last_name}}</option>
                            </select>
                            </div>
                            <div class="col">
                                <label for="inputdoctorid">Doctor's Id</label>
                        <input type="number" class="form-control" id="inputdoctorid" v-model="doctor_id">
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="inputDate">Date</label>
                        <input type="date" class="form-control" id="inputDate" v-model="date">
                    </div>
                    <div class="form-row">
                        <div class="form-group col-md-6">
                        <label for="description">Case Description</label>
                        <textarea id="description" rows="5" cols="45" v-model="description"></textarea>
                        </div>
                    
                    </div>         
                    <button type="submit" class="btn btn-primary">Book Appointment</button>
            </form>
    </base-card>
</template>
<script>
import axios from 'axios';
export default {
    data() {
        return {
            first_name: '',
            last_name: '',
            patient_username: '',
            doctor_username: '',
            email: '',
            mobile: '',
            doctor_name: '',
            description: '',
            date: '',
            doctor_id: null,
            isSuccess: '',
             doctorDetails: [],

        };
    },
    mounted() {
      this.getDoctorDetails();
  },
    methods: {
        addAppointment() {
            axios
            .post(
                `http://localhost:5000/appointments`,
                { doctor_id: this.doctor_id, date: this.date, patient_username: this.patient_username, doctor_username: this.patient_username, description: this.description},
                {
                    headers: {
                        Authorization: 'Bearer ' + localStorage.getItem('token')
                    },
                }
                )
            .then((response) => {
                this.isSuccess = true;
                this.$router.push('/patienthome');
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
      }
  }

}
</script>