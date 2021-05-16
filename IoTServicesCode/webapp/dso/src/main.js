import Vue from 'vue'
import App from './App.vue'
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
Vue.config.productionTip = false

import VueRouter from "vue-router";
Vue.use(VueRouter);
import Measurements from "./components/Measurements.vue";
import Device from "./components/Device.vue";


const routes = [
  { path: "/", component: Measurements },
  { path: "/device/:id", component: Device },
];

const router = new VueRouter({
  routes, // short for `routes: routes`
});


new Vue({
  render: h => h(App),
  router
}).$mount('#app')
