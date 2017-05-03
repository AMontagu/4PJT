<template xmlns:v-on="http://www.w3.org/1999/xhtml">
  <div id="Home" class="text-center">
    <navbar></navbar>

    <div class="container-form">
      <div class="form-login">
        <h2 class="form-login-heading">Please Log in</h2>
        <label for="inputEmail" class="sr-only">Email address or User Name</label>
        <input type="email" id="inputEmail" class="form-control" placeholder="Email address, User name" v-model="user.username" required autofocus>
        <label for="inputPassword" class="sr-only">Password</label>
        <input type="password" id="inputPassword" class="form-control" placeholder="Password" v-model="user.password" required>
        <div class="checkbox">
          <label>
            <input type="checkbox" value="remember-me"> Remember me
          </label>
        </div>
        <button class="btn btn-lg btn-primary btn-block" type="button" v-on:click="logIn">Log in</button>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from './shared/Navbar.vue'
import {User} from '../../static/js/model.js';

export default{
    name:"Home",
    data(){
        return{
          user: new User()
        }
    },
    mounted: function(){},
    methods: {
      logIn: function(){
        this.$http.post('http://localhost:8000/login/', this.user).then(function(response){
        console.log("sucess login", response);
        this.$cookie.set('token', response.body, 1);

        this.$router.push('user/');
      }, function(err){
        console.log("error :", err);
      });
      }
    },
    components:{
      Navbar
    }
}

</script>

<style scoped>
</style>
