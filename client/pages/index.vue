<template>
    <div id="app">
        <div class="error">
            {{ error }}
        </div>
        <transition-group
                name="card"
                tag="div"
        >
            <div
                    v-for="face in faces"
                    :key="face.id"
                    class="card"
            >
                <div
                        class="image"
                        :style="{backgroundImage:`url(data:image/jpeg;base64,${face.image})`}"
                />

                <div class="summary">
                    <input
                            type="text"
                            class="name"
                            :value="face.name"
                            @input="value = $event.target.value"
                            @change="update(face)"
                    >
                    <h3>{{ face.datetime }}</h3>
                </div>
            </div>
        </transition-group>
    </div>
</template>

<script>

  export default {
    data() {
      return {
        polling: null,
        faces: [],
        error: '',
      };
    },

    beforeDestroy() {
      clearInterval(this.polling);
    },

    created() {
      this.pollData();
    },

    methods: {
      pollData() {
        this.polling = setInterval(() => {
          this.get()
        }, 1000);
      },

      update() {
        //  console.log(face);
      },

      async get() {
        const res = await this.$axios.get('/current_face/1')
        const newFace = res.data;

        if (newFace.id) {
          newFace.datetime = Date.now();

          if (this.faces.length === 5) {
            this.faces.pop();
          }

          const oldFace = this.faces.find(f => f.id === newFace.id);

          if (oldFace) {
            oldFace.datetime = Date.now();
          } else {
            this.faces.unshift(newFace);
          }
        }
      }
    },
  };

</script>
<style lang="scss">
    #app {
        color: #2c3e50;
        line-height: 1.6;
        padding: 1rem 2rem;
    }

    .card {
        padding: 2rem 0rem 0;
        display: flex;
        flex-flow: row nowrap;
        height: calc(100vh / 3);
        min-height: 300px;
        transition: all 0.5s ease-in-out;

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
        }
    }

    .card-enter, .card-leave-to
        /* .card-leave-active for <2.1.8 */
    {
        opacity: 0;
        transform: scale(0);
    }

    .card-enter-to {
        opacity: 1;
        transform: scale(1);
    }
</style>
