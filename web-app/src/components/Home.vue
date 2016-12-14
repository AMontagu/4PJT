<template>
  <div id="Home" class="text-center">
    <navbar></navbar>

    <div class="container-form">
      <div class="form-signin">
        <h2 class="form-signin-heading">Please Log in</h2>
        <label for="inputEmail" class="sr-only">Email address</label>
        <input type="email" id="inputEmail" class="form-control" placeholder="Email address" required autofocus>
        <label for="inputPassword" class="sr-only">Password</label>
        <input type="password" id="inputPassword" class="form-control" placeholder="Password" required>
        <div class="checkbox">
          <label>
            <input type="checkbox" value="remember-me"> Remember me
          </label>
        </div>
        <button class="btn btn-lg btn-primary btn-block" type="button">Sign in</button>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from './shared/Navbar.vue'
export default{
    name:"Home",
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
  .form-login {
    max-width: 330px;
    padding: 15px;
    margin: 0 auto;
  }
  .form-login .form-login-heading,
  .form-login .checkbox {
    margin-bottom: 10px;
  }
  .form-login .checkbox {
    font-weight: normal;
  }
  .form-login .form-control {
    position: relative;
    height: auto;
    -webkit-box-sizing: border-box;
       -moz-box-sizing: border-box;
            box-sizing: border-box;
    padding: 10px;
    font-size: 16px;
  }
  .form-login .form-control:focus {
    z-index: 2;
  }
  .form-login input[type="email"] {
    margin-bottom: -1px;
    border-bottom-right-radius: 0;
    border-bottom-left-radius: 0;
  }
  .form-login input[type="password"] {
    margin-bottom: 10px;
    border-top-left-radius: 0;
    border-top-right-radius: 0;
  }
  .container-form{
    width: 80%;
    max-width: 400px;
    margin-right: auto;
    margin-left: auto;
    margin-top: 50px;
  }
</style>
