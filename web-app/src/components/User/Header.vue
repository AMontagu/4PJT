<template xmlns:v-on="http://www.w3.org/1999/xhtml">
  <div id="UserHeader">
    <div v-if="isReady">
      <div class="leftHeader">
        <h4>{{groupInformations.titleGroupName}}</h4>
        <div v-if="groupInformations.isContactGroup">
          <span :class="getConnectionColor(groupInformations.qwirkUsers[0].status)"></span> <p class="statusText">{{groupInformations.qwirkUsers[0].status}}</p>
        </div>
        <div v-else>
          <button type="button" id="showGroupusersInformations"><span class="glyphicon glyphicon-user" aria-hidden="true"></span> {{usersNumber}}</button>
        </div>
      </div>
      <div class="rightHeader">
      </div>
    </div>
  </div>
</template>

<script>
export default{
    name:"UserHeader",
    data(){
        return{
          currentGroupName: "",
          titleGroupName: "",
          groupInformations: {},
          isReady: false
        }
    },
    created: function(){
    },
    mounted: function(){
      this.currentGroupName = this.$route.params.name;

      this.getGroupInformations();
    },
    methods: {
      getGroupInformations: function(){
        let self = this;
        if(self.currentGroupName != "" && self.currentGroupName != undefined){
          self.$http.post('http://localhost:8000/groupinformations/', {groupname: self.currentGroupName}, {headers: {'Authorization': "Token " + this.$cookie.get('token')}}).then(function(response){
            console.log("sucess request groupinformations", response);
            self.groupInformations = JSON.parse(response.body);
            console.log(self.groupInformations);
            console.log(self.groupInformations.qwirkUsers);
            self.isReady = true;
          })
        }
      },
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
        this.getGroupInformations();
      }
    },
    components:{}
}
</script>

<style scoped>
  .leftHeader{
    width: 50%;
    text-align: left;
    padding-left: 20px;
  }

  .rightHeader{
    width: 50%;
    text-align: right;
    padding-right: 20px;
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
</style>
