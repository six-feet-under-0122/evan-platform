<template>
  <div id="app" class="min-h-screen bg-[--color-bg-primary] text-[--color-text-primary]">
    <router-view />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useTheme } from '@/composables/useTheme'

const { theme } = useTheme()

onMounted(() => {
  console.log('当前主题:', theme.value)
})
</script>

<style>
#app {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* 覆盖 Element UI 菜单组件的默认边框 */
.el-menu {
  border-right: none !important;
}

.el-sub-menu {
  border-right: none !important;
}
</style>