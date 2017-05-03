<template xmlns:v-on="http://www.w3.org/1999/xhtml">
  <div id="UserHome">
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

        <autoComplete
          url="http://localhost:8000/user-autocomplete/"
          anchor="username"
          placeholder="username"
          class-name="inputText inputSearch"
          id="searchBarText">
        </autoComplete>

        <!-- <input type="text" class="inputText inputSearch" placeholder="username" v-model="searchBarText"/> -->
        <button type="button" class="btn btn-action" v-on:click="addContact">Add</button>
      </div>
      <div class="chatKind">
        <h3>Contacts</h3>
        <div class="leftNavbar">
          <div v-for="contact in qwirkUser.contacts">
            <router-link :to="contact.qwirkGroup.name | groupPath">{{ contact.qwirkUser.user.username }}</router-link>
          </div>
        </div>
      </div>
      <div class="chatKind">
        <div class="titleChatKind">
          <h3>Groups</h3>
          <span class="glyphicon glyphicon-plus" aria-hidden="true" v-on:click="showAddGroup()"></span>
        </div>
        <div class="leftNavbar">
          <div v-for="group in qwirkUser.qwirkGroups" v-if="group.isPrivate">
            <router-link :to="group.name | groupPath">{{ group.name }}</router-link>
          </div>
        </div>
      </div>
      <div class="chatKind">
        <div class="titleChatKind">
          <h3>Channels</h3>
          <span class="glyphicon glyphicon-plus" aria-hidden="true" v-on:click="showAddChannel()"></span>
        </div>
        <div class="leftNavbar">
          <div v-for="group in qwirkUser.qwirkGroups" v-if="!group.isPrivate">
            <router-link :to="group.name | groupPath">{{ group.name }}</router-link>
          </div>
        </div>
      </div>
    </div>
    <div id="content">
      <div class="activeView">
        <transition name="fade" mode="out-in">
          <router-view class="view"></router-view>
        </transition>
      </div>
    </div>

    <modal v-if="showModal" @close="showModal = false">
      <h3 slot="header">Create {{modalHeader}}</h3>
      <div slot="body">
        <label for="inputCreate">Name *</label>
        <input type="text" class="form-control" v-model="groupName" id="inputCreate"/>

        <label for="inputPrivate">Private ?</label>
        <input type="checkbox" v-model="createPrivateGroup" id="inputPrivate"/>
      </div>


      <div slot="footer">
        <button class="modal-default-button" @click="showModal = false">
          Close
        </button>
        <button class="modal-default-button" v-on:click="createGroup()">
          Create
        </button>
      </div>
    </modal>
  </div>
</template>


<script>
import Modal from '../shared/Modal.vue'
import {User, QwirkUser} from '../../../static/js/model.js';
import AutoComplete from '../shared/AutoComplete.vue'
export default{
    name:"UserHome",
    data(){
        return{
          qwirkUser: new QwirkUser(),
          showModal: false,
          modalHeader: "",
          createPrivateGroup: true,
          groupName: ""
        }
    },
    created: function(){
      self.$http.get('http://localhost:8000/userinfos/').then((response) => {
          self.qwirkUser.copyConstructor(response.body);
          //console.log(this.qwirkUser);
          //console.log(this.qwirkUser.contacts[0]);
          //console.log(this.qwirkUser.qwirkGroups);
        }, function(err){
          console.log("error :", err);
        });
    },
    mounted: function(){},
    methods:{
      addContact: function(){
        self = this;
        let username = document.getElementById('searchBarText').value;
        console.log('username: ', username);
        console.log("token " + self.$cookie.get('token'));
        self.$http.post('http://localhost:8000/addcontact/', {'username': username}, {headers: {'Authorization': "Token " + self.$cookie.get('token')}}).then(function(response){
          console.log("sucess add contact", response);
          self.currentGroupName = response.body;
          document.getElementById('searchBarText').value = "";
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
      },
      showAddGroup: function(){
        this.modalHeader = "group";
        this.createPrivateGroup = true;
        this.showModal = true;
      },
      showAddChannel: function(){
        this.modalHeader = "channel";
        this.createPrivateGroup = false;
        this.showModal = true;
      },
      createGroup: function(){
        // TODO check if name exist
        let self = this;
        let data = {groupName: this.groupName, isPrivate: this.createPrivateGroup};
        this.$http.post('http://localhost:8000/creategroup/', data, {headers: {'Authorization': "Token " + this.$cookie.get('token')}}).then(function(response){
          console.log("sucess create group", response);
          // TODO display message that said your modifications was good taken
          self.showModal = false;
          self.$router.push(self.groupName);
          self.showModal = false;
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
      Modal,
      AutoComplete
    },
}

</script>

<style>
  body, html {
      padding : 0px;
      margin : 0px;
      height : 100% !important;
  }

  #UserHome {
      width: 100%;
      height: 100%;
      margin: 0px;
      padding: 0px;
  }

  #UserChat{
    width:100%;
    overflow: auto;
    height: 100%;
    position: relative;
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
    width: 100%;
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

  .titleChatKind h3{
    display: inline-block;
  }

  .titleChatKind span{
    font-size: 18px;
    margin-left: 10px;
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
