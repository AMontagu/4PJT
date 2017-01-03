<template>
  <div id="UserHome" v-if="isConnected">
    <userNavbar></userNavbar>
    <div id="content">
      <userHeader></userHeader>
      <transition name="fade" mode="out-in">
        <router-view class="view"></router-view>
      </transition>
    </div>
  </div>
</template>

<script>
import UserNavbar from './Navbar.vue'
import UserHeader from './Header.vue'

export default{
    name:"UserHome",
    data(){
        return{
          isConnected: false
        }
    },
    created: function(){
      this.checkIfUserLoggedIn();
    },
    mounted: function(){},
    methods:{
      checkIfUserLoggedIn: function(){
        //TODO look into cookies
        let self = this;
        this.$http.get('http://localhost:8000/isloggedin/', {headers: {'Authorization': "Token " + this.$cookie.get('token')}}).then(function(response){
            console.log("sucess request", response);
            if(response.body == "True"){
              console.log("user is logged in");
              self.isConnected = true;
            }else{
              console.log("user is NOT logged in");
              this.$router.push('/');
            }
          }, function(err){
            console.log("error :", err);
        });
      }
    },
    components:{
      UserNavbar,
      UserHeader
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
      width:100%;
      height:100%;
      margin: 0px;
      padding: 0px;
  }

  #UserHeader {
      height:10%;
      background-color:#930;
      width:100%;
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

  #UserChat{
    width:100%;
    overflow: auto;
    height: 90%;
  }

  #content {
      width:80%;
      height:100%;
      background-color:#363;
      float:left;
  }
</style>
