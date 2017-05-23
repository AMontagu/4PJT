<template xmlns:v-on="http://www.w3.org/1999/xhtml">
  <div id="UserHeader">
    <div v-if="isReady">
      <div class="leftHeader">
        <div class="topLeftHeader">
          <h4>{{groupInformations.titleGroupName}}</h4>
        </div>
        <div class="bottomLeftHeader">
          <div v-if="groupInformations.isContactGroup">
            <span :class="getConnectionColor(groupInformations.qwirkUsers[0].status)"></span> <p class="statusText">{{groupInformations.qwirkUsers[0].status}}</p>
          </div>
          <div class="btn-group" v-else>
            <button type="button" class="unstyleBtn" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><span class="glyphicon glyphicon-user" aria-hidden="true"></span> {{usersNumber}}</button>
            <ul class="dropdown-menu">
              <li v-for="qwirkUser in groupInformations.qwirkUsers"><a v-on:click="showUser(qwirkUser)">{{ qwirkUser.user.username }}</a></li>
            </ul>
          </div>
        </div>
      </div>
      <div class="rightHeader">
        <span v-if="!inCall" class="glyphicon glyphicon glyphicon-earphone qwirkHeaderIcon" aria-hidden="true" v-on:click="emitCallWebRTC()"></span>
        <span v-if="!groupInformations.isContactGroup" class="glyphicon glyphicon-plus qwirkHeaderIcon" aria-hidden="true" v-on:click="showAddUser()"></span>
        <div class="btn-group">
          <button type="button" id="settingGroupBtn" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" class="unstyleBtn"><span class="glyphicon glyphicon-cog qwirkHeaderIcon" aria-hidden="true"></span></button>
          <ul v-if="!groupInformations.isContactGroup" class="dropdown-menu" style="left: -125px;">
            <li><a v-on:click="quitGroup()">Leave {{groupInformations.titleGroupName}}</a></li>
            <li v-if="groupInformations.isAdmin" role="separator" class="divider"></li>
            <li v-if="groupInformations.isAdmin"><a v-on:click="removeGroup()">Remove {{groupInformations.titleGroupName}}</a></li>
          </ul>
          <ul class="dropdown-menu" style="left: -125px;" v-else>
            <li><a v-on:click="removeGroup()">Remove relationship</a></li>
          </ul>
        </div>
      </div>
    </div>

    <modal v-if="showModal" @close="showModal = false">
      <h3 slot="header">Add user</h3>
      <div slot="body">
        <label for="inputAddUser">Name *</label>
        <input type="text" class="form-control" v-model="usernameUser" id="inputAddUser"/>
        <span class="colorError">{{errorUserName}}</span>

        <div v-if="groupInformations.isAdmin">
          <label for="inputAdmin">Admin ?</label>
          <input type="checkbox" v-model="adminUser" id="inputAdmin"/>
        </div>
      </div>


      <div slot="footer">
        <button class="modal-default-button" @click="showModal = false">
          Close
        </button>
        <button class="modal-default-button" v-on:click="addUser()">
          Add
        </button>
      </div>
    </modal>


    <modal v-if="showUserModal" @close="showUserModal = false">
      <h3 slot="header" class="headerUserModal">{{ userToShow.user.username }}</h3>

      <div slot="body">
        <ul v-if="userToShow.user.username != $root.qwirkUser.user.username" class="listActions">
          <li v-on:click="goToUserProfile(userToShow.user.username)">View user profile</li>
          <li v-on:click="goToUserMessage(userToShow.user.username)">Direct Messages</li>
          <li v-if="groupInformations.isAdmin" v-on:click="giveAdminRight(userToShow.user.username)">Give moderator right</li>
          <li v-if="groupInformations.isAdmin" v-on:click="banUser(userToShow.user.username)">Ban User</li>
        </ul>
        <ul class="listActions" v-else>
          <li v-on:click="goToUserProfile(userToShow.user.username)">Edit profile</li>
          <li v-on:click="changeConnectionStatus()">Set yourself to away</li>
        </ul>
      </div>

      <div slot="footer">
        <button class="modal-default-button" @click="showUserModal = false">
          Close
        </button>
      </div>
    </modal>

    <modal v-if="showModalUserNotFriend" @close="showModalUserNotFriend = false">
      <h3 slot="header">You are not friend with {{ usernameUserNotFriend }}</h3>

      <div slot="body">
        <p>Would you send a contact request to {{ usernameUserNotFriend }} ?</p>
      </div>

      <div slot="footer">
        <button class="modal-default-button" @click="showModalUserNotFriend = false">
          No
        </button>
        <button class="modal-default-button" @click="addContact()">
          Yes
        </button>
      </div>
    </modal>
  </div>
</template>

<script>
import Modal from '../shared/Modal.vue'
import {QwirkUser, Contact} from '../../../static/js/model'

export default{
    name:"UserHeader",
    props: ['groupInformations', 'isReady', 'inCall'],
    data(){
        return{
          currentGroupName: "",
          titleGroupName: "",
          showModal: false,
          usernameUser: "",
          adminUser: false,
          errorUserName: "",
          showUserModal: false,
          userToShow: new QwirkUser(),
          usernameUserNotFriend: '',
          showModalUserNotFriend: false,
        }
    },
    created: function(){
      let self = this;
      /*console.log("aaaaaa");
      console.log(this.groupInformations);
      console.log(this.isReady);

      setTimeout(function(){
        console.log("bbbbbb");
        console.log(self.groupInformations);
        console.log(self.isReady);
      }, 3000);*/
    },
    mounted: function(){
      this.currentGroupName = this.$route.params.name;
    },
    methods: {
      getConnectionColor: function(status){
        let cssClass = "statusIcon ";
        if (status == "Online"){
          cssClass += "green";
        } else if (status == "Offline"){
          cssClass += "grey";
        } else if (status == "Busy"){
          cssClass += "red";
        } else if (status == "Absent"){
          cssClass += "orange";
        }

        return cssClass
      },
      showAddUser: function(){
        this.errorUsername = null;
        this.createPrivateGroup = true;
        this.showModal = true;
      },
      addUser: function(){
        if(this.usernameUser != ""){
          this.$http.post(this.$root.server + '/addusertogroup/', {groupName: this.currentGroupName, username: this.usernameUser, isAdmin: this.adminUser}, {headers: {'Authorization': "Token " + this.$cookie.get('token')}}).then((response) => {
            console.log("sucess request add user to group/channels", response);
            let data = response.body;

            if(typeof data === 'string'){
            	data = JSON.parse(data);
            }

            console.log(data);
            if(data["status"] == "success"){
              this.showModal = false;
            }else{
              this.errorUsername = data["text"];
            }
          })
        }
        else{
          this.errorUserName = "Please enter a username or close";
        }
      },
      removeGroup: function () {
        this.$http.post(this.$root.server + '/removegroup/', {groupName: this.currentGroupName}, {headers: {'Authorization': "Token " + this.$cookie.get('token')}}).then((response) => {
          console.log("successfully deleted ", this.currentGroupName);
          this.$router.go('/user/');
        });
      },
      quitGroup: function(){
        this.$http.post(this.$root.server + '/quitGroup/', {groupName: this.currentGroupName}, {headers: {'Authorization': "Token " + this.$cookie.get('token')}}).then((response) => {
          console.log("successfully quitted ", this.currentGroupName);
          this.$router.go('/user/');
        });
      },
      emitCallWebRTC: function(){
        this.$emit("callWebRTC");
      },
      showUser(qwirkUser){
      	this.userToShow = qwirkUser;
      	console.log(this.userToShow);
      	this.showUserModal = true;
      },
      goToUserProfile(username){
      	//this.$router.push('/user/profile/' + username);
        window.location.href = '/user/profile/' + username;
      },
      giveAdminRight(username){
        this.$http.post(this.$root.server + '/giveadminright/', {username: username, groupName: this.currentGroupName}, {headers: {'Authorization': "Token " + this.$cookie.get('token')}}).then((response) => {
          console.log("successfully give admin right ");
          this.showUserModal = false;
        });

      },
      checkFriendship(username){
      	return new Promise((resolve) => {
          this.$http.post(this.$root.server + '/checkfriendship/', {username: username}, {headers: {'Authorization': "Token " + this.$cookie.get('token')}}).then((response) => {
            console.log("friendship status: ", response.body);
            let data = response.body;

            if(typeof data === 'string'){
            	data = JSON.parse(data);
            }

            resolve(data);
          });
        });
      },
      addContact(){

        this.$http.post(this.$root.server + '/addcontact/', {'username': this.usernameUserNotFriend}).then((response) => {

          console.log("sucess add contact", response.data);

          let contact = new Contact();

          contact.copyConstructor(response.data);

          if (!this.$root.qwirkUser.existContact(contact)) {

            this.$root.qwirkUser.contacts.push(contact);
          }

          this.showModalUserNotFriend = false;

          this.$router.push('/user/' + contact.qwirkGroup.name)

        }, function(err){

          console.log("error :", err);
        });
      },
      goToUserMessage(username){
      	this.checkFriendship(username).then((response) => {
      		if(response.isFriend || response.isFriend === 'True'){
            this.showUserModal = false;
      			this.$router.push('/user/' + response.groupName);
          }else {
      			this.showUserModal = false;
      			this.usernameUserNotFriend = username;
            this.showModalUserNotFriend = true;
          }
        })
      },
      banUser(username){
        this.$http.post(this.$root.server + '/banuser/', {username: username, groupName: this.currentGroupName}, {headers: {'Authorization': "Token " + this.$cookie.get('token')}}).then((response) => {
          console.log("user banned");
          this.showUserModal = false;
        });
      },
      changeConnectionStatus(){
      	//TODO
      }
    },
    computed: {
      // a computed getter
      usersNumber: function () {
        return this.groupInformations.qwirkUsers.length;
      }
    },
    watch: {
      '$route' (to, from) {
        this.currentGroupName = this.$route.params.name;
      }
    },
    components:{
      Modal
    }
}
</script>

<style scoped>
  .leftHeader{
    width: 50%;
    text-align: left;
    padding-left: 20px;
    float: left;
    height: 60px;
  }

  .rightHeader{
    width: 50%;
    text-align: right;
    padding-right: 20px;
    float: right;
  }

  .leftHeader h4{
    font-weight: bold;
  }

  .statusIcon{
    border-radius: 50%;
    width: 10px;
    height: 10px;
    display: inline-block;
  }

  .statusText{
    display: inline-block;
  }

  .qwirkHeaderIcon{
    font-size: 30px;
  }

  .headerUserModal{
    background-image: linear-gradient(rgba(0,0,0,0), rgba(0,0,0,0) 34%, rgba(0,0,0,0.2) 66%, rgba(0,0,0,0.2) 83%, rgba(0,0,0,0.6)), url(/static/media/defaultUser.png), url(/static/media/defaultUser.png);
    background-size: cover;
    height: 150px;
    margin: -35px -45px;
    border-radius: 1%;
    line-height: 240px;
    color: white;
  }

  .listActions{
    padding-left: 0;
    cursor: pointer;
  }

  .listActions li {
    display: block;
    color: #000;
    padding: 8px 16px;
    text-decoration: none;
    text-align: left;
  }

  .listActions li:hover {
    background-color: #555;
    color: white;
  }
</style>
