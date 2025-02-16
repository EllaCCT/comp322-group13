import { createApp } from 'vue'
import App from './App.vue'
import router from './router/'
import axios from 'axios'
import { createPinia } from 'pinia'

const app = createApp(App)

const pinia = createPinia()

axios.defaults.baseURL = "http://localhost:8000"
app.config.globalProperties.$axios = axios

app.use(pinia)

app.use(router)

app.mount('#app')