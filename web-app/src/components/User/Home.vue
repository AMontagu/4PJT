<template xmlns:v-on="http://www.w3.org/1999/xhtml">
  <div id="UserHome">
    <div id="UserNavbar">
      <div id="userPart">
        <!-- Split button -->
        <div class="btn-group">
          <button type="button" id="userNameBtn" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"
                  class="unstyleBtn">{{ $root.qwirkUser.user.username }} <span
            class="glyphicon glyphicon-chevron-down marginL20p" aria-hidden="true"></span></button>
          <ul class="dropdown-menu">
            <li><a href="/user/profile">Profile & account</a></li>
            <li><a v-on:click="changeConnectionStatus()">Change connection status</a></li>
            <li role="separator" class="divider"></li>
            <li><a v-on:click="logOut()">Log Out</a></li>
          </ul>
        </div>
      </div>
      <div id="searchPart">

        <autoComplete
          :url="this.$root.server + '/userchannel-autocomplete/'"
          anchor="name"
          placeholder="Search"
          class-name="inputText inputSearch"
          :multiple="true"
          :onSelect="selectName"
          id="searchBarText">
        </autoComplete>

      </div>
      <div class="chatKind">
        <h3>Contacts</h3>
        <div class="leftNavbar">
          <div v-for="contact in $root.qwirkUser.contacts">
            <div v-if="contact.status != 'Refuse' && contact.status != 'Block'">
              <router-link :to="contact.qwirkGroup.name | groupPath">{{ contact.qwirkUser.user.username }}</router-link>
              <span :id="contact.qwirkGroup.name" class="notification"></span>
            </div>
          </div>
        </div>
      </div>
      <div class="chatKind">
        <div class="titleChatKind">
          <h3>Groups</h3>
          <span class="glyphicon glyphicon-plus" aria-hidden="true" v-on:click="showAddGroup()"></span>
        </div>
        <div class="leftNavbar">
          <div v-for="group in $root.qwirkUser.qwirkGroups" v-if="group.isPrivate">
            <router-link :to="group.name | groupPath">{{ group.name }}</router-link>
            <span :id="group.name" class="notification"></span>
          </div>
        </div>
      </div>
      <div class="chatKind">
        <div class="titleChatKind">
          <h3>Channels</h3>
          <span class="glyphicon glyphicon-plus" aria-hidden="true" v-on:click="showAddChannel()"></span>
        </div>
        <div class="leftNavbar">
          <div v-for="group in $root.qwirkUser.qwirkGroups" v-if="!group.isPrivate">
            <router-link :to="group.name | groupPath">{{ group.name }}</router-link>
            <span :id="group.name" class="notification"></span>
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

    <modal v-if="showModalError" @close="showModalError = false">
      <h3 slot="header">Error {{error.name}}</h3>
      <div slot="body">
        <p class="errorMessage">{{error.message}}</p>
      </div>


      <div slot="footer">
        <button class="modal-default-button" @click="showModalError = false">
          Close
        </button>
      </div>
    </modal>
  </div>
</template>


<script>
import Modal from '../shared/Modal.vue'
import {User, QwirkUser, Notification, Contact, QwirkGroup, Error} from '../../../static/js/model.js';
import AutoComplete from '../shared/AutoComplete.vue'
export default{
  name:"UserHome",
  data(){
    return{
      showModal: false,
      showModalError: false,
      error: new Error(),
      modalHeader: "",
      createPrivateGroup: true,
      groupName: "",
      currentGroupName: "",
      loading: true,
      userSocket: null
    }
  },
  created: function(){

    if(this.loading){
      setTimeout(() => {
        this.$root.qwirkUser.notifications.forEach((notification) => {
          this.processNotification(notification);
        })
      }, 500)
    }else{
      this.$root.qwirkUser.notifications.forEach((notification) => {
          this.processNotification(notification);
        })
    }
  },
  mounted: function(){
  	console.log("route name : ", this.$route.params.name)
    this.currentGroupName = this.$route.params.name;

    this.$http.get(this.$root.server + '/userinfos/').then((response) => {
      //console.log(response.body)
      let qwirkUser = new QwirkUser();
      qwirkUser.copyConstructor(response.body);
      //console.log(this.qwirkUser);
      //console.log(this.qwirkUser.contacts);
      //console.log(this.qwirkUser.qwirkGroups);
      this.$root.qwirkUser = qwirkUser;
      //console.log(this.$root.qwirkUser)

      this.loading = false;

      this.userSocket = new WebSocket(this.$root.wssServer + '/ws/user/' + this.$cookie.get('token') + '/' + this.$root.qwirkUser.user.username);

      this.userSocket.onmessage = (message) => {
        //console.log("receive message user: ", message);

        let data = JSON.parse(message.data);
        //console.log(data);

        if(data.action === "notification"){

          //console.log(data.notification);
          let notification = new Notification();
          notification.copyConstructor(data.notification);
          //console.log(notification);
          this.processNotification(notification);
        }

        else if(data.action === "newDemand"){

          console.log("new contact demand", data.contact);

          let contact = new Contact();
          contact.copyConstructor(data.contact);

          if (!this.$root.qwirkUser.existContact(contact)) {
            this.$root.qwirkUser.contacts.push(contact);
          }

          /*let notification = new Notification();
          notification.copyConstructor(data.notification);

          this.processNotification(notification);*/
        }

        else if(data.action === "newGroup"){

        	let qwirkGroup = new QwirkGroup();
        	qwirkGroup.copyConstructor(data.qwirkGroup);

          this.$root.qwirkUser.qwirkGroups.push(qwirkGroup);

          if (!this.$root.qwirkUser.existGroup(qwirkGroup)) {
            this.$root.qwirkUser.qwirkGroups.push(qwirkGroup);
          }

          /*let notification = new Notification();
          notification.copyConstructor(data.notification);

          this.processNotification(notification);*/
        }

        else if(data.action === "removeGroup"){
        	if(data.isContactGroup === true || data.isContactGroup === 'true' || data.isContactGroup === 'True'){
        		let index = -1;
            this.$root.qwirkUser.contacts.forEach((contact, i) => {
            	if(contact.qwirkGroup.name === data.groupName){
            		index = i;
              }
            });

            if(index !== -1){
              this.$root.qwirkUser.contacts.splice(index, 1);
              if(this.currentGroupName === data.groupName){
              	if(this.$root.qwirkUser.contacts.length > 0){
                  this.currentGroupName = this.$root.qwirkUser.contacts[index].qwirkGroup.name;
              		this.$router.push('/user/' + this.currentGroupName)
                }else{
                  window.location.href = '/user/';
                }
              }
            }else{
            	console.error("can't find contact group to delete: ", data.groupName);
            }
          }
          else{
            let index = -1;
            this.$root.qwirkUser.qwirkGroups.forEach((qwirkGroup, i) => {
              if(qwirkGroup.name === data.groupName){
                index = i;
              }
            });

            if(index !== -1){
              this.$root.qwirkUser.qwirkGroups.splice(index, 1);
              if(this.currentGroupName === data.groupName){
                if(this.$root.qwirkUser.qwirkGroups.length > 0){
                  this.currentGroupName = this.$root.qwirkUser.qwirkGroups[index].name;
                  this.$router.push('/user/' + this.currentGroupName)
                }else{
                  window.location.href = '/user/';
                }
              }
            }else{
              console.error("can't find group to delete: ", data.groupName);
            }
          }
        }
      };

      this.userSocket.onopen = () => {
        console.log("user socket open");
      };

      this.userSocket.onerror = (err) => {
        console.error("user socket error: ", err);
      };

    }, (err) => {
      console.log("error :", err);
    });
  },
  methods:{
    selectName: function(data){
    	console.log("ici ", data);
    	if(data.type === 'user'){
    		this.addContact(data.name);
      }else if(data.type === 'channel'){
    		this.addUserToChannel(data.name);
      }
    },
    addContact: function(username){
      this.$http.post(this.$root.server + '/addcontact/', {'username': username}).then((response) => {

      	console.log("sucess add contact", response.data);

      	let contact = new Contact();

        contact.copyConstructor(response.data);

        document.getElementById('searchBarText').value = "";
        //console.log("currentGroupName: ", this.currentGroupName)

        if (!this.$root.qwirkUser.existContact(contact)) {

          this.$root.qwirkUser.contacts.push(contact);
        }


        this.currentGroupName = contact.qwirkGroup.name;

        console.log("currentGroupName: ", this.currentGroupName)

        this.$router.push('/user/' + this.currentGroupName)

      }, (err) => {
        if(err.body.status === 'error'){
          console.log("error :", err);
          this.error.copyConstructor(err.body);
          this.showModalError = true;
        }
      });
    },
    addUserToChannel: function(channelName){
      this.$http.post(this.$root.server + '/joinchannel/', {channelName: channelName, username: this.$root.qwirkUser.user.username}, {headers: {'Authorization': "Token " + this.$cookie.get('token')}}).then((response) => {
        console.log("sucess request add user to channels", response);
        let data = response.body;

        if(typeof data === 'string'){
          data = JSON.parse(data);
        }

        console.log(data);
        if(data.status === "success"){
        	let qwirkGroup = new QwirkGroup();
        	qwirkGroup.copyConstructor(data.qwirkGroup);
        	this.$root.qwirkUser.qwirkGroups.push(qwirkGroup);
          this.$router.push('/user/' + channelName)
        }else{
        	console.error("error join channel");
          //display error modal
        }
      })
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
      let data = {groupName: this.groupName, isPrivate: this.createPrivateGroup};
      console.log(data);
      this.$http.post('http://localhost:8000/creategroup/', data, {headers: {'Authorization': "Token " + this.$cookie.get('token')}}).then((response) => {

      	console.log("sucess create group", response);
      	let qwirkGroup = new QwirkGroup();
      	qwirkGroup.copyConstructor(response.body);

        this.$root.qwirkUser.qwirkGroups.push(qwirkGroup);

        // TODO display message that said your modifications was good taken
        this.currentGroupName = this.groupName;
        this.showModal = false;

        this.$router.push('/user/' + this.currentGroupName);
        this.groupName = '';

      }, (err) => {
        console.log("error :", err);
        if(err.body.status === 'error'){
          this.error.copyConstructor(err.body);
          this.showModalError = true;
        }
      });
    },
    processNotification: function(notification){
    	//console.log("1: ", this.currentGroupName, " 2: ", notification.groupName);
    	if(this.currentGroupName !== notification.groupName){

        let el = document.getElementById(notification.groupName);
        if(typeof el !== "undefined" && el !== null) {
          if (el.textContent === "") {

            let txt = document.createTextNode("1");
            el.innerText = txt.textContent;
            el.classList.add('active');

          } else {

            let value = parseInt(el.textContent);
            value++;
            let txt = document.createTextNode(value.toString());
            el.innerText = txt.textContent;
          }
        }else{
        	setTimeout(() => {
            let els = document.getElementsByClassName('notification');

            for(let i=0; i< els.length; i++){
              if(els[i].id === notification.groupName){
                if (els[i].textContent === "") {

                  let txt = document.createTextNode("1");
                  els[i].innerText = txt.textContent;
                  els[i].classList.add('active');

                } else {

                  let value = parseInt(els[i].textContent);
                  value++;
                  let txt = document.createTextNode(value.toString());
                  els[i].innerText = txt.textContent;
                }
              }
            }
          }, 1000);

        }
      }
    },
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
  beforeRouteUpdate (to, from, next) {
    //console.log(to.params.name);
    if(typeof to.params.name !== "undefined") {

    	this.currentGroupName = to.params.name;

      let el = document.getElementById(to.params.name);

      if(typeof el !== "undefined" && el !== null){
        if (el.textContent !== "") {

          let txt = document.createTextNode("");
          el.innerText = txt.textContent;
          el.classList.remove("active");
        }
      }
      next();
    }
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
    padding-left: 30px;
    width: 15%;
    min-width: 200px;
    background-color: #555;
    height: 100%;
    overflow: auto;
    float:left;
    text-align: left;
  }

  #UserNavbar p, #UserNavbar h3, #UserNavbar h1, #UserNavbar h2, #UserNavbar h4, #UserNavbar a, #UserNavbar button, #UserNavbar span{
    color: white;
  }

  .activeView{
    width: 100%;
    overflow: auto;
    height: 100%;
    position: relative;
  }

  #content {
      width:85%;
      max-width: calc(100% - 200px);
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

  #searchPart{
    position: relative;
    width: 80%;
  }

  #searchBarText{
    width: 100%;
  }

  .chatKind{
    width:100%;
  }

  .chatKind a{
    font-size: 18px;
    line-height: 30px;

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
    padding-left: 20px;
    width: 100%;
    position: relative;
  }

  li a {
    display: block;
    color: #000 !important;
    padding: 8px 16px;
    text-decoration: none;
  }

  li a.active {
    background-color: #4CAF50;
    color: white !important;
  }

  li a:hover:not(.active) {
    background-color: #555;
    color: white !important;
  }

  .notification{
    width: 25px;
    height: 25px;
    margin-left: 10px;
    font-size: 16px;
    display: inline-block;
    text-align: center;
    vertical-align: middle;
    line-height: 25px;
  }

  .notification.active{
    background-color: red;
    border-radius: 50%;
  }

</style>
