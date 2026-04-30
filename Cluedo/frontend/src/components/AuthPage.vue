<script setup>
import { ref, onMounted } from 'vue'
import AppHeader from './AppHeader.vue'
import AppFooter from './AppFooter.vue'
import Login from './Login.vue'
import Register from './Register.vue'

const isLogin = ref(true)

onMounted(() => {
  const path = window.location.pathname
  if (path.includes('register')) {
    isLogin.value = false
  }
})

const switchToRegister = () => {
  isLogin.value = false
  window.history.pushState({}, '', '/static/register')
}

const switchToLogin = () => {
  isLogin.value = true
  window.history.pushState({}, '', '/static/login')
}
</script>

<template>
  <div class="caso-abierto-body">
    <AppHeader :activePage="isLogin ? 'login' : 'register'" :badgeText="isLogin ? 'Accés Segur' : 'Nou Agent'" />

    <main class="container py-5 my-5 d-flex justify-content-center align-items-center auth-main">
      <Login v-if="isLogin" @switch-to-register="switchToRegister" />
      <Register v-else @switch-to-login="switchToLogin" />
    </main>

    <AppFooter />
  </div>
</template>

<style scoped>
.caso-abierto-body {
  --bg-deep: #13111C;
  --bg-mid: #1E1B2E;
  --bg-panel: #2D2A45;
  --gold: #D4AF7A;
  --gold-dim: #8A6D3B;
  --crimson: #C0392B;
  --crimson-dk: #7B1F16;
  --cream: #F0EAD6;
  --muted: #7A738F;
  --border: rgba(212, 175, 122, 0.18);
  --border-hv: rgba(212, 175, 122, 0.45);
  
  background: var(--bg-deep);
  color: var(--cream);
  font-family: 'IBM Plex Mono', monospace;
  min-height: 100vh;
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
}

.caso-abierto-body::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.06'/%3E%3C/svg%3E");
  pointer-events: none;
  z-index: -2;
  opacity: 0.35;
}

.caso-abierto-body::after {
  content: '';
  position: fixed;
  inset: 0;
  background: radial-gradient(ellipse at center, transparent 40%, rgba(13, 11, 20, 0.7) 100%);
  pointer-events: none;
  z-index: -1;
}

.auth-main {
  flex-grow: 1;
}
</style>
