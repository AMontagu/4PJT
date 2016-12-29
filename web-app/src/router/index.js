/**
 * Created by Adrien on 08/11/2016.
 */

import Vue from 'vue'
import Router from 'vue-router'

import Home from '../components/Home.vue'
import SignIn from '../components/SignIn.vue'
Vue.use(Router);

export default new Router({
  mode: 'history',
  scrollBehavior: () => ({ y: 0 }),
  routes: [
    { path: '/', component: Home},
    { path: '/signin', component: SignIn}
  ]
})
