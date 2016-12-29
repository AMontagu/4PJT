<template>
  <div id="SignIn">
    <navbar></navbar>

    <div class="container-form">
      <div class="form-login">
        <h2 class="form-login-heading">Please Sign in</h2>
        <label for="inputUserName" class="sr-only">User Name *</label>
        <input type="text" id="inputUserName" class="form-control" placeholder="User Name" required autofocus>
        <label for="inputEmail" class="sr-only">Email address *</label>
        <input type="email" id="inputEmail" class="form-control" placeholder="Email address" required>
        <label for="inputPassword" class="sr-only">Password *</label>
        <input type="password" id="inputPassword" class="form-control" placeholder="Password" required>
        <label for="inputConfirmPassword" class="sr-only">Confirm Password *</label>
        <input type="password" id="inputConfirmPassword" class="form-control" placeholder="Confirm Password" required>

        <label for="inputBirthDate" class="sr-only">Birth Date</label>
        <input type="date" id="inputBirthDate" class="form-control">
        <label class="sr-only">Bio</label>
        <textarea rows="4" cols="50" class="form-control"></textarea>
        <div class="checkbox">
          <label>
            <input type="checkbox" value="remember-me"> Remember me
          </label>
        </div>
        <div>
          <p>Already have a account? <router-link to="/">Log In</router-link></p>
        </div>
        <button class="btn btn-lg btn-primary btn-block" type="button">Log in</button>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from './shared/Navbar.vue'
export default{
    name:"SingIn",
    data(){
        return{}
    },
    mounted: function(){},
    components:{
      Navbar
    }
}

</script>

<style scoped>
</style>
