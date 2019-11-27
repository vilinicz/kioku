<template>
  <div id="app">
    <template v-if="face.hasOwnProperty('id')">
      <h1>{{face.name}}</h1>
      <img v-bind:src="'data:image/jpeg;base64,'+ face.image"/>
    </template>
  </div>
</template>

<script>
export default {
  data() {
    return {
      face: {},
      polling: null,
    };
  },

  methods: {
    pollData() {
      this.polling = setInterval(() => {
        this.$http.get('/current_face/1')
          .then((res) => {
            this.face = res.data.id === this.face.id ? this.face : res.data;
          });
      }, 1000);
    },
  },

  beforeDestroy() {
    clearInterval(this.polling);
  },

  created() {
    this.pollData();
  },
};

</script>
<style lang="scss">
  #app {
    color: #2c3e50;
  }
</style>
