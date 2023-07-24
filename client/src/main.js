import axios from "axios";
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.css'
import './css/style.css';

const app = createApp(App)

app.use(router)

app.mount('#app')

// window.serverPath = "http://localhost:5001/"
const httpClient = axios.create({
	baseURL: 'http://localhost:5001/',
});
window.httpClient = httpClient