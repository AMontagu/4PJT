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
