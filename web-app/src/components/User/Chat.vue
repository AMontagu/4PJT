<template xmlns:v-on="http://www.w3.org/1999/xhtml">
  <div id="UserChat">

    <userHeader v-bind:group-informations="groupInformations" v-bind:is-ready="headerReady" v-bind:in-call="inCall"
                v-on:callWebRTC="callWebRTC()"></userHeader>
    <!--<p>User Chat with {{currentGroupName}}</p>-->

    <div v-if="inCall" id="containVideoChat" class="fullHeightScrolling"
         v-bind:class="{ 'containVideoChatFullScreen': fullScreen, 'containVideoChatMinimise': !fullScreen }">
      <div class="containerScroll">
        <span v-if="!fullScreen" v-on:click="setFullScreen(true)" class="glyphicon glyphicon-resize-full btnResize"
              aria-hidden="true"></span>
        <span v-if="fullScreen" v-on:click="setFullScreen(false)" class="glyphicon glyphicon-resize-small btnResize"
              aria-hidden="true"></span>
        <div id="videoList"></div>
      </div>

      <div id="icons" class="active fixBottom">

        <svg v-on:click="muteAudio()" v-bind:class="{ on: !isAudioEnable }" id="mute-audio"
             xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewbox="-10 -10 68 68">
          <title>title</title>
          <circle cx="24" cy="24" r="34">
            <title>Mute audio</title>
          </circle>
          <path class="on" transform="scale(0.6), translate(17,18)"
                d="M38 22h-3.4c0 1.49-.31 2.87-.87 4.1l2.46 2.46C37.33 26.61 38 24.38 38 22zm-8.03.33c0-.11.03-.22.03-.33V10c0-3.32-2.69-6-6-6s-6 2.68-6 6v.37l11.97 11.96zM8.55 6L6 8.55l12.02 12.02v1.44c0 3.31 2.67 6 5.98 6 .45 0 .88-.06 1.3-.15l3.32 3.32c-1.43.66-3 1.03-4.62 1.03-5.52 0-10.6-4.2-10.6-10.2H10c0 6.83 5.44 12.47 12 13.44V42h4v-6.56c1.81-.27 3.53-.9 5.08-1.81L39.45 42 42 39.46 8.55 6z"
                fill="white"/>
          <path class="off" transform="scale(0.6), translate(17,18)"
                d="M24 28c3.31 0 5.98-2.69 5.98-6L30 10c0-3.32-2.68-6-6-6-3.31 0-6 2.68-6 6v12c0 3.31 2.69 6 6 6zm10.6-6c0 6-5.07 10.2-10.6 10.2-5.52 0-10.6-4.2-10.6-10.2H10c0 6.83 5.44 12.47 12 13.44V42h4v-6.56c6.56-.97 12-6.61 12-13.44h-3.4z"
                fill="white"/>
        </svg>

        <svg v-on:click="muteVideo()" v-bind:class="{ on: !isVideoEnable }" id="mute-video"
             xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewbox="-10 -10 68 68">
          <circle cx="24" cy="24" r="34">
            <title>Mute video</title>
          </circle>
          <path class="on" transform="scale(0.6), translate(17,16)"
                d="M40 8H15.64l8 8H28v4.36l1.13 1.13L36 16v12.36l7.97 7.97L44 36V12c0-2.21-1.79-4-4-4zM4.55 2L2 4.55l4.01 4.01C4.81 9.24 4 10.52 4 12v24c0 2.21 1.79 4 4 4h29.45l4 4L44 41.46 4.55 2zM12 16h1.45L28 30.55V32H12V16z"
                fill="white"/>
          <path class="off" transform="scale(0.6), translate(17,16)"
                d="M40 8H8c-2.21 0-4 1.79-4 4v24c0 2.21 1.79 4 4 4h32c2.21 0 4-1.79 4-4V12c0-2.21-1.79-4-4-4zm-4 24l-8-6.4V32H12V16h16v6.4l8-6.4v16z"
                fill="white"/>
        </svg>

        <svg id="hangup" v-on:click="hangup()" xmlns="http://www.w3.org/2000/svg" width="48" height="48"
             viewbox="-10 -10 68 68">
          <circle cx="24" cy="24" r="34">
            <title>Hangup</title>
          </circle>
          <path transform="scale(0.7), translate(11,10)"
                d="M24 18c-3.21 0-6.3.5-9.2 1.44v6.21c0 .79-.46 1.47-1.12 1.8-1.95.98-3.74 2.23-5.33 3.7-.36.35-.85.57-1.4.57-.55 0-1.05-.22-1.41-.59L.59 26.18c-.37-.37-.59-.87-.59-1.42 0-.55.22-1.05.59-1.42C6.68 17.55 14.93 14 24 14s17.32 3.55 23.41 9.34c.37.36.59.87.59 1.42 0 .55-.22 1.05-.59 1.41l-4.95 4.95c-.36.36-.86.59-1.41.59-.54 0-1.04-.22-1.4-.57-1.59-1.47-3.38-2.72-5.33-3.7-.66-.33-1.12-1.01-1.12-1.8v-6.21C30.3 18.5 27.21 18 24 18z"
                fill="white"/>
        </svg>
      </div>
    </div>

    <div v-if="!fullScreen" id="containerChat" class="fullHeightScrolling"
         v-bind:class="{'containerChatCallMinimise': inCall && !fullScreen}">
      <div class="containerScroll" id="containerMessages">
        <div v-for="message in messages" class="containerMessage">
          <div v-if="displayMessage(message.type)">
            <div class="pictureUser">
              <img :src="getAvatarSrc(message.qwirkUser.avatar)">
            </div>
            <div class="messageContent">
              <div class="messageUserName">
                <p>{{message.qwirkUser.user.username}} <span class="messageTime">{{message.dateTime | hours}}</span></p>
              </div>
              <div v-if="message.type != 'codeMessage'" class="messageText" v-html="getMarkedMessage(message.text)">
              </div>
              <div v-else-if="message.type == 'codeMessage'">
                <pre class="prettyprint linenums codeBlock" v-html="getCodeMessage(message.text)"></pre>
              </div>
            </div>
          </div>

          <div v-if="message.type == 'requestMessage'">

            <div v-if="groupInformations.statusContact == 'Asking'">
              <h3>Your demand is actually in waiting state. Please wait for a respond.</h3>
            </div>

            <div v-else-if="groupInformations.statusContact == 'Pending'">
              <h3>{{ groupInformations.qwirkUsers[0].user.username }} is asking you as friend</h3>
              <div class="containBtnInline">
                <button class="btn btnAction" v-on:click="acceptRequest()">Accept</button>
                <button class="btn btnAction" v-on:click="declineRequest()">Decline</button>
                <button class="btn btnAction" v-on:click="blockUser(groupInformations.qwirkUsers[0].user.username)">
                  Block
                </button>
              </div>
            </div>

            <div v-else-if="groupInformations.statusContact == 'Friend'">
              <h3> You and {{ groupInformations.qwirkUsers[0].user.username }} are now friends</h3>
            </div>

            <div v-else-if="groupInformations.statusContact == 'Refuse'">
              <h3>The demand has been refused.</h3>
            </div>

            <div v-else-if="groupInformations.statusContact == 'Block'">
              <h3>This user has been blocked</h3>
            </div>

          </div>

          <div v-if="message.type == 'fileMessage'">

            <div class="containerFile">
              <div class="fileAction">
                <p>{{ message.file }}</p>
                <a class="btn btnAction" :href="$root.server+'/downloadfile/?fileName=' + message.file">Download file</a>
              </div>
            </div>

          </div>

          <div v-if="message.type == 'imageMessage'">

            <div class="containerImageMessage">
              <div class="containerImage">
                <img :src="'/static/media/files/' + message.file"/>
                <a class="btn" :href="$root.server+'/downloadfile/?fileName=' + message.file">Download</a>
              </div>
            </div>

          </div>

        </div>

      </div>
      <div class="chatBar">
        <textarea class="inputChat" v-model="inputText" :disabled="!socketIsOpen" v-on:keyup.enter="sendText('message', $event)"></textarea>

        <div class="btn-group dropup chatOptions">
          <button type="button" id="settingGroupBtn" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" class="unstyleBtn"><i class="glyphicon glyphicon-plus"></i></button>
          <ul class="dropdown-menu listActions">
            <li><label for="file_upload">Upload file</label></li>
            <li><label for="image_upload">Upload image</label></li>
            <li><a v-on:click="showModalCodeSnippet = true">Upload code snippet</a></li>
          </ul>
        </div>

        <input type="file" id="file_upload" class="hidden" v-on:change.prevent="fileUpload">
        <input type="file" id="image_upload" class="hidden" v-on:change.prevent="imageUpload">

        <button type="button" class="btn_unstyle emo_menu">
          <i class="glyphicon glyphicon-heart"></i>
        </button>

      </div>
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

    <modal v-if="showModalCodeSnippet" @close="showModalCodeSnippet = false">
      <h3 slot="header">Add a code snippet</h3>
      <div slot="body">
        <label for="codeArea">Language: </label>
        <textarea id="codeArea" v-model="inputText" placeholder="Your code here"></textarea>
      </div>


      <div slot="footer">
        <button class="modal-default-button" @click="showModalCodeSnippet = false">
          Close
        </button>
        <button class="modal-default-button" v-on:click="sendText('codeMessage')">
          Send
        </button>
      </div>
    </modal>

  </div>
</template>

<script>
  import UserHeader from './Header.vue'
  import Modal from '../shared/Modal.vue'
  import {Message, GroupInformations, QwirkUser} from '../../../static/js/model.js';
  import Marked from 'marked';
  export default{
    name: "UserChat",
    data(){
      return {
        socket: undefined,
        socketIsOpen: false,
        inputText: "",
        currentGroupName: "",
        messages: [],
        groupInformations: new GroupInformations(),
        headerReady: false,
        inCall: false,
        fullScreen: false,
        userCallUsername: "",
        showModal: false,
        isAudioEnable: true,
        isVideoEnable: true,
        langageCode: '',
        showModalCodeSnippet: false
      }
    },
    created: function () {
    },
    mounted: function () {


      console.log(Marked('I am using __markdown__.'));

      //console.log(this.$route.params);
      this.currentGroupName = this.$route.params.name;
      if (this.currentGroupName !== "" && typeof this.currentGroupName !== 'undefined') {
        this.socket = new WebSocket(this.$root.wssServer + "/ws/chat/" + this.$cookie.get('token') + "/" + this.currentGroupName);

        this.socket.onmessage = this.socketMessage;
        this.socket.onopen = this.socketOpen;
        this.socket.onerror = this.socketError;
      }

      PR.prettyPrintOne()
    },
    methods: {
      displayMessage: function (type) {
        return (type.includes("message") || type.includes("Message"));
      },
      scrollUpdated: function () {
        let objDiv = document.getElementById("containerMessages");
        objDiv.scrollTop = objDiv.scrollHeight;
      },
      sendText: function (type, event) {
        console.log("send text: " + this.inputText)
        console.log(this.inputText)
        console.log(this.inputText != '')
        console.log({inputText: this.inputText.trim()});
        if (typeof this.socket !== 'undefined' && this.inputText.trim() !== '' && (typeof event === 'undefined' || !event.shiftKey)) {
          let text = this.inputText.replace(/(?:\r\n|\r|\n)/g, '<br />');
          this.socket.send(JSON.stringify({action: 'message', content: {text: text, type: type}}));
          this.inputText = "";
          if(this.showModalCodeSnippet){
          	this.showModalCodeSnippet = false;
          }
        } else {
          console.log("socket is undefined or message empty");
        }
      },
      socketOpen: function () {
        this.socketIsOpen = true;
        console.log("socket is open");
        //get the last fifty messages of this discussion
        this.socket.send(JSON.stringify({action: 'get-message', content: {startMessage: 0, endMessage: 30}}));
        this.socket.send(JSON.stringify({action: 'get-group-informations'}));
      },
      socketError: function (err) {
        console.log("ERROR : ", err);
        window.location.href = "/user";
      },
      socketMessage: function (message) {
        let data = JSON.parse(message.data);
        //console.log(data);
        if (data.action === "new-message") {
          this.messages.push(JSON.parse(data.content));
          //console.log(this.messages);
          setTimeout(() => {
            this.scrollUpdated()
          }, 200);
        } else if (data.action === "saved-messages") {
          //console.log(data.content)
          this.messages = this.messages.concat(JSON.parse(data.content).reverse());
          //console.log(this.messages);

          setTimeout(() => {
            this.scrollUpdated()
          }, 300);
        } else if (data.action === "group-informations") {
          //console.log(data.content)
          this.groupInformations.copyConstructor(data.content);
          this.headerReady = true;
        } else if (data.action === "call") {
          console.log("receive call from ", data.content.username);
          if (this.$root.qwirkUser.user.username !== data.content.username && !this.inCall) {
            this.userCallUsername = data.content.username;
            this.showModal = true;
          }
        }
      },
      askAgain: function () {
        this.socket.send(JSON.stringify({action: 'ask-again-contact-request'}));
        this.groupInformations.statusContact = "Asking";
      },
      acceptRequest: function () {
        this.socket.send(JSON.stringify({action: 'accept-contact-request'}));
        this.groupInformations.statusContact = "Friend";
      },
      declineRequest: function () {
        this.socket.send(JSON.stringify({action: 'decline-contact-request'}));
        this.groupInformations.statusContact = "Refuse";
      },
      blockUser: function (username) {
        this.socket.send(JSON.stringify({action: 'block-contact', content: {username: username}}));
        this.groupInformations.statusContact = "Block";
      },
      fileUpload: function(e) {
        let files = e.target.files || e.dataTransfer.files;

        if (files.length > 0) {
          this.postFile(files, 'fileMessage')
        }
      },
      imageUpload: function(e) {
        let files = e.target.files || e.dataTransfer.files;

        if (files.length > 0) {
          this.postFile(files, 'imageMessage')
        }
      },
      postFile: function (files, type) {
        let formData = new FormData();
        formData.append('file', files[0]);
        formData.append('groupName', this.currentGroupName);
        formData.append('type', type);

        this.$http.post(this.$root.server + '/postfile/', formData).then((response) => {

          let data = response.body;

        }, (response) => {
          console.error(response);
        });
      },
      getMarkedMessage: function(message) {

        let text = message.replace('<br />', '\n');
      	return Marked(text);
      },
      getCodeMessage: function(message) {
        return PR.prettyPrintOne(message);
      },
      callWebRTC: function () {
        console.log("we call !");
        this.connection = new RTCMultiConnection();

        // this line is VERY_important
        this.connection.socketURL = this.$root.serverRtc;

        // all below lines are optional; however recommended.

        this.connection.session = {
          audio: true,
          video: true
        };

        this.connection.onstream = (event) => {
          if (document.getElementById(event.streamid)) {
            console.log("duplicate video");
            return;
          }
          event.mediaElement.id = event.streamid;
          let containerVideoChat = document.getElementById("videoList");
          containerVideoChat.appendChild(event.mediaElement);
          this.initHark({
            stream: event.stream,
            streamedObject: event,
            connection: this.connection
          });
        };

        this.connection.keepStreamsOpened = false;

        this.connection.sdpConstraints.mandatory = {
          OfferToReceiveAudio: true,
          OfferToReceiveVideo: true
        };

        this.connection.onspeaking = function (e) {
          // e.streamid, e.userid, e.stream, etc.
          e.mediaElement.style.border = '1px solid red';
        };

        this.connection.onsilence = function (e) {
          // e.streamid, e.userid, e.stream, etc.
          e.mediaElement.style.border = '';
        };

        this.connection.onvolumechange = function (event) {
          event.mediaElement.style.borderWidth = event.volume;
        };

        /*this.connection.onmute = function(event) {
         if (event.session.video) {
         event.mediaElement.src2 = event.mediaElement.src;
         event.mediaElement.src = '';
         event.mediaElement.style.background = 'transparent url(https://cdn.webrtc-experiment.com/images/muted.png) no-repeat center center';
         return;
         }

         if (event.stream.pause) {
         // for audio-streams
         // ask hark.js to resume looping and checking for voice activity
         event.stream.pause();
         }
         };

         this.connection.onunmute = function(event) {
         if (event.session.video) {
         console.log("ici");
         //event.mediaElement.removeAttribute('poster');
         //event.mediaElement.removeAttribute('style');
         event.mediaElement.src = event.mediaElement.src2;
         event.mediaElement.play();
         event.mediaElement.style.background = '';
         return;
         }

         if (event.stream.resume) {
         // for audio-streams
         // ask hark.js to stop looping and checking for voice activity
         event.stream.resume();
         }
         };*/

        this.connection.onerror = function (e) {
          console.log("RTCMultiConnection error: ", e);
        };

        if (!this.inCall) {
          this.inCall = true;
          this.connection.openOrJoin(this.currentGroupName);
          this.socket.send(JSON.stringify({
            action: 'call',
            content: {username: this.$root.qwirkUser.user.username}
          }))
        } else {
          this.connection.join(this.currentGroupName);
        }
      },
      setFullScreen: function (isFullScreen) {
        this.fullScreen = isFullScreen;
      },
      acceptCall: function () {
        this.inCall = true;
        this.callWebRTC();
        this.showModal = false;
      },
      muteAudio: function () {
        console.log(this.connection.attachStreams);
        console.log("mute audio");
        if (this.isAudioEnable) {
          this.connection.attachStreams.forEach(function (stream) {
            stream.mute({/*type:'local', */audio: true}); // mute all tracks
          });
          //this.connection.streamEvents['stream-id'].stream.mute('audio');
        } else {
          this.connection.attachStreams.forEach(function (stream) {
            stream.unmute({/*type:'local', */audio: true}); // mute all tracks
          });
          //this.connection.streamEvents['stream-id'].stream.unmute('audio');
        }
        this.isAudioEnable = !this.isAudioEnable;
      },
      muteVideo: function () {
        console.log("mute video");
        if (this.isVideoEnable) {
          this.connection.attachStreams.forEach(function (stream) {
            stream.mute({/*type:'local', */video: true}); // mute all tracks
          });
          //this.connection.streamEvents['stream-id'].stream.mute('video');
        } else {
          this.connection.attachStreams.forEach(function (stream) {
            stream.unmute({/*type:'local', */video: true}); // mute all tracks
          });
          //this.connection.streamEvents['stream-id'].stream.unmute('video');
        }
        this.isVideoEnable = !this.isVideoEnable;
      },
      hangup: function () {
        console.log("hangUp");
        this.connection.attachStreams.forEach(function (stream) {
          stream.stop();
        });
        //this.connection.streams.stop();
        //this.connection.leave();
        //this.connection.close();
        this.connection.disconnect();
        this.inCall = false;
      },
      initHark: function (args) {
        if (!window.hark) {
          throw 'Please link hark.js';
          return;
        }

        let connection = args.connection;
        let streamedObject = args.streamedObject;
        let stream = args.stream;

        let options = {};
        let speechEvents = hark(stream, options);

        speechEvents.on('speaking', function () {
          connection.onspeaking(streamedObject);
        });

        speechEvents.on('stopped_speaking', function () {
          connection.onsilence(streamedObject);
        });

        speechEvents.on('volume_change', function (volume, threshold) {
          streamedObject.volume = volume;
          streamedObject.threshold = threshold;
          connection.onvolumechange(streamedObject);
        });
      },
      getAvatarSrc(avatar){
        if(typeof avatar === 'undefined' || avatar === null || avatar === ""){
          return '/static/media/defaultUser.png';
        }else{
          return '/static/media/avatar/' + avatar;
        }
      }
    },
    watch: {
      '$route' (to, from) {
        this.currentGroupName = this.$route.params.name;
        this.messages = [];

        if (this.socket != undefined) {
          this.socket.close();
          this.socketIsOpen = false;
        }

        if (this.currentGroupName != "") {

          this.socket = new WebSocket(this.$root.wssServer + "/ws/chat/" + this.$cookie.get('token') + "/" + this.currentGroupName);


          this.socket.onmessage = this.socketMessage;

          this.socket.onopen = this.socketOpen;

          this.socket.onerror = this.socketError;
        }
      }
    },
    filters: {
      hours: function (value) {
        //console.log(value);
        let parts = value.split('T');
        let date = parts[0];
        let time = parts[1];

        //console.log(date);
        //console.log(time);

        date = date.split('-');
        time = time.split(':');

        let hour;

        if (parseInt(time[0], 10) > 12) {
          hour = parseInt(time[0], 10) % 12;
        }
        else {
          hour = parseInt(time[0], 10);
        }

        hour = hour < 10 ? '0' + hour : hour;
        //return '[' + date[1] + '/' + date[2] + ' ' + hour + ':' + time[1] + ']';
        return hour + ':' + time[1];
      }
    },
    components: {
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


  .chatBar{
    position: relative;
    width: 95%;
    margin-left: auto;
    margin-right: auto;
  }

  .inputChat  {
    padding: 0 50px 0 50px;
    height: auto;
    max-height: none;
    min-height: 41px;

    overflow: auto;
    margin: 0;
    width: 100%;
    border: 2px solid #E0E0E0;
    border-radius: .375rem;
    outline: 0;
    background: #fff;
    resize: none;
    box-shadow: none;
    color: #3D3C40;
    font-size: .9375rem;
    line-height: 1.2rem;
    -webkit-user-select: auto;
    -moz-user-select: auto;
    -ms-user-select: auto;
    user-select: auto;

    box-sizing: border-box;
    position: relative;
  }

  .emo_menu{
    position: absolute;
    z-index: 1;
    right: 5px;
    top: 0;
    width: 36px;
    height: 42px;
    line-height: 42px;
    text-align: center;
    color: rgba(0,0,0,.35);
    opacity: 1;
  }

  .chatOptions {
    position: absolute;
    bottom: 0;
    top: 0;
    left: 0;
    width: 44px;
    padding: 0;
    border: 2px solid #E0E0E0;
    background: #FFF;
    color: rgba(0,0,0,.35);
    line-height: 42px;
    text-shadow: none;
    text-align: center;
    -webkit-transition: background 50ms,color 50ms;
    -moz-transition: background 50ms,color 50ms;
    transition: background 50ms,color 50ms;
    border-radius: 6px 0 0 6px;


    -webkit-font-smoothing: antialiased;
    font-family: Slack-Lato,appleLogo,sans-serif;
    background: 0 0;
    -webkit-appearance: none;
    -moz-appearance: none;
    font-size: inherit;
    font-weight: inherit;
    outline: 0;
  }

  .listActions{
    padding-left: 0;
    cursor: pointer;
  }

  .listActions li {
    display: block;
    color: #000;
    text-decoration: none;
    text-align: left;
  }

  .listActions li:hover {
    background-color: #555;
    color: white;
  }

  .dropdown-menu>li>label {
    display: block;
    padding: 10px 20px;
    clear: both;
    font-weight: normal;
    line-height: 1.428571429;
    color: #333;
    white-space: nowrap;
    cursor: pointer;
  }

  .dropdown-menu>li>a {
    padding: 10px 20px;
  }

  li label:hover:not(.active) {
    background-color: #555;
    color: white;
  }

  #containVideoChat {
    float: left;
    height: calc(100% - 60px);
    position: relative;
  }

  .containVideoChatFullScreen {
    width: 100%;
  }

  .containVideoChatMinimise {
    width: 40%;
  }

  .btnResize {
    position: absolute;
    width: 40px;
    height: 40px;
    top: 10px;
    left: 15px;
    font-size: 30px;
    z-index: 100;
  }

  .containerScroll {
    height: calc(100% - 60px);
    overflow-y: scroll;
    overflow-x: hidden;
  }

  #containerChat {
    height: calc(100% - 60px);
    position: relative;
  }

  .containerChatCallMinimise {
    float: right;
    width: 60%;
  }

  .containerMessage {
    text-align: left;
    display: block;
    margin-left: 20px;
    position: relative;
  }

  .pictureUser {
    padding-top: 0.25rem;
    width: 4.5rem;
    padding-right: .625rem;
    position: absolute;
    top: 0;
    left: 0;
  }

  .pictureUser img {
    border-radius: 5px;
    width: 2.25rem;
    height: 2.25rem;
  }

  .messageContent {
    margin-left: 3.5rem;
  }

  .messageTime {
    color: #9e9ea6;
    font-size: .75rem;
    white-space: nowrap;
    margin-right: .25rem;
    opacity: 1;
    display: inline;
  }

  .messageUserName {
  }

  .messageUserName p {
    font-size: .9375rem;
    font-weight: 900;
    color: #2C2D30;
    line-height: 1.125rem;
    display: inline;
    user-select: text;
    word-wrap: break-word;
  }

  .messageText {
    padding-right: 15px;
  }

  .messageText p {
    color: #2C2D30;
    font-size: .9375rem;
    line-height: 1.375rem;
    -webkit-user-select: text;
    -moz-user-select: text;
    -ms-user-select: text;
    user-select: text;
    word-wrap: break-word;
  }

  /*////// icons CSS start ////////////////////////*/

  #icons {
    bottom: 0;
    position: absolute;
  }

  circle {
    fill: #666;
    fill-opacity: 0.6;
  }

  svg.on circle {
    fill-opacity: 0;
  }

  /* on icons are hidden by default */
  path.on {
    display: none;
  }

  /* off icons are displayed by default */
  path.off {
    display: block;
  }

  /* on icons are displayed when parent svg has class 'on' */
  svg.on path.on {
    display: block;
  }

  /* off icons are hidden when parent svg has class 'on' */
  svg.on path.off {
    display: none;
  }

  svg {
    box-shadow: 2px 2px 24px #444;
    border-radius: 48px;
    margin: 0 10px 3vh 0;
    transform: translateX(calc(-6vw - 96px));
    transition: all .1s;
    transition-timing-function: ease-in-out;
  }

  svg:hover {
    box-shadow: 4px 4px 48px #666;
  }

  #icons.active svg {
    transform: translateX(0);
  }

  #mute-audio {
    transition: 40ms;
  }

  #mute-audio:hover,
  #mute-audio.on {
    background: #407cf7;
  }

  #mute-audio:hover circle {
    fill: #407cf7;
  }

  #mute-video {
    transition: 120ms;
  }

  #mute-video:hover,
  #mute-video.on {
    background: #407cf7;
  }

  #mute-video:hover circle {
    fill: #407cf7;
  }

  #switch-video {
    transition: 200ms;
  }

  #switch-video:hover {
    background: #407cf7;
  }

  #switch-video:hover circle {
    fill: #407cf7;
  }

  #fullscreen {
    transition: 280ms;
  }

  #fullscreen:hover,
  #fullscreen.on {
    background: #407cf7;
  }

  #fullscreen:hover circle {
    fill: #407cf7;
  }

  #hangup {
    transition: 360ms;
  }

  #hangup:hover {
    background: #dd2c00;
  }

  #hangup:hover circle {
    fill: #dd2c00;
  }

  /*////// icons CSS end /////////////////////////*/

</style>
