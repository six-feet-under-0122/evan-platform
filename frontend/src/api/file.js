import request from './request'

// 上传文件
export function uploadFile(file, purpose = 'attachment') {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('purpose', purpose)

  return request.post('/files/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 获取文件 URL
export function getFileUrl(fileId) {
  const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'
  return `${baseURL}/api/files/${fileId}`
}
