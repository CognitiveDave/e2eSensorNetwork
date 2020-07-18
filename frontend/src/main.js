import Vue from 'vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.css'
import BootstrapVue from 'bootstrap-vue'
import routes from './router/index.js'

Vue.config.productionTip = false
Vue.use(BootstrapVue)

new Vue({
  el: '#app',
  router: routes,
  render(h) { return h(App) },
}).$mount('#app')