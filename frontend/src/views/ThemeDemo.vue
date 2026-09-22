<template>
  <div class="min-h-screen p-8 bg-primary">
    <div class="max-w-4xl mx-auto space-y-8">
      <!-- 页面标题 -->
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-text-primary mb-3">
          Evan 主题系统演示
        </h1>
        <p class="text-text-secondary">
          体验四种主题风格：学习/温馨 × 白天/黑暗
        </p>
      </div>

      <!-- 主题切换器 -->
      <ThemeSwitcher />

      <!-- 组件演示区 -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- 卡片演示 -->
        <div class="p-6 bg-secondary rounded-xl border border-border">
          <h3 class="text-lg font-semibold text-text-primary mb-4">
            卡片组件
          </h3>
          <p class="text-text-secondary mb-3">
            这是一个演示卡片，使用了主题变量来控制背景色、文字颜色和边框。
          </p>
          <button class="px-4 py-2 bg-accent text-white rounded-lg hover:bg-accent transition-colors">
            主题按钮
          </button>
        </div>

        <!-- Element Plus 组件演示 -->
        <div class="p-6 bg-secondary rounded-xl border border-border">
          <h3 class="text-lg font-semibold text-text-primary mb-4">
            Element Plus 组件
          </h3>
          <el-input
            v-model="inputValue"
            placeholder="输入一些文字试试"
            class="mb-3"
          />
          <el-button type="primary">主要按钮</el-button>
          <el-button>次要按钮</el-button>
        </div>

        <!-- 代码块演示 -->
        <div class="p-6 bg-secondary rounded-xl border border-border">
          <h3 class="text-lg font-semibold text-text-primary mb-4">
            代码块演示
          </h3>
          <pre class="p-4 bg-tertiary rounded-lg text-sm text-text-primary overflow-x-auto"><code>const useTheme = () => {
  const { theme } = useTheme()
  return theme.value
}</code></pre>
        </div>

        <!-- 状态色演示 -->
        <div class="p-6 bg-secondary rounded-xl border border-border">
          <h3 class="text-lg font-semibold text-text-primary mb-4">
            状态颜色
          </h3>
          <div class="space-y-3">
            <div class="flex items-center gap-2">
              <span class="w-4 h-4 rounded-full bg-success"></span>
              <span class="text-text-secondary">成功状态</span>
            </div>
            <div class="flex items-center gap-2">
              <span class="w-4 h-4 rounded-full bg-warning"></span>
              <span class="text-text-secondary">警告状态</span>
            </div>
            <div class="flex items-center gap-2">
              <span class="w-4 h-4 rounded-full bg-error"></span>
              <span class="text-text-secondary">错误状态</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 当前主题信息 -->
      <div class="p-6 bg-secondary rounded-xl border border-border">
        <h3 class="text-lg font-semibold text-text-primary mb-4">
          当前主题信息
        </h3>
        <div class="grid grid-cols-2 gap-4 text-sm">
          <div>
            <span class="text-text-secondary">主题名称：</span>
            <span class="text-accent font-medium">{{ theme }}</span>
          </div>
          <div>
            <span class="text-text-secondary">模式类型：</span>
            <span class="text-accent font-medium">{{ isStudy ? '学习模式' : '温馨模式' }}</span>
          </div>
          <div>
            <span class="text-text-secondary">亮暗状态：</span>
            <span class="text-accent font-medium">{{ isDark ? '黑暗' : '白天' }}</span>
          </div>
          <div>
            <span class="text-text-secondary">持久化：</span>
            <span class="text-accent font-medium">localStorage ✓</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ThemeSwitcher from '@/components/ThemeSwitcher.vue'
import { useTheme } from '@/composables/useTheme'

const { theme, isDark, isStudy } = useTheme()
const inputValue = ref('')
</script>
