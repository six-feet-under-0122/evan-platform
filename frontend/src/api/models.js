import request from './request'

// 获取可用模型列表
export function getModels() {
  return request.get('/models/')
}

// 获取默认模型
export function getDefaultModel() {
  return request.get('/models/default')
}
