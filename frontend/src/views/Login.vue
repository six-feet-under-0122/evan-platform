<template>
  <div class="min-h-screen flex items-center justify-center p-6 bg-linear-to-r from-[--bg-primary] to-[--bg-secondary] transition-colors duration-300">
    <div class="w-full max-w-xl px-4">
      <!-- 登录卡片 -->
      <div class="bg-primary rounded-2xl  p-10  backdrop-blur-sm">
        <!-- Logo 区域（可以加图片） -->
        <div class="flex justify-center mb-8">
          <div class="w-16 h-16 rounded-full bg-accent flex items-center justify-center shadow-lg">
            <el-icon :size="32" class="text-white">
              <ChatDotRound />
            </el-icon>
          </div>
        </div>

        <!-- 标题 -->
        <div class="text-center mb-10">
          <h1 class="text-4xl font-bold text-text-primary mb-3 tracking-tight">
            欢迎回来
          </h1>
        </div>

        <!-- 登录表单 -->
        <el-form class="space-y-6" label-position="top">
          <el-form-item>
            <template #label>
              <span class="text-text-primary font-medium">用户名</span>
            </template>
            <el-input
              v-model="username"
              placeholder="输入你的用户名"
              size="large"
              :prefix-icon="User"
            />
          </el-form-item>

          <el-form-item>
            <template #label>
              <span class="text-text-primary font-medium">密码</span>
            </template>
            <el-input
              v-model="password"
              type="password"
              placeholder="输入密码"
              size="large"
              :prefix-icon="Lock"
              @keyup.enter="handleLogin"
            />
          </el-form-item>

          <el-form-item class="mb-0 mt-8">
            <el-button
              type="primary"
              @click="handleLogin"
              :loading="loginLoading"
              :disabled="!username || !password"
              size="large"
              class="w-full h-12 text-base font-medium"
            >
              {{ loginLoading ? '登录中...' : '登录' }}
            </el-button>
          </el-form-item>
        </el-form>

        <!-- 底部提示 -->
        <div class="mt-8 pt-6 border-t border-divider text-center text-sm text-text-tertiary">
          首次使用？请联系管理员创建账号
        </div>
      </div>

      <!-- 主题切换（开发用） -->
      <div class="mt-6 text-center">
        <button
          @click="toggleTheme"
          class="text-sm text-text-secondary hover:text-accent transition-colors duration-200 px-4 py-2 rounded-lg flex items-center justify-center gap-2 mx-auto"
        >
          <el-icon :size="16">
            <Sunny v-if="isDark" />
            <Moon v-else />
          </el-icon>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { User, Lock, ChatDotRound, Sunny, Moon } from '@element-plus/icons-vue'
import { login } from '../api/auth'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { useTheme } from '@/composables/useTheme'

const username = ref('')
const password = ref('')
const router = useRouter()
const loginLoading = ref(false)

const { isDark, toggleDarkMode } = useTheme()
const toggleTheme = () => {
  toggleDarkMode()
}

const handleLogin = async () => {
  if (!username.value || !password.value) {
    ElMessage.warning('用户名和密码不能为空')
    return
  }

  loginLoading.value = true

  try {
    const res = await login(username.value, password.value)
    if (res) {
      localStorage.setItem('access_token', res.data.access_token)
      localStorage.setItem('refresh_token', res.data.refresh_token)

      const userStore = useUserStore()
      userStore.setUser(res.data.user)

      ElMessage.success('登录成功！')
      router.push('/chat')
    }
  } catch (error) {
    ElMessage.error('登录失败，请检查用户名和密码')
    console.error(error)
  } finally {
    loginLoading.value = false
  }
}
</script>

<style scoped>
/* 渐变背景动画 */
.bg-linear-to-br {
  background: linear-gradient(
    135deg,
    var(--bg-primary) 0%,
    var(--bg-secondary) 100%
  );
}

/* 卡片悬浮效果 */
.shadow-2xl {
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.15);
}

/* 按钮自定义 */
:deep(.el-button--primary) {
  background: linear-gradient(
    135deg,
    var(--accent) 0%,
    var(--accent-hover) 100%
  );
  border: none;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

:deep(.el-button--primary:hover) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
}

:deep(.el-button--primary:active) {
  transform: translateY(0);
}

/* 输入框自定义 */
:deep(.el-input__wrapper) {
  padding: 12px 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

:deep(.el-input__wrapper:hover) {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
</style>
