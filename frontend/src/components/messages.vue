<template>
  <div id="appl"> 
      Message details
      <table class="table">
          <thead>
            <tr>
              <th scope="col">Directory</th>
              <th scope="col">File</th>
              <th scope="col">Size</th>
              <th scope="col">Time</th>
              </tr>
          </thead>
          <tbody>
            <tr v-for="(proj, ID) in current" :key="ID">
              <td>{{ proj["directory"] }}</td>
              <td>{{ proj["file"] }}</td>
              <td>{{ proj.size }}</td>
              <td>{{ proj.timestamp }}</td>
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
      const path = '/api/v1/resources/messages'
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
