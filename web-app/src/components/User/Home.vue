<template>
  <div id="UserHome" v-if="isConnected">
    <userNavbar v-bind:qwirk-user="qwirkUser"></userNavbar>
    <div id="content">
      <userHeader></userHeader>
      <transition name="fade" mode="out-in">
        <router-view class="view"></router-view>
      </transition>
    </div>
  </div>
</template>

<script>
import UserNavbar from './Navbar.vue'
import UserHeader from './Header.vue'
import {User, QwirkUser} from '../../../static/js/model.js';
export default{
    name:"UserHome",
    data(){
        return{
          isConnected: false,
          qwirkUser: new QwirkUser()
        }
    },
    created: function(){
      this.checkIfUserLoggedIn();
    },
    mounted: function(){},
    methods:{
      checkIfUserLoggedIn: function(){
        //TODO look into cookies
        let self = this;
        if (this.$cookie.get('token') == null){
          location.href = '/';
        }else{
          this.$http.get('http://localhost:8000/isloggedin/', {headers: {'Authorization': "Token " + this.$cookie.get('token')}}).then(function(response){
            console.log("sucess request", response);
            if(response.body == "True"){
              console.log("user is logged in");
              self.isConnected = true;
              console.log(self.$cookie.get('token'));
              self.$http.get('http://localhost:8000/userinfos/', {headers: {'Authorization': "Token " + self.$cookie.get('token')}}).then(function(response){
                self.qwirkUser.copyConstructor(response.body);
                console.log(self.qwirkUser);
              }, function(err){
                console.log("error :", err);
              });
            }else{
              console.log("user is NOT logged in");
              // TODO look cookies for username and password
              self.$router.push('/');
            }
          }, function(err){
            console.log("error :", err);
            location.href = '/';
          });
        }
      }
    },
    components:{
      UserNavbar,
      UserHeader
    }
}

</script>

<style>
  body, html {
      padding : 0px;
      margin : 0px;
      height : 100% !important;
  }

  #UserHome {
      width:100%;
      height:100%;
      margin: 0px;
      padding: 0px;
  }

  #UserHeader {
      height:10%;
      background-color:#930;
      width:100%;
  }

  #UserNavbar{
    margin: 0;
    padding: 0;
    width: 20%;
    background-color: #f1f1f1;
    height: 100%;
    overflow: auto;
    float:left;
  }

  #UserChat{
    width:100%;
    overflow: auto;
    height: 90%;
  }

  #content {
      width:80%;
      height:100%;
      background-color:#363;
      float:left;
  }
</style>
