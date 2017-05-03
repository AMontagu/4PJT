/**
 * Created by Adrien on 08/11/2016.
 */

import Vue from 'vue'
import Router from 'vue-router'

import Home from '../components/Home.vue'
import SignIn from '../components/SignIn.vue'
import TestRoomCall from '../components/TestRoomCall.vue'

import UserHome from '../components/User/Home.vue'
import UserChat from '../components/User/Chat.vue'
import UserProfile from '../components/User/Profile.vue'

Vue.use(Router);

export default new Router({
  mode: 'history',
  scrollBehavior: () => ({ y: 0 }),
  routes: [
    { path: '/', component: Home},
    { path: '/signin', component: SignIn},
    { path: '/testRoomCall', component: TestRoomCall},
    { path: '/user', component: UserHome,
      beforeEnter: (to, from, next) => {
        let self = this;
        if (Vue.cookie.get('token') == null) {
          next('/');
        } else {

          Vue.http.get('http://localhost:8000/isloggedin/', {headers: {'Authorization': "Token " + Vue.cookie.get('token')}}).then(function (response) {

            if (response.body == "True") {
              console.log("user is logged in");
              Vue.http.headers.common['Authorization'] = 'Token ' + Vue.cookie.get('token');
              next();
            } else {
              console.log("user is NOT logged in");
              // TODO look cookies for username and password
              next('/');
            }
          }, function (err) {
            console.log("error :", err);
            next('/')
          });
        }
      },
      children: [
        {
          path: '',
          component: UserChat
        },
        {
          path: 'profile',
          component: UserProfile
        },
        {
          path: ':name',
          component: UserChat
        }
      ]
    }
  ]
})
