<script setup>
import { getUrl } from '../utils.js'
</script>

<template>
  <footer class="d-flex flex-wrap align-items-center justify-content-between p-4 border-top shadow-sm">
    <a :href="getUrl('/')" class="footer-logo mb-3 mb-md-0 d-block text-decoration-none">
      CasoAbierto
      <span class="d-block mt-1">Operació Full-Stack · Django + Vue.js</span>
    </a>
    <div class="footer-links d-flex gap-3 mb-3 mb-md-0 flex-wrap">
      <a :href="getUrl('/')">El Joc</a>
      <a :href="getUrl('/com-jugar')">Com Jugar</a>
      <a :href="getUrl('/users')">Expedient</a>
      <a href="/admin">Admin</a>
    </div>
    <div class="footer-copy">
      Dossier Confidencial &mdash; Destrueix després de llegir
    </div>
  </footer>
</template>

<style scoped>
footer { background: rgba(13, 11, 20, 0.8); border-top: 1px solid var(--border); }
.footer-logo { font-family: 'Special Elite', cursive; font-size: 1rem; color: var(--gold); }
.footer-logo span { color: var(--muted); font-size: 0.7rem; font-family: 'IBM Plex Mono', monospace; }
.footer-links a { font-family: 'IBM Plex Mono', monospace; font-size: 0.65rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted); text-decoration: none; transition: color 0.2s; }
.footer-links a:hover { color: var(--gold); }
.footer-copy { font-family: 'IBM Plex Mono', monospace; font-size: 0.62rem; color: var(--muted); opacity: 0.5; letter-spacing: 0.05em; }
</style>