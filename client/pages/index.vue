<template>
  <div id="app">
    <div v-if="error" class="error">
      {{ error }}
    </div>
    <transition-group
      name="cards"
      tag="div"
    >
      <FaceCard
        v-for="face in faces"
        :key="face.id"
        @destroy="removeOldFace"
        v-bind="face"
      />
    </transition-group>
  </div>
</template>

<script>
import FaceCard from '../components/FaceCard'

export default {
  components: {
    FaceCard
  },

  data () {
    return {
      polling: null,
      sorting: null,
      faces: [],
      error: undefined
    }
  },

  beforeDestroy () {
    clearInterval(this.polling)
    clearInterval(this.sorting)
  },

  created () {
    this.pollData()
    this.sortFaces()
  },

  methods: {
    removeOldFace (id) {
      this.faces = this.faces.filter(f => f.id !== id)
    },

    sortFaces () {
      this.polling = setInterval(() => {
        this.faces = this.faces.sort((a, b) => b.datetime - a.datetime)
      }, 2000)
    },

    pollData () {
      this.polling = setInterval(() => {
        this.get()
      }, 1000)
    },

    async get () {
      let newFaces = []
      try {
        const res = await this.$axios.get('/current_faces/1')
        newFaces = res.data
        this.error = undefined
      } catch (e) {
        this.error = e
      }

      for (const newFace of newFaces) {
        if (newFace.id) {
          newFace.datetime = Date.now()

          const oldFace = this.faces.find(f => f.id === newFace.id)

          if (oldFace) {
            if (((Date.now() - oldFace.datetime) / 1000) > 3) {
              oldFace.image = newFace.image
            }
            oldFace.datetime = Date.now()
          } else {
            if (this.faces.length === 8) {
              this.faces.pop()
            }
            this.faces.unshift(newFace)
          }
        }
      }
    }
  }
}

</script>
<style lang="scss">
#app {
  color: $gray-darkest;
  line-height: 1.6;
  // padding: 2vw 0;
  min-height: 100vh;
  font-family: "Avenir Next", sans-serif;
  // background: linear-gradient(to bottom, $gray-silver, $gray-lightest);

  input {
    color: $gray-darkest;
  }
}

.error {
  background-color: rgba($danger, 0.8);
  color: #fff;
  font-weight: bold;
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  text-align: center;
  padding: 0.75rem;
  z-index: 99;
}

.cards-enter {
  opacity: 0;
  transform: translateY(-30vh);
  background-color: $yellow-highlight;
  // transition: background-color 1s ease, translate 0.5s ease-in-out, opacity 0.5s ease;
}

.cards-enter-to {
  opacity: 1;
  transform: none;
  background-color: #fff;
}

.cards-leave-to {
  opacity: 0;
}

.cards-leave-active {
  position: absolute;
}
</style>
