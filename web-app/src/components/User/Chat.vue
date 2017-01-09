<template xmlns:v-on="http://www.w3.org/1999/xhtml">
  <div id="UserChat">
    <p>User Chat with {{currentGroupName}}</p>

    <input class="inputChat" type="text" v-model="inputText" :disabled="!socketIsOpen" v-on:keyup.enter="sendText"/>
  </div>
</template>

<script>

export default{
    name:"UserChat",
    data(){
        return{
          socket: undefined,
          socketIsOpen: false,
          inputText: "",
          currentGroupName: ""
        }
    },
    created: function(){},
    mounted: function(){
      self = this;
      console.log(this.$route.params);
      self.currentGroupName = this.$route.params.name;
      if(self.currentGroupName != "" && self.currentGroupName != undefined){

          var wsProtocol = location.protocol === 'https:' ? 'wss://' : 'ws://';
          self.socket = new WebSocket(wsProtocol + "localhost:8000/ws/chat/" + self.$cookie.get('token') + "/" + self.currentGroupName);

          self.socket.onmessage = function (message) {
            console.log(message);
            //var data = JSON.parse(message.data);
            //console.log(data);
          }

          self.socket.onopen = function () {
            self.socketIsOpen = true;

            console.log("socket is open");
          };

          self.socket.onerror = function (err) {
            console.log("ERROR : ", err);
          };
        }
    },
    methods: {
      sendText: function(){
        console.log("send text: " + this.inputText)
        if(this.socket != undefined){
          this.socket.send(JSON.stringify({text: this.inputText}));
        }
      }
    },
    watch: {
      '$route' (to, from) {
        let self = this;
        self.currentGroupName = this.$route.params.name;

        if(this.socket != undefined){
          this.socket.close();
          this.socketIsOpen = false;
        }

        if(self.currentGroupName != ""){

          var wsProtocol = location.protocol === 'https:' ? 'wss://' : 'ws://';
          self.socket = new WebSocket(wsProtocol + "localhost:8000/ws/chat/" + self.$cookie.get('token') + "/" + self.currentGroupName);

          self.socket.onmessage = function (message) {
            console.log(message);
            //var data = JSON.parse(message.data);
            //console.log(data);
          }

          self.socket.onopen = function () {
            self.socketIsOpen = true;

            console.log("socket is open");
          };

          self.socket.onerror = function (err) {
            console.log("ERROR : ", err);
          };
        }
      }
    },
    components:{}
}

</script>

<style scoped>
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
  }
</style>
