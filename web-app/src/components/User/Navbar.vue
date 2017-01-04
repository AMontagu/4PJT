<template xmlns:v-on="http://www.w3.org/1999/xhtml">
  <div id="UserNavbar">
    <div id="userPart">
      <h3>{{ qwirkUser.user.username }}</h3>
    </div>
    <div id="searchPart">
      <input type="text" class="inputText inputSearch" placeholder="username" v-model="searchBarText"/>
      <button type="button" class="btn btn-action" v-on:click="addContact">Add</button>
    </div>
    <div class="chatKind">
      <h3>Groups</h3>
      <ul class="leftNavbar">
        <router-link v-for="group in groups" tag="li" :to="group | groupPath">
          <a>{{group}}</a>
        </router-link>
      </ul>
    </div>
    <div class="chatKind">
      <h3>Contacts</h3>
      <ul class="leftNavbar">
        <router-link v-for="contact in contacts" tag="li" :to="contact | contactPath">
          <a>{{ contact }}</a>
        </router-link>
      </ul>
    </div>

  </div>
</template>

<script>
export default{
    name:"UserNavbar",
    props: ['qwirkUser'],
    data(){
        return{
          groups: ["test", "test2", "test", "test2", "test", "test2"],
          contacts: ["test", "test2"],
          searchBarText: ""
        }
    },
    created: function(){},
    mounted: function(){},
    methods: {
      addContact: function(){
        let username = this.searchBarText;
        console.log("token " + this.$cookie.get('token'));
        this.$http.post('http://localhost:8000/addcontact/', {'username': username}, {headers: {'Authorization': "Token " + this.$cookie.get('token')}}).then(function(response){
          console.log("sucess add contact", response);
          this.$router.push('user/' + username);
        }, function(err){
          console.log("error :", err);
        });

      }
    },
    filters: {
      groupPath: function (name) {
        return '/user/' + name;
      },
      contactPath: function (name) {
        return '/user/' + name;
      }
    },
    watch: {
      searchBarText: function (name) {
        //console.log(name);
      }
    },
    components:{}
}

</script>

<style scoped>

  .chatKind{
    width:100%;

  }
  .leftNavbar {
    list-style-type: none;
    margin: 0;
    padding: 0;
    width: 100%;
    position: relative;
  }

  li a {
    display: block;
    color: #000;
    padding: 8px 16px;
    text-decoration: none;
  }

  li a.active {
    background-color: #4CAF50;
    color: white;
  }

  li a:hover:not(.active) {
    background-color: #555;
    color: white;
  }
</style>
