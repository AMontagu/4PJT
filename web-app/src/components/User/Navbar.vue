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
      <h3>Contacts</h3>
      <ul class="leftNavbar">
        <li v-for="contact in qwirkUser.contacts" v-on:click="changeGroupName(contact.qwirkGroup.name)">
          <a>{{ contact.qwirkUser.user.username }}</a>
        </li>
      </ul>
    </div>
    <div class="chatKind">
      <h3>Groups</h3>
      <ul class="leftNavbar">
        <router-link v-for="group in qwirkUser.qwirkGroups" tag="li" :to="group.name | groupPath">
          <a>{{ group.name }}</a>
        </router-link>
      </ul>
    </div>
  </div>
</template>

<script>
export default{
    name:"UserNavbar",
    props: ['qwirkUser', 'currentGroupName'],
    data(){
        return{
          groups: ["test", "test2", "test", "test2", "test", "test2"],
          searchBarText: ""
        }
    },
    created: function(){},
    mounted: function(){},
    methods: {
      addContact: function(){
        self = this;
        let username = self.searchBarText;
        console.log("token " + self.$cookie.get('token'));
        self.$http.post('http://localhost:8000/addcontact/', {'username': username}, {headers: {'Authorization': "Token " + self.$cookie.get('token')}}).then(function(response){
          console.log("sucess add contact", response);
          self.currentGroupName = response.body;
        }, function(err){
          console.log("error :", err);
        });
      },
      changeGroupName: function(groupName){
        console.log(groupName);
        this.currentGroupName = groupName;
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
