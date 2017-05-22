<template xmlns:v-on="http://www.w3.org/1999/xhtml">
  <div id="UserProfile">
    <div class="container-fluid">

      <div class="row marginL10p marginR0">
        <div class="form-login col-xs-12 col-md-8">
          <h2 class="form-login-heading">Edit your profile</h2>
          <label>User Name:</label>
          <p>{{qwirkUser.user.username}}</p>
          <label for="inputFirstName">First Name *</label>
          <input type="text" id="inputFirstName" class="form-control" placeholder="First Name" v-model="qwirkUser.user.first_name" required autofocus>
          <label for="inputLastName">Last Name *</label>
          <input type="text" id="inputLastName" class="form-control" placeholder="Last Name" v-model="qwirkUser.user.last_name" required autofocus>
          <label for="inputEmail">Email address *</label>
          <input type="email" id="inputEmail" class="form-control" placeholder="Email address" v-model="qwirkUser.user.email" required>
          <label for="inputBirthDate">Birth Date</label>
          <input type="date" id="inputBirthDate" class="form-control" v-model="qwirkUser.birthDate">
          <label>Bio</label>
          <textarea rows="4" cols="50" class="form-control" v-model="qwirkUser.bio"></textarea>

          <button type="button" class="btnAction">Change Password</button>
        </div>
        <div class="form-login col-xs-12 col-md-4">
          <!-- profile picture here-->
        </div>
      </div>

      <div class="row marginR0">
        <button type="button" class="btnAction" v-on:click="cancel()">Cancel</button>
        <button type="button" class="btnAction" v-on:click="saveChanges()">Save Changes</button>
      </div>
    </div>
  </div>
</template>

<script>
import {QwirkUser} from '../../../static/js/model.js';
export default{
    name:"UserProfile",
    data(){
        return{
          qwirkUser: new QwirkUser()
        }
    },
    created: function(){
      this.$http.get(this.$root.server + '/simpleuserinfos/', {headers: {'Authorization': "Token " + this.$cookie.get('token')}}).then((response) => {
        this.qwirkUser.copyConstructor(response.body);
        //console.log(self.qwirkUser);
      }, (err) => {
        console.log("error :", err);
      });
    },
    mounted: function(){},
    methods: {
      saveChanges: function(){
        this.$http.post(this.$root.server + '/useredit/', this.qwirkUser, {headers: {'Authorization': "Token " + this.$cookie.get('token')}}).then((response) => {
          console.log("sucess edit", response);
          // TODO display message that said your modifications was good taken
        }, (err) => {
          console.log("error :", err);
        });
      },
      cancel: function(){
        this.$router.push('/user/');
      }
    },
    components:{}
}

</script>

<style scoped>
</style>
