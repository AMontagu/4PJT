<template>
  <div id="videoCall">
    <div id="localGif" v-if="isLocalGifActive">
      <img id="waitOperatorgif" src="/static/images/giphy.gif">
      <p id="waitOperatorText">Please wait while we are calling an operator</p>
    </div>
    <div id="videos">
      <video id="miniVideo" autoplay muted v-bind:class="{ active: isMiniVideoActive }"></video>
      <video id="remoteVideo" autoplay v-bind:class="{ active: isRemoteVideoActive }"></video>
    </div>

    <div id="icons" class="active">

      <svg v-on:click="muteAudio()" v-bind:class="{ on: !isAudioEnable }" id="mute-audio" xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewbox="-10 -10 68 68">
        <title>title</title>
        <circle cx="24" cy="24" r="34">
          <title>Mute audio</title>
        </circle>
        <path class="on" transform="scale(0.6), translate(17,18)" d="M38 22h-3.4c0 1.49-.31 2.87-.87 4.1l2.46 2.46C37.33 26.61 38 24.38 38 22zm-8.03.33c0-.11.03-.22.03-.33V10c0-3.32-2.69-6-6-6s-6 2.68-6 6v.37l11.97 11.96zM8.55 6L6 8.55l12.02 12.02v1.44c0 3.31 2.67 6 5.98 6 .45 0 .88-.06 1.3-.15l3.32 3.32c-1.43.66-3 1.03-4.62 1.03-5.52 0-10.6-4.2-10.6-10.2H10c0 6.83 5.44 12.47 12 13.44V42h4v-6.56c1.81-.27 3.53-.9 5.08-1.81L39.45 42 42 39.46 8.55 6z" fill="white"/>
        <path class="off" transform="scale(0.6), translate(17,18)"  d="M24 28c3.31 0 5.98-2.69 5.98-6L30 10c0-3.32-2.68-6-6-6-3.31 0-6 2.68-6 6v12c0 3.31 2.69 6 6 6zm10.6-6c0 6-5.07 10.2-10.6 10.2-5.52 0-10.6-4.2-10.6-10.2H10c0 6.83 5.44 12.47 12 13.44V42h4v-6.56c6.56-.97 12-6.61 12-13.44h-3.4z"  fill="white"/>
      </svg>

      <svg v-on:click="muteVideo()" v-bind:class="{ on: !isVideoEnable }" id="mute-video" xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewbox="-10 -10 68 68">
        <circle cx="24" cy="24" r="34">
          <title>Mute video</title>
        </circle>
        <path class="on" transform="scale(0.6), translate(17,16)" d="M40 8H15.64l8 8H28v4.36l1.13 1.13L36 16v12.36l7.97 7.97L44 36V12c0-2.21-1.79-4-4-4zM4.55 2L2 4.55l4.01 4.01C4.81 9.24 4 10.52 4 12v24c0 2.21 1.79 4 4 4h29.45l4 4L44 41.46 4.55 2zM12 16h1.45L28 30.55V32H12V16z" fill="white"/>
        <path class="off" transform="scale(0.6), translate(17,16)" d="M40 8H8c-2.21 0-4 1.79-4 4v24c0 2.21 1.79 4 4 4h32c2.21 0 4-1.79 4-4V12c0-2.21-1.79-4-4-4zm-4 24l-8-6.4V32H12V16h16v6.4l8-6.4v16z" fill="white"/>
      </svg>

      <svg id="hangup" v-on:click="hangup()" xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewbox="-10 -10 68 68">
        <circle cx="24" cy="24" r="34">
          <title>Hangup</title>
        </circle>
        <path transform="scale(0.7), translate(11,10)" d="M24 18c-3.21 0-6.3.5-9.2 1.44v6.21c0 .79-.46 1.47-1.12 1.8-1.95.98-3.74 2.23-5.33 3.7-.36.35-.85.57-1.4.57-.55 0-1.05-.22-1.41-.59L.59 26.18c-.37-.37-.59-.87-.59-1.42 0-.55.22-1.05.59-1.42C6.68 17.55 14.93 14 24 14s17.32 3.55 23.41 9.34c.37.36.59.87.59 1.42 0 .55-.22 1.05-.59 1.41l-4.95 4.95c-.36.36-.86.59-1.41.59-.54 0-1.04-.22-1.4-.57-1.59-1.47-3.38-2.72-5.33-3.7-.66-.33-1.12-1.01-1.12-1.8v-6.21C30.3 18.5 27.21 18 24 18z" fill="white"/>
      </svg>

    </div>
  </div>
</template>
<script>
export default{
  data () {
    name: "VideoCall",
    props: ['answer'],
    return {
      isMiniVideoActive: true,
      isRemoteVideoActive: false,
      isLocalGifActive: true,
      isAudioEnable: true,
      isVideoEnable: true,
      inCall: false,
      peer: null
    }
  },
  mounted: function () {
    var remoteVideo = document.getElementById("remoteVideo");
    var localGif = document.getElementById("localGif");
    var miniVideo = document.getElementById("miniVideo");

    var self = this;

    console.log("is this an answer ? ", this.answer);

    self.peer = new Peer({host: this.$root.serverRtcIp, port: this.$root.serverRtcPort, path: 'peerjs', key: 'peerjs', debug: 10});

    this.hease.setCallbackPeerCall(function (call) {
      console.log("in callback call");

      component.inCall = true;
      call.answer(component.hease.localStream);

      component.isMiniVideoActive = true;
      component.isRemoteVideoActive = true;
      component.isLocalGifActive = false;

      call.on('stream', function (remotestream) {
        console.log("in call on stream");

        if(remotestream.getAudioTracks().length)// checking audio presence
          console.log("have audio");

        if(remotestream.getVideoTracks().length)// checking video presence
          console.log("have video");

        console.log(component.isRemoteVideoActive);
        console.log(component.isLocalGifActive);

        remoteVideo.src = URL.createObjectURL(remotestream);
        remoteVideo.play();
      });
      call.on('error', function (err) {
        console.log("error peer js : " + err.message);
      });
      call.on('close', function () {
        console.log("peer close call");
        component.isMiniVideoActive = false;
        component.isRemoteVideoActive = false;

        miniVideo.src = "";
        remoteVideo.src = "";

        // TODO display message : operator close connection recall or go to home page

        component.isAudioEnable = true;
        component.isVideoEnable = true;

        router.push({ path: '/'});
      });
    });

    this.hease.prepareCall("operator");

    // TODO Check if we can call + launch call

    //this.hease.notify.sendNotifification("we prepare a call with " + this.hease.robotInfos.robotName);

    //this.hease.notify.callOperator();
  },
  methods:{
    muteAudio: function() {
      this.isAudioEnable = this.hease.muteAudio();
    },

    muteVideo: function() {
      this.isVideoEnable = this.hease.muteVideo();
    },

    hangup: function() {
      this.hease.hangUp();
      this.inCall = false;
    }
  },
  beforeDestroy: function () {
    console.log("before destroy Telepresence");
    this.isMiniVideoActive = false;
    //this.miniVideo.src = "";
    if (this.inCall) {
      this.isMiniVideoActive = false;
      this.isRemoteVideoActive = false;
      //this.miniVideo.src = "";
      //this.remoteVideo.src = "";

      this.hease.hangUp();

    }else{
      this.hease.cleanPeerClose();
    }
  },
    }
</script>

<style scoped>
.hidden {
    display: none;
}

a {
    color: #4285F4;
    text-decoration: none;
}

a:hover {
    color: #3B78E7;
    text-decoration: underline;
}

#room-link {
    position: absolute;
    top: 20px;
    max-width: 10%;
    left: 6vw;
}

#room-link p {
    text-align: center;
    color: white;
}

body {
    background-color: #333;
    font-family: 'Roboto', 'Open Sans', 'Lucida Grande', sans-serif;
    height: 100%;
    margin: 0;
    padding: 0;
    width: 100%;
    color: #fff;
}

#remote-canvas {
    display: none;
    height: 100%;
    margin: 0 auto;
    width: 100%;
}

div.warning {
    background-color: #a80202;
    color: black;
    font-weight: 400;
    opacity: .9;
}

#container {
    height: 100%;
    position: absolute;
}

#info-div {
    z-index: 3;
}

#room-link {
    margin: 0 0 29px 0;
}

#status {
    z-index: 4;
}


#videos {
    font-size: 0; /* to fix whitespace/scrollbars problem */
    margin-top: 15px;
    height: 85%;
    pointer-events: none;
    position: absolute;
    transition: all 1s;
    left: 0;
    right: 0;
}

#videos.active {
    -moz-transform: rotateY(180deg);
    -ms-transform: rotateY(180deg);
    -o-transform: rotateY(180deg);
    -webkit-transform: rotateY(180deg);
    transform: rotateY(180deg);
}

html {
    height: 100%;
    margin: 0;
    width: 100%;
}

label {
    margin: 0 10px 0 0;
}

#miniVideo {
    border: 1px solid gray;
    bottom: 20px;
    right: 20px;
    width: 17%;
    position: absolute;
    opacity: 0;
    transition: opacity 1s;
}

#miniVideo.active {
    opacity: 1;
    z-index: 2;
}

#remoteVideo {
    display: block;
    height: 100%;
    max-height: 100%;
    max-width: 100%;
    object-fit: cover;  /* no letterboxing */
    opacity: 0;
    position: absolute;
    -moz-transform: rotateY(180deg);
    -ms-transform: rotateY(180deg);
    -o-transform: rotateY(180deg);
    -webkit-transform: rotateY(180deg);
    transform: rotateY(180deg);
    transition: opacity 1s;
    right: 0;
    left: 0;
    margin-right: auto;
    margin-left: auto;
}

#remoteVideo.active {
    opacity: 1;
    z-index: 1;
}

button {
    background-color: #4285F4;
    border: none;
    border-radius: 2px;
    color: white;
    font-size: 0.8em;
    margin: 0 5px 20px 5px;
    width: 8em;
    height: 2.75em;
    padding: 0.5em 0.7em 0.5em 0.7em;
    -webkit-box-shadow: 1px 1px 5px 0 rgba(0,0,0,.5);
    -moz-box-shadow: 1px 1px 5px 0 rgba(0,0,0,.5);
    box-shadow: 1px 1px 5px 0 rgba(0,0,0,.5);
}

button:active {
    background-color: #3367D6;
}

button:hover {
    background-color: #3B78E7;
}

button:focus {
    outline: none;
    -webkit-box-shadow: 0 10px 15px 0 rgba(0,0,0,.5);
    -moz-box-shadow: 0 10px 15px 0 rgba(0,0,0,.5);
    box-shadow: 0 10px 15px 0 rgba(0,0,0,.5);
}

button[disabled] {
    color: rgb(76, 76, 76);
    color: rgba(255, 255, 255, 0.3);
    background-color: rgb(30, 30, 30);
    background-color: rgba(255, 255, 255, 0.12);
}

input[type=text] {
    border: none;
    border-bottom: solid 1px #4c4c4f;
    font-size: 1em;
    background-color: transparent;
    color: #fff;
    padding:.4em 0;
    margin-right: 20px;
    width: 100%;
    display: block;
}

input[type="text"]:focus {
    border-bottom: solid 2px #4285F4;
    outline: none;
}

input[type="text"].invalid {
    border-bottom: solid 2px #F44336;
}

label.error-label {
    color: #F44336;
    font-size: .85em;
    font-weight: 200;
    margin: 0;
}

#room-id-input-div {
    margin: 15px;
}

#room-id-input-buttons {
    margin: 15px;
}

h1 {
    font-weight: 300;
    margin: 0 0 0.8em 0;
    padding: 0 0 0.2em 0;
}

div#room-selection {
    margin: 3em auto 0 auto;
    width: 25em;
    padding: 1em 1.5em 1.3em 1.5em;
}

p {
    color: #eee;
    font-weight: 300;
    line-height: 1.6em;
}

/*////// room selection end /////////////////////*/

/*////// icons CSS start ////////////////////////*/

#icons {
    bottom: 77px;
    left: 6vw;
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
    display: block;
    margin: 0 0 3vh 0;
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

#localGif{
  margin: auto;
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  width: 500px;
  height: 300px;
  text-align: center;
}

/*////// icons CSS end /////////////////////////*/

</style>
