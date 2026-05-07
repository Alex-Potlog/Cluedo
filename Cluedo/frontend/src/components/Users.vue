<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { getUrl } from '../utils.js'
import AppHeader from './AppHeader.vue'

// ---------------- Estat ----------------
const username = ref('')
const isAuthenticated = ref(false)
const perfil = ref(null) // { id_agencia, data_ingres }
const casActiu = ref(null) // cas amb intents
const casosTancats = ref([]) // historial
const carregant = ref(true)

const segons = ref(0)
let timerInterval = null

const pad = (n) => String(n).padStart(2, '0')

const tempsFormatejat = computed(() => {
  const h = Math.floor(segons.value / 3600)
  const m = Math.floor((segons.value % 3600) / 60)
  const s = segons.value % 60
  return `${pad(h)}:${pad(m)}:${pad(s)}`
})

// ---------------- Helpers ----------------
const formatDuracio = (totalSegons) => {
  if (!totalSegons && totalSegons !== 0) return '--:--:--'
  const h = Math.floor(totalSegons / 3600)
  const m = Math.floor((totalSegons % 3600) / 60)
  const s = totalSegons % 60
  return `${pad(h)}:${pad(m)}:${pad(s)}`
}

const formatDataCurta = (iso) => {
  if (!iso) return ''
  try {
    const d = new Date(iso)
    return `${pad(d.getDate())}/${pad(d.getMonth() + 1)}/${d.getFullYear()}`
  } catch (e) {
    return iso
  }
}

const formatMesAny = (iso) => {
  if (!iso) return ''
  try {
    const d = new Date(iso)
    return `${pad(d.getMonth() + 1)}.${d.getFullYear()}`
  } catch (e) {
    return iso
  }
}

const fa = (iso) => {
  if (!iso) return ''
  const ara = new Date()
  const d = new Date(iso)
  const diff = Math.max(0, Math.floor((ara - d) / 1000))
  if (diff < 60) return `fa ${diff}s`
  if (diff < 3600) return `fa ${Math.floor(diff / 60)} min`
  if (diff < 86400) return `fa ${Math.floor(diff / 3600)} h`
  return `fa ${Math.floor(diff / 86400)} d`
}

// ---------------- Càrrega de dades ----------------
const carregarStatus = async () => {
  try {
    const resp = await fetch('/api/status/', { credentials: 'include' })
    const data = await resp.json()
    isAuthenticated.value = !!data.is_authenticated
    if (data.is_authenticated) username.value = data.username
  } catch (err) {
    console.error('Error carregant status:', err)
  }
}

const carregarCasActiu = async () => {
  try {
    const resp = await fetch('/api/cas/active/', { credentials: 'include' })
    const data = await resp.json()
    if (data && data.success) {
      casActiu.value = data.cas
    }
  } catch (err) {
    console.error('Error carregant cas actiu:', err)
  }
}

const carregarHistorial = async () => {
  try {
    const resp = await fetch('/api/cas/history/', { credentials: 'include' })
    const data = await resp.json()
    if (data && data.success) {
      perfil.value = data.perfil
      casosTancats.value = data.casos || []
    }
  } catch (err) {
    console.error('Error carregant historial:', err)
  }
}

// ---------------- Cronòmetre ----------------
const iniciarCronometre = () => {
  if (timerInterval) clearInterval(timerInterval)
  if (!casActiu.value || !casActiu.value.iniciat_el) {
    segons.value = 0
    return
  }
  const inici = new Date(casActiu.value.iniciat_el).getTime()
  const update = () => {
    segons.value = Math.max(0, Math.floor((Date.now() - inici) / 1000))
  }
  update()
  timerInterval = setInterval(update, 1000)
}

onMounted(async () => {
  carregant.value = true
  await carregarStatus()
  if (isAuthenticated.value) {
    await Promise.all([carregarCasActiu(), carregarHistorial()])
    iniciarCronometre()
  }
  carregant.value = false
})

onUnmounted(() => {
  if (timerInterval) clearInterval(timerInterval)
})

// ---------------- Computed: estadístiques i visuals ----------------
const intentsCasActiu = computed(() => (casActiu.value ? casActiu.value.intents || [] : []))
const intentsUsats = computed(() => (casActiu.value ? casActiu.value.intents_usats : 0))
const intentsMax = computed(() => (casActiu.value ? casActiu.value.intents_max : 5))
const dotsIntents = computed(() => {
  const total = intentsMax.value
  return Array.from({ length: total }, (_, i) => i < intentsUsats.value)
})
const percentIntents = computed(() => {
  if (!intentsMax.value) return 0
  return Math.round((intentsUsats.value / intentsMax.value) * 100)
})

const totalCasos = computed(() => {
  return (casosTancats.value.length) + (casActiu.value ? 1 : 0)
})
const casosResolts = computed(() => casosTancats.value.filter((c) => c.estat === 'resolt').length)
const casosArxivats = computed(() => casosTancats.value.filter((c) => c.estat === 'arxivat').length)
const precisio = computed(() => {
  const total = casosTancats.value.length
  if (total === 0) return null
  return Math.round((casosResolts.value / total) * 100)
})

const millorTemps = computed(() => {
  const resolts = casosTancats.value.filter((c) => c.estat === 'resolt' && c.segons_acumulats)
  if (resolts.length === 0) return null
  return Math.min(...resolts.map((c) => c.segons_acumulats))
})

const tempsMig = computed(() => {
  const resolts = casosTancats.value.filter((c) => c.estat === 'resolt' && c.segons_acumulats)
  if (resolts.length === 0) return null
  const suma = resolts.reduce((acc, c) => acc + c.segons_acumulats, 0)
  return Math.round(suma / resolts.length)
})

const codiCas = (id) => `#${String(id).padStart(4, '0')}`

const titolCasActiu = computed(() => {
  if (!casActiu.value) return ''
  return `Cas ${codiCas(casActiu.value.id)} — ${casActiu.value.titol || 'Investigació en curs'}`
})

const inicialsBadge = computed(() => {
  if (!username.value) return ''
  return username.value.slice(0, 2).toUpperCase()
})

const nomMostrar = computed(() => username.value || 'Agent')
</script>

<template>
  <div class="caso-abierto-body">
    <AppHeader activePage="expedient" badgeText="Perfil Agent" />

    <!-- Avis si no autenticat -->
    <section v-if="!carregant && !isAuthenticated" class="container py-5 my-5 text-center">
      <h2 class="section-title mb-3">Accés restringit</h2>
      <p class="profile-rank mb-4">Cal iniciar sessió per veure el teu expedient.</p>
      <a :href="getUrl('/login')" class="btn-play d-inline-block px-4 py-2 text-decoration-none">Iniciar sessió</a>
    </section>

    <template v-else>
    <!-- PROFILE HERO -->
    <section class="profile-hero p-5 overflow-hidden position-relative">
      <div class="profile-hero-inner container position-relative z-1 d-flex flex-column flex-md-row align-items-md-start gap-4">

        <div class="agent-badge d-flex align-items-center justify-content-center position-relative flex-shrink-0">
          <span v-if="inicialsBadge" class="badge-text">{{ inicialsBadge }}</span>
          <i v-else class="bi bi-incognito"></i>
        </div>

        <div class="profile-info flex-grow-1">
          <div class="profile-stamp d-inline-block mb-3">Dossier Confidencial · Agent Assignat</div>
          <h1 class="profile-name mb-2">{{ nomMostrar }}</h1>
          <p class="profile-rank mb-4">// Agent · Cluedo Digital</p>
          <div class="profile-meta d-flex gap-4 flex-wrap">
            <div class="meta-item">
              <span class="meta-label d-block text-uppercase mb-1">ID Agència</span>
              <span class="meta-value">{{ perfil ? perfil.id_agencia : '—' }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label d-block text-uppercase mb-1">Data d'Ingrés</span>
              <span class="meta-value">{{ perfil ? formatMesAny(perfil.data_ingres) : '—' }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label d-block text-uppercase mb-1">Estat</span>
              <span class="meta-value" :style="{ color: casActiu ? 'var(--crimson)' : 'var(--muted)' }">
                ● {{ casActiu ? 'Investigació Activa' : 'Sense cas actiu' }}
              </span>
            </div>
          </div>
        </div>

        <div class="profile-stats d-flex gap-3 flex-wrap">
          <div class="stat-box p-3 text-center border">
            <span class="stat-num d-block fw-bold text-gold">{{ totalCasos }}</span>
            <span class="stat-lbl d-block text-uppercase mt-2 text-gold">Casos Totals</span>
          </div>
          <div class="stat-box p-3 text-center border">
            <span class="stat-num d-block fw-bold text-success">{{ casosResolts }}</span>
            <span class="stat-lbl d-block text-uppercase mt-2 text-success">Resolts</span>
          </div>
          <div class="stat-box p-3 text-center border">
            <span class="stat-num d-block fw-bold text-danger">{{ casosArxivats }}</span>
            <span class="stat-lbl d-block text-uppercase mt-2 text-danger">Fracassos</span>
          </div>
          <div v-if="precisio !== null" class="stat-box p-3 text-center border">
            <span class="stat-num d-block fw-bold text-gold">{{ precisio }}%</span>
            <span class="stat-lbl d-block text-uppercase text-muted mt-2 text-gold">Precisió</span>
          </div>
        </div>

      </div>
    </section>

    <!-- MAIN + SIDEBAR -->
    <div class="container py-5 my-5 page-wrap">
      <div class="row g-5">
        <!-- COLUMNA PRINCIPAL -->
        <main class="col-lg-8 animate-fade-up">

          <!-- Cas Actiu -->
          <div v-if="casActiu" class="active-case-panel p-4 mb-4 position-relative border bg-mid">
            <p class="case-title m-0 mt-3 mb-2">{{ titolCasActiu }}</p>
            <p class="case-sub mb-4">// Iniciat {{ fa(casActiu.iniciat_el) }} · Solució Secreta en custòdia del sistema</p>

            <div class="progress-block mb-4">
              <div class="progress-label d-flex justify-content-between mb-2 text-uppercase">
                <span>Intents usats</span>
                <strong>{{ intentsUsats }} / {{ intentsMax }}</strong>
              </div>
              <div class="progress-track w-100 position-relative">
                <div class="progress-fill h-100" :style="{ width: percentIntents + '%' }"></div>
              </div>
            </div>

            <div class="dots-row d-flex gap-2 mb-4">
              <div
                v-for="(usat, idx) in dotsIntents"
                :key="idx"
                class="dot rounded-circle border"
                :class="{ used: usat }"
              ></div>
            </div>

            <a :href="getUrl('/')" class="btn-play w-100 p-3 text-center text-decoration-none border-0 text-uppercase fw-bold"><i class="bi bi-scales me-2"></i>Continuar Investigació</a>
          </div>

          <div v-else class="active-case-panel p-4 mb-4 position-relative border bg-mid">
            <p class="case-title m-0 mt-3 mb-2">Sense cas actiu</p>
            <p class="case-sub mb-4">// No tens cap investigació oberta. Comença'n una.</p>
            <a :href="getUrl('/')" class="btn-play w-100 p-3 text-center text-decoration-none border-0 text-uppercase fw-bold"><i class="bi bi-plus-lg me-2"></i>Començar Cas</a>
          </div>

          <!-- Cronòmetre -->
          <div v-if="casActiu" class="timer-panel p-4 mb-5 position-relative border bg-mid d-flex flex-column flex-md-row justify-content-md-between align-items-md-center gap-3">
            <div>
              <div class="timer-display" id="timer">{{ tempsFormatejat }}</div>
              <div class="timer-label text-uppercase">temps acumulat en aquest cas</div>
            </div>
            <div class="timer-status border px-3 py-1 text-uppercase d-flex align-items-center justify-content-center gap-2">
              En Curs
            </div>
          </div>

          <!-- Historial d'intents del cas actiu -->
          <template v-if="casActiu">
            <div class="section-label mb-2">// Arxiu d'Interrogatoris</div>
            <h2 class="section-title mb-4">Historial <em>d'Intents</em></h2>

            <div class="panel position-relative border bg-mid p-4 mb-4">
              <div class="panel-tag position-absolute text-uppercase border-bottom-0 p-1 px-3">Cas Actual · {{ codiCas(casActiu.id) }}</div>
              <ul v-if="intentsCasActiu.length" class="attempt-list list-unstyled mt-3 mb-0">
                <li
                  v-for="intent in intentsCasActiu"
                  :key="intent.numero"
                  class="attempt-item d-flex align-items-center gap-3 p-3 border mb-2 bg-panel"
                >
                  <div class="attempt-num fw-bold pb-1 px-2 text-center">{{ pad(intent.numero) }}</div>
                  <div class="attempt-details flex-grow-1">
                    <div class="attempt-combo mb-1">
                      <span :class="{ 'text-gold': intent.encerta_acusado }">{{ intent.acusado }}</span> ·
                      <span :class="{ 'text-gold': intent.encerta_arma }">{{ intent.arma }}</span> ·
                      <span :class="{ 'text-gold': intent.encerta_lugar }">{{ intent.lugar }}</span>
                    </div>
                    <div class="attempt-hints d-flex gap-2 flex-wrap mt-1">
                      <span v-if="intent.encerta_acusado" class="hint-chip text-uppercase">sospitós correcte</span>
                      <span v-if="intent.encerta_arma" class="hint-chip text-uppercase">arma correcta</span>
                      <span v-if="intent.encerta_lugar" class="hint-chip text-uppercase">habitació correcta</span>
                    </div>
                    <div class="attempt-time mt-1">{{ fa(intent.creat_el) }} · {{ formatDuracio(intent.segons_des_inici) }}</div>
                  </div>
                  <div
                    class="attempt-result text-uppercase border px-2 py-1"
                    :class="{
                      success: intent.resultat === 'correcte',
                      partial: intent.resultat === 'parcial',
                      fail: intent.resultat === 'incorrecte'
                    }"
                  >
                    {{
                      intent.resultat === 'correcte' ? 'Correcte'
                      : intent.resultat === 'parcial' ? 'Parcialment Correcte'
                      : 'Incorrecte'
                    }}
                  </div>
                </li>
              </ul>
              <p v-else class="text-muted mt-3 mb-0" style="font-family: 'IBM Plex Mono', monospace; font-size: 0.75rem;">
                Encara no has fet cap intent en aquest cas.
              </p>
            </div>
          </template>

          <div class="divider d-flex align-items-center gap-3 my-5"><span>casos anteriors</span></div>

          <!-- Casos anteriors -->
          <div class="panel position-relative border bg-mid p-4 mb-4">
            <div class="panel-tag position-absolute text-uppercase border-bottom-0 p-1 px-3">Arxiu Tancat</div>
            <ul v-if="casosTancats.length" class="attempt-list list-unstyled mt-3 mb-0">
              <li
                v-for="c in casosTancats"
                :key="c.id"
                class="attempt-item d-flex align-items-center gap-3 p-3 border mb-2 bg-panel"
              >
                <div
                  class="attempt-num fw-bold pb-1 px-2 text-center"
                  :class="c.estat === 'resolt' ? 'text-success-custom' : 'text-danger-custom'"
                >
                  <i :class="c.estat === 'resolt' ? 'bi bi-check-lg' : 'bi bi-x-lg'"></i>
                </div>
                <div class="attempt-details flex-grow-1">
                  <div class="attempt-combo mb-1">
                    Cas {{ codiCas(c.id) }} —
                    <template v-if="c.solucio">
                      <span>{{ c.solucio.acusado }}</span> · {{ c.solucio.arma }} · {{ c.solucio.lugar }}
                    </template>
                  </div>
                  <div class="attempt-time">
                    {{ formatDataCurta(c.finalitzat_el || c.iniciat_el) }} ·
                    <template v-if="c.estat === 'resolt'">
                      Resolt en {{ c.intents_usats }} intent{{ c.intents_usats === 1 ? '' : 's' }} · {{ formatDuracio(c.segons_acumulats) }}
                    </template>
                    <template v-else>
                      Esgotat · {{ c.intents_usats }} intents
                    </template>
                  </div>
                </div>
                <div
                  class="attempt-result text-uppercase border px-2 py-1"
                  :class="c.estat === 'resolt' ? 'success' : 'fail'"
                >
                  {{ c.estat === 'resolt' ? 'CAS TANCAT' : 'ARXIVAT' }}
                </div>
              </li>
            </ul>
            <p v-else class="text-muted mt-3 mb-0" style="font-family: 'IBM Plex Mono', monospace; font-size: 0.75rem;">
              Encara no tens casos tancats a l'arxiu.
            </p>
          </div>
        </main>

        <!-- SIDEBAR -->
        <aside class="col-lg-4 sidebar animate-fade-up-delay">

          <!-- Estadístiques -->
          <div class="stats-card p-4 mb-4 border position-relative bg-mid">
            <div class="stats-card-tag position-absolute text-uppercase p-1 px-3 border border-bottom-0">ESTADÍSTIQUES</div>
            <div class="mt-4 pt-1">
              <div v-if="millorTemps !== null" class="stat-row d-flex justify-content-between py-2 border-bottom">
                <span class="stat-row-label">Millor temps</span>
                <span class="stat-row-val text-gold">{{ formatDuracio(millorTemps) }}</span>
              </div>
              <div v-if="tempsMig !== null" class="stat-row d-flex justify-content-between py-2 border-bottom">
                <span class="stat-row-label">Temps mitjà</span>
                <span class="stat-row-val text-cream">{{ formatDuracio(tempsMig) }}</span>
              </div>
              <div class="stat-row d-flex justify-content-between py-2 border-bottom">
                <span class="stat-row-label">Casos totals</span>
                <span class="stat-row-val text-cream">{{ totalCasos }}</span>
              </div>
              <div class="stat-row d-flex justify-content-between py-2 border-bottom">
                <span class="stat-row-label">Resolts</span>
                <span class="stat-row-val text-success-custom">{{ casosResolts }}</span>
              </div>
              <div class="stat-row d-flex justify-content-between py-2 border-bottom">
                <span class="stat-row-label">Arxivats</span>
                <span class="stat-row-val text-danger-custom">{{ casosArxivats }}</span>
              </div>
              <div v-if="precisio !== null" class="stat-row d-flex justify-content-between py-2">
                <span class="stat-row-label">Ràtio resolució</span>
                <span class="stat-row-val text-cream">{{ precisio }}%</span>
              </div>
            </div>
          </div>
        </aside>
      </div>
    </div>
    </template>

    <!-- FOOTER -->
    <footer class="d-flex flex-wrap align-items-center justify-content-between p-4 border-top shadow-sm">
      <div class="footer-logo mb-3 mb-md-0 d-block">
        CasoAbierto
        <span class="d-block mt-1">Operació Full-Stack · Django + Vue.js</span>
      </div>
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
  </div>
</template>


<!--BOOTSTAP PER DEFECTE (sense contar colors)-->
<style scoped> 
@import url('https://fonts.googleapis.com/css2?family=Special+Elite&family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=IBM+Plex+Mono:wght@300;400;500&display=swap');

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

.profile-hero {
  background: var(--bg-mid);
  border-bottom: 1px solid var(--border);
}

.profile-hero::before {
  content: '';
  position: absolute; inset: 0;
  background-image: repeating-linear-gradient(0deg, transparent, transparent 39px, rgba(212, 175, 122, 0.03) 39px, rgba(212, 175, 122, 0.03) 40px),
                    repeating-linear-gradient(90deg, transparent, transparent 39px, rgba(212, 175, 122, 0.03) 39px, rgba(212, 175, 122, 0.03) 40px);
  pointer-events: none;
  z-index: 0;
}

.agent-badge {
  width: 110px; height: 110px;
  border: 2px solid var(--gold-dim);
  background: var(--bg-panel);
  font-size: 3rem;
}

.badge-text {
  font-family: 'Playfair Display', serif;
  font-size: 2rem;
  color: var(--gold);
  font-weight: 700;
  letter-spacing: 0.1em;
}

.agent-badge::after {
  content: 'AGENT';
  position: absolute; bottom: -12px; left: 50%; transform: translateX(-50%);
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.55rem;
  letter-spacing: 0.2em;
  background: var(--crimson);
  color: #fff;
  padding: 2px 8px;
  white-space: nowrap;
}

.profile-stamp {
  font-family: 'Special Elite', cursive;
  font-size: 0.62rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--crimson);
  border: 1px solid var(--crimson);
  padding: 3px 12px;
  transform: rotate(-1deg);
  opacity: 0.85;
}

.profile-name {
  font-family: 'Playfair Display', serif;
  font-size: clamp(1.8rem, 4vw, 2.8rem);
  font-weight: 700;
  color: var(--cream);
  line-height: 1;
}

.profile-name span { color: var(--gold); font-style: italic; }

.profile-rank {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.7rem;
  color: var(--muted);
  letter-spacing: 0.2em;
  text-transform: uppercase;
}

.meta-label { font-size: 0.58rem; letter-spacing: 0.2em; color: var(--gold-dim); }
.meta-value { font-family: 'Special Elite', cursive; font-size: 0.95rem; color: var(--cream); }

.stat-box { min-width: 90px; background: var(--bg-panel); border-color: var(--border) !important; }
.stat-num { font-family: 'Playfair Display', serif; font-size: 2rem; line-height: 1; }
.stat-lbl { font-family: 'IBM Plex Mono', monospace; font-size: 0.58rem; letter-spacing: 0.15em; }

.bg-mid { background-color: var(--bg-mid); }
.bg-panel { background-color: var(--bg-panel); }
.border { border-color: var(--border) !important; }

/* Cas Actiu */
.active-case-panel::before {
  content: 'CAS EN CURS';
  position: absolute; top: -1px; left: 1.5rem;
  background: var(--crimson-dk);
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.58rem;
  letter-spacing: 0.18em;
  color: var(--cream);
  padding: 3px 12px;
  border: 1px solid var(--crimson);
  border-top: none;
  text-transform: uppercase;
}
.case-title { font-family: 'Special Elite', cursive; font-size: 1.1rem; color: var(--gold); }
.case-sub { font-family: 'IBM Plex Mono', monospace; font-size: 0.68rem; color: var(--muted); letter-spacing: 0.1em; }
.progress-label { font-family: 'IBM Plex Mono', monospace; font-size: 0.62rem; letter-spacing: 0.12em; color: var(--muted); }
.progress-track { height: 4px; background: var(--bg-panel); }
.progress-fill { background: linear-gradient(90deg, var(--gold-dim), var(--gold)); transition: width 0.4s ease; }

.dot { width: 11px; height: 11px; border-color: var(--gold-dim) !important; }
.dot.used { background: var(--crimson); border-color: var(--crimson) !important; }

.btn-play {
  font-family: 'Special Elite', cursive;
  font-size: 1rem; letter-spacing: 0.2em;
  color: var(--bg-deep); background: var(--gold);
  transition: background 0.2s, letter-spacing 0.2s;
  display: block; cursor: pointer;
}
.btn-play:hover { background: #e8c88a; letter-spacing: 0.28em; }

/* Cronometre */
.timer-panel::before {
  content: 'TEMPS DE RESOLUCIÓ';
  position: absolute; top: -1px; left: 2rem;
  background: var(--bg-panel);
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.58rem; letter-spacing: 0.18em;
  color: var(--gold-dim); padding: 3px 12px;
  border: 1px solid var(--border); border-top: none;
}
.timer-display { font-family: 'IBM Plex Mono', monospace; font-size: 2rem; font-weight: 500; color: var(--gold); letter-spacing: 0.1em; }
.timer-label { font-family: 'IBM Plex Mono', monospace; font-size: 0.62rem; letter-spacing: 0.15em; color: var(--muted); }
.timer-status {
  font-family: 'IBM Plex Mono', monospace; font-size: 0.65rem; letter-spacing: 0.1em;
  color: var(--crimson); border-color: var(--crimson) !important;
}
.timer-status::before {
  content: ''; width: 6px; height: 6px; background: var(--crimson);
  border-radius: 50%; animation: pulse 1.2s ease-in-out infinite; margin-right: 4px;
}

/* Intents */
.section-label { font-family: 'IBM Plex Mono', monospace; font-size: 0.62rem; letter-spacing: 0.28em; text-transform: uppercase; color: var(--crimson); }
.section-title { font-family: 'Playfair Display', serif; font-size: clamp(1.2rem, 2.5vw, 1.7rem); font-weight: 700; color: var(--cream); }
.section-title em { color: var(--gold); font-style: italic; }

.panel-tag {
  top: -1px; left: 2rem; background: var(--bg-panel);
  font-family: 'IBM Plex Mono', monospace; font-size: 0.58rem; letter-spacing: 0.18em;
  color: var(--gold-dim); border-color: var(--border) !important; border-top: none;
}
.attempt-item { transition: border-color 0.2s; }
.attempt-item:hover { border-color: var(--border-hv) !important; }
.attempt-num { font-family: 'Playfair Display', serif; font-size: 1.5rem; color: var(--bg-deep); min-width: 28px; }
.attempt-combo { font-family: 'Special Elite', cursive; font-size: 0.88rem; color: var(--cream); }
.attempt-combo span { color: var(--cream); }
.attempt-combo .text-gold { color: var(--gold) !important; }
.attempt-time { font-family: 'IBM Plex Mono', monospace; font-size: 0.62rem; color: var(--muted); letter-spacing: 0.1em; }

.attempt-result { font-family: 'IBM Plex Mono', monospace; font-size: 0.65rem; letter-spacing: 0.1em; }
.attempt-result.fail { color: var(--crimson); border-color: var(--crimson) !important; background: rgba(192,57,43,0.08); }
.attempt-result.success { color: #2ecc71; border-color: #27ae60 !important; background: rgba(39, 174, 96, 0.08); }
.attempt-result.partial { color: var(--gold); border-color: var(--gold-dim) !important; background: rgba(212,175,122,0.07); }

.hint-chip {
  font-family: 'IBM Plex Mono', monospace; font-size: 0.58rem; letter-spacing: 0.08em;
  padding: 2px 7px; border: 1px solid rgba(212,175,122,0.25); color: var(--gold-dim);
  background: rgba(212,175,122,0.05);
}

.divider::before, .divider::after { content: ''; flex: 1; height: 1px; background: var(--border); }
.divider span { font-family: 'IBM Plex Mono', monospace; font-size: 0.58rem; letter-spacing: 0.28em; text-transform: uppercase; color: var(--muted); }

/* Sidebar */
.rank-card-tag, .badges-card-tag, .stats-card-tag {
  top: -1px; left: 1.5rem; background: var(--bg-panel);
  font-family: 'IBM Plex Mono', monospace; font-size: 0.58rem; letter-spacing: 0.18em;
  color: var(--gold-dim); border-color: var(--border) !important;
}

.stat-row-label { font-family: 'IBM Plex Mono', monospace; font-size: 0.68rem; color: var(--muted); letter-spacing: 0.05em; }
.stat-row-val { font-family: 'Special Elite', cursive; font-size: 0.9rem; color: var(--cream); }

/* Utilitats de color personalitzades per mantenir el CSS existent */
.text-gold { color: var(--gold) !important; }
.text-success-custom { color: #2ecc71 !important; }
.text-danger-custom { color: #e74c3c !important; }
.text-cream { color: var(--cream) !important; }

/* Footer */
footer { background: rgba(13, 11, 20, 0.8); border-top-color: var(--border) !important; }
.footer-logo { font-family: 'Special Elite', cursive; font-size: 1rem; color: var(--gold); }
.footer-logo span { color: var(--muted); font-size: 0.7rem; font-family: 'IBM Plex Mono', monospace; }
.footer-links a { font-family: 'IBM Plex Mono', monospace; font-size: 0.65rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted); text-decoration: none; transition: color 0.2s; }
.footer-links a:hover { color: var(--gold); }
.footer-copy { font-family: 'IBM Plex Mono', monospace; font-size: 0.62rem; color: var(--muted); opacity: 0.5; letter-spacing: 0.05em; }

/* Animations */
.animate-fade-up { animation: fadeUp 0.5s ease 0.1s both; }
.animate-fade-up-delay { animation: fadeUp 0.5s ease 0.25s both; }
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(16px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 900px) {
  .sidebar { margin-top: 2rem; }
}
</style>
