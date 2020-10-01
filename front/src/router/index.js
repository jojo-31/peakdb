import Vue from 'vue';
import VueRouter from 'vue-router';
import Ping from '../components/Ping.vue';
import Peaks from '../components/Peaks.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/peaks',
    name: 'Peaks',
    component: Peaks,
  },
  {
    path: '/',
    name: 'Peaks',
    component: Peaks,
  },
  {
    path: '/ping',
    name: 'Ping',
    component: Ping,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
