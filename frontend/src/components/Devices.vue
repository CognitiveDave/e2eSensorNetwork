<template>
  <div class="appl">
      Details for devices
      <table class="table">
          <thead>
            <tr>
              <th scope="col">Clock</th>
              <th scope="col">Temp</th>
              <th scope="col">Device</th>
              <th scope="col">Host</th>
              <th scope="col">Volts</th>
              <th scope="col">Date</th>
              <th scope="col">Time</th>
              </tr>
          </thead>
          <tbody>
            <tr v-for="(proj, ID) in current" :key="ID">
              <td>{{ proj["CPU Clock"] }}</td>
              <td>{{ proj["CPU Core"] }}</td>
              <td>{{ proj.Device }}</td>
              <td>{{ proj.Host }}</td>
              <td>{{ proj["CPU Volts"] }}</td>
              <td>{{ proj.Date.slice(0,16) }}</td>
              <td>{{ proj.Time.slice(17,-7)}}</td>
            </tr>
          </tbody>
        </table>    
  </div>  
</template>
<script>
import axios from 'axios'

export default {
  name: 'App',
  data () {
    return {
      current: [null],
      interval: null
    }
  },
  components: { 
 
  },
  methods: {
    getStats () {
      const path = '/api/v1/resources/hosts'
      axios.get(path)
        .then((res) => {
          this.current = res.data
          console.error(this.current)
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
        })
    }
  }, 
  beforeDestroy: function () {
      clearInterval(this.interval);
  },
  mounted: function () {
  this.$nextTick(function () {
    // code that assumes this.$el is in-document
    this.getStats();
    this.interval = setInterval(function () {
          this.getStats();
      }.bind(this), 60000);
  })
 }
}  
</script>

<style>
#appl {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 5px;
}
#table {
  width: 90%;
  max-width: 90%;
  margin-bottom: 1rem;
}
</style>
