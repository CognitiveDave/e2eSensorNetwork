<template>
  <div id="appl"> 
      Details for Indoor temperate by device
      <table class="table">
          <thead>
            <tr>
              <th scope="col">Avg Freq</th>
              <th scope="col">Avg Temp</th>
              <th scope="col">Device</th>
              <th scope="col">Host</th>
              <th scope="col">Recs</th>
              <th scope="col">Date</th>
              <th scope="col">Indoor</th>
              </tr>
          </thead>
          <tbody>
            <tr v-for="(proj, ID) in current" :key="ID">
              <td>{{ proj["Avg Freq"] }}</td>
              <td>{{ proj["Avg Temp"] }}</td>
              <td>{{ proj.Device }}</td>
              <td>{{ proj.Host }}</td>
              <td>{{ proj.Obs }}</td>
              <td>{{ proj.Date.slice(0,16) }}</td>
              <td>{{ proj.Humidity}}</td>
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
      const path = '/api/v1/resources/sensors'
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
  margin-top: 1px;
}
#table {
  width: 90%;
  max-width: 90%;
  margin-bottom: 1rem;
}
</style>
