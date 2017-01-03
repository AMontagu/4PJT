// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'

import router from './router'
let VueResource = require('vue-resource');
var VueCookie = require('vue-cookie');
// Tell Vue to use the plugin
Vue.use(VueResource);
Vue.use(VueCookie);

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router: router,
  http: {
    root: '/',
  },
  template: '<App/>',
  components: { App }
})
