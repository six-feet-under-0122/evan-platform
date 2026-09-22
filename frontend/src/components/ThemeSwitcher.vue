
<template>
  <div class="theme-switcher p-4 bg-secondary rounded-lg shadow-md">
    <h3 class="text-lg font-semibold mb-4 text-text-primary">
      主题切换器
    </h3>

    <!-- 当前主题信息 -->
    <div class="mb-6 p-4 bg-tertiary rounded-md">
      <p class="text-sm text-text-secondary">
        当前主题: <span class="font-medium text-accent">{{ themeInfo.theme }}</span>
      </p>
      <p class="text-sm text-text-secondary">
        模式: {{ themeInfo.isStudy ? '学习模式' : '温馨模式' }} /
        {{ themeInfo.isDark ? '黑暗' : '白天' }}
      </p>
    </div>

    <!-- 快速切换按钮 -->
    <div class="flex gap-2 mb-6">
      <el-button
        type="primary"
        @click="toggleDarkMode"
        class="flex-1"
      >
        切换 {{ isDark ? '白天' : '黑暗' }} 模式
      </el-button>
      <el-button
        @click="toggleModeType"
        class="flex-1"
      >
        切换 {{ isStudy ? '温馨' : '学习' }} 模式
      </el-button>
    </div>

    <!-- 四种主题选择 -->
    <div class="grid grid-cols-2 gap-2">
      <button
        v-for="(label, key) in themeLabels"
        :key="key"
        @click="setTheme(THEMES[key])"
        :class="[
          'theme-card p-4 rounded-md border-2 transition-all',
          'hover:scale-105 hover:shadow-md',
          theme === THEMES[key]
            ? 'border-accent bg-accent bg-opacity-10'
            : 'border-border bg-primary'
        ]"
      >
        <div class="text-sm font-medium text-text-primary mb-1">
          {{ label }}
        </div>
        <div class="flex gap-1">
          <span
            v-for="color in getThemePreview(THEMES[key])"
            :key="color"
            :style="{ backgroundColor: color }"
            class="w-4 h-4 rounded-full"
            />
        </div>
      </button>
    </div>

    <!-- 主题颜色演示 -->
    <div class="mt-6 p-4 bg-primary rounded-md border border-border">
      <h4 class="text-sm font-semibold mb-2 text-text-primary">
        当前主题色板
      </h4>
      <div class="grid grid-cols-3 gap-2 text-xs">
        <div class="flex items-center gap-2">
          <span class="w-6 h-6 rounded bg-accent"></span>
          <span class="text-text-secondary">主色</span>
        </div>
        <div class="flex items-center gap-2">
          <span class="w-6 h-6 rounded bg-secondary"></span>
          <span class="text-text-secondary">次背景</span>
        </div>
        <div class="flex items-center gap-2">
          <span class="w-6 h-6 rounded bg-text-primary"></span>
          <span class="text-text-secondary">主文字</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useTheme } from '@/composables/useTheme'

const {
  THEMES,
  theme,
  themeInfo,
  isDark,
  isStudy,
  setTheme,
  toggleDarkMode,
  toggleModeType
} = useTheme()

const themeLabels = {
  STUDY_LIGHT: '学习 · 白天',
  STUDY_DARK: '学习 · 黑暗',
  COZY_LIGHT: '温馨 · 白天',
  COZY_DARK: '温馨 · 黑暗'
}

const getThemePreview = (themeName) => {
  const previewColors = {
    'study-light': ['#FFFFFF', '#1A1A1A', '#8B7355'],
    'study-dark': ['#0F0F0F', '#E8E8E8', '#C4A574'],
    'cozy-light': ['#FFF8F0', '#2D2520', '#A67C52'],
    'cozy-dark': ['#1A1410', '#F5EDE0', '#C4A574']
  }
  return previewColors[themeName] || []
}
</script>

<style scoped>
.theme-card {
  cursor: pointer;
  user-select: none;
}
</style>
