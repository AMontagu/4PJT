// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'

import router from './router'
let VueResource = require('vue-resource');

Vue.use(VueResource);

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router: router,
  http: {
    root: '/root',
    headers: {
      Authorization: 'Basic YXBpOnBhc3N3b3Jk'
    }
  },
  template: '<App/>',
  components: { App }
})
