<template>    
    <div id="MyClockDisplay" class="clock"> 
      <p>       </p>
      <div>  {{ time }} </div> 
      <p>       </p> 
     </div>
</template>

<script>

let { DateTime } = require('luxon')

export default {
  name: 'App',
  components: {
    
  },
  data () {
    return {
        now: DateTime.local(),
        interval: 0,
        timeFormat: 'cccc DD t'
    }
  },
  computed: {
        time() {
        return this.now.toFormat(this.timeFormat);
    }
  },
  methods: {

},
mounted() {
    this.interval = setInterval(() => this.now = DateTime.local(), 1000);
    }
} 
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.clock {
    color: #061ac9;
    font-size: 30px;
    font-family: Orbitron;
}
</style>
