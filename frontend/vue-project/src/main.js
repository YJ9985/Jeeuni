import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

import App from './App.vue'
import router from './router'
import axios from 'axios'

import './assets/global.css' 
import './assets/fonts.css'
import GoogleLoginPlugin from 'vue3-google-login'

const app = createApp(App)
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

app.use(pinia)
app.use(router)

app.use(GoogleLoginPlugin, {
  clientId: import.meta.env.VITE_APP_GOOGLE_CLIENT_ID,
})

app.mount('#app')

function isTokenExpired(token) {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    const exp = payload.exp
    const now = Math.floor(Date.now() / 1000)
    return exp < now
  } catch (e) {
    console.error('토큰 디코딩 실패:', e)
    return true
  }
}

const access = localStorage.getItem('access')
const refresh = localStorage.getItem('refresh')

if (access && refresh && !isTokenExpired(access)) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${access}`
} else {
  localStorage.removeItem('access')
  localStorage.removeItem('refresh')
}