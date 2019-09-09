<template>
  <div id="app">
    <h1 style="color:black"> Box Office Guesstimator 3000 </h1>

<!--
    <router-link to="/">Home</router-link> |
    <router-link to="/api_example">API example</router-link>
    <br>
    <br>
  -->
    <router-view/>

  </div>
</template>



<script>
//import '@/assets/theme.css';
import '@/assets/bootstrap.css';

export default{
  name:'app',
  components:{

  }
}
</script>



<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  margin-top: 60px;
  margin-left: 10%;
  margin-right: 10%;
  margin-bottom: 60px;

}

</style>
