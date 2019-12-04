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
      faces: [],
      error: undefined
    }
  },

  beforeDestroy () {
    clearInterval(this.polling)
  },

  created () {
    this.pollData()
  },

  methods: {
    pollData () {
      this.polling = setInterval(() => {
        this.get()
      }, 1000)
    },

    async get () {
      let newFace = {}
      try {
        const res = await this.$axios.get('/current_face/1')
        newFace = res.data
        this.error = undefined
      } catch (e) {
        this.error = e
      }

      if (newFace.id) {
        newFace.datetime = Date.now()

        const oldFace = this.faces.find(f => f.id === newFace.id)

        if (oldFace) {
          oldFace.datetime = Date.now()
        } else {
          if (this.faces.length === 6) {
            this.faces.pop()
          }
          this.faces.unshift(newFace)
        }
      }

      // Clear too old faces
      this.faces = this.faces.filter(f => ((Date.now() - f.datetime) / 1000) < 5)
    }
  }
}

</script>
<style lang="scss">
#app {
  color: #2c3e50;
  line-height: 1.6;
  padding: 2vw 4vw;
  min-height: 100vh;
  background: linear-gradient(to bottom, #fff, #dcdcdc);

  input {
    color: #2c3e50;
  }
}

.error {
  background-color: rgba(orangered, 0.6);
  color: #fff;
  font-weight: bold;
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  text-align: center;
  padding: 0.5rem;
}

.cards-enter
  /* .card-leave-active for <2.1.8 */
{
  opacity: 0;
  transform: translateY(-30vh);
}

.cards-enter-to {
  opacity: 1;
  transform: none;
}

.cards-leave-to {
  opacity: 0;
}

.cards-leave-active {
  position: absolute;
}
</style>
