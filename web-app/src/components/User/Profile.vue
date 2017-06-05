<template xmlns:v-on="http://www.w3.org/1999/xhtml">
  <div id="UserProfile">
    <div class="container-fluid">

      <div v-if="!editProfile">
        <div class="row marginL10p marginR0">
          <div class="form-login col-xs-12 col-md-8">
            <h1 class="form-login-heading">Your profile:</h1>
            <div class="divField">
              <p class="titleField">User Name:</p>
              <p class="field">{{ qwirkUser.user.username }}</p>
            </div>

            <div class="divField">
              <p class="titleField">First Name:</p>
              <p class="field">{{ qwirkUser.user.first_name }}</p>
            </div>

            <div class="divField">
              <p class="titleField">Last Name:</p>
              <p class="field">{{ qwirkUser.user.last_name }}</p>
            </div>

            <div class="divField">
              <p class="titleField">Email address:</p>
              <p class="field">{{ qwirkUser.user.email }}</p>
            </div>

            <div class="divField">
              <p class="titleField">Birth Date: </p>
              <p class="field">{{ qwirkUser.birthDate }}</p>
            </div>

            <div class="divField">
              <p class="titleField">Bio: </p>
              <p class="field">{{ qwirkUser.bio }}</p>
            </div>

            <!--<button type="button" class="btnAction">Change Password</button>-->
          </div>
          <div class="col-xs-12 col-md-4">
            <div class="avatarContainer">
              <img :src="getAvatarSrc()"/>
            </div>
          </div>
        </div>

        <div v-if="isUserConnected" class="row marginR0">
          <button type="button" class="btnAction" v-on:click="edit()">Edit informations</button>
        </div>
      </div>

      <div v-else>
        <div class="row marginL10p marginR0">
          <div class="form-login col-xs-12 col-md-8">
            <h1 class="form-login-heading">Edit your profile</h1>
            <label>User Name:</label>
            <p class="field">{{qwirkUser.user.username}}</p>
            <label for="inputFirstName">First Name: *</label>
            <input type="text" id="inputFirstName" class="form-control" placeholder="First Name" v-model="qwirkUser.user.first_name" required autofocus>
            <label for="inputLastName">Last Name: *</label>
            <input type="text" id="inputLastName" class="form-control" placeholder="Last Name" v-model="qwirkUser.user.last_name" required autofocus>
            <label for="inputEmail">Email address: *</label>
            <input type="email" id="inputEmail" class="form-control" placeholder="Email address" v-model="qwirkUser.user.email" required>
            <label for="inputBirthDate">Birth Date:</label>
            <input type="date" id="inputBirthDate" class="form-control" v-model="qwirkUser.birthDate">
            <label>Bio:</label>
            <textarea rows="4" cols="50" class="form-control" v-model="qwirkUser.bio"></textarea>

            <!--<button type="button" class="btnAction">Change Password</button>-->
          </div>
          <div class="col-xs-12 col-md-4 avatarContainer">

            <img :src="getAvatarSrc()"/>

            <input type="hidden" name="MAX_FILE_SIZE" value="26214400"/>
            <input type="file" name="avatar" id="avatar" class="hidden" v-on:change.prevent="fileUpload">
            <label for="avatar" class="btn btn-primary changeAvatarLabel">Change Avatar</label>
            <p class="inputError">{{ uploadError }}</p>
          </div>
        </div>

        <div class="row marginR0 marginB50 marginT20">
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
    name:'UserProfile',
    data(){
        return{
          qwirkUser: new QwirkUser(),
          userName: '',
          isUserConnected: true,
          editProfile: false,
          uploadError: '',
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
      },
      fileUpload: function (e) {
        let files = e.target.files || e.dataTransfer.files;

        if (files.length > 0) {
          this.postFile(files)
        }
      },
      postFile: function (files) {
        let formData = new FormData();
        formData.append('file', files[0]);

        this.$http.post(this.$root.server + '/changeavatar/', formData).then((response) => {

        	let data = response.body;

        	if(typeof data === 'string'){
        		data = JSON.parse(data)
          }

          this.$root.qwirkUser.avatar = data.name + '?' +new Date().getMilliseconds();

        }, (response) => {
          console.error(response);
        });
      },
      getAvatarSrc(){
      	let avatar = "";
      	if(this.isUserConnected){
      		avatar = this.$root.qwirkUser.avatar;
        }

        if(typeof avatar === 'undefined' || avatar === null || avatar === ""){
          return '/static/media/defaultUser.png';
        }else{
          return '/static/media/avatar/' + avatar;
        }
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

  .inputError{
    color: red;
  }

  .avatarContainer{
    padding: 50px;
    margin-top: 50px;
    margin-left: auto;
    margin-right: auto;
  }

  .avatarContainer img{
    max-width: 100%;
    max-height: 400px;
  }

  .changeAvatarLabel{
    margin: 25px;
  }

  .divField{
    width: 80%;
    margin-right: auto;
    margin-left: auto;
    -webkit-box-shadow: 0px 0px 20px 0px rgba(0,0,0,0.75);
    -moz-box-shadow: 0px 0px 20px 0px rgba(0,0,0,0.75);
    box-shadow: 0px 0px 20px 0px rgba(0,0,0,0.75);

    margin-top: 30px;
  }

  .titleField{
    padding-top: 10px;
    font-size: 22px;
    font-weight: 500;
  }

  .field{
    text-align: left;
    padding-left: 50px;
    padding-top: 10px;
    padding-bottom: 10px;
    font-size: 18px;
  }

  .form-login label{
    font-size: 22px;
  }

  .form-login input{
    margin-top: 20px;
  }

</style>
