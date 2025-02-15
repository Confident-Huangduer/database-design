import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import router from './router';
import 'element-plus/dist/index.css'
import App from './App.vue'
import '../src/assets/font/font.css'

const app = createApp(App)

app.use(router)
app.use(ElementPlus)
app.mount('#app')