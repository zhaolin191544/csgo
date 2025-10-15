<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'

// 响应式变量，用于存储经过的秒数
const seconds = ref(0)
let interval = null

// 计算属性，将秒数格式化为 MM:SS 格式
const formattedTime = computed(() => {
  const mins = Math.floor(seconds.value / 60)
  const secs = seconds.value % 60
  // 使用 padStart 确保数字总是两位数，例如 01, 09
  return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`
})

// 组件挂载时，启动一个每秒更新一次的定时器
onMounted(() => {
  interval = setInterval(() => {
    seconds.value++
  }, 1000)
})

// 组件卸载时，清除定时器以防止内存泄漏
onUnmounted(() => {
  if (interval) {
    clearInterval(interval)
  }
})
</script>

<template>
  <div class="fixed top-4 right-4 p-2 text-sm bg-gray-500/10 rounded-md">
    <span>{{ formattedTime }}</span>
  </div>
</template>