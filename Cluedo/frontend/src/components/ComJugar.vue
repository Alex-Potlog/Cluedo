<script setup>
import { getUrl } from '../utils.js'
import AppHeader from './AppHeader.vue'
</script>

<template>
  <div class="caso-abierto-body">
    <AppHeader activePage="com-jugar" badgeText="Manual" />

    <!-- PAGE HERO -->
    <section class="page-hero px-4 py-5 overflow-hidden position-relative">
      <div class="page-hero-inner container position-relative z-1">
        <div class="breadcrumb d-flex align-items-center gap-2 mb-3">
          CasoAbierto <span>/</span> Com Jugar
        </div>
        <h1 class="mb-3">Anatomia d'una<br><em>Investigació</em></h1>
        <p class="page-hero-desc mb-0">
          Tot detective necessita conèixer les regles del joc abans d'entrar a la sala d'interrogatoris. Llegeix amb atenció, Inspector.
        </p>
      </div>
    </section>

    <!-- MAIN -->
    <main class="container py-5 my-5 max-w-1100">
      
      <!-- FLOW PASOS -->
      <section class="mb-5 pb-5">
        <div class="section-label mb-2">// Funcionament del Joc</div>
        <h2 class="section-title mb-5">Els tres <em>passos</em> de la investigació</h2>

        <div class="flow position-relative">
          <div class="flow-step d-flex flex-column flex-md-row gap-4 py-4 position-relative">
            <div class="flow-num d-flex justify-content-center align-items-center">01</div>
            <div class="flow-content flex-grow-1 pt-2">
              <div class="flow-tag mb-2">Fase inicial</div>
              <h3 class="mb-3">Generació del Misteri</h3>
              <p class="mb-3">
                En el moment que inicies una partida, el sistema defineix en segon pla la <strong>Solució Secreta</strong>: una combinació aleatòria d'un personatge, una arma i una habitació. Aquesta informació queda guardada al servidor Django i tu, com a investigador, no tens cap accés directe.
              </p>
              <div class="flow-detail p-3 mt-3">
                ⚙ Backend (Django ORM) genera i desa la Solució Secreta de forma anònima a la base de dades.
              </div>
            </div>
          </div>

          <div class="flow-step d-flex flex-column flex-md-row gap-4 py-4 position-relative border-top-custom">
            <div class="flow-num d-flex justify-content-center align-items-center">02</div>
            <div class="flow-content flex-grow-1 pt-2">
              <div class="flow-tag mb-2">Fase central</div>
              <h3 class="mb-3">L'Interrogatori</h3>
              <p class="mb-3">
                A la interfície (Vue.js) veuràs tres llistes: <strong>Personatges</strong>, <strong>Armes</strong> i <strong>Habitacions</strong>. Selecciona un element de cada categoria, formula la teva teoria i prem el botó <strong style="color:var(--crimson)">ACUSAR</strong>. La petició s'envia via <code style="color:var(--gold-dim)">fetch</code> a l'API de Django sense recarregar la pàgina.
              </p>
              <div class="flow-detail p-3 mt-3">
                ⚙ POST /api/acusar/ → El frontend envia { personatge, arma, habitacio } i rep la resposta en temps real.
              </div>
            </div>
          </div>

          <div class="flow-step d-flex flex-column flex-md-row gap-4 py-4 position-relative border-top-custom">
            <div class="flow-num d-flex justify-content-center align-items-center">03</div>
            <div class="flow-content flex-grow-1 pt-2">
              <div class="flow-tag mb-2">Fase final</div>
              <h3 class="mb-3">El Veredicte</h3>
              <p class="mb-3">
                El sistema compara la teva acusació amb la Solució Secreta i retorna immediatament el resultat. Si has encertat els tres elements, el <strong>cas es tanca</strong>. Si no, la investigació continua: analitza les pistes que el sistema et proporciona i torna a intentar-ho.
              </p>
              <div class="flow-detail p-3 mt-3">
                ⚙ Resposta JSON: { "correcte": true/false, "pistes": "Arma correcta, lloc no" }
              </div>
            </div>
          </div>
        </div>
      </section>

      <div class="divider d-flex align-items-center gap-3 mb-5"><span>regles obligatòries</span></div>

      <!-- REGLES -->
      <section class="mb-5 pb-5">
        <div class="section-label mb-2">// Regles d'Or de l'Investigador</div>
        <h2 class="section-title mb-5">Restriccions <em>tècniques</em></h2>

        <div class="row g-4">
          <div class="col-md-4">
            <div class="rule-card p-4 h-100 position-relative" data-rule="Regla 01">
              <span class="rule-icon mb-3 d-block"><i class="bi bi-clock-history text-gold"></i></span>
              <h4 class="mb-2">L'ORM és la Llei</h4>
              <p class="mb-0">Tota interacció amb la base de dades s'ha de fer obligatòriament a través del Django ORM. No s'accepta SQL cru sota cap circumstància.</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="rule-card p-4 h-100 position-relative" data-rule="Regla 02">
              <span class="rule-icon mb-3 d-block"><i class="bi bi-slash-circle text-gold"></i></span>
              <h4 class="mb-2">Prohibit Recarregar</h4>
              <p class="mb-0">La vista de Vue.js és completament reactiva. Totes les accions —obtenir llistes, acusar— s'han de realitzar via JavaScript <code style="color:var(--gold-dim)">fetch</code>, sense cap recàrrega de pàgina.</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="rule-card p-4 h-100 position-relative" data-rule="Regla 03">
              <span class="rule-icon mb-3 d-block"><i class="bi bi-bank text-gold"></i></span>
              <h4 class="mb-2">Silos Tecnològics</h4>
              <p class="mb-0">Vue.js s'encarrega exclusivament de la interfície i la interactivitat. Django gestiona exclusivament la seguretat de les dades i l'API. Cap dels dos envaeix el territori de l'altre.</p>
            </div>
          </div>
        </div>
      </section>

      <div class="divider d-flex align-items-center gap-3 mb-5"><span>veredictes possibles</span></div>

      <!-- VEREDICTES -->
      <section class="verdict-section mb-5 pb-5">
        <div class="section-label mb-2">// El Sistema Avalua l'Intent</div>
        <h2 class="section-title mb-5">Resultats <em>possibles</em></h2>

        <div class="row g-4">
          <div class="col-md-6">
            <div class="verdict-card success p-4 h-100 d-flex gap-3">
              <div class="verdict-icon"><i class="bi bi-shield-check"></i></div>
              <div>
                <h4 class="mb-2 text-success-custom">Correcte → El Cas es Tanca</h4>
                <p class="mb-0">Has identificat correctament el personatge, l'arma i l'habitació. El sistema confirma l'acusació i declara el cas resolt. La teva reputació com a detectiu queda intacta.</p>
              </div>
            </div>
          </div>
          <div class="col-md-6">
            <div class="verdict-card fail p-4 h-100 d-flex gap-3">
              <div class="verdict-icon"><i class="bi bi-shield-x"></i></div>
              <div>
                <h4 class="mb-2 text-danger-custom">Incorrecte → La Investigació Continua</h4>
                <p class="mb-0">Un o més elements de la teva acusació no coincideixen amb la Solució Secreta. El sistema et pot proporcionar pistes parcials si has assolit el nivell Inspector o superior.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <div class="divider d-flex align-items-center gap-3 mb-5"><span>consells del comissari</span></div>

      <!-- TIPS -->
      <section class="mb-5 pb-5">
        <div class="section-label mb-2">// Consells d'Or</div>
        <h2 class="section-title mb-5">Notes del <em>Comissari</em></h2>

        <div class="tips-panel p-4 position-relative">
          <ul class="row list-unstyled m-0 g-3">
            <li class="col-md-6 tips-li position-relative"><strong>Comença pel mínim funcional (MVP).</strong> No busquis l'Excel·lent abans de tenir un joc que funcioni per a l'Aprovat.</li>
            <li class="col-md-6 tips-li position-relative"><strong>L'API és el teu pont.</strong> Prova els endpoints (ex: <code style="color:var(--gold-dim)">/api/personatges/</code>) directament al navegador abans de programar el Vue.</li>
            <li class="col-md-6 tips-li position-relative"><strong>Revisa les teves eines.</strong> Les URLs, la consola del navegador (F12) per errors de Vue, i el terminal de Django. Allà hi ha les pistes.</li>
            <li class="col-md-6 tips-li position-relative"><strong>Totes les dades base s'han de crear prèviament</strong> des de la interfície de Django Admin: personatges, armes, habitacions i la solució.</li>
            <li class="col-md-6 tips-li position-relative"><strong>Pensa en capes.</strong> Primer els models, després l'API, finalment el frontend. No saltis passos o et perdràs.</li>
            <li class="col-md-6 tips-li position-relative"><strong>Prova cada endpoint per separat.</strong> Confirma que el GET funciona abans d'implementar el POST d'acusació.</li>
          </ul>
        </div>
      </section>

      <!-- CTA -->
      <div class="cta-final text-center p-5 position-relative border overflow-hidden">
        <p class="stamp mb-4 d-inline-block">Missió Activa</p>
        <h2 class="mb-3 position-relative z-1">Estàs llest per <em>resoldre</em> el cas?</h2>
        <p class="sub mb-4 position-relative z-1">El temps corre, Detectiu. Endinsa't al codi i resol el misteri.</p>
        <a href="/#joc" class="btn-primary-custom position-relative z-1 text-decoration-none"><i class="bi bi-scales me-2"></i>Iniciar Investigació</a>
      </div>

    </main>

    <!-- FOOTER -->
    <footer class="d-flex flex-wrap align-items-center justify-content-between p-4 border-top shadow-sm">
      <a :href="getUrl('/')" class="footer-logo mb-3 mb-md-0 d-block text-decoration-none">
        CasoAbierto
        <span class="d-block mt-1">Operació Full-Stack · Django + Vue.js</span>
      </a>
      <div class="footer-links d-flex gap-3 mb-3 mb-md-0 flex-wrap">
        <a :href="getUrl('/')">El Joc</a>
        <a :href="getUrl('/com-jugar')" class="active">Com Jugar</a>
        <a :href="getUrl('/users')">Expedient</a>
        <a href="/admin">Admin</a>
      </div>
      <div class="footer-copy">
        Dossier Confidencial &mdash; Destrueix després de llegir
      </div>
    </footer>
  </div>
</template>

<script setup>
</script>

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

.page-hero {
  border-bottom: 1px solid var(--border);
}

.page-hero::before {
  content: '';
  position: absolute; inset: 0;
  background-image: repeating-linear-gradient(0deg, transparent, transparent 39px, rgba(212, 175, 122, 0.04) 39px, rgba(212, 175, 122, 0.04) 40px),
                    repeating-linear-gradient(90deg, transparent, transparent 39px, rgba(212, 175, 122, 0.04) 39px, rgba(212, 175, 122, 0.04) 40px);
  pointer-events: none;
  z-index: 0;
}

.page-hero::after {
  content: '?';
  position: absolute; right: 3rem; top: 50%; transform: translateY(-50%);
  font-family: 'Playfair Display', serif;
  font-size: 22rem;
  font-weight: 700;
  color: rgba(212, 175, 122, 0.04);
  line-height: 1;
  pointer-events: none;
}

.breadcrumb {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.62rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--muted);
}
.breadcrumb span { color: var(--gold-dim); }
.page-hero h1 {
  font-family: 'Playfair Display', serif;
  font-size: clamp(2.5rem, 7vw, 5rem);
  font-weight: 700;
  color: var(--cream);
  line-height: 1;
  letter-spacing: -0.02em;
}
.page-hero h1 em { color: var(--gold); font-style: italic; }
.page-hero-desc {
  font-family: 'Special Elite', cursive;
  font-size: 1rem;
  color: var(--muted);
  max-width: 500px;
  line-height: 1.8;
}

.max-w-1100 { max-width: 1100px; }

.section-label {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.65rem;
  letter-spacing: 0.3em;
  text-transform: uppercase;
  color: var(--crimson);
}
.section-title {
  font-family: 'Playfair Display', serif;
  font-size: clamp(1.5rem, 3.5vw, 2.2rem);
  font-weight: 700;
  color: var(--cream);
}
.section-title em { color: var(--gold); font-style: italic; }

.flow::before {
  content: '';
  position: absolute;
  left: 28px; top: 0; bottom: 0;
  width: 1px;
  background: linear-gradient(to bottom, var(--crimson), var(--gold-dim), transparent);
}

.flow-step { transition: background 0.2s; }
.border-top-custom { border-top: 1px solid var(--border); }

.flow-num {
  flex-shrink: 0;
  width: 56px; height: 56px;
  background: var(--bg-mid);
  border: 1px solid var(--border);
  font-family: 'Playfair Display', serif;
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--gold);
  position: relative; z-index: 1;
  transition: border-color 0.2s, background 0.2s;
}
.flow-step:hover .flow-num { border-color: var(--gold); background: var(--bg-panel); }

.flow-tag {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.58rem;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  color: var(--crimson);
}
.flow-content h3 { font-family: 'Special Elite', cursive; font-size: 1.3rem; color: var(--gold); }
.flow-content p { font-size: 0.78rem; color: var(--muted); line-height: 1.9; max-width: 600px; }
.flow-content strong { color: var(--cream); }

.flow-detail {
  background: var(--bg-panel);
  border-left: 2px solid var(--gold-dim);
  font-size: 0.72rem;
  color: var(--cream);
  opacity: 0.8;
  line-height: 1.8;
  font-family: 'IBM Plex Mono', monospace;
}

.divider::before, .divider::after { content: ''; flex: 1; height: 1px; background: var(--border); }
.divider span {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.6rem;
  letter-spacing: 0.3em;
  text-transform: uppercase;
  color: var(--muted);
}

.rule-card {
  background: var(--bg-mid);
  border: 1px solid var(--border);
  transition: border-color 0.25s, transform 0.2s;
}
.rule-card:hover { border-color: var(--border-hv); transform: translateY(-3px); }
.rule-card::before {
  content: attr(data-rule);
  position: absolute; top: -1px; left: 16px;
  background: var(--bg-panel);
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.58rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--gold-dim);
  padding: 3px 10px;
  border: 1px solid var(--border);
  border-top: none;
}
.rule-icon { font-size: 1.6rem; }
.rule-card h4 { font-family: 'Special Elite', cursive; font-size: 1rem; color: var(--gold); }
.rule-card p { font-size: 0.72rem; color: var(--muted); line-height: 1.75; }

.verdict-card {
  background: var(--bg-mid);
  border: 1px solid var(--border);
  transition: border-color 0.2s;
}
.verdict-card.success { border-left: 3px solid #27ae60; }
.verdict-card.fail { border-left: 3px solid var(--crimson); }
.verdict-card:hover { border-color: var(--border-hv); }

.verdict-icon { font-size: 2rem; line-height: 1; margin-top: 2px; }
.verdict-card h4 { font-family: 'Special Elite', cursive; font-size: 1.05rem; }
.text-success-custom { color: #2ecc71; }
.text-danger-custom { color: #e74c3c; }
.verdict-card p { font-size: 0.72rem; color: var(--muted); line-height: 1.75; }

.tips-panel {
  background: var(--bg-mid);
  border: 1px solid var(--border);
}
.tips-panel::before {
  content: 'NOTES DEL COMISSARI';
  position: absolute; top: -1px; left: 2rem;
  background: var(--bg-panel);
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.58rem;
  letter-spacing: 0.2em;
  color: var(--gold-dim);
  padding: 4px 14px;
  border: 1px solid var(--border);
  border-top: none;
}
.tips-li { font-size: 0.75rem; color: var(--muted); line-height: 1.7; padding-left: 1.6rem !important; }
.tips-li::before {
  content: '→';
  position: absolute; left: 0.5rem;
  color: var(--gold-dim);
  font-family: 'IBM Plex Mono', monospace;
}
.tips-li strong { color: var(--cream); font-weight: 500; }

.cta-final {
  background: var(--bg-mid);
  border-color: var(--border) !important;
}
.cta-final::before {
  content: 'CAS OBERT';
  position: absolute;
  top: 50%; left: 50%; transform: translate(-50%, -50%);
  font-family: 'Playfair Display', serif;
  font-size: 10rem;
  font-weight: 700;
  color: rgba(212, 175, 122, 0.03);
  white-space: nowrap;
  pointer-events: none;
  z-index: 0;
}
.cta-final .stamp {
  font-family: 'Special Elite', cursive;
  font-size: 0.7rem;
  letter-spacing: 0.3em;
  text-transform: uppercase;
  color: var(--crimson);
  border: 1px solid var(--crimson);
  padding: 4px 16px;
  transform: rotate(-1deg);
  opacity: 0.85;
}
.cta-final h2 { font-family: 'Playfair Display', serif; font-size: clamp(1.8rem, 4vw, 3rem); font-weight: 700; color: var(--cream); }
.cta-final h2 em { color: var(--gold); font-style: italic; }
.cta-final .sub { font-family: 'Special Elite', cursive; font-size: 0.95rem; color: var(--muted); }

.btn-primary-custom {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.78rem;
  font-weight: 500;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--bg-deep) !important;
  background: var(--gold);
  padding: 14px 36px;
  display: inline-block;
  transition: background 0.2s, transform 0.15s;
}
.btn-primary-custom:hover { background: #e8c88a; transform: translateY(-2px); }

footer { background: rgba(13, 11, 20, 0.8); border-top: 1px solid var(--border) !important; }
.footer-logo { font-family: 'Special Elite', cursive; font-size: 1rem; color: var(--gold); }
.footer-logo span { color: var(--muted); font-size: 0.7rem; font-family: 'IBM Plex Mono', monospace; }
.footer-links a { font-family: 'IBM Plex Mono', monospace; font-size: 0.65rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted); text-decoration: none; transition: color 0.2s; }
.footer-links a:hover { color: var(--gold); }
.footer-copy { font-family: 'IBM Plex Mono', monospace; font-size: 0.62rem; color: var(--muted); opacity: 0.5; letter-spacing: 0.05em; }

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(18px); }
  to { opacity: 1; transform: translateY(0); }
}
.page-hero-inner { animation: fadeUp 0.6s ease 0.1s both; }

@media (max-width: 768px) {
  .flow::before { display: none; }
  .page-hero::after { display: none; }
}
</style>