import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import MainPage from '@/views/MainPage.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'login',
      component: Login, // 登录页面
    },
    {
      path: '/register',
      name: 'register',
      component: Register, // 注册页面
    },
    {
      path: '/mainpage',
      name: 'mainpage',
      component: MainPage, // 主页面
    },
  ],
});

export default router;
