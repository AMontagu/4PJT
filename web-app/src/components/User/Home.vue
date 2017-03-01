<template xmlns:v-on="http://www.w3.org/1999/xhtml">
  <div id="UserHome" v-if="isConnected">
    <div id="UserNavbar">
      <div id="userPart">
        <!-- Split button -->
        <div class="btn-group">
          <button type="button" id="userNameBtn" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" class="unstyleBtn">{{ qwirkUser.user.username }} <span class="glyphicon glyphicon-chevron-down marginL20p" aria-hidden="true"></span></button>
          <ul class="dropdown-menu">
            <li><a href="/user/profile">Profile & Account</a></li>
            <li><a v-on:click="changeConnectionStatus()">Change connection status</a></li>
            <li role="separator" class="divider"></li>
            <li><a v-on:click="logOut()">Log Out</a></li>
          </ul>
        </div>
      </div>
      <div id="searchPart">
        <input type="text" class="inputText inputSearch" placeholder="username" v-model="searchBarText"/>
        <button type="button" class="btn btn-action" v-on:click="addContact">Add</button>
      </div>
      <div class="chatKind">
        <h3>Contacts</h3>
        <ul class="leftNavbar">
          <router-link v-for="contact in qwirkUser.contacts" tag="li" :to="contact.qwirkGroup.name | groupPath">
            <a>{{ contact.qwirkUser.user.username }}</a>
          </router-link>
        </ul>
      </div>
      <div class="chatKind">
        <h3>Groups</h3>
        <ul class="leftNavbar">
          <router-link v-for="group in qwirkUser.qwirkGroups" tag="li" :to="group.name | groupPath">
            <a>{{ group.name }}</a>
          </router-link>
        </ul>
      </div>
    </div>
    <div id="content">
      <userHeader></userHeader>
      <div class="activeView">
        <transition name="fade" mode="out-in">
          <router-view class="view"></router-view>
        </transition>
      </div>
    </div>
  </div>
</template>

<script>
import UserHeader from './Header.vue'
import UserChat from './Chat.vue'
import {User, QwirkUser} from '../../../static/js/model.js';
export default{
    name:"UserHome",
    data(){
        return{
          isConnected: false,
          qwirkUser: new QwirkUser(),
          searchBarText: ""
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
                console.log(self.qwirkUser.contacts[0]);
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
      },
      addContact: function(){
        self = this;
        let username = self.searchBarText;
        console.log("token " + self.$cookie.get('token'));
        self.$http.post('http://localhost:8000/addcontact/', {'username': username}, {headers: {'Authorization': "Token " + self.$cookie.get('token')}}).then(function(response){
          console.log("sucess add contact", response);
          self.currentGroupName = response.body;
        }, function(err){
          console.log("error :", err);
        });
      },
      logOut: function(){
        this.$cookie.delete('token');
        //console.log(this.$cookie.get('token'))
        this.$router.push('/');
      },
      changeConnectionStatus: function(){
        console.log("user want to change it's connection status")
      }
    },
    filters: {
      groupPath: function (name) {
        return '/user/' + name;
      }
    },
    watch: {
      searchBarText: function (name) {
        //console.log(name);
      }
    },
    components:{
      UserHeader,
      UserChat
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

  .activeView{
    width:100%;
    overflow: auto;
    height: 90%;
    position: relative;
  }

  #UserChat{
    width:100%;
    overflow: auto;
    height: 100%;
    position: relative;
  }

  #content {
      width:80%;
      height:100%;
      background-color: white;
      float:left;
  }

  #userPart{
    text-align: left;

  }

  #userPart{
    text-align: left;

  }

  #userPart .btn-group{
    width: 90%;
    margin-left: 10%;
  }

  #userNameBtn{
    font-size: 1.45rem;
    text-align: left;
    padding-top: 1rem;
    padding-left: 1.7rem;
    margin-bottom: 1rem;
  }

  .chatKind{
    width:100%;

  }
  .leftNavbar {
    list-style-type: none;
    margin: 0;
    padding: 0;
    width: 100%;
    position: relative;
  }

  li a {
    display: block;
    color: #000;
    padding: 8px 16px;
    text-decoration: none;
  }

  li a.active {
    background-color: #4CAF50;
    color: white;
  }

  li a:hover:not(.active) {
    background-color: #555;
    color: white;
  }
</style>
