---
title: "Remotion + Claude Code Quickstart"
description: "15-minute quickstart to create programmatic videos with Remotion and Claude Code"
tags: [tutorial, workflow, integration]
---

# Remotion + Claude Code Quickstart

**Objectif**: Créer votre première vidéo programmatique avec Remotion et Claude Code en 15 minutes.

**Niveau**: Débutant React (connaissances basiques suffisantes)

---

## ⚡ Prérequis

| Requis | Version minimum | Vérification |
|--------|-----------------|--------------|
| **Node.js** | 18+ | `node --version` |
| **npm** | 8+ | `npm --version` |
| **Claude Code** | 2.1+ | `claude --version` |
| **React basics** | JSX syntax | Connaître `<div>`, `props`, `useState` |

**Temps estimé**: 15-20 minutes (première fois)

---

## 📦 Étape 1: Installation des Remotion Skills

### Option A: Via skills.sh (Recommandé)

```bash
# Dans un nouveau dossier de projet
mkdir my-remotion-test && cd my-remotion-test

# Installer les skills Remotion pour Claude Code
npx skills add remotion-dev/skills
```

**Résultat attendu**:
```
✓ Skills added to .claude/skills/
  - remotion-best-practices
  - remotion-animations
  - remotion-audio
  [... 20+ skills installés]
```

### Option B: Manual (si skills.sh indisponible)

```bash
# Cloner le repo skills directement
git clone https://github.com/remotion-dev/skills.git .claude/skills/remotion
```

---

## 🎬 Étape 2: Créer votre premier projet Remotion

### Via Claude Code (méthode recommandée)

Lancez Claude Code et utilisez ce prompt:

```
Create a new Remotion project for a simple 5-second video with:
- A fade-in title "Hello Remotion"
- Background gradient (blue to purple)
- Smooth animation

Use npx create-video to scaffold the project.
```

**Ce que Claude va faire**:
1. Exécuter `npx create-video@latest my-video`
2. Générer le boilerplate Remotion
3. Créer un composant React pour votre vidéo
4. Configurer `remotion.config.ts`

### Résultat attendu

```
my-remotion-test/
├── src/
│   ├── Root.tsx           # Entry point
│   ├── HelloWorld.tsx     # Votre composition vidéo
│   └── ...
├── public/
├── package.json
└── remotion.config.ts
```

---

## 🖼️ Étape 3: Prévisualiser votre vidéo

### Lancer le studio Remotion

```bash
npm start
```

**Résultat**: Un serveur local démarre à `http://localhost:3000`

**Interface du Studio**:
- Timeline interactive (scrub pour voir les frames)
- Live preview de votre composition
- Contrôles de playback
- Panel de props (modifier les paramètres en temps réel)

### Tester les modifications

Dans `src/HelloWorld.tsx`, modifiez le texte:

```tsx
<h1 style={{fontSize: 100}}>Hello Remotion!</h1>
```

**Hot reload** → Changement visible immédiatement dans le studio.

---

## 📹 Étape 4: Rendre votre vidéo

### Commande de base

```bash
npm run build
```

**Ce qui se passe**:
1. Remotion compile votre React code
2. Génère chaque frame (30 fps × durée = 150 frames pour 5s)
3. FFmpeg encode les frames en MP4
4. Sortie: `out/video.mp4`

### Options de rendu avancées

```bash
# Haute qualité (1080p, 60fps)
npx remotion render src/index.ts HelloWorld out/video.mp4 \
  --width 1920 \
  --height 1080 \
  --fps 60

# Format GIF
npx remotion render src/index.ts HelloWorld out/video.gif \
  --image-format png
```

---

## 🤖 Étape 5: Itérer avec Claude Code

### Prompts efficaces

**Exemple 1: Ajouter une animation**
```
Add a smooth scale animation to the title:
- Start at scale 0.8
- End at scale 1.0
- Use spring physics with config {damping: 20}
```

**Exemple 2: Ajouter de l'audio**
```
Add background music to the video:
- Use a public domain track from /public/music.mp3
- Fade in over 1 second
- Volume at 0.5
```

**Exemple 3: Séquences multiples**
```
Create a 3-scene video:
1. Intro (0-2s): Logo fade in
2. Main (2-8s): Product showcase with transitions
3. Outro (8-10s): Call to action text
```

### Pattern Claude Code efficace

```
1. Describe what you want (natural language)
   └─ Claude génère le JSX + animations

2. Preview in Studio
   └─ Vérifier visuellement

3. Iterate with specific feedback
   └─ "Make the transition slower"
   └─ "Change color to #FF6B35"

4. Render final video
   └─ npm run build
```

---

## 🐛 Troubleshooting

### Problème: "Command not found: remotion"

**Solution**:
```bash
# Installer globalement
npm install -g @remotion/cli

# Ou utiliser npx
npx remotion --version
```

### Problème: "React is not defined"

**Solution**: Vérifier que `react` et `react-dom` sont dans `package.json`:
```bash
npm install react react-dom
```

### Problème: FFmpeg error lors du rendu

**Solution**: Installer FFmpeg:
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows
choco install ffmpeg
```

### Problème: Claude génère du code qui ne compile pas

**Cause**: Skills pas chargés correctement.

**Solution**:
```bash
# Vérifier que .claude/skills/ existe
ls -la .claude/skills/remotion

# Re-sourcer les skills
claude --reload-skills
```

### Problème: Vidéo rendue mais écran noir

**Debug**:
1. Vérifier la console du Studio (F12)
2. Chercher les erreurs TypeScript
3. Vérifier que `<Composition>` a les bonnes props:
   ```tsx
   <Composition
     id="HelloWorld"
     component={HelloWorld}
     durationInFrames={150}  // 5s × 30fps
     fps={30}
     width={1920}
     height={1080}
   />
   ```

---

## 📊 Métriques de succès

Après ce quickstart, vous devriez avoir:

- ✅ Projet Remotion fonctionnel (structure scaffoldée)
- ✅ Vidéo de test rendue (MP4 dans `out/`)
- ✅ Comprendre le workflow Claude → Preview → Render
- ✅ 1-2 animations créées via prompts Claude

**Temps de rendu typique** (5s video, 1080p):
- MacBook Pro M1: ~10-15 secondes
- Intel i5: ~30-45 secondes
- Cloud (GitHub Actions): ~60-90 secondes

---

## 🎯 Prochaines étapes

### Niveau intermédiaire

1. **Ajouter des assets**:
   ```
   Claude, import an image from /public/logo.png and animate it rotating 360°
   ```

2. **Data-driven videos**:
   ```tsx
   // Générer 100 vidéos à partir d'un dataset
   const data = [{name: "John", score: 95}, ...];
   npx remotion render --props='{"data": data}'
   ```

3. **Compositions complexes**:
   ```
   Create a video with 3 scenes using <Sequence>:
   - Scene 1: Intro (0-30 frames)
   - Scene 2: Content (30-150 frames)
   - Scene 3: Outro (150-180 frames)
   ```

### Ressources

| Ressource | URL | Type |
|-----------|-----|------|
| **Remotion Docs** | [remotion.dev/docs](https://www.remotion.dev/docs/) | Documentation officielle |
| **Agent Skills Repo** | [github.com/remotion-dev/skills](https://github.com/remotion-dev/skills) | GitHub |
| **Discord Community** | [remotion.dev/discord](https://www.remotion.dev/discord) | Support communautaire (~1.5K membres) |
| **Examples Gallery** | [remotion.dev/showcase](https://www.remotion.dev/showcase) | Inspiration |

---

## 💡 Cas d'usage validés

| Use Case | Exemple | Difficulté |
|----------|---------|------------|
| **Product demos** | Feature walkthrough avec highlights | ⭐⭐ |
| **YouTube intros** | Animated logo + title card | ⭐ |
| **Data viz** | Graphiques animés, infographics | ⭐⭐⭐ |
| **Social media** | Instagram stories, TikTok templates | ⭐⭐ |
| **Explainer videos** | Step-by-step tutorials animés | ⭐⭐⭐⭐ |

**Success stories**: Icon.me ($5M ARR), Submagic ($8M ARR), Crayo ($500K/mois)

---

## ⚠️ Limitations importantes

1. **React knowledge requise**: Claude aide, mais comprendre JSX = essentiel pour debug
2. **Courbe d'apprentissage**: Premières vidéos = 2-4h. Maîtrise = 2-4 semaines
3. **Coûts**: License commerciale (>3 personnes) + Claude API + compute pour rendering
4. **Pas un remplaçant After Effects**: Paradigme différent (code vs timeline)

---

## 🎓 Exemple complet de session

```bash
# 1. Setup
mkdir remotion-demo && cd remotion-demo
npx skills add remotion-dev/skills

# 2. Claude Code prompt
claude

> Create a 10-second countdown timer video:
> - Large numbers (1-10) centered
> - Each number appears for 1 second
> - Use spring animations for each transition
> - Background gradient that changes color per number
> - Add a "beep" sound effect on each number change

# Claude génère le code...

# 3. Preview
npm start
# Ouvrir http://localhost:3000

# 4. Ajustements
> Make the spring animation bouncier (increase damping to 40)
> Change gradient colors to warm tones (orange to red)

# 5. Render final
npm run build

# Résultat: out/video.mp4 (10 secondes, 300 frames)
```

**Durée totale session**: ~25 minutes (incluant itérations)

---

## 📝 Checklist avant production

- [ ] Tester le rendu complet (pas juste preview)
- [ ] Vérifier les performances (watch mode vs production)
- [ ] Valider les assets (licences, résolution, formats)
- [ ] Prévoir les coûts de rendering (cloud vs local)
- [ ] Documenter les props dynamiques (pour data-driven use cases)
- [ ] Setup CI/CD si génération automatique (GitHub Actions + Remotion Lambda)

---

## 📚 Ressources Complémentaires

### 🎯 Top 3 Essentielles (Start Here)

| Ressource | Type | URL | Pourquoi |
|-----------|------|-----|----------|
| **Official Resources** | Hub central | [remotion.dev/docs/resources](https://www.remotion.dev/docs/resources) | 50+ templates, intégrations, effects |
| **Fireship Tutorial** | Vidéo (8min) | [This video was made with code](https://www.youtube.com/watch?v=deg8bOoziaE) | Intro ultra-rapide, 1M+ vues |
| **Discord Community** | Support live | [Remotion Discord](https://discord.com/servers/remotion-809501355504959528) | 5.6K+ membres, bot AI intégré |

### 📖 Tutoriels Écrits Recommandés

| Article | Niveau | URL | Spécialité |
|---------|--------|-----|-----------|
| **ClipCat Beginner's Guide** | Débutant | [Create Videos Programmatically](https://www.clipcat.com/blog/create-videos-programmatically-using-react-a-beginners-guide-to-remotion/) | Installation pas-à-pas |
| **Prismic Tutorial** | Débutant | [Learn to Create Videos](https://prismic.io/blog/create-videos-with-code-remotion-tutorial) | Fondamentaux complets |
| **SitePoint Introduction** | Intermédiaire | [Remotion Tutorial](https://www.sitepoint.com/remotion-create-animated-videos-using-html-css-react/) | Data fetching, composants |

### 🎥 Tutoriels Vidéo par Objectif

**Démarrer rapidement** (15 min):
- [Fireship - This video was made with code](https://www.youtube.com/watch?v=deg8bOoziaE) (8:41, 1M vues)

**Apprendre en profondeur** (1-2h):
- [CoderOne - Create Videos with React](https://www.youtube.com/watch?v=VOX98RoITMk) (1h, exemple complet logo animé)

**Intégration Claude Code** (30 min):
- [Snapper AI - Generate Animated Videos](https://www.youtube.com/watch?v=EwKCAgt4aKI) (9:48, jan 2026)
- [chantastic - Making Remotion Videos](https://www.youtube.com/watch?v=z87bczUZ0uo) (30 min, jan 2026)

### 🛠️ Templates & Exemples

| Template | Usage | Lien | Complexité |
|----------|-------|------|-----------|
| **Hello World** | Premier projet | [Official Templates](https://www.remotion.dev/templates/) | ⭐ Simple |
| **Audiogram** | Podcast viz | [Official Templates](https://www.remotion.dev/templates/) | ⭐⭐ Moyen |
| **GitHub Unwrapped** | Cas prod réel | [github.com/remotion-dev/github-unwrapped](https://github.com/remotion-dev/github-unwrapped) | ⭐⭐⭐ Avancé |

**Page complète**: [remotion.dev/docs/resources](https://www.remotion.dev/docs/resources) (50+ templates maintenus)

### 🏆 Success Stories (Inspiration)

Produits réels générant des revenus avec Remotion:

- **Icon.me**: $5M ARR en 30 jours (créateur d'annonces)
- **Revid.ai**: $1M ARR en 15 mois (plateforme vidéo IA)
- **Typeframes**: Post-acquisition (vidéos présentation produit)

[Voir tous les showcases](https://www.remotion.dev/showcase)

### 💬 Où Poser des Questions

| Plateforme | URL | Meilleur pour | Activité |
|------------|-----|---------------|----------|
| **Discord** | [Remotion Discord](https://discord.com/servers/remotion-809501355504959528) | Support rapide, bot AI | ⭐⭐⭐⭐⭐ Très élevée |
| **GitHub Discussions** | [remotion-dev/discussions](https://github.com/orgs/remotion-dev/discussions) | Questions architecturales | ⭐⭐⭐ Modérée |
| **Stack Overflow** | [#remotion tag](https://stackoverflow.com/questions/tagged/remotion) | Problèmes spécifiques | ⭐⭐ Faible |

**Tip**: Sur Discord, taggez le bot CrawlChat AI pour réponses instantanées avec sources docs.

### 🚀 Ressources Avancées

**Performance & Optimization**:
- [Official Performance Docs](https://www.remotion.dev/docs/performance)
- [YouTube: Optimizing Remotion Lambda](https://www.youtube.com/results?search_query=optimizing+remotion+lambda+jonny+burger) (Jonny Burger, 17 min)

**Agent Skills & IA**:
- [Official AI Skills Docs](https://www.remotion.dev/docs/ai/skills)
- [AIbase Article](https://news.aibase.com/news/24827) (jan 2026, très récent)

**Déploiement**:
- [Railway Template](https://railway.com/deploy/remotion-on-rails) (1-click deploy)
- [Lambda Docs](https://www.remotion.dev/docs/lambda) (AWS serverless rendering)

### 📊 Paquets Utiles

| Paquet | Usage | Installation |
|--------|-------|--------------|
| `@remotion/shapes` | Formes SVG (triangles, étoiles) | `npm i @remotion/shapes` |
| `remotion-transition-series` | Transitions entre scènes | `npm i remotion-transition-series` |
| `remotion-subtitle` | Sous-titres automatiques | `npm i remotion-subtitle` |
| `@remotion/tailwind` | Intégration Tailwind CSS | `npm i @remotion/tailwind` |

[Liste complète sur Resources page](https://www.remotion.dev/docs/resources)

---

## 🎓 Itinéraire d'Apprentissage Suggéré

### Semaine 1: Fondamentaux (6-8h)
1. Lire docs officielles (2h)
2. Regarder Fireship tutorial (15 min)
3. Faire ClipCat guide - créer Hello World (2h)
4. Reproduire exemple CoderOne (2-3h)
5. Joindre Discord, poser questions

### Semaine 2: Pratique (8-10h)
1. Créer 3 vidéos différentes (intros, countdown, data viz)
2. Explorer GitHub Unwrapped code source
3. Tester intégration Claude Code (Agent Skills)
4. Expérimenter avec paquets (@remotion/shapes, transitions)

### Semaine 3: Production (ongoing)
1. Créer projet réel pour use case spécifique
2. Optimiser performances (Lambda si nécessaire)
3. Setup CI/CD (GitHub Actions)
4. Partager sur Discord pour feedback

---

**Créé**: 2026-01-23
**Mis à jour**: 2026-01-24 (ajout ressources)
**Testé avec**: Claude Code 2.1.17, Remotion 4.x, Node.js 20.x
**Durée moyenne**: 15-20 min (première vidéo), 5-10 min (suivantes)
**Ressources vérifiées**: 2026-01-24 (Perplexity Pro, 50+ sources)
