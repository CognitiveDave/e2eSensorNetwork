<template>
    <div class='container'>
<div>
  <b-card no-body>
    <b-tabs card>

      <b-tab no-body title="Camera 1" :active="active_tab === 1">
          <iframe class="embed-responsive-item" src="http://192.168.1.13:8081" width="640" height="400" allowfullscreen></iframe>
      </b-tab>

      <b-tab no-body title="Camera 2" :active="active_tab === 2">
        <iframe class="embed-responsive-item" src="http://192.168.1.14:8081" width="640" height="400" allowfullscreen></iframe>
        </b-tab>

      <b-tab no-body title="Camera 3" :active="active_tab === 3">
        <iframe class="embed-responsive-item" src="http://192.168.1.3:8081" width="640" height="400" allowfullscreen></iframe>
      </b-tab>

      <b-tab no-body title="Camera 4" :active="active_tab === 4">
        <iframe class="embed-responsive-item" src="http://192.168.1.15:8081" width="640" height="400" allowfullscreen></iframe>
       </b-tab>

       <b-tab no-body title="Camera 5" :active="active_tab === 5">
        <iframe class="embed-responsive-item" src="http://192.168.1.4:8081" width="640" height="400" allowfullscreen></iframe>
      </b-tab>     
    </b-tabs>
  </b-card>
</div>
    </div>
</template>

<script>
export default {
 data () {
    return {
        interval: 0,
        active_tab: 5
    }
  },
  methods: {
    getStats () {
      if (this.active_tab == 5) {
        this.active_tab = 1
      }
      else {
        this.active_tab = this.active_tab + 1
      }
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

