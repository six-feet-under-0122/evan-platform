import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
  },
  {
    path: '/chat',
    name: 'Chat',
    component: () => import('../views/Chat.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/theme-demo',
    name: 'ThemeDemo',
    component: () => import('../views/ThemeDemo.vue'),
  },
  {
    path: '/',
    redirect: '/chat',
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})


router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')

  // 如果访问需要认证的页面但没有 token
  if (to.meta.requiresAuth && !token) {
    console.log('[Router] 未登录，跳转到登录页')
    next('/login')
  }
  // 如果已登录访问登录页，跳转到聊天页
  else if (to.path === '/login' && token) {
    console.log('[Router] 已登录，跳转到聊天页')
    next('/chat')
  }
  // 其他情况放行
  else {
    console.log('[Router] 放行:', to.path)
    next()
  }
})

export default router