import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'
import { useThemeStore } from '@/stores/theme'

import '@/styles/themes.css'
import '@/styles/element-override.css'

const app = createApp(App)

const pinia = createPinia()
app.use(pinia)
app.use(router)
app.use(ElementPlus)

const themeStore = useThemeStore()
themeStore.loadTheme()

app.mount('#app')