import Vue from 'vue';
import VueRouter from 'vue-router';
import Peaks from '../components/Peaks.vue';
import Ips from '../components/Ips.vue';

Vue.use(VueRouter);

const routes = [{
  path: '/peaks',
  name: 'Peaks',
  component: Peaks,
}, {
  path: '/',
  name: 'Ips',
  component: Ips,
}];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
