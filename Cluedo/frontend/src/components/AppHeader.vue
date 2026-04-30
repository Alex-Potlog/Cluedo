<script setup>
import { ref, onMounted } from 'vue'
import { getUrl } from '../utils.js'
import { postApi } from '../api.js'

defineProps({
  activePage: String,
  badgeText: String
})

const isAuthenticated = ref(false)
const username = ref('')

onMounted(async () => {
  try {
    const response = await fetch('/api/status/', { credentials: 'include' })
    const data = await response.json()
    if (data.is_authenticated) {
      isAuthenticated.value = true
      username.value = data.username
    }
  } catch (error) {
    console.error('Error checking auth status:', error)
  }
})

const handleLogout = async () => {
  try {
    const response = await postApi('/api/logout/', {})
    if (response.ok) {
      isAuthenticated.value = false
      username.value = ''
      window.location.reload()
    }
  } catch (error) {
    console.error('Error logging out:', error)
  }
}
</script>

<template>
  <header class="d-flex align-items-center justify-content-between p-3 sticky-top main-header">
    <a :href="getUrl('/')" class="logo d-flex align-items-center gap-2 text-decoration-none">
      <div class="logo-dot"></div>
      CasoAbierto
    </a>
    <nav class="d-none d-md-flex align-items-center gap-4">
      <a :href="getUrl('/')" :class="{ active: activePage === 'joc' }">El Joc</a>
      <a :href="getUrl('/com-jugar')" :class="{ active: activePage === 'com-jugar' }">Com Jugar</a>
      <a :href="getUrl('/users')" :class="{ active: activePage === 'expedient' }">Expedient</a>
    </nav>
    <div class="header-right d-flex align-items-center gap-3">
      <div v-if="badgeText" class="header-badge">{{ badgeText }}</div>
      <div class="user-actions">
        <template v-if="isAuthenticated">
          <a href="#" @click.prevent="handleLogout" class="user-icon-link" title="Tancar Sessió">
            <i class="bi bi-box-arrow-right fs-4"></i>
          </a>
        </template>
        <template v-else>
          <a :href="getUrl('/login')" class="user-icon-link" title="Iniciar Sessió o Registre">
            <i class="bi bi-person-circle fs-4"></i>
          </a>
        </template>
      </div>
    </div>
  </header>
</template>

<style scoped>
.main-header {
  background: rgba(19, 17, 28, 0.92);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--border);
  height: 64px;
}
.logo {
  font-family: 'Special Elite', cursive;
  font-size: 1.35rem;
  color: var(--gold);
  letter-spacing: 0.05em;
}
.logo-dot {
  width: 8px;
  height: 8px;
  background: var(--crimson);
  border-radius: 50%;
  box-shadow: 0 0 6px var(--crimson);
  animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(0.7); }
}
nav a {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.72rem;
  font-weight: 400;
  color: var(--muted);
  text-decoration: none;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  transition: color 0.2s;
  padding-bottom: 2px;
  border-bottom: 1px solid transparent;
}
nav a:hover, nav a.active {
  color: var(--gold);
  border-bottom-color: var(--gold);
}
.user-icon-link {
  color: var(--crimson);
  transition: all 0.2s ease-in-out;
  display: flex;
  align-items: center;
}
.user-icon-link:hover {
  color: var(--gold);
  transform: scale(1.1);
}
.header-badge {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.65rem;
  background: var(--crimson-dk);
  color: var(--cream);
  border: 1px solid var(--crimson);
  padding: 3px 10px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}
</style>