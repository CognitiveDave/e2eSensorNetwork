<template>
        <div class="container">   
            <digital></digital>       
            <div class="row justify-content-sm-center">
                <div class="col justify-content-sm-center">
                    <div class="card rounded shadow-sm border-0">
                        <div class="card-header">
                            Alerts
                        </div>
                        <div class="card-body p-4">  
                            <img src="/static/img/emergency.png" alt="Card image cap" class="img-fluid d-block mx-auto mb-3" style="width: 6rem; height: 6rem;">
                            <strong class="card-text" style="font-size: 29px;margin: 1px;padding: 1px;"> {{ current['alerts'] }} </strong>
                        </div>
                         <div class="card-footer text-muted">
                            <p> Check all views! </p>
                        </div>
                    </div>
                  </div>
                  <div class="col justify-content-sm-center">
                    <div class="card rounded shadow-sm border-0">                       
                        <div class="card-header">
                            Sensors online
                        </div>                        
                        <div class="card-body p-4">
                            <img src="/static/img/sensor.png" alt="Card image cap" class="img-fluid d-block mx-auto mb-3" style="width: 6rem; height: 6rem;">                            
                            <Strong class="card-text" style="font-size: 29px;padding: 1px;margin: 1px;">  </Strong>                
                        </div>    
                         <div class="card-footer text-muted">
                            <a href="#/Devices" class="btn btn-primary stretched-link">Detail</a>
                        </div>    
                    </div>                        
                </div>
                  <div class="col justify-content-sm-center">
                    <div class="card rounded shadow-sm border-0">                       
                        <div class="card-header">
                            Messages
                        </div>                        
                        <div class="card-body p-4">
                            <img src="/static/img/reminder.png" alt="Card image cap" class="img-fluid d-block mx-auto mb-3" style="width: 6rem; height: 6rem;">                            
                            <Strong class="card-text" style="font-size: 29px;padding: 1px;margin: 1px;">{{ current['messages'] }} </Strong>                
                        </div>    
                         <div class="card-footer text-muted">
                            <a href="#/Messages" class="btn btn-primary stretched-link">Detail</a>
                        </div>    
                    </div>                        
                </div>
            </div>
        </div>  
</template>


<script>
import axios from 'axios'
import clock from '@/components/clock'

export default {
  name: 'App',
  data () {
    return {
      current: {
          "temp": 0,
          "humidity" : 0,
          "gas" : "-",
          "alerts" : -0,
          "messages" : -0,
          "pressure" : 0
      },
      interval: null
    }
  },
  components: { 
    digital: clock
  },
  methods: {
    getStats () {
      const path = '/api/v1/resources/current'
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
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 5px;
}
</style>

