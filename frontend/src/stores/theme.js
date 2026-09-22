import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  // 主题类型定义
  const THEMES = {
    STUDY_LIGHT: 'study-light',
    STUDY_DARK: 'study-dark',
    COZY_LIGHT: 'cozy-light',
    COZY_DARK: 'cozy-dark'
  }

  // 当前主题（默认学习模式 - 白天）
  const currentTheme = ref(THEMES.STUDY_LIGHT)

  // 从 localStorage 加载主题
  const loadTheme = () => {
    const savedTheme = localStorage.getItem('evan-theme')
    if (savedTheme && Object.values(THEMES).includes(savedTheme)) {
      currentTheme.value = savedTheme
    }
    applyTheme(currentTheme.value)
  }

  // 应用主题到 DOM
  const applyTheme = (theme) => {
    document.documentElement.setAttribute('data-theme', theme)
  }

  // 切换主题
  const setTheme = (theme) => {
    if (!Object.values(THEMES).includes(theme)) {
      console.warn(`未知主题: ${theme}`)
      return
    }
    currentTheme.value = theme
    applyTheme(theme)
    localStorage.setItem('evan-theme', theme)
  }

  // 切换亮/暗模式（保持当前模式类型）
  const toggleDarkMode = () => {
    const isStudyMode = currentTheme.value.startsWith('study')
    const isDarkMode = currentTheme.value.endsWith('dark')

    if (isStudyMode) {
      setTheme(isDarkMode ? THEMES.STUDY_LIGHT : THEMES.STUDY_DARK)
    } else {
      setTheme(isDarkMode ? THEMES.COZY_LIGHT : THEMES.COZY_DARK)
    }
  }

  // 切换模式类型（保持当前亮/暗）
  const toggleModeType = () => {
    const isDarkMode = currentTheme.value.endsWith('dark')
    const isStudyMode = currentTheme.value.startsWith('study')

    if (isDarkMode) {
      setTheme(isStudyMode ? THEMES.COZY_DARK : THEMES.STUDY_DARK)
    } else {
      setTheme(isStudyMode ? THEMES.COZY_LIGHT : THEMES.STUDY_LIGHT)
    }
  }

  // 获取当前主题信息
  const getThemeInfo = () => {
    return {
      theme: currentTheme.value,
      isDark: currentTheme.value.endsWith('dark'),
      isStudy: currentTheme.value.startsWith('study'),
      isCozy: currentTheme.value.startsWith('cozy')
    }
  }

  // 监听主题变化
  watch(currentTheme, (newTheme) => {
    applyTheme(newTheme)
  })

  return {
    THEMES,
    currentTheme,
    loadTheme,
    setTheme,
    toggleDarkMode,
    toggleModeType,
    getThemeInfo
  }
})
