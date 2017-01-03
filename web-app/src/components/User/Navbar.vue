<template>
  <div id="UserNavbar">
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
    data(){
        return{
          groups: ["test", "test2", "test", "test2", "test", "test2"],
          contacts: ["test", "test2"]
        }
    },
    created: function(){},
    mounted: function(){},
    methods: {},
    filters: {
      groupPath: function (name) {
        return '/user/' + name;
      },
      contactPath: function (name) {
        return '/user/' + name;
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
