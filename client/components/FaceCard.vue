<template>
  <div class="face-card">
    <div class="wrapper">
      <div
        :style="{backgroundImage:`url(data:image/jpeg;base64,${image})`}"
        class="image"
      >
        <div :class="{on: online}" class="status" />
      </div>

      <div class="summary">
        <div class="wrap">
          <input
            v-model.lazy="editableName"
            v-debounce="delay"
            placeholder="Имя"
            type="text"
            class="input input-name"
          >
          <input
            v-model.lazy="editableRoom"
            v-debounce="delay"
            placeholder="#"
            type="number"
            min="0"
            inputmode="numeric"
            pattern="[0-9]*"
            class="input input-room"
          >
        </div>
        <textarea
          v-model.lazy="editableNote"
          v-debounce="delay"
          rows="4"
          placeholder="Дополнительно"
          type="text"
          class="input input-note"
        />
      </div>
    </div>
  </div>
</template>

<script>
import debounce from 'v-debounce'
export default {
  name: 'FaceCard',

  directives: {
    debounce
  },

  props: {
    id: {
      type: Number,
      default: 0
    },
    name: {
      type: String,
      default: ''
    },
    room: {
      type: Number,
      default: undefined
    },
    note: {
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
      editableName: this.name,
      editableRoom: this.room,
      editableNote: this.note,

      refreshing: null,
      online: true,
      delay: 400
    }
  },

  watch: {
    editableName () {
      this.update()
    },
    editableRoom () {
      this.update()
    },
    editableNote () {
      this.update()
    }
  },

  beforeDestroy () {
    clearInterval(this.refreshing)
  },

  created () {
    this.refresh()
  },

  methods: {
    async update () {
      const payload = {
        name: this.editableName,
        room: this.editableRoom,
        note: this.editableNote
      }
      await this.$axios.patch(`faces/${this.id}`, payload)
    },

    refresh () {
      this.refreshing = setInterval(() => {
        this.online = ((Date.now() - this.datetime) / 1000) < 3
        if (((Date.now() - this.datetime) / 1000) > 180) {
          this.$emit('destroy', this.id)
        }
      }, 1000)
    }
  }
}
</script>

<style scoped lang="scss">
$padding-sm: 1rem;
$padding-md: 2rem;

.face-card {
  padding: $padding-sm;
  display: flex;
  flex-flow: column;
  justify-content: center;
  // height: calc(100vh / 3);
  // min-height: 300px;
  transition: all 0.4s ease, background-color 1.5s ease-in-out;

  &:not(:last-child) {
    border-bottom: 1px solid $gray-lightest;
  }

  .wrapper {
    display: flex;
    flex-flow: row nowrap;
  }

  .image {
    position: relative;
    border-radius: 16px;
    width: 28vw;
    height: 28vw;
    max-width: 230px;
    max-height: 230px;
    min-width: 100px;
    min-height: 100px;
    margin-right: $padding-sm;
    background-color: $gray-silver;
    background-repeat: no-repeat;
    background-size: cover;
    background-position: center;
    flex-shrink: 0;
    box-shadow: inset 0 0 10px rgba(#000, 0.2);

    .status {
      position: absolute;
      top: -8px;
      right: -8px;
      width: 26px;
      height: 26px;
      box-shadow: 0 0 0 4px #fff;
      border-radius: 13px;
      background-color: $gray-light;

      &.on {
        background-color: $success;
      }
    }

    @media(min-width: 768px) {
      margin-right: $padding-md;
    }
  }

  .wrap {
    display: flex;
    flex-flow: row nowrap;

    .input-name {
      margin-right: $padding-sm;
      flex-basis: 75%;
    }

    .input-room {
      flex-basis: 25%;
      text-align: right;
      font-weight: 500;
    }
  }

  .input {
    font-size: 1.4rem;
    width: 100%;
    color: #2c3e50;
    background-color: $gray-silver;
    margin-bottom: $padding-sm;
    padding: 0.25rem 0.5rem;
    border-radius: 8px;
    @media (min-width: 768px) {
      font-size: 2.2rem;
      padding: 0.25rem 1rem;
    }
  }

  .input-note {
    font-size: 1.2rem;
    resize: none;
    margin-bottom: 0;
    display: block;
    @media (min-width: 768px) {
      font-size: 1.75rem;
    }
  }

  @media(min-width: 768px) {
    padding: $padding-md;
  }
}
</style>
