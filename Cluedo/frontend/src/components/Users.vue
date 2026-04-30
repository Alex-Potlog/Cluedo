<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { getUrl } from '../utils.js'
import AppHeader from './AppHeader.vue'

const segons = ref(12 * 60 + 47) // 12:47
let timerInterval = null

const pad = (n) => String(n).padStart(2, '0')

const tempsFormatejat = computed(() => {
  const h = Math.floor(segons.value / 3600)
  const m = Math.floor((segons.value % 3600) / 60)
  const s = segons.value % 60
  return `${pad(h)}:${pad(m)}:${pad(s)}`
})

onMounted(() => {
  timerInterval = setInterval(() => {
    segons.value++
  }, 1000)
})

onUnmounted(() => {
  if (timerInterval) clearInterval(timerInterval)
})
</script>

<template>
  <div class="caso-abierto-body">
    <AppHeader activePage="expedient" badgeText="Perfil Agent" />

    <!-- PROFILE HERO -->
    <section class="profile-hero p-5 overflow-hidden position-relative">
      <div class="profile-hero-inner container position-relative z-1 d-flex flex-column flex-md-row align-items-md-start gap-4">
        
        <div class="agent-badge d-flex align-items-center justify-content-center position-relative flex-shrink-0"><i class="bi bi-incognito"></i></div>

        <div class="profile-info flex-grow-1">
          <div class="profile-stamp d-inline-block mb-3">Dossier Confidencial · Agent Assignat</div>
          <h1 class="profile-name mb-2">Roger <span>Vidal</span></h1>
          <p class="profile-rank mb-4">// Inspector en Pràctiques · Rang 3</p>
          <div class="profile-meta d-flex gap-4 flex-wrap">
            <div class="meta-item">
              <span class="meta-label d-block text-uppercase mb-1">ID Agència</span>
              <span class="meta-value">AGT-00742</span>
            </div>
            <div class="meta-item">
              <span class="meta-label d-block text-uppercase mb-1">Data d'Ingrés</span>
              <span class="meta-value">04.2026</span>
            </div>
            <div class="meta-item">
              <span class="meta-label d-block text-uppercase mb-1">Estat</span>
              <span class="meta-value" style="color:var(--crimson)">● Investigació Activa</span>
            </div>
          </div>
        </div>

        <div class="profile-stats d-flex gap-3 flex-wrap">
          <div class="stat-box p-3 text-center border">
            <span class="stat-num d-block fw-bold text-gold">7</span>
            <span class="stat-lbl d-block text-uppercase text-muted mt-2">Casos Totals</span>
          </div>
          <div class="stat-box p-3 text-center border">
            <span class="stat-num d-block fw-bold text-success">3</span>
            <span class="stat-lbl d-block text-uppercase text-muted mt-2">Resolts</span>
          </div>
          <div class="stat-box p-3 text-center border">
            <span class="stat-num d-block fw-bold text-danger">4</span>
            <span class="stat-lbl d-block text-uppercase text-muted mt-2">Fracassos</span>
          </div>
          <div class="stat-box p-3 text-center border">
            <span class="stat-num d-block fw-bold text-gold">43%</span>
            <span class="stat-lbl d-block text-uppercase text-muted mt-2">Precisió</span>
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
          <div class="active-case-panel p-4 mb-4 position-relative border bg-mid">
            <p class="case-title m-0 mt-3 mb-2">Cas #0008 — La Mansió de les Ombres</p>
            <p class="case-sub mb-4">// Iniciat avui · Solució Secreta en custòdia del sistema</p>

            <div class="progress-block mb-4">
              <div class="progress-label d-flex justify-content-between mb-2 text-uppercase">
                <span>Intents usats</span>
                <strong>2 / 5</strong>
              </div>
              <div class="progress-track w-100 position-relative">
                <div class="progress-fill h-100" style="width: 40%"></div>
              </div>
            </div>

            <div class="dots-row d-flex gap-2 mb-4">
              <div class="dot used rounded-circle border"></div>
              <div class="dot used rounded-circle border"></div>
              <div class="dot rounded-circle border"></div>
              <div class="dot rounded-circle border"></div>
              <div class="dot rounded-circle border"></div>
            </div>

            <a href="#" class="btn-play w-100 p-3 text-center text-decoration-none border-0 text-uppercase fw-bold"><i class="bi bi-scales me-2"></i>Continuar Investigació</a>
          </div>

          <!-- Cronòmetre -->
          <div class="timer-panel p-4 mb-5 position-relative border bg-mid d-flex flex-column flex-md-row justify-content-md-between align-items-md-center gap-3">
            <div>
              <div class="timer-display" id="timer">{{ tempsFormatejat }}</div>
              <div class="timer-label text-uppercase">temps acumulat en aquest cas</div>
            </div>
            <div class="timer-status border px-3 py-1 text-uppercase d-flex align-items-center justify-content-center gap-2">
              En Curs
            </div>
          </div>

          <!-- Historial d'intents -->
          <div class="section-label mb-2">// Arxiu d'Interrogatoris</div>
          <h2 class="section-title mb-4">Historial <em>d'Intents</em></h2>

          <div class="panel position-relative border bg-mid p-4 mb-4">
            <div class="panel-tag position-absolute text-uppercase border-bottom-0 p-1 px-3">Cas Actual · #0008</div>
            <ul class="attempt-list list-unstyled mt-3 mb-0">
              <li class="attempt-item d-flex align-items-center gap-3 p-3 border mb-2 bg-panel">
                <div class="attempt-num fw-bold pb-1 px-2 text-center">02</div>
                <div class="attempt-details flex-grow-1">
                  <div class="attempt-combo mb-1">
                    <span>Dr. Negre</span> · Revòlver · Biblioteca
                  </div>
                  <div class="attempt-hints d-flex gap-2 flex-wrap mt-1">
                    <span class="hint-chip text-uppercase">arma correcta</span>
                  </div>
                  <div class="attempt-time mt-1">fa 3 min · 00:09:22</div>
                </div>
                <div class="attempt-result partial text-uppercase border px-2 py-1">Parcialment Correcte</div>
              </li>
              <li class="attempt-item d-flex align-items-center gap-3 p-3 border mb-2 bg-panel">
                <div class="attempt-num fw-bold pb-1 px-2 text-center">01</div>
                <div class="attempt-details flex-grow-1">
                  <div class="attempt-combo mb-1">
                    Coronel Mostaza · Corda · Cuina
                  </div>
                  <div class="attempt-hints d-flex gap-2 flex-wrap mt-1"></div>
                  <div class="attempt-time mt-1">fa 9 min · 00:03:11</div>
                </div>
                <div class="attempt-result fail text-uppercase border px-2 py-1">Incorrecte</div>
              </li>
            </ul>
          </div>

          <div class="divider d-flex align-items-center gap-3 my-5"><span>casos anteriors</span></div>

          <!-- Casos anteriors -->
          <div class="panel position-relative border bg-mid p-4 mb-4">
            <div class="panel-tag position-absolute text-uppercase border-bottom-0 p-1 px-3">Arxiu Tancat</div>
            <ul class="attempt-list list-unstyled mt-3 mb-0">
              <li class="attempt-item d-flex align-items-center gap-3 p-3 border mb-2 bg-panel">
                <div class="attempt-num fw-bold pb-1 px-2 text-center text-success-custom"><i class="bi bi-check-lg"></i></div>
                <div class="attempt-details flex-grow-1">
                  <div class="attempt-combo mb-1">
                    Cas #0007 — <span>Professora Plum</span> · Canelobre · Biblioteca
                  </div>
                  <div class="attempt-time">23/04/2026 · Resolt en 3 intents · 00:08:04</div>
                </div>
                <div class="attempt-result success text-uppercase border px-2 py-1">CAS TANCAT</div>
              </li>
              <li class="attempt-item d-flex align-items-center gap-3 p-3 border mb-2 bg-panel">
                <div class="attempt-num fw-bold pb-1 px-2 text-center text-danger-custom"><i class="bi bi-x-lg"></i></div>
                <div class="attempt-details flex-grow-1">
                  <div class="attempt-combo mb-1">
                    Cas #0006 — Srta. Escarlata · Ganivet · Saló
                  </div>
                  <div class="attempt-time">20/04/2026 · Esgotat · 5 intents</div>
                </div>
                <div class="attempt-result fail text-uppercase border px-2 py-1">ARXIVAT</div>
              </li>
              <li class="attempt-item d-flex align-items-center gap-3 p-3 border mb-2 bg-panel">
                <div class="attempt-num fw-bold pb-1 px-2 text-center text-success-custom"><i class="bi bi-check-lg"></i></div>
                <div class="attempt-details flex-grow-1">
                  <div class="attempt-combo mb-1">
                    Cas #0005 — <span>Sr. Verd</span> · Clau anglesa · Billar
                  </div>
                  <div class="attempt-time">17/04/2026 · Resolt en 2 intents · 00:04:51</div>
                </div>
                <div class="attempt-result success text-uppercase border px-2 py-1">CAS TANCAT</div>
              </li>
              <li class="attempt-item d-flex align-items-center gap-3 p-3 border mb-2 bg-panel">
                <div class="attempt-num fw-bold pb-1 px-2 text-center text-danger-custom"><i class="bi bi-x-lg"></i></div>
                <div class="attempt-details flex-grow-1">
                  <div class="attempt-combo mb-1">
                    Cas #0004 — Sra. Blanch · Tub de Plom · Conservatori
                  </div>
                  <div class="attempt-time">14/04/2026 · Esgotat · 5 intents</div>
                </div>
                <div class="attempt-result fail text-uppercase border px-2 py-1">ARXIVAT</div>
              </li>
              <li class="attempt-item d-flex align-items-center gap-3 p-3 border mb-2 bg-panel">
                <div class="attempt-num fw-bold pb-1 px-2 text-center text-success-custom"><i class="bi bi-check-lg"></i></div>
                <div class="attempt-details flex-grow-1">
                  <div class="attempt-combo mb-1">
                    Cas #0003 — <span>Coronel Mostaza</span> · Revòlver · Estudi
                  </div>
                  <div class="attempt-time">10/04/2026 · Resolt en 4 intents · 00:15:22</div>
                </div>
                <div class="attempt-result success text-uppercase border px-2 py-1">CAS TANCAT</div>
              </li>
            </ul>
          </div>
        </main>

        <!-- SIDEBAR -->
        <aside class="col-lg-4 sidebar animate-fade-up-delay">
          
          <!-- Rang -->
          <div class="rank-card p-4 mb-4 border position-relative bg-mid">
            <div class="rank-card-tag position-absolute text-uppercase p-1 px-3 border border-bottom-0">CREDENCIAL</div>
            <div class="rank-icon pt-4 pb-2"><i class="bi bi-search"></i></div>
            <div class="rank-title mb-2">Inspector</div>
            <div class="rank-desc mb-4">Has demostrat instint investigador. La teva carrera avança cap al rang de Comissari.</div>
            <div class="xp-track">
              <div class="xp-label d-flex justify-content-between mb-1 pb-1">
                <span>Experiència</span>
                <span>600 / 1000 XP</span>
              </div>
              <div class="xp-bar w-100 position-relative">
                <div class="xp-fill h-100" style="width: 60%"></div>
              </div>
              <div class="xp-next mt-1 pt-1 text-end">400 XP per a Comissari</div>
            </div>
          </div>

          <!-- Distintius -->
          <div class="badges-card p-4 mb-4 border position-relative bg-mid">
            <div class="badges-card-tag position-absolute text-uppercase p-1 px-3 border border-bottom-0">DISTINTIUS</div>
            <ul class="badges-grid list-unstyled mt-4 pt-2 mb-0 row g-2">
              <li class="col-4 badge-item-col">
                <div class="badge-item p-2 border text-center h-100 bg-panel">
                  <span class="badge-emoji pb-1"><i class="bi bi-award"></i></span>
                  <span class="badge-name d-block">Primer Cas</span>
                </div>
              </li>
              <li class="col-4 badge-item-col">
                <div class="badge-item p-2 border text-center h-100 bg-panel">
                  <span class="badge-emoji pb-1"><i class="bi bi-lightning-charge"></i></span>
                  <span class="badge-name d-block">Resolució Ràpida</span>
                </div>
              </li>
              <li class="col-4 badge-item-col">
                <div class="badge-item p-2 border text-center h-100 bg-panel">
                  <span class="badge-emoji pb-1"><i class="bi bi-bullseye"></i></span>
                  <span class="badge-name d-block">2 Intents</span>
                </div>
              </li>
              <li class="col-4 badge-item-col">
                <div class="badge-item p-2 border text-center h-100 bg-panel opacity-50">
                  <span class="badge-emoji pb-1"><i class="bi bi-lock-fill"></i></span>
                  <span class="badge-name d-block">Sense Errors</span>
                </div>
              </li>
              <li class="col-4 badge-item-col">
                <div class="badge-item p-2 border text-center h-100 bg-panel opacity-50">
                  <span class="badge-emoji pb-1"><i class="bi bi-lock-fill"></i></span>
                  <span class="badge-name d-block">10 Casos</span>
                </div>
              </li>
              <li class="col-4 badge-item-col">
                <div class="badge-item p-2 border text-center h-100 bg-panel opacity-50">
                  <span class="badge-emoji pb-1"><i class="bi bi-lock-fill"></i></span>
                  <span class="badge-name d-block">Comissari</span>
                </div>
              </li>
            </ul>
          </div>

          <!-- Estadístiques -->
          <div class="stats-card p-4 mb-4 border position-relative bg-mid">
            <div class="stats-card-tag position-absolute text-uppercase p-1 px-3 border border-bottom-0">ESTADÍSTIQUES</div>
            <div class="mt-4 pt-1">
              <div class="stat-row d-flex justify-content-between py-2 border-bottom">
                <span class="stat-row-label">Millor temps</span>
                <span class="stat-row-val text-gold">00:04:51</span>
              </div>
              <div class="stat-row d-flex justify-content-between py-2 border-bottom">
                <span class="stat-row-label">Temps mitjà</span>
                <span class="stat-row-val text-cream">00:09:17</span>
              </div>
              <div class="stat-row d-flex justify-content-between py-2 border-bottom">
                <span class="stat-row-label">Intents per cas</span>
                <span class="stat-row-val text-cream">3.2</span>
              </div>
              <div class="stat-row d-flex justify-content-between py-2 border-bottom">
                <span class="stat-row-label">Sospitós encertat</span>
                <span class="stat-row-val text-success-custom">57%</span>
              </div>
              <div class="stat-row d-flex justify-content-between py-2 border-bottom">
                <span class="stat-row-label">Arma encertada</span>
                <span class="stat-row-val text-gold">71%</span>
              </div>
              <div class="stat-row d-flex justify-content-between py-2 border-bottom">
                <span class="stat-row-label">Habitació encertada</span>
                <span class="stat-row-val text-danger-custom">42%</span>
              </div>
              <div class="stat-row d-flex justify-content-between py-2">
                <span class="stat-row-label">Ràtio resolució</span>
                <span class="stat-row-val text-cream">43%</span>
              </div>
            </div>
          </div>
        </aside>
      </div>
    </div>

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
.attempt-combo span { color: var(--gold); }
.attempt-time { font-family: 'IBM Plex Mono', monospace; font-size: 0.62rem; color: var(--muted); letter-spacing: 0.1em; }

.attempt-result { font-family: 'IBM Plex Mono', monospace; font-size: 0.65rem; letter-spacing: 0.1em; }
.attempt-result.fail { color: var(--crimson); border-color: var(--crimson) !important; background: rgba(192,57,43,0.08); }
.attempt-result.success { color: var(--green); border-color: var(--green) !important; background: var(--green-lt); }
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
.rank-icon { font-size: 2.8rem; text-align: center; }
.rank-title { font-family: 'Playfair Display', serif; font-size: 1.5rem; font-weight: 700; color: var(--gold); text-align: center; }
.rank-desc { font-family: 'IBM Plex Mono', monospace; font-size: 0.68rem; color: var(--muted); text-align: center; line-height: 1.6; }

.xp-label { font-family: 'IBM Plex Mono', monospace; font-size: 0.6rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted); }
.xp-bar { height: 3px; background: var(--bg-panel); }
.xp-fill { background: linear-gradient(90deg, var(--gold-dim), var(--gold)); }
.xp-next { font-family: 'IBM Plex Mono', monospace; font-size: 0.6rem; color: var(--muted); opacity: 0.6; }

.badge-item { transition: border-color 0.2s; cursor: default; }
.badge-item:hover { border-color: var(--border-hv) !important; }
.badge-emoji { font-size: 1.6rem; }
.badge-name { font-family: 'IBM Plex Mono', monospace; font-size: 0.55rem; letter-spacing: 0.1em; color: var(--muted); line-height: 1.3; }

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