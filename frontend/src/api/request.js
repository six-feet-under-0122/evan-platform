
import axios from 'axios'
import { ElMessage } from 'element-plus'


const request = axios.create({
  baseURL: 'http://localhost:5000/api',
  timeout: 30000,
})


request.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)


request.interceptors.response.use(
  (response) => {
    const res = response.data
    if (res.ok === false) {
      ElMessage.error(res.message || '请求失败')
      return Promise.reject(new Error(res.message || '请求失败'))
    } else {
      return res
    }
  
  },
  (error) => {

    if (error.response) {
      const { status, data } = error.response
      if (status === 401) {
        localStorage.removeItem('access_token') 
        localStorage.removeItem('refresh_token')
        ElMessage.error('登录已过期，请重新登录')
        window.location.href = '/login'
      } else {
        ElMessage.error(data.message || '请求失败')
      }
    } else {
      ElMessage.error('网络错误，请检查后端是否启动')
    }

    return Promise.reject(error)
  }
)

export default request
