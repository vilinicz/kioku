<template>
  <div id="app">
    <div v-for="face in faces" :key="face.id">
      <h1>{{face.name}}</h1>
      <h3>{{face.datetime}}</h3>
      <img class="image" v-bind:src="'data:image/jpeg;base64,'+ face.image" alt="image"/>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      polling: null,
    };
  },

  methods: {
    pollData() {
      this.polling = setInterval(() => {
        this.$store.dispatch('get_current_face');
      }, 1000);
    },
  },

  computed: {
    faces() {
      return this.$store.state.faces;
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

  .image {
    width: 100px;
    height: 100px;
  }
</style>
