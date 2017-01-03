<template>
  <div id="UserChat">
    <p>User Chat with {{chatName}}</p>
    <p>User Chat with {{chatName}}</p>
    <p>User Chat with {{chatName}}</p>
    <p>User Chat with {{chatName}}</p>
    <p>User Chat with {{chatName}}</p>
    <p>User Chat with {{chatName}}</p>
    <p>User Chat with {{chatName}}</p>
    <p>User Chat with {{chatName}}</p>
    <p>User Chat with {{chatName}}</p>
    <p>User Chat with {{chatName}}</p>
    <p>User Chat with {{chatName}}</p>
    <p>User Chat with {{chatName}}</p>
    <p>User Chat with {{chatName}}</p>
    <p>User Chat with {{chatName}}</p>
    <p>User Chat with {{chatName}}</p>
    <p>User Chat with {{chatName}}</p>
    <p>User Chat with {{chatName}}</p>
    <p>User Chat with {{chatName}}</p>
    <p>User Chat with {{chatName}}</p>
    <p>User Chat with {{chatName}}</p>
    <p>User Chat with {{chatName}}</p>
    <p>User Chat with {{chatName}}</p>
    <p>User Chat with {{chatName}}</p>
    <p>User Chat with {{chatName}}</p>
  </div>
</template>

<script>
export default{
    name:"UserChat",
    data(){
        return{
          chatName: ""
        }
    },
    created: function(){},
    mounted: function(){
      console.log(this.$route.params);
      this.chatName = this.$route.params.name;
    },
    methods: {},
    watch: {
      '$route' (to, from) {
        this.chatName = this.$route.params.name;
      }
    },
    components:{}
}

</script>

<style scoped>
</style>
