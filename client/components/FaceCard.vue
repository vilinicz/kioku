<template>
  <div class="face-card">
    <div
      :style="{backgroundImage:`url(data:image/jpeg;base64,${image})`}"
      class="image"
    />

    <div class="summary">
      <input
        v-model="fname"
        @change="update"
        placeholder="Укажите имя"
        type="text"
        class="input input-name"
      >
      <h3>{{ datetime }}</h3>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FaceCard',

  props: {
    id: {
      type: Number,
      default: 0
    },
    name: {
      type: String,
      default: ''
    },
    image: {
      type: String,
      default: ''
    },
    datetime: {
      type: Number,
      default: 0
    }

  },

  data () {
    return {
      fname: this.name
    }
  },

  methods: {
    async update () {
      await this.$axios.patch(`faces/${this.id}`, { name: this.fname })
    }
  }
}
</script>

<style scoped lang="scss">
.face-card {
  padding: 4vw 0 0;
  display: flex;
  flex-flow: row nowrap;
  height: calc(100vh / 3);
  min-height: 300px;
  transition: all 0.5s ease;

  &:not(:last-child) {
    border-bottom: 1px solid #f2f2f2;
  }

  .image {
    border-radius: 8px;
    width: 30vw;
    height: 30vw;
    max-width: 250px;
    max-height: 250px;
    min-width: 100px;
    min-height: 100px;
    margin-right: 2rem;
    background-repeat: no-repeat;
    background-size: cover;
    background-position: center;
    flex-shrink: 0;
  }

  .input {
    font-size: 3rem;
    width: 100%;
  }
}
</style>
