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
          <div v-else>
            <p><span class="glyphicon glyphicon-user" aria-hidden="true"></span> {{usersNumber}}</p>
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
          <ul v-else class="dropdown-menu" style="left: -125px;">
            <li v-if="groupInformations.isAdmin"><a v-on:click="removeGroup()">Remove relationship</a></li>
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
  </div>
</template>

<script>
import Modal from '../shared/Modal.vue'

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
          this.$http.post(this.$root.server + 'addusertogroup/', {groupName: this.currentGroupName, username: this.usernameUser, isAdmin: this.adminUser}, {headers: {'Authorization': "Token " + this.$cookie.get('token')}}).then((response) => {
            console.log("sucess request add user to group/channels", response);
            let data = JSON.parse(response.body);
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

      },
      emitCallWebRTC: function(){
        this.$emit("callWebRTC");
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
        let self = this;
        self.currentGroupName = this.$route.params.name;
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
    overflow: hidden;
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
</style>
