// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'

import router from './router'

import {QwirkUser} from '../static/js/model.js';
import {Picker, Emoji} from 'emoji-mart-vue';
import VueResource from 'vue-resource';
import VueCookie from 'vue-cookie';
// Tell Vue to use the plugin
Vue.use(VueResource);
Vue.use(VueCookie);
Vue.component('picker', Picker)
Vue.component('emoji', Emoji)

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
      serverRtcPort: 9001,
      httpProtocol: location.protocol === 'https:' ? 'https://' : 'http://',
      wssProtocol: location.protocol === 'https:' ? 'wss://' : 'ws://',
    }
  },
  computed: {
    wssServer(){
      //return this.wssProtocol + this.serverIp + ':' + this.serverPort;
      return this.wssProtocol + location.host + '/server';
    },
    server(){
      //return this.httpProtocol + this.serverIp + ':' + this.serverPort;
      return '/server';
    },
    serverRtc(){
      //return this.httpProtocol + this.serverRtcIp + ':' + this.serverRtcPort;
      return '/rtc/';
    }
  },
  components: { App }
})
