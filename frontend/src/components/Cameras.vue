<template>
    <div class='container'>
<div>
  <b-card no-body>
    <b-tabs card>

      <b-tab no-body title="Camera 1">
          <iframe class="embed-responsive-item" src="http://192.168.1.13:8081" width="640" height="400" allowfullscreen></iframe>
      </b-tab>

      <b-tab no-body title="Camera 2">
        <iframe class="embed-responsive-item" src="http://192.168.1.14:8081" width="640" height="400" allowfullscreen></iframe>
        </b-tab>

      <b-tab no-body title="Camera 3">
        <iframe class="embed-responsive-item" src="http://192.168.1.3:8081" width="640" height="400" allowfullscreen></iframe>
      </b-tab>

      <b-tab no-body title="Camera 4">
        <iframe class="embed-responsive-item" src="http://192.168.1.15:8081" width="640" height="400" allowfullscreen></iframe>
       </b-tab>

       <b-tab no-body title="Camera 5">
        <iframe class="embed-responsive-item" src="http://192.168.1.4:8081" width="640" height="400" allowfullscreen></iframe>
      </b-tab>     
    </b-tabs>
  </b-card>
</div>
    </div>
</template>


