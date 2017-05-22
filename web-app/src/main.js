// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'

import router from './router'

import {QwirkUser} from '../static/js/model.js';
let VueResource = require('vue-resource');
let VueCookie = require('vue-cookie');
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
  data(){
    return{
      qwirkUser: new QwirkUser(),
      serverIp: "localhost",
      serverPort: 8000,
      serverRtcIp: "localhost",
      serverRtcPort: 9000,
      httpProtocol: location.protocol === 'https:' ? 'https://' : 'http://',
      wssProtocol: location.protocol === 'https:' ? 'wss://' : 'ws://',
    }
  },
  computed: {
    wssServer(){
      return this.wssProtocol + this.serverIp + ':' + this.serverPort;
    },
    server(){
      return this.httpProtocol + this.serverIp + ':' + this.serverPort;
    },
    serverRtc(){
      return this.httpProtocol + this.serverRtcIp + ':' + this.serverRtcPort;
    }
  },
  components: { App }
})
