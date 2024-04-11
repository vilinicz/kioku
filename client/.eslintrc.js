module.exports = {
  extends: ["@nuxtjs", "plugin:nuxt/recommended"],
  overrides: [
    {
      files: ['layouts/*.vue', 'pages/**/*.vue'],
      rules: { 'vue/multi-word-component-names': 'off' }
    }
  ]
};