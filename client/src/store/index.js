import Vue from 'vue';
import Vuex from 'vuex';
import Axios from 'axios';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    faces: [],
  },
  mutations: {
    add_face(state, face) {
      state.faces.unshift(face);
    },

    remove_face(state) {
      state.faces.pop();
    },

    update_face(state, face) {
      const of = state.faces.find(f => f.id === face.id);
      of.datetime = Date.now();
    },
  },
  actions: {
    async get_current_face(ctx) {
      const res = await Axios.get('/current_face/1');
      const newFace = res.data;

      if (!newFace.id) {
        return;
      }

      newFace.datetime = Date.now();
      if (ctx.state.faces.length === 5) {
        ctx.commit('remove_face');
      }

      const oldFace = ctx.state.faces.find(f => f.id === newFace.id);
      if (oldFace) {
        console.log(oldFace);
        ctx.commit('update_face', oldFace);
      } else {
        ctx.commit('add_face', newFace);
      }
    },
  },
});
