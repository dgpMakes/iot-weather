<template>
  <h1 class="text-center my-3">
    Dispositivo <strong>{{ deviceName }}</strong>
  </h1>
</template>

<script>
export default {
  computed: {
    deviceName() {
      return this.$route.params.id;
    },
  },
};
</script>

<style>
</style>