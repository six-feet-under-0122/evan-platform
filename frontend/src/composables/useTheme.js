import { computed } from 'vue'
import { useThemeStore } from '@/stores/theme'

export function useTheme() {
  const themeStore = useThemeStore()

  // 主题常量（暴露给组件使用）
  const THEMES = themeStore.THEMES

  // 当前主题
  const theme = computed(() => themeStore.currentTheme)

  // 当前主题信息
  const themeInfo = computed(() => themeStore.getThemeInfo())

  // 是否为暗色模式
  const isDark = computed(() => themeInfo.value.isDark)

  // 是否为学习模式
  const isStudy = computed(() => themeInfo.value.isStudy)

  // 是否为温馨模式
  const isCozy = computed(() => themeInfo.value.isCozy)

  // 设置主题
  const setTheme = (newTheme) => {
    themeStore.setTheme(newTheme)
  }

  // 切换亮/暗模式
  const toggleDarkMode = () => {
    themeStore.toggleDarkMode()
  }

  // 切换模式类型（学习/温馨）
  const toggleModeType = () => {
    themeStore.toggleModeType()
  }

  return {
    THEMES,
    theme,
    themeInfo,
    isDark,
    isStudy,
    isCozy,
    setTheme,
    toggleDarkMode,
    toggleModeType
  }
}
