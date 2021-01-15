<template>
<patient-nav-bar></patient-nav-bar>
    <base-card>
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <!-- <th>Id</th> -->
                        <th>Id</th>
                        <th>The Diagnosis</th>
                        <th>The Prescription</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="prescriptions in prescriptionDetails" :key="prescriptions.id">
                    <!-- <td>{{ prescriptions.id }}</td> -->
                        <td>{{ prescriptions._id }}</td>
                        <td>{{ prescriptions.diagnosis }}</td>
                        <td>{{ prescriptions.prescription }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </base-card>
</template>
<script>
import axios from 'axios';
export default {
    data() {
      return {
          prescriptionDetails: [],
      };
  },
  mounted() {
      this.getPrescriptionDetails();
  },
  methods: {
      getPrescriptionDetails() {
          axios.get(
              `http://localhost:5000/examinations`, {
            headers: {
                Authorization: 'Bearer ' + localStorage.getItem('token')
            }
                }).then((response) => {
              this.formatPrescriptionDetails(response.data);
          });
      },
      formatPrescriptionDetails(Prescriptions) {
          for (let key in Prescriptions) {
              this.prescriptionDetails.push({...Prescriptions[key], id:key});
          }
          console.log(this.prescriptionDetails);
      }
  }
}
</script>