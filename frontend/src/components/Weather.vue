<template>
  <div id="appl"> 
      Details for local weather
      <table class="table">
          <thead>
            <tr>
              <th scope="col">Place</th>
              <th scope="col">Status</th>
              <th scope="col">Temp</th>
              <th scope="col">Humidity</th>
              <th scope="col">Pressure</th>
              <th scope="col">As of</th>
              <th scope="col">Rain</th>
              <th scope="col">Wind</th>
              </tr>
          </thead>
          <tbody>
            <tr v-for="(proj, ID) in current" :key="ID">
              <td>{{ proj["place"] }}</td>
              <td>{{ proj["det_status"] }}</td>
              <td>{{ proj['temps']['feels_like'] }}</td>
              <td>{{ proj['humidity'] }}</td>
              <td>{{ proj['pressure'] }}</td>
              <td>{{ proj['Ref Time'] }}</td>
              <td>{{ proj['rain'] }}</td>
              <td>{{ proj['wind']['speed'] }}</td>
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
      const path = '/api/v1/resources/weather'
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
</style>
