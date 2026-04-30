<template>
  <div class="auth-container">
    <div class="card auth-card p-4 mx-auto mt-5">
      <h2 class="text-center mb-4 author-title">Iniciar Sessió</h2>
      <div v-if="errorMsg" class="alert alert-danger text-center" style="font-family: 'IBM Plex Mono', monospace; font-size: 0.8rem; background: rgba(192,57,43,0.1); color: var(--crimson); border-color: var(--crimson);">
        {{ errorMsg }}
      </div>
      <form @submit.prevent="handleLogin">
        <div class="mb-3">
          <label for="loginEmail" class="form-label auth-label">Correu Electrònic</label>
          <input type="email" class="form-control auth-input" id="loginEmail" v-model="email" required>
        </div>
        <div class="mb-4">
          <label for="loginPassword" class="form-label auth-label">Contrasenya</label>
          <input type="password" class="form-control auth-input" id="loginPassword" v-model="password" required>
        </div>
        <button type="submit" class="btn auth-btn w-100">Entrar</button>
      </form>
      <div class="text-center mt-3">
        <a href="#" @click.prevent="$emit('switch-to-register')" class="auth-link">No tens compte? Registra't</a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { postApi } from '../api.js'

const email = ref('')
const password = ref('')
const errorMsg = ref('')

defineEmits(['switch-to-register'])

const handleLogin = async () => {
  errorMsg.value = ''
  try {
    const response = await postApi('/api/login/', {
      email: email.value,
      password: password.value
    })
    const data = await response.json()
    
    if (response.ok && data.success) {
      window.location.href = '/static/' // Redirect to home
    } else {
      errorMsg.value = data.message || "Error d'autenticació"
    }
  } catch (error) {
    errorMsg.value = 'Error de connexió'
  }
}
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem 0;
}
.auth-card {
  background: rgba(19, 17, 28, 0.92);
  border: 1px solid var(--border);
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.5);
  max-width: 400px;
  width: 100%;
}
.author-title {
  font-family: 'Special Elite', cursive;
  color: var(--gold);
}
.auth-label {
  font-family: 'IBM Plex Mono', monospace;
  color: var(--muted);
  font-size: 0.85rem;
}
.auth-input {
  background: rgba(10, 8, 16, 0.8);
  border: 1px solid var(--border);
  color: var(--cream);
}
.auth-input:focus {
  background: rgba(10, 8, 16, 1);
  border-color: var(--gold);
  box-shadow: 0 0 5px rgba(212, 175, 55, 0.3);
  color: var(--cream);
}
.auth-btn {
  background: var(--crimson-dk);
  color: var(--cream);
  border: 1px solid var(--crimson);
  font-family: 'IBM Plex Mono', monospace;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  transition: all 0.2s;
}
.auth-btn:hover {
  background: var(--crimson);
  color: white;
  box-shadow: 0 0 10px rgba(121, 26, 31, 0.5);
}
.auth-link {
  color: var(--muted);
  text-decoration: none;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.8rem;
  transition: color 0.2s;
}
.auth-link:hover {
  color: var(--gold);
}
</style>
