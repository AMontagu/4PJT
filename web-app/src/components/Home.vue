<template>
  <div id="Home" class="text-center">
    <navbar></navbar>

    <div class="container-form">
      <div class="form-login">
        <h2 class="form-login-heading">Please Log in</h2>
        <label for="inputEmail" class="sr-only">Email address</label>
        <input type="email" id="inputEmail" class="form-control" placeholder="Email address" required autofocus>
        <label for="inputPassword" class="sr-only">Password</label>
        <input type="password" id="inputPassword" class="form-control" placeholder="Password" required>
        <div class="checkbox">
          <label>
            <input type="checkbox" value="remember-me"> Remember me
          </label>
        </div>
        <button class="btn btn-lg btn-primary btn-block" type="button">Log in</button>
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
    mounted: function(){
      let data = {email: "test@bla.com", username:"test", password:"testtest"};
      this.$http.post('http://localhost:8000/signin/', {email: "test@bla.com", username:"test", password:"testtest"}).then(function(response){
        console.log("sucess signin", response);
      }, function(err){
        console.log("error :", err);
      });
    },
    components:{
      Navbar
    }
}

</script>

<style scoped>
</style>
