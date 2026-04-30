<script setup>
import { computed } from 'vue'
import Index from './components/Index.vue'
import ComJugar from './components/ComJugar.vue'
import Users from './components/Users.vue'
import AuthPage from './components/AuthPage.vue'

const currentView = computed(() => {
  const path = window.location.pathname
  if (path.includes('com-jugar')) return ComJugar
  if (path.includes('users') || path.includes('expedient')) return Users
  if (path.includes('login') || path.includes('register')) return AuthPage
  return Index
})
</script>

<template>
  <component :is="currentView" />
</template>
