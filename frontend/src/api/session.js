import request from './request'

// 获取所有会话
export function getSessions(limit = 50, offset = 0) {
  return request.get('/sessions/', { params: { limit, offset } })
}

// 创建新会话
export function createSession(title = '新对话') {
  return request.post('/sessions/', { title })
}

// 获取单个会话
export function getSession(id) {
  return request.get(`/sessions/${id}`)
}

// 更新会话
export function updateSession(id, data) {
  return request.patch(`/sessions/${id}`, data)
}

// 删除会话
export function deleteSession(id) {
  return request.delete(`/sessions/${id}`)
}

// 获取会话的所有消息
export function getSessionMessages(id, limit = 50, before_id = null) {
  const params = { limit }
  if (before_id) params.before_id = before_id
  return request.get(`/sessions/${id}/messages`, { params })
}

// 全局搜索所有会话的消息
export function searchAllMessages(query, limit = 50) {
  return request.get('/sessions/search', {
    params: { q: query, limit }
  })
}

// 搜索指定会话内的消息
export function searchSessionMessages(sessionId, query, limit = 20) {
  return request.get(`/sessions/${sessionId}/messages/search`, {
    params: { q: query, limit }
  })
}