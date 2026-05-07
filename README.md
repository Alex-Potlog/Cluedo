# Cluedo Web — Cas Obert

Joc de tipus Cluedo implementat com a aplicació web amb un backend en Django (API REST + ORM + Admin) i un frontend en Vue 3 amb Vite. L'usuari es registra, inicia sessió i ha de descobrir un crim seleccionant un personatge, una arma i una habitació abans d'esgotar els intents disponibles.

## 1. Com funciona el joc, pas a pas

1. Registre o login. L'usuari entra a /register per crear un compte o a /login per accedir-hi. La sessió es manté per cookie amb el sistema d'autenticació nadiu de Django, i el frontend obté un token CSRF abans de qualsevol POST.
2. Creació del cas. En entrar a la pàgina principal, el frontend consulta /api/cas/active/. Si l'usuari no té cap cas en curs, en crea un de nou amb POST /api/cas/new/. El backend tria aleatòriament un personatge, una arma i una habitació de la base de dades i els guarda com a solució secreta del cas. Aquesta solució mai surt al client fins que el cas es tanca.
3. Càrrega de catàlegs. El frontend demana les llistes amb GET /api/personatges/, GET /api/armes/ i GET /api/habitacions/, i les pinta dins els tres selects de la sala d'interrogatoris.
4. Acusació. L'usuari escull una combinació i fa clic a Acusar. El frontend envia POST /api/acusar/ amb els tres identificadors. El backend comprova quins dels tres elements coincideixen amb la solució, crea un registre Intent amb el resultat (correcte, parcial o incorrecte) i el temps transcorregut. Si encerta els tres, el cas queda marcat com a resolt; si arriba al límit d'intents (5 per defecte) sense encertar-los tots, el cas queda arxivat i la solució es revela.
5. Feedback al jugador. El frontend mostra, sense recarregar la pàgina, el missatge corresponent: sospitós correcte, arma correcta, habitació correcta o combinacions. El comptador d'intents i els punts visuals s'actualitzen en temps real.
6. Tornar a jugar. Quan el cas es tanca, apareix un botó Tornar a jugar que crida de nou /api/cas/new/ per generar un cas amb solució diferent.
7. Expedient de l'agent a /users. Mostra el perfil de l'usuari (codi AGT-xxxxx, data d'ingrés), el cas en curs amb el seu cronòmetre real, l'historial d'intents del cas actiu i els casos anteriors tancats amb estadístiques: resolts, arxivats, millor temps i ràtio de resolució.

## 2. Tecnologies implementades

### Backend

- Python 3.13.
- Django 5: framework web, sistema d'autenticació, sistema de sessions i panell d'Admin per a la gestió manual dels catàlegs i dels casos.
- Django ORM: totes les consultes a la base de dades es fan via ORM, sense SQL cru.
- SQLite com a base de dades per defecte, generada amb les migracions.
- Comanda personalitzada (python manage.py seed) per omplir els catàlegs inicials de personatges, armes i habitacions.

### Frontend

- Vue 3 amb Composition API.
- Vite com a empaquetador i servidor de desenvolupament.
- Bootstrap 5 i Bootstrap Icons per al disseny base.
- Fetch API i cookies de sessió per a la comunicació amb el backend.
- CSS scoped per component amb tipografies Playfair Display, Special Elite i IBM Plex Mono per a l'estètica de dossier policial.

### Integració

- django-vite per exposar els assets compilats per Vite a les plantilles de Django.
- Endpoints JSON sota /api/ consumits íntegrament via fetch. El frontend mai recarrega la pàgina per a accions de joc.

## 3. Extres i millores afegides

A més del bloc obligatori, s'han implementat tots els punts del bloc Notable i del bloc Excel·lent.

### Bloc Notable

- Missatges detallats en acusar. Cada intent retorna els flags encerta_acusado, encerta_arma i encerta_lugar, que el frontend tradueix en pistes com arma correcta o habitació correcta.
- Comptador d'intents real. El nombre d'intents usats i el màxim vénen del backend (intents_usats sobre intents_max), no estan hardcoded.
- Botó Tornar a jugar. Quan un cas es tanca, l'usuari pot iniciar un cas nou amb una sola clicada i el backend genera una solució nova.
- Disseny CSS treballat. Estètica tipus dossier amb tipografies serioses, paleta gold i crimson i efectes de rejilla, grain i animacions de fade-up.

### Bloc Excel·lent

- Sistema de login, registre i logout complet via API JSON, amb validacions de servidor (camps obligatoris, longitud mínima de contrasenya, unicitat de username i email) i protecció CSRF.
- Solució secreta única per usuari. Cada cas té la seva pròpia solució generada aleatòriament i només es revela al client si l'usuari resol el cas o esgota els intents.
- Historial d'intents persistent. Cada intent queda guardat amb el seu resultat, els flags d'encert i el temps acumulat. La pàgina Expedient mostra el detall del cas actual i la llista de casos tancats, amb la solució i la durada.
- Cronòmetre real. Calcula els segons transcorreguts a partir del camp iniciat_el retornat pel servidor i es manté coherent encara que l'usuari recarregui la pàgina.
- Perfil d'agent automàtic. A cada usuari se li assigna en el primer cas un codi AGT-xxxxx únic i una data d'ingrés.
- Estadístiques calculades. Casos totals, resolts, arxivats, ràtio de resolució, millor temps i temps mitjà, tot derivat de les dades reals de l'API.
- Estats del cas (en_curs, resolt, arxivat) gestionats al backend amb TextChoices.

### Decisions tècniques

- Els endpoints amb els noms exactes que demana l'enunciat (/api/personatges/, /api/armes/, /api/habitacions/, /api/acusar/) actuen com a wrappers sobre els models reals (Acusado, Arma, Lugar, Cas i Intent). D'aquesta manera s'ajusten als noms del briefing sense duplicar lògica.
- La solució no és un model independent: viu com tres claus foranes dins el model Cas, perquè cada partida és pròpia de cada usuari i té sentit acoblar-la al cas concret en lloc de a una taula global.

## 4. Posada en marxa

### Servidor Django

```bash
cd Cluedo
python3 -m venv venv
source venv/bin/activate
cd ..
pip install -r ./requirements.txt
python3 manage.py migrate
python3 manage.py seed          # carrega catàlegs inicials
python3 manage.py createsuperuser
python3 manage.py runserver
```

### Build del frontend

```bash
cd Cluedo/frontend
npm install
npm run dev
```

### URLs principals

| Ruta                 | Descripció                       |
| -------------------- | -------------------------------- |
| /                    | Pàgina del joc                   |
| /com-jugar           | Instruccions                     |
| /users               | Expedient de l'agent             |
| /login i /register   | Autenticació                     |
| /admin               | Panell d'administració de Django |