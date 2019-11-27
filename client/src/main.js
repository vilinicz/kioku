import Vue from 'vue';
import axios from 'axios';
import VueAxios from 'vue-axios';

import App from './App.vue';
import './registerServiceWorker';
import router from './router';
import store from './store';

import './assets/reset.scss';

Vue.config.productionTip = false;

Vue.use(VueAxios, axios);

Vue.axios.defaults.baseURL = process.env.VUE_APP_BASE_URL;


new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app');
