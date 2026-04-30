<template>
  <div class="auth-container">
    <div class="card auth-card p-4 mx-auto mt-5">
      <h2 class="text-center mb-4 author-title">Registre</h2>
      <div v-if="errorMsg" class="alert alert-danger text-center" style="font-family: 'IBM Plex Mono', monospace; font-size: 0.8rem; background: rgba(192,57,43,0.1); color: var(--crimson); border-color: var(--crimson);">
        {{ errorMsg }}
      </div>
      <form @submit.prevent="handleRegister">
        <div class="mb-3">
          <label for="regName" class="form-label auth-label">Nom d'usuari</label>
          <input type="text" class="form-control auth-input" id="regName" v-model="username" required>
        </div>
        <div class="mb-3">
          <label for="regEmail" class="form-label auth-label">Correu Electrònic</label>
          <input type="email" class="form-control auth-input" id="regEmail" v-model="email" required>
        </div>
        <div class="mb-4">
          <label for="regPassword" class="form-label auth-label">Contrasenya</label>
          <input type="password" class="form-control auth-input" id="regPassword" v-model="password" required>
        </div>
        <button type="submit" class="btn auth-btn w-100">Crear Compte</button>
      </form>
      <div class="text-center mt-3">
        <a href="#" @click.prevent="$emit('switch-to-login')" class="auth-link">Ja tens compte? Inicia sessió</a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { postApi } from '../api.js'

const username = ref('')
const email = ref('')
const password = ref('')
const errorMsg = ref('')

defineEmits(['switch-to-login'])

const handleRegister = async () => {
  errorMsg.value = ''
  
  if (password.value.length < 8) {
    errorMsg.value = 'La contrasenya ha de tenir almenys 8 caràcters.'
    return
  }

  try {
    const response = await postApi('/api/register/', {
      username: username.value,
      email: email.value,
      password: password.value
    })
    const data = await response.json()
    
    if (response.ok && data.success) {
      window.location.href = '/static/' // Redirect to home
    } else {
      errorMsg.value = data.message || 'Error en el registre'
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
