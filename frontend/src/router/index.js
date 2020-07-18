import Vue from 'vue'
import Router from 'vue-router'
import dash from '@/components/dash'
import stats from '@/components/other'
import spies from '@/components/Cameras'
import devices from '@/components/Devices'
import sensors from '@/components/Sensors'
import weather from '@/components/Weather'
import history from '@/components/history'
import temp from '@/components/historyTemp'
import humHis from '@/components/historyPressure'
import mess from '@/components/messages'


Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'dash',
      component: dash
    },
    {
      path: '/Messages',
      name: 'mess',
      component: mess
    },    
    {
      path: '/humidity',
      name: 'humHis',
      component: humHis
    },    
    {
      path: '/Other',
      name: 'stats',
      component: stats
    }, 
    {
      path: '/TempHistory',
      name: 'temp',
      component: temp
    },     
    {
      path: '/Cameras',
      name: 'spies',
      component: spies
    },
    {
      path: '/Devices',
      name: 'devices',
      component: devices
    },
    {
      path: '/Sensors',
      name: 'sensors',
      component: sensors
    },
    {
      path: '/Weather',
      name: 'weather',
      component: weather 
    },
    {
      path: '/History',
      name: 'history',
      component: history 
    }  
  ]
})