
<script setup>
import { ref } from 'vue'
import { getUrl } from '../utils.js'
import AppHeader from './AppHeader.vue'

const acusacio = ref({
  personatge: '',
  arma: '',
  habitacio: ''
})

const solucio = {
  personatge: 'Professora Plum',
  arma: 'Canelobre',
  habitacio: 'Biblioteca'
}

const mostrarResultat = ref(false)
const resultatClasse = ref('')
const missatgeResultat = ref('')

const ferAcusacio = () => {
  const p = acusacio.value.personatge
  const a = acusacio.value.arma
  const h = acusacio.value.habitacio

  if (!p || !a || !h) {
    resultatClasse.value = 'fail-border fail-bg color-fail'
    missatgeResultat.value = '⚠ Selecciona un sospitós, una arma i una habitació abans d\'acusar.'
    mostrarResultat.value = true
    return
  }

  const correcte = (p === solucio.personatge && a === solucio.arma && h === solucio.habitacio)

  if (correcte) {
    resultatClasse.value = 'success-border success-bg color-success'
    missatgeResultat.value = `✔ CAS TANCAT. Has descobert la veritat. ${p} va cometre el crim amb ${a.toLowerCase()} a la ${h}.`
  } else {
    let pistes = []
    if (p === solucio.personatge) pistes.push('sospitós correcte')
    if (a === solucio.arma) pistes.push('arma correcta')
    if (h === solucio.habitacio) pistes.push('habitació correcta')
    const msg = pistes.length > 0
      ? ' Incorrecte. Pista: ' + pistes.join(', ') + '.'
      : ' Acusació incorrecta. La investigació continua.'
    
    resultatClasse.value = 'fail-border fail-bg color-fail'
    missatgeResultat.value = msg
  }
  mostrarResultat.value = true
}
</script>


<template>
  <div class="caso-abierto-body">
    <AppHeader activePage="joc" badgeText="Cas Obert" />

    <!-- HERO -->
    <section class="hero d-flex align-items-center justify-content-center p-5 text-center">
      <div class="hero-inner container">
        <div class="hero-stamp mb-4">Dossier Confidencial · Operació Full-Stack</div>
        <h1 class="hero-title mb-3">Resol el<br><span>Misteri.</span></h1>
        <p class="hero-sub mb-5">Django + Vue.js · Detectiu Digital</p>
        <p class="hero-desc mx-auto mb-5">
          Un crim ha tingut lloc a la mansió. El sistema ha amagat la solució secreta.
          Ets l'únic investigador capaç de descobrir el culpable, l'arma i el lloc.
        </p>
        <div class="cta-group d-flex gap-3 justify-content-center flex-wrap">
          <a href="#joc" class="btn-primary-custom text-decoration-none">Iniciar Investigació</a>
          <a :href="getUrl('/com-jugar')" class="btn-secondary-custom text-decoration-none">Com Jugar</a>
        </div>
      </div>
    </section>

    <!-- MAIN -->
    <main class="container py-5 my-5">
      <!-- Expedient -->
      <section id="expedient" class="mb-5 pb-5">
        <div class="section-label mb-2">// Expedient Policial</div>
        <h2 class="section-title mb-5">Tres <em>pistes</em> a descobrir</h2>

        <div class="row g-4">
          <div class="col-md-4">
            <div class="evidence-card h-100 p-4 position-relative">
              <span class="evidence-tag">Evidència 01</span>
              <span class="evidence-icon mb-3 d-block"><i class="bi bi-person-fill-exclamation text-gold"></i></span>
              <h3 class="mb-2">El Personatge</h3>
              <p class="m-0">Qui ha comès el crim? Entre la llista de sospitosos, un d'ells amaga la veritat. El teu instint t'ha de guiar.</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="evidence-card h-100 p-4 position-relative">
              <span class="evidence-tag">Evidència 02</span>
              <span class="evidence-icon mb-3 d-block"><i class="bi bi-crosshair text-gold"></i></span>
              <h3 class="mb-2">L'Arma</h3>
              <p class="m-0">Amb quin objecte es va cometre el crim? Cada arma deixa una empremta única. Analitza les proves amb cura.</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="evidence-card h-100 p-4 position-relative">
              <span class="evidence-tag">Evidència 03</span>
              <span class="evidence-icon mb-3 d-block"><i class="bi bi-bank text-gold"></i></span>
              <h3 class="mb-2">L'Habitació</h3>
              <p class="m-0">En quina estança de la mansió va ocórrer tot? El lloc del crim revela molt sobre qui el va cometre.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Joc -->
      <section id="joc" class="mb-5 pb-5">
        <div class="section-label mb-2">// Sala d'Interrogatoris</div>
        <h2 class="section-title mb-4">Fes la teva <em>acusació</em></h2>

        <div class="attempts-row d-flex align-items-center gap-2 mb-4">
          <div class="attempt-dot used"></div>
          <div class="attempt-dot used"></div>
          <div class="attempt-dot"></div>
          <div class="attempt-dot"></div>
          <div class="attempt-dot"></div>
          <span class="attempts-label ms-2">2 / 5 intents usats</span>
        </div>

        <div class="game-panel p-4 p-md-5 position-relative">
          <div class="row g-4 mb-4">
            <div class="col-md-4 form-group">
              <label class="d-block mb-2">Sospitós</label>
              <select v-model="acusacio.personatge" class="w-100 form-select-custom">
                <option value="">— Selecciona —</option>
                <option>Coronel Mostaza</option>
                <option>Professora Plum</option>
                <option>Srta. Escarlata</option>
                <option>Dr. Negre</option>
                <option>Sra. Blanch</option>
                <option>Sr. Verd</option>
              </select>
            </div>
            <div class="col-md-4 form-group">
              <label class="d-block mb-2">Arma</label>
              <select v-model="acusacio.arma" class="w-100 form-select-custom">
                <option value="">— Selecciona —</option>
                <option>Canelobre</option>
                <option>Ganivet</option>
                <option>Tub de Plom</option>
                <option>Revòlver</option>
                <option>Corda</option>
                <option>Clau anglesa</option>
              </select>
            </div>
            <div class="col-md-4 form-group">
              <label class="d-block mb-2">Habitació</label>
              <select v-model="acusacio.habitacio" class="w-100 form-select-custom">
                <option value="">— Selecciona —</option>
                <option>Cuina</option>
                <option>Sala de Ball</option>
                <option>Conservatori</option>
                <option>Billar</option>
                <option>Biblioteca</option>
                <option>Estudi</option>
                <option>Vestíbul</option>
                <option>Saló</option>
                <option>Terrassa</option>
              </select>
            </div>
          </div>

          <button class="acusar-btn w-100 py-3" @click="ferAcusacio"><i class="bi bi-scales me-2"></i>Acusar</button>

          <div v-if="mostrarResultat" :class="['result-panel mt-4 p-3 border', resultatClasse]">
            <i :class="missatgeResultat.includes('CAS TANCAT') ? 'bi bi-check-circle-fill me-2' : 'bi bi-exclamation-triangle-fill me-2'"></i>{{ missatgeResultat.replace('⚠ ', '').replace('✔ ', '') }}
          </div>
        </div>
      </section>

      <div class="divider d-flex align-items-center gap-3 mb-5"><span>com funciona</span></div>

      <!-- Com Jugar -->
      <section id="com-jugar">
        <div class="section-label mb-2">// Anatomia d'una Investigació</div>
        <h2 class="section-title mb-5">Tres <em>passos</em> per resoldre el cas</h2>

        <div class="row g-4">
          <div class="col-md-4">
            <div class="step px-3 border-start">
              <div class="step-num mb-2">01</div>
              <h4 class="mb-2">Generació del Misteri</h4>
              <p class="m-0">El sistema defineix en segon pla la Solució Secreta: un personatge, una arma i una habitació. Tu no saps res. Comença la investigació.</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="step px-3 border-start">
              <div class="step-num mb-2">02</div>
              <h4 class="mb-2">Interrogatori</h4>
              <p class="m-0">Selecciona la teva teoria a la interfície i fes una acusació. Cada intent et dóna pistes sobre si t'acostes a la veritat.</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="step px-3 border-start">
              <div class="step-num mb-2">03</div>
              <h4 class="mb-2">El Veredicte</h4>
              <p class="m-0">El sistema avalua l'acusació. Si has encertat els tres elements, el cas es tanca. Si no, la investigació continua fins arribar a la veritat.</p>
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- FOOTER -->
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

.hero {
  position: relative;
  min-height: calc(100vh - 64px);
  overflow: hidden;
}

.hero::before {
  content: '';
  position: absolute; inset: 0;
  background-image: repeating-linear-gradient(0deg, transparent, transparent 39px, rgba(212, 175, 122, 0.04) 39px, rgba(212, 175, 122, 0.04) 40px),
                    repeating-linear-gradient(90deg, transparent, transparent 39px, rgba(212, 175, 122, 0.04) 39px, rgba(212, 175, 122, 0.04) 40px);
  pointer-events: none;
}

.hero-stamp {
  display: inline-block;
  font-family: 'Special Elite', cursive;
  font-size: 0.68rem;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  color: var(--crimson);
  border: 2px solid var(--crimson);
  padding: 5px 18px;
  transform: rotate(-1.5deg);
  opacity: 0.85;
}

.hero-title {
  font-family: 'Playfair Display', serif;
  font-size: clamp(3rem, 9vw, 6.5rem);
  font-weight: 700;
  line-height: 0.9;
  letter-spacing: -0.02em;
}

.hero-title span {
  color: var(--gold);
  font-style: italic;
}

.hero-sub {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.78rem;
  color: var(--muted);
  letter-spacing: 0.2em;
  text-transform: uppercase;
}

.hero-desc {
  font-family: 'Special Elite', cursive;
  font-size: 1.05rem;
  color: var(--cream);
  opacity: 0.7;
  max-width: 560px;
  line-height: 1.8;
}

.btn-primary-custom {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.78rem;
  font-weight: 500;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--bg-deep) !important;
  background: var(--gold);
  padding: 14px 36px;
  transition: background 0.2s, transform 0.15s;
}

.btn-primary-custom:hover {
  background: #e8c88a;
  transform: translateY(-2px);
}

.btn-secondary-custom {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.78rem;
  font-weight: 400;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--gold) !important;
  background: transparent;
  border: 1px solid var(--border-hv);
  padding: 14px 36px;
  transition: border-color 0.2s, color 0.2s, transform 0.15s;
}

.btn-secondary-custom:hover {
  border-color: var(--gold);
  transform: translateY(-2px);
}

.section-label {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.65rem;
  letter-spacing: 0.3em;
  text-transform: uppercase;
  color: var(--crimson);
}

.section-title {
  font-family: 'Playfair Display', serif;
  font-size: clamp(1.6rem, 4vw, 2.4rem);
  font-weight: 700;
  color: var(--cream);
}

.section-title em {
  color: var(--gold);
  font-style: italic;
}

.evidence-card {
  background: var(--bg-mid);
  border: 1px solid var(--border);
  transition: border-color 0.25s, transform 0.2s;
}

.evidence-card:hover {
  border-color: var(--border-hv);
  transform: translateY(-4px);
}

.evidence-tag {
  position: absolute; top: -1px; right: 20px;
  background: var(--crimson);
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.6rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: #fff;
  padding: 3px 10px;
}

.evidence-icon { font-size: 2rem; }
.evidence-card h3 { font-family: 'Special Elite', cursive; font-size: 1.1rem; color: var(--gold); }
.evidence-card p { font-size: 0.75rem; color: var(--muted); line-height: 1.7; }

.game-panel {
  background: var(--bg-mid);
  border: 1px solid var(--border);
}

.game-panel::before {
  content: 'SALA D\'INTERROGATORIS';
  position: absolute; top: -1px; left: 3rem;
  background: var(--bg-panel);
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.6rem;
  letter-spacing: 0.2em;
  color: var(--gold-dim);
  padding: 4px 14px;
  border: 1px solid var(--border);
  border-top: none;
}

.form-group label {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.62rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--gold-dim);
}

.form-select-custom {
  background: var(--bg-panel);
  border: 1px solid var(--border);
  color: var(--cream);
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.78rem;
  padding: 10px 14px;
  appearance: none;
  cursor: pointer;
  outline: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6'%3E%3Cpath d='M0 0l5 6 5-6z' fill='%238A6D3B'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  transition: border-color 0.2s;
}

.form-select-custom:focus { border-color: var(--gold-dim); }

.acusar-btn {
  font-family: 'Special Elite', cursive;
  font-size: 1.2rem;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  color: var(--cream);
  background: var(--crimson);
  border: none; outline: none;
  transition: background 0.2s, letter-spacing 0.2s;
}

.acusar-btn:hover { background: #d44030; letter-spacing: 0.35em; }

.result-panel {
  font-family: 'Special Elite', cursive;
  font-size: 0.95rem;
}

.success-border { border-color: #27ae60 !important; }
.success-bg { background: rgba(39, 174, 96, 0.08) !important; }
.color-success { color: #2ecc71 !important; }

.fail-border { border-color: var(--crimson) !important; }
.fail-bg { background: rgba(192, 57, 43, 0.08) !important; }
.color-fail { color: #e74c3c !important; }

.step { border-left-color: var(--border) !important; transition: border-left-color 0.2s; }
.step:hover { border-left-color: var(--gold-dim) !important; }
.step-num {
  font-family: 'Playfair Display', serif;
  font-size: 3rem;
  font-weight: 700;
  color: var(--bg-panel);
  line-height: 1;
}
.step h4 { font-family: 'Special Elite', cursive; font-size: 1rem; color: var(--gold); }
.step p { font-size: 0.73rem; color: var(--muted); line-height: 1.75; }

.divider::before, .divider::after {
  content: ''; flex: 1; height: 1px; background: var(--border);
}
.divider span {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.6rem;
  letter-spacing: 0.3em;
  text-transform: uppercase;
  color: var(--muted);
}

.attempt-dot {
  width: 10px; height: 10px;
  border: 1px solid var(--gold-dim);
  border-radius: 50%;
}
.attempt-dot.used { background: var(--crimson); border-color: var(--crimson); }
.attempts-label { font-family: 'IBM Plex Mono', monospace; font-size: 0.65rem; color: var(--muted); letter-spacing: 0.1em; }

footer { background: rgba(13, 11, 20, 0.8); border-top: 1px solid var(--border); }
.footer-logo { font-family: 'Special Elite', cursive; font-size: 1rem; color: var(--gold); }
.footer-logo span { color: var(--muted); font-size: 0.7rem; font-family: 'IBM Plex Mono', monospace; }
.footer-links a { font-family: 'IBM Plex Mono', monospace; font-size: 0.65rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted); text-decoration: none; transition: color 0.2s; }
.footer-links a:hover { color: var(--gold); }
.footer-copy { font-family: 'IBM Plex Mono', monospace; font-size: 0.62rem; color: var(--muted); opacity: 0.5; letter-spacing: 0.05em; }

/* Animations */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.hero-stamp { animation: fadeUp 0.6s ease 0.1s both; }
.hero-title { animation: fadeUp 0.6s ease 0.25s both; }
.hero-sub { animation: fadeUp 0.6s ease 0.4s both; }
.hero-desc { animation: fadeUp 0.6s ease 0.5s both; }
.cta-group { animation: fadeUp 0.6s ease 0.65s both; }
</style>