<template xmlns:v-on="http://www.w3.org/1999/xhtml">
  <div id="testRoomCall">
    <button id="btn-open-room" v-on:click="openRoom()">Open Room</button>
    <button id="btn-join-room" v-on:click="joinRoom()">Join Room</button><hr>
  </div>
</template>

<script>
export default{
    name:"TestRoomCall",
    data(){
        return{
          predefinedRoomId: "defaultRoom",
          connection: null
        }
    },
    created: function(){},
    mounted: function(){
      let self = this;
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
          document.body.appendChild( event.mediaElement );
      };
    },
    methods: {
      openRoom: function(){
        this.connection.open( this.predefinedRoomId );
      },
      joinRoom: function(){
        this.connection.join( this.predefinedRoomId );
      }
    },
    components:{}
}

</script>

<style scoped>
</style>
