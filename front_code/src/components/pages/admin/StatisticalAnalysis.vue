<template>
  <admin-nav-bar></admin-nav-bar>
  <new-base-card>
    <form
      class="form-inline my-2 my-lg-0"
      @submit.prevent="getDataAndFillChart"
    >
      <input
        class="form-control mr-sm-2"
        type="date"
        placeholder="search by patient Id"
        aria-label="Search"
        v-model="date"
      />
      <button class="btn btn-outline-success my-2 my-sm-0" type="submit">
        See Analytics
      </button>
    </form>
    <canvas id="planet-chart"></canvas>
  </new-base-card>
</template>
<script>
import Chart from 'chart.js';
import axios from 'axios';
//import planetChartData from '../../../services/chart-data.js';
export default {
  data() {
    return {
      date: '',
      time: [],
      doctors: [],
      patients: [],
      appointments: [],
      planetChartData: null
    };
  },
  mounted() {},
  methods: {
    getDataAndFillChart() {
      this.getData().then(() => {
        this.fillData();
        this.createChart('planet-chart', this.planetChartData);
      });
    },
    fillData() {
      this.planetChartData = {
        type: 'line',
        data: {
          labels: this.time,
          datasets: [
            {
              // one line graph
              label: 'Number of Doctors',
              data: this.doctors,
              backgroundColor: 'rgba(255, 255, 0, 0.2)',
              borderColor: 'yellow',
              pointBackgroundColor: 'orange',
              borderWidth: 1,
              pointBorderColor: 'orange'
            },
            {
              // another line graph
              label: 'Number of Patients',
              data: this.patients,
              backgroundColor: 'rgba(255, 0, 0, 0.2)',
              borderColor: 'lightpink',
              pointBackgroundColor: 'red',
              borderWidth: 1,
              pointBorderColor: 'red'
            },
            {
              // another line graph
              label: 'Number of Appointments',
              data: this.appointments,
              backgroundColor: 'rgba(0, 0, 255, 0.2)',
              borderColor: 'lightblue',
              pointBackgroundColor: 'blue',
              borderWidth: 1,
              pointBorderColor: 'blue'
            }
          ]
        },
        options: {
          responsive: true,
          lineTension: 1,
          scales: {
            yAxes: [
              {
                ticks: {
                  beginAtZero: true,
                  padding: 25
                }
              }
            ]
          }
        }
      };
    },
    async getData() {
      await axios
        .get(`http://localhost:5000/analytics`, {
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('token')
          },
          params: {
            date: this.date
          }
        })
        .then(response => {
          let results = response.data;
          let doc = [];
          let pat = [];
          let appo = [];
          let time = [];
          for (let i = results.length - 1; i >= 0; i--) {
            let d = results[i].doctors;
            let p = results[i].patients;
            let a = results[i].appointments;
            let ti = results[i].date;
            doc.push(d);
            pat.push(p);
            appo.push(a);
            time.push(ti);
          }
          this.doctors = doc;
          this.patients = pat;
          this.appointments = appo;
          this.time = time;
        });
    },

    createChart(chartId, chartData) {
      const ctx = document.getElementById(chartId);
      new Chart(ctx, {
        type: chartData.type,
        data: chartData.data,
        options: chartData.options
      });
    }
  }
};
</script>
