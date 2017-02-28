<template xmlns:v-on="http://www.w3.org/1999/xhtml">
  <div id="UserHome" v-if="isConnected">
    <div id="UserNavbar">
      <div id="userPart">
        <h3>{{ qwirkUser.user.username }}</h3>
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
      <transition name="fade" mode="out-in">
        <router-view class="view"></router-view>
      </transition>
    </div>
  </div>
</template>

<script>
import UserNavbar from './Navbar.vue'
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
      UserNavbar,
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

  #UserChat{
    width:100%;
    overflow: auto;
    height: 90%;
    position: relative;
  }

  #content {
      width:80%;
      height:100%;
      background-color: white;
      float:left;
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
