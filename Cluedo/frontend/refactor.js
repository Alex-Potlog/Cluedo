const fs = require('fs');
const path = require('path');
const dir = '/home/roger/Optativa/Cluedo/Cluedo/Cluedo/frontend/src/components';
const config = {
  'Index.vue': { active: 'joc', badge: 'Cas Obert' },
  'Users.vue': { active: 'expedient', badge: 'Perfil Agent' },
  'ComJugar.vue': { active: 'com-jugar', badge: 'Manual' }
};

for (const [file, props] of Object.entries(config)) {
  const p = path.join(dir, file);
  let content = fs.readFileSync(p, 'utf8');

  // Imports logic
  if (!content.includes('AppHeader')) {
    if (content.includes('<script setup>')) {
      content = content.replace(/<script setup>\n/, "<script setup>\nimport AppHeader from './AppHeader.vue'\nimport AppFooter from './AppFooter.vue'\n");
    } else {
      content = `<script setup>\nimport AppHeader from './AppHeader.vue'\nimport AppFooter from './AppFooter.vue'\n</script>\n\n` + content;
    }
  }

  // HTML replacements
  content = content.replace(/<!-- HEADER -->\s*<header[\s\S]*?<\/header>/, `<!-- HEADER -->\n    <AppHeader activePage="${props.active}" badgeText="${props.badge}" />`);
  content = content.replace(/<!-- FOOTER -->\s*<footer[\s\S]*?<\/footer>/, `<!-- FOOTER -->\n    <AppFooter />`);

  // CSS replacements (be careful to only remove matched blocks)
  const cssToRemove = [
    /\.main-header\s*\{[\s\S]*?\}/g,
    /\.logo\s*\{[\s\S]*?\}/g,
    /\.logo-dot\s*\{[\s\S]*?\}/g,
    /@keyframes\s*pulse\s*\{[\s\S]*?\}/g,
    /nav\s*a\s*\{[\s\S]*?\}/g,
    /nav\s*a:hover,\s*nav\s*a\.active\s*\{[\s\S]*?\}/g,
    /\.header-badge\s*\{[\s\S]*?\}/g,
    /footer\s*\{[\s\S]*?\}/g,
    /\.footer-logo\s*\{[\s\S]*?\}/g,
    /\.footer-logo\s*span\s*\{[\s\S]*?\}/g,
    /\.footer-links\s*a\s*\{[\s\S]*?\}/g,
    /\.footer-links\s*a:hover\s*\{[\s\S]*?\}/g,
    /\.footer-copy\s*\{[\s\S]*?\}/g
  ];

  cssToRemove.forEach(regex => {
    content = content.replace(regex, '');
  });

  fs.writeFileSync(p, content);
}
console.log('Refactoring complete.');
