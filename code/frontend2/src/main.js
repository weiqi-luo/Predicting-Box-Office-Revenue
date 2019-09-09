import '@babel/polyfill'
import 'mutationobserver-shim'

import Vue from 'vue'
import './plugins/bootstrap-vue'
import App from './App.vue'
import router from './router'
//import axios from 'axios'
import getYouTubeID from 'get-youtube-id'
import VueYouTubeEmbed from 'vue-youtube-embed'

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')

Vue.mixin({
  methods: {
    capitalizeFirstLetter: str => str.charAt(0).toUpperCase() + str.slice(1),
    getYTID: function(URL){return getYouTubeID(URL, {fuzzy: true})}
  }
})

Vue.use(VueYouTubeEmbed)
