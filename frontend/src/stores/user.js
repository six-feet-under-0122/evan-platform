import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
    
  const userInfo = ref(null)

  function setUser(user) {
    userInfo.value = user
  }

  function clearUser() {
    userInfo.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  return {
    userInfo,
    setUser,
    clearUser,
  }
})