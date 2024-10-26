import { registerPlugins } from '@/plugins'
import {createPinia} from 'pinia'
import { VNumberInput } from 'vuetify/labs/VNumberInput'

// Components
import App from './App.vue'

// Composables
import { createApp } from 'vue'

const pinia = createPinia()
const app = createApp(App)

registerPlugins(app)

app.
  use(pinia).
  mount('#app')
