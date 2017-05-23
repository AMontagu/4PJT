<template xmlns:v-on="http://www.w3.org/1999/xhtml">
  <div id="UserProfile">
    <div class="container-fluid">

      <div v-if="!editProfile">
        <div class="row marginL10p marginR0">
          <div class="form-login col-xs-12 col-md-8">
            <h2 class="form-login-heading">Edit your profile</h2>
            <p class="titleField">User Name:</p>
            <p class="field">{{ qwirkUser.user.username }}</p>
            <p class="titleField">First Name :</p>
            <p class="field">{{ qwirkUser.user.first_name }}</p>
            <p class="titleField">Last Name :</p>
            <p class="field">{{ qwirkUser.user.last_name }}</p>
            <p class="titleField">Email address</p>
            <p class="field">{{ qwirkUser.user.email }}</p>
            <p class="titleField">Birth Date: </p>
            <p class="field">{{ qwirkUser.birthDate }}</p>
            <p class="titleField">Bio: </p>
            <p class="field">{{ qwirkUser.bio }}</p>

            <button type="button" class="btnAction">Change Password</button>
          </div>
          <div class="form-login col-xs-12 col-md-4">
            <!-- profile picture here-->
          </div>
        </div>

        <div v-if="isUserConnected" class="row marginR0">
          <button type="button" class="btnAction" v-on:click="edit()">Edit informations</button>
        </div>
      </div>

      <div v-else>
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
  </div>
</template>

<script>
import {QwirkUser} from '../../../static/js/model.js';
export default{
    name:"UserProfile",
    data(){
        return{
          qwirkUser: new QwirkUser(),
          userName: "",
          isUserConnected: true,
          editProfile: false,
        }
    },
    created: function(){
      this.userName = this.$route.params.username;
    },
    mounted: function(){
    	if(this.$root.qwirkUser.user.username === ''){
    		setTimeout(this.getUserInfos, 100);
      }else{
        this.getUserInfos();
      }
    },
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
        this.editProfile = false;
      },
      edit: function(){
      	this.editProfile = true;
      },
      getUserInfos(){
        let url = this.$root.server + '/simpleuserinfos/';
        console.log(this.userName, this.$root.qwirkUser.user.username);
        if (this.userName !== "" && typeof this.userName !== 'undefined' && this.userName !== this.$root.qwirkUser.user.username) {
        	console.log("ici");
          url += "?username=" + this.userName;
          this.isUserConnected = false;
        }
        console.log(url);
        this.$http.get(url, {headers: {'Authorization': "Token " + this.$cookie.get('token')}}).then((response) => {
          this.qwirkUser.copyConstructor(response.body);
          //console.log(self.qwirkUser);
        }, (err) => {
          console.log("error :", err);
        });
      }
    },
    watch: {
      '$route' (to, from) {
        this.userName = this.$route.params.username;

        this.getUserInfos();
      }
    },
    components:{}
}

</script>

<style scoped>
</style>
