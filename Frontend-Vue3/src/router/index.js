import { createRouter, createWebHistory } from 'vue-router'
import IndexView from '../views/IndexView.vue'
import LoginView from '../views/user/account/LoginView.vue'
import RegisterView from '../views/user/account/RegisterView.vue'

const routes = [
  {
    path: "/",
    name: "Index",
    component: IndexView,
  },
  {
    path: "/user/account/login/",
    name: "UserLogin",
    component: LoginView,
  },
  {
    path: "/user/account/register/",
    name: "UserRegister",
    component: RegisterView,
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router