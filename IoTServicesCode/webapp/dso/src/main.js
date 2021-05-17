import Vue from 'vue'
import App from './App.vue'
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
Vue.config.productionTip = false

import VueRouter from "vue-router";
Vue.use(VueRouter);
import Measurements from "./components/Measurements.vue";
import Devices from "./components/Devices.vue";


const routes = [
  { path: "/", component: Devices },
  { path: "/device/:id", component: Measurements },
];

const router = new VueRouter({
  routes, // short for `routes: routes`
});


new Vue({
  render: h => h(App),
  router
}).$mount('#app')
