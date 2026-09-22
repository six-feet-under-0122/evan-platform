import request from './request'
import { fetchEventSource } from '@microsoft/fetch-event-source'
//普通对话
export function sendMessage(session_id, message, model = 'gpt-4o-mini', file_id = null) {
  return request.post('/chat/', { session_id, message, model, file_id })
}

export async function sendMessageStream(
  session_id,
  message,
  model = 'gpt-4o-mini',
  file_id = null,
  onChunk,
  onDone,
  onError
) {
  const token = localStorage.getItem('access_token')
  const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'
  const ctrl = new AbortController()

  try {
    await fetchEventSource(`${baseURL}/api/chat/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        session_id,
        message,
        model,
        file_id
      }),
      signal: ctrl.signal,

      async onopen(response) {
        if (response.ok) {
          console.log('[SSE] 连接成功')
          return
        }

        // 处理错误响应
        if (response.status >= 400 && response.status < 500 && response.status !== 429) {
          const error = await response.json()
          throw new Error(error.message || '请求失败')
        }

        throw new Error(`HTTP ${response.status}`)
      },

      onmessage(event) {
        if (event.data === '[DONE]') {
          ctrl.abort()
          onDone()
          return
        }

        try {
          const data = JSON.parse(event.data)
          if (data.chunk) {
            onChunk(data.chunk)
          }
        } catch (err) {
          console.error('[SSE] 解析错误:', err, event.data)
        }
      },

      onerror(err) {
        console.error('[SSE] 连接错误:', err)
        ctrl.abort()
        onError(err)
        throw err  // 停止重连
      }
    })
  } catch (err) {
    console.error('[SSE] 流式请求失败:', err)
    onError(err)
  }

  // 返回 AbortController，用于手动取消
  return ctrl
}