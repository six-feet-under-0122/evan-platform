<template>
  <div class="fixed inset-0 overflow-hidden">
    <el-splitter class="h-full">
    <el-splitter-panel :size="288" min="288" max="400"
    class="bg-secondary border-r border-border flex flex-col shadow-lg">

    <!-- 左侧边栏：工具 + 会话列表 -->
      <!-- 工具菜单 -->
      <div class="shrink-0 p-6 border-b border-divider">
        <div class="flex items-center gap-3 mb-4">
          <div class="w-10 h-10 rounded-full bg-accent flex items-center justify-center shadow-md">
            <el-icon :size="20" class="text-white">
              <ChatDotRound />
            </el-icon>
          </div>
          <div>
            <h2 class="text-lg font-bold text-text-primary">Evan</h2>
            <p class="text-xs text-text-tertiary">[^]-[^]</p>
          </div>
        </div>
        <!-- 新建会话按钮 -->
        <el-button
          type="primary"
          class="w-full mb-4"
          @click="createNewSession"
          :loading="isCreatingSession"
        >
          <el-icon class="mr-2"><Plus /></el-icon>
          新建会话
        </el-button>
        <el-menu mode="vertical" class="border-none bg-transparent" @select="handleMenuSelect">
          <el-sub-menu index="tools">
            <template #title>
              <el-icon><More /></el-icon>
              <span class="ml-2">工具</span>
            </template>
            <el-menu-item index="search">
              <el-icon><Search /></el-icon>
              <span>搜索历史</span>
            </el-menu-item>
            <el-menu-item index="help">
              <el-icon><QuestionFilled /></el-icon>
              <span>帮助</span>
            </el-menu-item>
          </el-sub-menu>
        </el-menu>
      </div>
      <!-- 会话列表 -->
      <div class="flex-1 overflow-y-auto p-4 space-y-2">
        <div
          v-for="session in sessions"
          :key="session.id"
          @click="selectSession(session.id)"
          :class="[
            'session-item p-4 group relative rounded-xl cursor-pointer transition-all duration-200',
            'hover:bg-tertiary hover:shadow-md hover:scale-[1.02]',
            currentSessionId === session.id
              ? 'bg-accent text-white shadow-lg scale-[1.02]'
              : 'bg-primary shadow-sm'
          ]"
        >
          <div :class="[
            'text-sm font-semibold truncate mb-1',
            currentSessionId === session.id ? 'text-white' : 'text-text-primary'
          ]">
            {{ session.title }}
          </div>
          <div :class="[
            'text-xs',
            currentSessionId === session.id ? 'text-white opacity-80' : 'text-text-tertiary'
          ]">
            {{ formatDate(session.updated_at) }}
          </div>
          <button
            @click.stop="handleDeleteSession(session.id)"
            class="absolute right-2 top-1/2 -translate-y-1/2
                  opacity-0 group-hover:opacity-100
                  p-2 hover:text-accent-hover text-accent
                  transition-all hover:scale-110"
            title="删除会话"
          >
            <el-icon :size="16"><Delete /></el-icon>
          </button>
        </div>
      </div>
      <!-- 左下角：暗色/白天滑动开关 + 设置按钮 -->
      <div class="shrink-0 p-4 border-t border-divider flex items-center gap-3">
        <el-switch
          v-model="darkModeSwitch"
          @change="toggleDarkMode"
          :active-action-icon="Moon"
          :inactive-action-icon="Sunny"
          inline-prompt
          style="--el-switch-on-color: #4c4d5e; --el-switch-off-color: #f2b84b;"
        />
        <button
          @click="showSettings = true"
          class="flex-1 px-4 py-2 rounded-lg bg-tertiary hover:bg-accent hover:text-white text-text-primary text-sm font-medium transition-all duration-200 flex items-center justify-center gap-2"
        >
          <el-icon :size="16"><Setting /></el-icon>
          设置
        </button>
      </div>
    </el-splitter-panel>
    <!-- 右侧聊天区域 -->
    <el-splitter-panel class="flex flex-col">
      <!-- 聊天头部 -->
      <div class="shrink-0 h-20 bg-secondary border-b border-border flex items-center justify-between px-8 shadow-sm">
        <div class="flex items-center gap-4">
          <div class="text-2xl font-bold text-text-primary">
            {{ currentSessionTitle }}
          </div>
          <div class="px-4 py-1 rounded-full bg-tertiary bg-opacity-10 text-accent text-xs font-medium flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-accent animate-pulse"></span>
            在线
          </div>
        </div>
        <div class="flex items-center gap-3">
          <div class="px-3 py-1 rounded-lg bg-tertiary text-text-secondary text-xs font-medium">
            {{ currentModelName }}
          </div>
        </div>
      </div>

      <!-- 消息区域 -->
      <div ref="messageContainer" class="flex-1 overflow-y-auto p-8 space-y-6 bg-primary">
        <div
          v-for="(msg, index) in messages"
          :key="msg.id || index"
          :data-msg-id="msg.id"
          :class="[
            'flex gap-4 animate-fade-in',
            msg.role === 'user' ? 'justify-end' : 'justify-start'
          ]"
        >
          <!-- 助手头像 -->
          <div v-if="msg.role === 'assistant'" class="shrink-0">
            <el-image :src="evanAvatar" class="w-12 h-12 rounded-full shadow-md" fit="cover" />
          </div>
          <!-- 消息气泡 -->
          <div
            :class="[
              'max-w-2xl rounded-2xl px-6 py-4 shadow-md transition-all duration-200 hover:shadow-lg',
              msg.role === 'user'
                ? 'bg-accent text-white'
                : 'bg-secondary text-text-primary border border-border'
            ]"
          >
            <div
              v-for="(block, blockIndex) in msg.content_json.blocks"
              :key="blockIndex"
              class="message-block"
            >
              <el-image
                v-if="block.type === 'image'"
                :src="getFileUrl(block.file_id)"
                alt="图片"
                fit="cover"
                class="max-w-sm rounded-xl mb-3 shadow-md"
                :preview-src-list="[getFileUrl(block.file_id)]"
              />
              <div
                v-if="block.type === 'text'"
                v-html="renderMarkdown(block.text)"
                :class="[
                  'markdown-body leading-relaxed',
                  msg.role === 'user' ? 'text-white' : 'text-text-primary'
                ]"
              ></div>
            </div>
            <div
              v-if="msg.role === 'assistant'"
              class="mt-3 pt-3 border-t border-divider text-xs text-text-tertiary flex items-center gap-2"
            >
              <span class="w-2 h-2 rounded-full bg-green-500"></span>
              {{ msg.model }}
            </div>
          </div>
          <!-- 用户头像 -->
          <div v-if="msg.role === 'user'" class="shrink-0">
            <el-image :src="sephAvatar" class="w-12 h-12 rounded-full shadow-md" fit="cover" />
          </div>
        </div>
        <!-- 流式消息 -->
        <div v-if="streamingMessage" class="flex gap-4 animate-fade-in justify-start">
          <div class="shrink-0">
            <el-image :src="evanAvatar" class="w-12 h-12 rounded-full shadow-md border-2 border-accent" fit="cover" />
          </div>
          <div class="max-w-2xl rounded-2xl px-6 py-4 shadow-md bg-secondary text-text-primary border border-border">
            <div v-html="renderMarkdown(streamingMessage)" class="markdown-body leading-relaxed text-text-primary"></div>
            <div class="mt-2 flex items-center gap-2 text-xs text-text-tertiary">
              <span class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
              正在输入...
            </div>
          </div>
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="shrink-0 p-6 bg-secondary border-t border-border shadow-lg">
        <div class="mx-auto">
          <div v-if="uploadedImage" class="mb-4 relative inline-block">
            <el-image
              :src="uploadedImage.url"
              class="max-w-37.5 rounded-lg border-2 border-accent cursor-pointer"
              fit="cover"
              :preview-src-list="[uploadedImage.url]"
              :preview-teleported="true"
            />
            <el-button type="danger" size="small" circle class="absolute top-2 right-2" @click="removeUploadedImage">
              <el-icon><Close /></el-icon>
            </el-button>
          </div>
          <div class="flex gap-4 items-center">
            <el-upload
              :show-file-list="false"
              :before-upload="handleImageUpload"
              accept="image/*"
              :disabled="isLoading"
            >
              <el-button :icon="Picture" size="large" :disabled="isLoading">图片</el-button>
            </el-upload>
            <el-input
              v-model="inputMessage"
              placeholder="输入消息... (Enter 发送, Shift+Enter 换行)"
              @keydown.enter.exact="handleSendMessage"
              :disabled="isLoading"
              size="large"
              class="flex-1"
              :autosize="{ minRows: 1, maxRows: 4 }"
              type="textarea"
              resize="none"
            />
            <el-button
              type="primary"
              @click="handleSendMessage"
              :loading="isLoading"
              :disabled="isLoading || (!inputMessage.trim() && !uploadedImage)"
              size="large"
              class="px-8 font-medium"
            >
              {{ isLoading ? '发送中...' : '发送' }}
            </el-button>
          </div>
        </div>
      </div>
    </el-splitter-panel>
  </el-splitter>
    <!-- 设置对话框 -->
    <el-dialog v-model="showSettings" title="设置" width="500px" :close-on-click-modal="false">
      <el-form label-position="left" label-width="100px">
        <el-form-item label="AI 模型">
          <el-select v-model="selectedModel" placeholder="选择模型" class="w-full">
            <el-option
              v-for="model in availableModels"
              :key="model.id"
              :label="model.name"
              :value="model.id"
            >
              <div class="flex flex-col py-1">
                <span class="font-medium">{{ model.name }}</span>
                <span class="text-xs text-text-tertiary">{{ model.description }}</span>
              </div>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="界面模式">
          <el-radio-group :model-value="isStudy ? 'study' : 'cozy'" @change="handleModeChange">
            <el-radio-button value="cozy">
              <el-icon class="mr-1"><HomeFilled /></el-icon>温馨
            </el-radio-button>
            <el-radio-button value="study">
              <el-icon class="mr-1"><Reading /></el-icon>学习
            </el-radio-button>
          </el-radio-group>
          <div class="text-xs text-text-tertiary mt-2 leading-relaxed">
            学习模式：冷色调，专注工作<br>
            温馨模式：暖色调，放松舒适
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showSettings = false">取消</el-button>
        <el-button type="primary" @click="handleSaveSettings">保存</el-button>
      </template>
    </el-dialog>

    <!-- 搜索对话框（全局搜索所有会话） -->
    <el-dialog v-model="showSearch" title="搜索历史消息" width="600px" :close-on-click-modal="false">
      <div class="space-y-4">
        <el-input
          ref="searchInputRef"
          v-model="searchQuery"
          placeholder="输入关键词搜索所有会话..."
          @keyup.enter="handleSearch"
          clearable
        >
          <template #prefix><el-icon><Search /></el-icon></template>
          <template #append>
            <el-button @click="handleSearch">搜索</el-button>
          </template>
        </el-input>
        <div v-loading="isSearching" class="min-h-24">
          <div v-if="searchResults.length > 0" class="max-h-96 overflow-y-auto space-y-2">
            <div
              v-for="result in searchResults"
              :key="result.id"
              class="p-3 bg-tertiary rounded-lg cursor-pointer hover:bg-accent hover:text-white transition group"
              @click="jumpToMessage(result)"
            >
              <div class="flex items-center gap-2 text-xs text-text-tertiary group-hover:text-white mb-1">
                <span class="px-2 py-0.5 rounded bg-primary group-hover:bg-white/20">
                  {{ result.role === 'user' ? '我' : 'Evan' }}
                </span>
                <span class="truncate">{{ sessionTitleOf(result.session_id) }}</span>
                <span class="ml-auto shrink-0">{{ formatDateTime(result.created_at) }}</span>
              </div>
              <div class="text-sm text-text-primary group-hover:text-white line-clamp-2"
                   v-html="highlightKeyword(result.content_text || '', searchQuery)"></div>
            </div>
          </div>
          <div v-else-if="hasSearched && searchResults.length === 0" class="text-center text-text-tertiary py-8">
            没有找到相关消息
          </div>
        </div>
      </div>
    </el-dialog>

    <!-- 帮助对话框 -->
    <el-dialog v-model="showHelp" title="快捷键与帮助" width="600px">
      <div class="space-y-6">
        <div>
          <h3 class="text-base font-bold text-text-primary mb-3">⌨️ 快捷键</h3>
          <div class="grid grid-cols-2 gap-2">
            <div v-for="item in shortcuts" :key="item.key"
                 class="flex items-center justify-between p-2 rounded-lg bg-tertiary">
              <span class="text-sm text-text-secondary">{{ item.desc }}</span>
              <kbd class="px-2 py-1 text-xs rounded bg-primary border border-border text-text-primary font-mono">
                {{ item.key }}
              </kbd>
            </div>
          </div>
        </div>
        <div>
          <h3 class="text-base font-bold text-text-primary mb-3">💡 功能说明</h3>
          <ul class="space-y-2 text-sm text-text-secondary">
            <li>• <strong class="text-text-primary">新建会话</strong>：开始一个新对话</li>
            <li>• <strong class="text-text-primary">图片上传</strong>：点击图片按钮上传（支持多模态对话）</li>
            <li>• <strong class="text-text-primary">流式输出</strong>：消息逐字显示（打字机效果）</li>
            <li>• <strong class="text-text-primary">Markdown</strong>：消息支持代码块、列表等格式</li>
            <li>• <strong class="text-text-primary">主题切换</strong>：左下角切换暗色/白天，设置里切换学习/温馨</li>
          </ul>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref, watch, computed, nextTick } from 'vue'
import {
  More, ChatDotRound, Sunny, Moon, HomeFilled, Reading,
  Setting, Plus, Picture, Close, Delete, Search, QuestionFilled
} from '@element-plus/icons-vue'
import { marked } from 'marked'
import {
  getSessions, getSessionMessages, createSession, deleteSession,
  searchAllMessages
} from '../api/session'
import { sendMessageStream } from '../api/chat'
import { uploadFile, getFileUrl } from '../api/file'
import { getModels } from '../api/models'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useTheme } from '@/composables/useTheme'
import evanAvatarImg from '@/assets/evan.jpg'
import sephAvatarImg from '@/assets/seph.jpg'

// 主题管理
const { isDark, isStudy, toggleDarkMode, toggleModeType } = useTheme()

// 状态
const sessions = ref([])
const messages = ref([])
const inputMessage = ref('')
const isLoading = ref(false)
const currentSessionId = ref(null)
const streamingMessage = ref('')
const messageContainer = ref(null)
const isCreatingSession = ref(false)
const currentStreamController = ref(null)
const uploadedImage = ref(null)

// 对话框显示状态
const showSettings = ref(false)
const showSearch = ref(false)
const showHelp = ref(false)

// 模型相关
const availableModels = ref([])
const selectedModel = ref('gpt-4o-mini')

// 搜索相关
const searchQuery = ref('')
const searchResults = ref([])
const searchInputRef = ref(null)
const isSearching = ref(false)
const hasSearched = ref(false)

// 暗色模式开关（el-switch 需要一个双向绑定值）
const darkModeSwitch = ref(isDark.value)
watch(isDark, (val) => { darkModeSwitch.value = val })

// 头像
const evanAvatar = ref(evanAvatarImg)
const sephAvatar = ref(sephAvatarImg)

// 快捷键列表（同时用于监听和帮助展示）
const shortcuts = [
  { key: 'Enter', desc: '发送消息' },
  { key: 'Shift+Enter', desc: '换行' },
  { key: 'Ctrl+K', desc: '新建会话' },
  { key: 'Ctrl+F', desc: '搜索历史' },
  { key: 'Ctrl+,', desc: '打开设置' },
  { key: 'Ctrl+/', desc: '显示帮助' },
  { key: 'Ctrl+D', desc: '切换暗色模式' },
  { key: 'Esc', desc: '关闭对话框' },
]
// 计算属性：当前会话标题
const currentSessionTitle = computed(() => {
  const session = sessions.value.find(s => s.id === currentSessionId.value)
  return session ? session.title : 'Chat'
})

// 计算属性：当前模型名称
const currentModelName = computed(() => {
  const model = availableModels.value.find(m => m.id === selectedModel.value)
  return model ? model.name : selectedModel.value
})

// 根据 session_id 拿标题（搜索结果展示用）
const sessionTitleOf = (sessionId) => {
  const s = sessions.value.find(s => s.id === sessionId)
  return s ? s.title : '未知会话'
}

// 格式化日期（会话列表）
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  if (days === 0) return '今天'
  if (days === 1) return '昨天'
  if (days < 7) return `${days} 天前`
  return date.toLocaleDateString('zh-CN')
}

// 格式化完整日期时间（搜索结果）
const formatDateTime = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleString('zh-CN')
}

// 初始化
onMounted(async () => {
  try {
    const res = await getSessions()
    sessions.value = res.data
    if (sessions.value.length > 0) {
      currentSessionId.value = sessions.value[0].id
    }
  } catch (error) {
    ElMessage.error('获取会话列表失败')
  }

  try {
    const res = await getModels()
    availableModels.value = res.data
  } catch (error) {
    console.error('获取模型列表失败:', error)
  }

  const savedModel = localStorage.getItem('selectedModel')
  if (savedModel) {
    selectedModel.value = savedModel
  }

  window.addEventListener('keydown', handleKeydown)
})

onBeforeUnmount(() => {
  window.removeEventListener('keydown', handleKeydown)
})
// 全局快捷键处理
const handleKeydown = (e) => {
  if (e.ctrlKey && e.key === 'k') {
    e.preventDefault()
    createNewSession()
  } else if (e.ctrlKey && e.key === 'f') {
    e.preventDefault()
    openSearch()
  } else if (e.ctrlKey && e.key === ',') {
    e.preventDefault()
    showSettings.value = true
  } else if (e.ctrlKey && e.key === '/') {
    e.preventDefault()
    showHelp.value = true
  } else if (e.ctrlKey && e.key === 'd') {
    e.preventDefault()
    toggleDarkMode()
  } else if (e.key === 'Escape') {
    showSettings.value = false
    showSearch.value = false
    showHelp.value = false
  }
}

// 菜单选择处理
const handleMenuSelect = (index) => {
  if (index === 'search') {
    openSearch()
  } else if (index === 'help') {
    showHelp.value = true
  }
}

// 监听会话切换
watch(currentSessionId, async (newSessionId) => {
  if (!newSessionId) return

  if (currentStreamController.value) {
    currentStreamController.value.abort()
    currentStreamController.value = null
  }

  streamingMessage.value = ''
  isLoading.value = false

  try {
    const resMessages = await getSessionMessages(newSessionId)
    messages.value = resMessages.data
    scrollToBottom()
  } catch (error) {
    ElMessage.error('获取消息失败')
  }
})

// 选择会话
const selectSession = (sessionId) => {
  currentSessionId.value = sessionId
}
// 发送消息（SSE 流式）
const handleSendMessage = async (event) => {
  if (event) event.preventDefault()

  const userText = inputMessage.value.trim()
  if ((!userText && !uploadedImage.value) || !currentSessionId.value) return

  const fileId = uploadedImage.value?.id || null

  inputMessage.value = ''
  uploadedImage.value = null
  isLoading.value = true
  streamingMessage.value = ''
  scrollToBottom()

  try {
    const controller = await sendMessageStream(
      currentSessionId.value,
      userText || '图片',
      selectedModel.value,
      fileId,
      (userMsg) => {
        messages.value.push(userMsg)
        scrollToBottom()
      },
      (chunk) => {
        streamingMessage.value += chunk
        scrollToBottom()
      },
      (assistantMsg) => {
        messages.value.push(assistantMsg)
        streamingMessage.value = ''
        isLoading.value = false
        currentStreamController.value = null
        scrollToBottom()
      },
      (error) => {
        ElMessage.error('发送消息失败')
        streamingMessage.value = ''
        isLoading.value = false
        currentStreamController.value = null
      }
    )
    currentStreamController.value = controller
  } catch (error) {
    ElMessage.error('发送消息失败')
    streamingMessage.value = ''
    isLoading.value = false
    currentStreamController.value = null
  }
}

// 删除会话
const handleDeleteSession = async (sessionId) => {
  try {
    await ElMessageBox.confirm('确定要删除这个会话吗？', '提示', {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await deleteSession(sessionId)
    const res = await getSessions()
    sessions.value = res.data
    if (sessionId === currentSessionId.value) {
      if (sessions.value.length > 0) {
        selectSession(sessions.value[0].id)
      } else {
        await createNewSession()
      }
    }
    ElMessage.success('会话已删除')
  } catch (err) {
    if (err !== 'cancel') {
      console.error('删除会话失败:', err)
      ElMessage.error('删除失败')
    }
  }
}

// 新建会话
const createNewSession = async () => {
  isCreatingSession.value = true
  try {
    const res = await createSession('新对话')
    sessions.value.unshift(res.data)
    currentSessionId.value = res.data.id
    ElMessage.success('创建会话成功')
  } catch (error) {
    ElMessage.error('创建会话失败')
  } finally {
    isCreatingSession.value = false
  }
}
// 图片上传
const handleImageUpload = async (file) => {
  if (!file.type.startsWith('image/')) {
    ElMessage.error('只能上传图片文件')
    return false
  }
  if (file.size > 10 * 1024 * 1024) {
    ElMessage.error('图片大小不能超过 10MB')
    return false
  }
  try {
    ElMessage.info('上传中...')
    const res = await uploadFile(file)
    uploadedImage.value = {
      id: res.data.id,
      url: getFileUrl(res.data.id)
    }
    ElMessage.success('上传成功')
  } catch (error) {
    ElMessage.error('上传失败')
  }
  return false
}

const removeUploadedImage = () => {
  uploadedImage.value = null
}

// ===== 搜索功能（全局搜索所有会话） =====
const openSearch = () => {
  showSearch.value = true
  nextTick(() => searchInputRef.value?.focus())
}

const handleSearch = async () => {
  const q = searchQuery.value.trim()
  if (!q) {
    searchResults.value = []
    hasSearched.value = false
    return
  }
  isSearching.value = true
  hasSearched.value = true
  try {
    const res = await searchAllMessages(q)
    searchResults.value = res.data
  } catch (error) {
    ElMessage.error('搜索失败')
    searchResults.value = []
  } finally {
    isSearching.value = false
  }
}

// 高亮关键词
const highlightKeyword = (text, keyword) => {
  if (!keyword || !text) return text
  const escaped = keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  const regex = new RegExp(`(${escaped})`, 'gi')
  return text.replace(regex, '<mark class="bg-yellow-300 text-black rounded px-0.5">$1</mark>')
}

// 跳转到消息：切换到对应会话，滚动定位到该消息
const jumpToMessage = async (result) => {
  showSearch.value = false
  // 如果不是当前会话，先切换
  if (result.session_id !== currentSessionId.value) {
    currentSessionId.value = result.session_id
    // 等 watch 加载完消息（简单延时，后续可优化为 await 加载）
    await nextTick()
    await new Promise(resolve => setTimeout(resolve, 300))
  }
  // 滚动定位到该消息
  await nextTick()
  const el = messageContainer.value?.querySelector(`[data-msg-id="${result.id}"]`)
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'center' })
    el.classList.add('highlight-flash')
    setTimeout(() => el.classList.remove('highlight-flash'), 2000)
  }
}

// ===== 设置功能 =====
const handleModeChange = (value) => {
  const targetIsStudy = value === 'study'
  if (targetIsStudy !== isStudy.value) {
    toggleModeType()
  }
}

const handleSaveSettings = () => {
  localStorage.setItem('selectedModel', selectedModel.value)
  showSettings.value = false
  ElMessage.success('设置已保存')
}

// 渲染 Markdown
const renderMarkdown = (text) => {
  return marked(text)
}

// 滚动到底部
const scrollToBottom = () => {
  nextTick(() => {
    if (messageContainer.value) {
      messageContainer.value.scrollTop = messageContainer.value.scrollHeight
    }
  })
}
</script>

<style scoped>
/* 动画 */
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fade-in 0.3s ease-out;
}

/* 搜索跳转高亮闪烁 */
@keyframes highlight-flash {
  0%, 100% { background-color: transparent; }
  30% { background-color: var(--accent, #f2b84b); opacity: 0.3; }
}

:deep(.highlight-flash) {
  animation: highlight-flash 1s ease-in-out 2;
  border-radius: 12px;
}

/* 搜索结果两行截断 */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Markdown 样式 */
.markdown-body :deep(p) {
  margin: 0.75em 0;
  line-height: 1.8;
}

.markdown-body :deep(code) {
  background: var(--color-code-bg);
  padding: 3px 8px;
  border-radius: 6px;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 0.9em;
}

.markdown-body :deep(pre) {
  background: var(--color-code-bg);
  padding: 1.25em;
  border-radius: 12px;
  overflow-x: auto;
  margin: 1em 0;
}

.markdown-body :deep(pre code) {
  background: none;
  padding: 0;
}

.markdown-body :deep(ul),
.markdown-body :deep(ol) {
  margin: 0.75em 0;
  padding-left: 1.75em;
  line-height: 1.8;
}

.markdown-body :deep(blockquote) {
  border-left: 4px solid var(--accent);
  padding-left: 1.25em;
  margin: 1em 0;
  color: var(--text-secondary);
  font-style: italic;
}

/* 用户消息的 Markdown（白色文字） */
.markdown-body.text-white :deep(code) {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.markdown-body.text-white :deep(pre) {
  background: rgba(255, 255, 255, 0.1);
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: var(--bg-secondary);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: var(--border-color);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: var(--accent);
}

/* Element Plus 自定义 */
:deep(.el-textarea__inner) {
  padding: 12px 16px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  border: 2px solid var(--border-color);
  transition: all 0.3s ease;
}

:deep(.el-textarea__inner:focus) {
  border-color: var(--accent);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

:deep(.el-button--primary) {
  background: linear-gradient(
    135deg,
    var(--accent) 0%,
    var(--accent-hover) 100%
  );
  border: none;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

:deep(.el-button--primary:hover) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
}

:deep(.el-menu) {
  background-color: transparent;
}
</style>
