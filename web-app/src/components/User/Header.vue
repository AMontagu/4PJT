<template xmlns:v-on="http://www.w3.org/1999/xhtml">
  <div id="UserHeader">
    <button type="button" class="btn btn-action" v-on:click="logOut">Log Out</button>
  </div>
</template>

<script>
export default{
    name:"UserHeader",
    data(){
        return{}
    },
    created: function(){},
    mounted: function(){},
    methods: {
      logOut: function(){
        this.$cookie.delete('token');
        //console.log(this.$cookie.get('token'))
        this.$router.push('/');
      }
    },
    components:{}
}
</script>

<style scoped>
</style>
