import request from './request'

export function login(username, password) {
  return request.post('/auth/login', { username, password })
}


export function refreshToken(refresh_token) {
  return request.post('/auth/refresh', { refresh_token })
}

export function getCurrentUser() {
  return request.get('/auth/me')
}
