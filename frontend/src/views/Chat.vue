<template>
  <div class="h-screen flex bg-primary overflow-hidden">
    <!-- 左侧边栏：工具 + 会话列表 -->
    <div class="w-72 bg-secondary border-r border-border flex flex-col shadow-lg">
      <!-- 工具菜单 -->
      <div class="p-6 border-b border-divider">
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
        <el-menu mode="vertical" class="border-none bg-transparent">
          <el-sub-menu index="1">
            <template #title>
              <el-icon><More /></el-icon>
              <span class="ml-2">工具</span>
            </template>
            <el-menu-item v-for="tool in tools" :key="tool.id" :index="tool.id">
              {{ tool.name }}
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
            'session-item p-4 rounded-xl cursor-pointer transition-all duration-200',
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
        </div>
      </div>

      <!-- 主题切换按钮 -->
      <div class="p-4 border-t border-divider space-y-2">
        <button
          @click="toggleDarkMode"
          class="w-full px-4 py-3 rounded-xl bg-tertiary hover:bg-accent hover:text-white text-text-primary text-sm font-medium transition-all duration-200 hover:shadow-lg hover:scale-105 flex items-center justify-center gap-2"
        >
          <el-icon :size="16">
            <Sunny v-if="isDark" />
            <Moon v-else />
          </el-icon>
          {{ isDark ? '白天模式' : '暗色模式' }}
        </button>
        <button
          @click="toggleModeType"
          class="w-full px-4 py-3 rounded-xl bg-tertiary hover:bg-accent hover:text-white text-text-primary text-sm font-medium transition-all duration-200 hover:shadow-lg hover:scale-105 flex items-center justify-center gap-2"
        >
          <el-icon :size="16">
            <HomeFilled v-if="isStudy" />
            <Reading v-else />
          </el-icon>
          {{ isStudy ? '温馨模式' : '学习模式' }}
        </button>
      </div>
    </div>

    <!-- 右侧聊天区域 -->
    <div class="flex-1 flex flex-col">
      <!-- 聊天头部 -->
      <div class="h-20 bg-secondary border-b border-border flex items-center justify-between px-8 shadow-sm">
        <div class="flex items-center gap-4">
          <div class="text-2xl font-bold text-text-primary">
            {{ currentSessionTitle }}
          </div>
          <div class="px-4 py-1 rounded-full bg-tertiary bg-opacity-10 text-[--accent] text-xs font-medium">
            在线
          </div>
        </div>
        <div class="flex gap-3">
          <button class="px-4 py-2 text-sm rounded-lg bg-tertiary hover:bg-accent text-text-secondary
           hover:text-white transition-all duration-200 font-medium flex items-center gap-2">
            <el-icon :size="16">
              <Setting />
            </el-icon>
            设置
          </button>
        </div>
      </div>

      <!-- 消息区域 -->
      <div class="flex-1 overflow-y-auto p-8 space-y-6 bg-primary">
        <div
          v-for="(msg, index) in messages"
          :key="index"
          :class="[
            'flex gap-4 animate-fade-in',
            msg.role === 'user' ? 'justify-end' : 'justify-start'
          ]"
        >
          <!-- 助手头像 -->
          <div v-if="msg.role === 'assistant'" class="shrink-0">
            <el-image
              :src="evanAvatar"
              class="w-12 h-12 rounded-full shadow-md "
              fit="cover"
            />
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
            <!-- 消息内容块 -->
            <div
              v-for="(block, blockIndex) in msg.content_json.blocks"
              :key="blockIndex"
              class="message-block"
            >
              <!-- 图片 -->
              <el-image
                v-if="block.type === 'image'"
                :src="`http://localhost:5000/api/files/${block.file_id}`"
                alt="图片"
                fit="cover"
                class="max-w-sm rounded-xl mb-3 shadow-md"
                :preview-src-list="[`http://localhost:5000/api/files/${block.file_id}`]"
              />

              <!-- 文本（Markdown） -->
              <div
                v-if="block.type === 'text'"
                v-html="renderMarkdown(block.text)"
                :class="[
                  'markdown-body leading-relaxed',
                  msg.role === 'user' ? 'text-white' : 'text-text-primary'
                ]"
              ></div>
            </div>

            <!-- 模型标签（仅助手消息） -->
            <div
              v-if="msg.role === 'assistant'"
              class="mt-3 pt-3 border-t border-divider text-xs text-text-tertiary flex items-center gap-2"
            >
              <span class="w-2 h-2 rounded-full bg-green-500"></span>
              {{ msg.model }}
            </div>
          </div>

          <!-- 用户头像 -->
          <div div
            v-if="msg.role === 'user'"
             class="shrink-0"
          >
            <el-image 
              :src="sephAvatar"
              class="w-12 h-12 rounded-full shadow-md  "
              fit="cover"
            />
          </div>
        </div>
        <div v-if="streamingMessage" class="flex gap-4 animate-fade-in justify-start">
          <div class="shrink-0">
            <el-image
              :src="evanAvatar"
              class="w-12 h-12 rounded-full shadow-md border-2 border-accent"
              fit="cover"
            />
          </div>
          <div class="max-w-2xl rounded-2xl px-6 py-4 shadow-md bg-secondary text-text-primary border border-border">
            <div
              v-html="renderMarkdown(streamingMessage)"
              class="markdown-body leading-relaxed text-text-primary"
            ></div>
            <div class="mt-2 flex items-center gap-2 text-xs text-text-tertiary">
              <span class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
              正在输入...
            </div>
          </div>
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="flex-none p-6 bg-secondary border-t border-border shadow-lg">
        <div class="flex gap-4 max-w-5xl mx-auto ">        
          <el-input
            v-model="inputMessage"
            placeholder="输入消息... (Enter 发送)"
            @keyup.enter="handleSendMessage"
            :disabled="isLoading"
            size="large"
            class="resize-none flex-1 "
            :autosize="{ minRows: 1, maxRows: 4 }"
            type="textarea" 
          />
          <el-button
            type="primary"
            @click="handleSendMessage"
            :loading="isLoading"
            :disabled="isLoading || !inputMessage.trim()"
            size="large"
            class="h-auto px-8 font-medium"
          >
            {{ isLoading ? '发送中...' : '发送' }}
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch, computed } from 'vue'
import { More, ChatDotRound, Sunny, Moon, HomeFilled, Reading, Setting, Plus } from '@element-plus/icons-vue'
import { marked } from 'marked'
import { getSessions, getSessionMessages, createSession } from '../api/session'
import { sendMessage as SendMessage } from '../api/chat'
import { ElMessage } from 'element-plus'
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
const tools = ref([
  { id: '1', name: '设置' },
  { id: '2', name: '历史记录' },
  { id: '3', name: '帮助' }
])
const streamingMessage = ref('')
const messageContainer = ref(null)
const isCreatingSession = ref(false)



// Evan 头像
const evanAvatar = ref(evanAvatarImg)
const sephAvatar = ref(sephAvatarImg)

// 计算属性：当前会话标题
const currentSessionTitle = computed(() => {
  const session = sessions.value.find(s => s.id === currentSessionId.value)
  return session ? session.title : 'Chat'
})

// 格式化日期
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

// 加载会话列表
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
})

// 监听会话切换
watch(currentSessionId, async (newSessionId) => {
  if (!newSessionId) return
  try {
    const resMessages = await getSessionMessages(newSessionId)
    messages.value = resMessages.data
    scrollToBottom()
  } catch (error) {
    ElMessage.error('获取消息失败')
  }
})

// 选择会话
const selectSession = async (sessionId) => {
  currentSessionId.value = sessionId
}

// 发送消息
const handleSendMessage = async () => {
  const userText = inputMessage.value.trim()
  if (!userText) return

  inputMessage.value = ''
  isLoading.value = true
  streamingMessage.value = ''
  scrollToBottom()

  try {
    sendMessageStream(
      currentSessionId.value,
      userText,
      'gpt-4o-mini',
      null,
      // onChunk
      (chunk) => {
        streamingMessage.value += chunk
        scrollToBottom()
      },
      // onDone
      () => {
        const assistantMessage = {
          role: 'assistant',
          content_json: {
            blocks: [{ type: 'text', text: streamingMessage.value }]
          },
          model: 'gpt-4o-mini'
        }
        messages.value.push(assistantMessage)
        streamingMessage.value = ''
        isLoading.value = false
        scrollToBottom()
      },
      // onError
      (error) => {
        ElMessage.error('发送消息失败')
        streamingMessage.value = ''
        isLoading.value = false
      }
    )
  } catch (error) {
    ElMessage.error('发送消息失败')
    streamingMessage.value = ''
    isLoading.value = false
  }

  // try {
  //   const res = await SendMessage(currentSessionId.value, userText)
  //   messages.value.push(res.data.user_message)
  //   messages.value.push(res.data.assistant_message)
  // } catch (error) {
  //   ElMessage.error('发送消息失败')
  // } finally {
  //   isLoading.value = false
  // }
}

// 渲染 Markdown
const renderMarkdown = (text) => {
  return marked(text)
}


const scrollToBottom = () => {
  nextTick(() => {
    if (messageContainer.value) {
      messageContainer.value.scrollTop = messageContainer.value.scrollHeight
    }
  })
}


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
