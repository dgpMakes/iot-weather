<template>
  <div id="app">
    <nav class="navbar navbar-dark sticky-top bg-dark">
      <router-link to="/">
        <a class="navbar-brand mx-4"> UC3M - Operating systems</a>
      </router-link>
    </nav>
    <div class="container">
      <router-view></router-view>
    </div>
  </div>
</template>
<script>
export default {
  name: "app",
  components: {},
};
</script>
<style>
router-link a {
  text-decoration: none;
}
</style>