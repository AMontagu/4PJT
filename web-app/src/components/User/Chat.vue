<template xmlns:v-on="http://www.w3.org/1999/xhtml">
  <div id="UserChat">

    <userHeader v-bind:group-informations="groupInformations" v-bind:is-ready="headerReady" v-bind:in-call="inCall" v-on:callWebRTC="callWebRTC()"></userHeader>
    <!--<p>User Chat with {{currentGroupName}}</p>-->

    <div v-if="inCall" id="containVideoChat" v-bind:class="{ 'containVideoChatFullScreen': fullScreen, 'containVideoChatMinimise': !fullScreen }">
      <span v-if="!fullScreen" v-on:click="setFullScreen(true)" class="glyphicon glyphicon-resize-full btnResize" aria-hidden="true"></span>
      <span v-if="fullScreen" v-on:click="setFullScreen(false)" class="glyphicon glyphicon-resize-small btnResize" aria-hidden="true"></span>
    </div>

    <div v-if="!fullScreen" id="containerChat" v-bind:class="{'containerChatCallMinimise': inCall && !fullScreen}">
      <div id="containerMessages">
        <div v-for="message in messages" class="containerMessage">
          <div class="pictureUser">
            <img src="/static/media/defaultUser.png">
          </div>
          <div class="messageContent">
            <div class="messageUserName">
              <p>{{message.qwirkUser.user.username}} <span class="messageTime">{{message.dateTime | hours}}</span></p>
            </div>
            <div class="messageText">
              <p>{{message.text}}</p>
            </div>
          </div>
        </div>
      </div>
      <input class="inputChat" type="text" v-model="inputText" :disabled="!socketIsOpen" v-on:keyup.enter="sendText"/>
    </div>

    <modal v-if="showModal" @close="showModal = false">
      <h3 slot="header">Call From {{userCallUsername}}</h3>
      <div slot="body">
        <button class="modal-default-button" v-on:click="acceptCall()">
          Accept
        </button>
        <button class="modal-default-button" @click="showModal = false">
          Decline
        </button>
      </div>


      <div slot="footer">
        <button class="modal-default-button" @click="showModal = false">
          Close
        </button>
      </div>
    </modal>

  </div>
</template>

<script>
import UserHeader from './Header.vue'
import Modal from '../shared/Modal.vue'
import {Message, GroupInformations, QwirkUser} from '../../../static/js/model.js';
export default{
    name:"UserChat",
    data(){
        return{
          socket: undefined,
          socketIsOpen: false,
          inputText: "",
          currentGroupName: "",
          messages: [],
          qwirkUser: new QwirkUser(),
          groupInformations: new GroupInformations(),
          headerReady: false,
          inCall: false,
          fullScreen: false,
          userCallUsername: "",
          showModal: false,
        }
    },
    created: function(){},
    mounted: function(){
      let self = this;

      self.$http.get('http://localhost:8000/userinfos/', {headers: {'Authorization': "Token " + self.$cookie.get('token')}}).then(function(response){
        self.qwirkUser.copyConstructor(response.body);
      }, function(err){
        console.log("error :", err);
      });

      console.log(this.$route.params);
      self.currentGroupName = this.$route.params.name;
      if(self.currentGroupName != "" && self.currentGroupName != undefined){
        var wsProtocol = location.protocol === 'https:' ? 'wss://' : 'ws://';
        self.socket = new WebSocket(wsProtocol + "localhost:8000/ws/chat/" + self.$cookie.get('token') + "/" + self.currentGroupName);

        self.socket.onmessage = function (message) {
          self.socketMessage(message);
        }

        self.socket.onopen = function () {
          self.socketOpen();
        };

        self.socket.onerror = function (err) {
          self.socketError(err);
        };
      }

      self.connection = new RTCMultiConnection();

      // this line is VERY_important
      self.connection.socketURL = 'http://localhost:9001/';

      // all below lines are optional; however recommended.

      self.connection.session = {
          audio: true,
          video: true
      };

      self.connection.sdpConstraints.mandatory = {
          OfferToReceiveAudio: true,
          OfferToReceiveVideo: true
      };

      self.connection.onstream = function(event) {
          let containerVideoChat = document.getElementById("containVideoChat");
          containerVideoChat.appendChild(event.mediaElement);
      };
    },
    methods: {
      scrollUpdated: function(){
        var objDiv = document.getElementById("containerMessages");
        objDiv.scrollTop = objDiv.scrollHeight;
      },
      sendText: function(){
        console.log("send text: " + this.inputText)
        if(this.socket != undefined){
          this.socket.send(JSON.stringify({action: 'message', content:{text: this.inputText}}));
        }else{
          console.log("socket is undefined");
        }
        this.inputText = "";
      },
      socketOpen: function(){
        this.socketIsOpen = true;
        console.log("socket is open");
        //get the last fifty messages of this discussion
        this.socket.send(JSON.stringify({action:'get-message', content:{startMessage: 0, endMessage: 30}}));
        this.socket.send(JSON.stringify({action:'get-group-informations'}));
      },
      socketError: function(err){
        console.log("ERROR : ", err);
      },
      socketMessage: function(message){
        let self = this;
        var data = JSON.parse(message.data);
        console.log(data);
        if(data.action == "new-message"){
          this.messages.push(JSON.parse(data.content));
          //console.log(this.messages);
          setTimeout(function(){
            self.scrollUpdated()
          }, 200);
        }else if(data.action == "saved-messages"){
          //console.log(data.content)
          this.messages = this.messages.concat(JSON.parse(data.content).reverse());
          //console.log(this.messages);

          setTimeout(function(){
            self.scrollUpdated()
          }, 300);
        }else if(data.action == "group-informations"){
          //console.log(data.content)
          this.groupInformations.copyConstructor(data.content);
          this.headerReady = true;
        }else if(data.action == "call"){
          console.log("receive call from ", data.content.username);
          if(this.qwirkUser.user.username != data.content.username){
            this.userCallUsername = data.content.username;
            this.showModal = true;
          }
        }
      },
      callWebRTC: function(){
        console.log("we call !");
        if(!this.inCall){
          this.inCall = true;

          this.connection.open(this.currentGroupName);
          this.socket.send(JSON.stringify({action:'call', content:{username: this.qwirkUser.user.username}}))
        }else{
          this.connection.join(this.currentGroupName);
        }
      },
      setFullScreen: function(isFullScreen){
        this.fullScreen = isFullScreen;
      },
      acceptCall: function(){
        this.inCall = true;
        this.connection.join(this.currentGroupName);
        this.showModal = false;
      }
    },
    watch: {
      '$route' (to, from) {
        let self = this;
        self.currentGroupName = this.$route.params.name;
        self.messages = [];

        if(this.socket != undefined){
          this.socket.close();
          this.socketIsOpen = false;
        }

        if(self.currentGroupName != ""){

          var wsProtocol = location.protocol === 'https:' ? 'wss://' : 'ws://';
          self.socket = new WebSocket(wsProtocol + "localhost:8000/ws/chat/" + self.$cookie.get('token') + "/" + self.currentGroupName);


          self.socket.onmessage = function (message) {
            self.socketMessage(message);
          }

          self.socket.onopen = function () {
            self.socketOpen();
          };

          self.socket.onerror = function (err) {
            self.socketError(err);
          };
        }
      }
    },
    filters:{
      hours: function(value){
        //console.log(value);
        var parts = value.split('T');
        var date = parts[0];
        var time = parts[1];

        //console.log(date);
        //console.log(time);

        date = date.split('-');
        time = time.split(':');

        if(parseInt(time[0], 10) > 12) {
          var hour = parseInt(time[0], 10) % 12;
        }
        else {
         var hour = parseInt(time[0], 10);
        }

        hour = hour < 10 ? '0' + hour : hour;
        //return '[' + date[1] + '/' + date[2] + ' ' + hour + ':' + time[1] + ']';
        return hour + ':' + time[1];
      }
    },
    components:{
      UserHeader,
      Modal
    }
}

</script>

<style scoped>
  #UserHeader {
      height: 60px;
      background-color: white;
      width: 100%;
      border-bottom: 1px solid grey;
  }

  .inputChat{
    width: 95%;
    border-radius: 20px;
    height: 30px;
    position: absolute;
    margin: auto;
    left: 0;
    right: 0;
    bottom: 10px;
    padding-left: 20px;
    outline: none;
  }

  #containVideoChat{
    float: left;
    height: calc(100% - 60px);
    position: relative;
  }

  .containVideoChatFullScreen{
    width: 100%;
  }

  .containVideoChatMinimise{
    width: 40%;
  }

  .btnResize{
    position: absolute;
    width: 30px;
    height: 30px;
    top: 45px;
    left: 15px;
  }

  #containerMessages{
     height: calc(100% - 60px);
     height: 90%;
     overflow-y: scroll;
     overflow-x: hidden;
  }
  #containerChat{
    height: calc(100% - 60px);
    position: relative;
  }

  .containerChatCallMinimise{
    float: right;
    width: 60%;
  }

  .containerMessage{
    text-align: left;
    display: block;
    margin-left: 20px;
    position: relative;
  }
  .pictureUser{
    padding-top: 0.25rem;
    width: 4.5rem;
    padding-right: .625rem;
    position: absolute;
    top: 0;
    left: 0;
  }
  .pictureUser img{
    border-radius: 5px;
    width: 2.25rem;
    height: 2.25rem;
  }
  .messageContent{
    margin-left: 3.5rem;
  }
  .messageTime{
    color: #9e9ea6;
    font-size: .75rem;
    white-space: nowrap;
    margin-right: .25rem;
    opacity: 1;
    display: inline;
  }
  .messageUserName{
  }
  .messageUserName p{
    font-size: .9375rem;
    font-weight: 900;
    color: #2C2D30;
    line-height: 1.125rem;
    display: inline;
    user-select: text;
    word-wrap: break-word;
  }
  .messageText{
    padding-right: 15px;
  }
  .messageText p{
    color: #2C2D30;
    font-size: .9375rem;
    line-height: 1.375rem;
    -webkit-user-select: text;
    -moz-user-select: text;
    -ms-user-select: text;
    user-select: text;
    word-wrap: break-word;
  }
</style>
