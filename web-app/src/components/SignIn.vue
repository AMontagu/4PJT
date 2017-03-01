<template xmlns:v-on="http://www.w3.org/1999/xhtml">
  <div id="SignIn">
    <navbar></navbar>

    <div class="container-form">
      <div class="form-login">
        <h2 class="form-login-heading">Please Sign in</h2>
        <label for="inputUserName" class="sr-only">User Name *</label>
        <input type="text" id="inputUserName" class="form-control" placeholder="User Name" v-model="qwirkUser.user.username" required autofocus>
        <label for="inputFirstName" class="sr-only">First Name *</label>
        <input type="text" id="inputFirstName" class="form-control" placeholder="First Name" v-model="qwirkUser.user.firstname" required autofocus>
        <label for="inputLastName" class="sr-only">Last Name *</label>
        <input type="text" id="inputLastName" class="form-control" placeholder="Last Name" v-model="qwirkUser.user.lastname" required autofocus>
        <label for="inputEmail" class="sr-only">Email address *</label>
        <input type="email" id="inputEmail" class="form-control" placeholder="Email address" v-model="qwirkUser.user.email" required>
        <label for="inputPassword" class="sr-only">Password *</label>
        <input type="password" id="inputPassword" class="form-control" placeholder="Password" v-model="qwirkUser.user.password" required>
        <label for="inputConfirmPassword" class="sr-only">Confirm Password *</label>
        <input type="password" id="inputConfirmPassword" class="form-control" placeholder="Confirm Password" v-model="confirmPassword" required>

        <label for="inputBirthDate" class="sr-only">Birth Date</label>
        <input type="date" id="inputBirthDate" class="form-control" v-model="qwirkUser.birthDate">
        <label class="sr-only">Bio</label>
        <textarea rows="4" cols="50" class="form-control" v-model="qwirkUser.bio"></textarea>
        <div class="checkbox">
          <label>
            <input type="checkbox" value="remember-me"> Remember me
          </label>
        </div>
        <div>
          <p>Already have a account? <router-link to="/">Log In</router-link></p>
        </div>
        <button class="btn btn-lg btn-primary btn-block" type="button" v-on:click="signIn">Sign in</button>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from './shared/Navbar.vue'
import {User, QwirkUser} from '../../static/js/model.js';


export default{
    name:"SingIn",
    data(){
        return{
          qwirkUser: new QwirkUser(),
          confirmPassword: ""
        }
    },
    created: function(){},
    mounted: function(){},
    methods:{
      signIn: function(){
        console.log(this.qwirkUser);
        if(this.qwirkUser.checkBeforeSignIn(this.confirmPassword)){
          this.$http.post('http://localhost:8000/signin/', this.qwirkUser).then(function(response){
            console.log("sucess signin", response);
            this.$cookie.set('token', response.body, 1);
            this.$router.push('user/');
          }, function(err){
            console.log("error :", err);
          });
        }else{
          console.log("checkBeforeSignIn failed");

        }
      }
    },
    components:{
      Navbar
    }
}

</script>

<style scoped>
</style>
