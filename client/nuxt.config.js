const development = process.env.NODE_ENV !== 'production'

export default {
  ssr: false,
  /*
  ** Headers of the page
  */
  head: {
    title: process.env.npm_package_name || '',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { name: 'apple-mobile-web-app-status-bar-style', content: 'default' },
      {
        hid: 'description',
        name: 'description',
        content: process.env.npm_package_description || ''
      }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },
  /*
  ** Customize the progress-bar color
  */
  loading: false,
  /*
  ** Global CSS
  */
  css: [
    '~/assets/reset.scss'
  ],

  styleResources: {
    scss: [
      '~/assets/vars.scss'
    ]
  },
  /*
  ** Plugins to load before mounting the App
  */
  plugins: [],
  /*
  ** Nuxt.js dev-modules
  */
  buildModules: [
    // Doc: https://github.com/nuxt-community/eslint-module
    '@nuxtjs/eslint-module',
    '@nuxtjs/dotenv'
  ],
  /*
  ** Nuxt.js modules
  */
  modules: [
    // Doc: https://axios.nuxtjs.org/usage
    '@nuxtjs/axios',
    '@nuxtjs/pwa',
    // Doc: https://github.com/nuxt-community/dotenv-module
    '@nuxtjs/dotenv',
    '@nuxtjs/style-resources'
  ],
  /*
  ** Axios module configuration
  ** See https://axios.nuxtjs.org/options
  */
  // env: {
  //   BASE_URL: process.env.BASE_URL
  // },

  axios: {
    baseURL: development ? '//192.168.1.254:8000/' : process.env.BASE_URL
  },

  // PWA configuration
  pwa: {
    icon: {
      source: 'static/icon.png'
    },
    meta: {
      appleStatusBarStyle: 'default'
    },
    manifest: {
      name: 'Kioku',
      lang: 'en',
      background_color: '#fff',
      theme_color: '#fff',
      description: 'Know your guests with Kioku app'
    }
  },

  /*
  ** Build configuration
  */
  build: {
    /*
    ** You can extend webpack config here
    */
    extend (config, ctx) {
    }
  },

  publicRuntimeConfig: {
    secondsToOffline: process.env.SECONDS_TO_OFFLINE || 3,
    secondsToHide: process.env.SECONDS_TO_HIDE || 100
  }
}
