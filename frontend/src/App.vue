<template>
  <div id="appl"> 
    <div class="container-sm">
      <div class="row">
        <div class="col">
          <ul class="nav nav-tabs">
           <li class="nav-item"><router-link class="nav-link" to="/">Home</router-link></li>
           <li class="nav-item"><router-link class="nav-link" to="/Other">Admin</router-link></li>
           <li class="nav-item"><router-link class="nav-link" to="/Cameras">Cameras</router-link></li>
           <li class="nav-item"><router-link class="nav-link" to="/Weather">Weather</router-link></li>
          </ul>   
        </div>        
      </div>   
    <router-view/>
  </div>
</template>

<script>


export default {
  name: 'App',
  components: { 
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
  margin-top: 15px;
}
</style>

