# Design System — Messagerie Clone

> Référence de conception du projet. Mise à jour au fur et à mesure du développement.
> Lien Stitch : [Ouvrir le projet](https://stitch.google.com/projects/15697197534492891007)

---

## 🎨 Identité visuelle

### Palette de couleurs

| Token | Valeur | Usage |
|---|---|---|
| `accent` | `#2563EB` | Boutons principaux, liens actifs, focus |
| `accent-hover` | `#1D4ED8` | État hover des boutons principaux |
| `accent-light` | `#EFF6FF` | Backgrounds légers liés à l'accent |
| `success` | `#10B981` | Indicateur en ligne, confirmations |
| `gray-50` | `#F8FAFC` | Fond de page clair |
| `gray-100` | `#F1F5F9` | Hover items, inputs clair |
| `gray-200` | `#E2E8F0` | Bordures claires |
| `gray-300` | `#CBD5E1` | Scrollbar thumb clair |
| `gray-400` | `#94A3B8` | Texte secondaire, icônes inactives |
| `gray-500` | `#64748B` | Sous-titres |
| `gray-600` | `#475569` | Labels sombres |
| `gray-700` | `#334155` | Textes sombres |
| `gray-800` | `#1E293B` | Backgrounds dark inputs |
| `gray-900` | `#0F172A` | Fond de card dark |
| `gray-950` | `#020617` | Fond de page dark |

### Mode sombre

Le mode sombre est géré via la classe `dark` sur `<html>`. L'utilisateur peut basculer via le toggle dans les paramètres. La préférence est sauvegardée dans `localStorage`.

```js
// Chargement du thème au démarrage (dans base.html)
if (localStorage.theme === 'dark' || prefers-color-scheme: dark)
    document.documentElement.classList.add('dark')
```

---

## 🔤 Typographie

| Propriété | Valeur |
|---|---|
| Police | **Inter** (Google Fonts) |
| Poids | 300, 400, 500, 600, 700, 800 |
| Corps de texte | 14–15px |
| Labels | 13px, `font-semibold` |
| Titres de page | 22–28px, `font-bold`, `tracking-tight` |
| Petits textes | 11–12px |

---

## 📐 Tokens de design

### Rayons (border-radius)

| Nom | Valeur | Usage |
|---|---|---|
| `rounded-xl` | 12px | Inputs, boutons |
| `rounded-2xl` | 16px | Items de liste, modals |
| `rounded-3xl` | 24px | Cards principales |
| `rounded-full` | 9999px | Avatars, badges, pills |

### Ombres

| Nom | Valeur | Usage |
|---|---|---|
| `shadow-soft` | `0 20px 25px -5px rgba(0,0,0,0.05)` | Card principale |
| `shadow-floating` | `0 0 50px -12px rgba(37,99,235,0.18)` | Bouton accent, logo |
| `shadow-sm` | — | Avatars, petites cartes |

---

## 🧩 Composants

### Card (page d'authentification)

```
bg-white dark:bg-gray-900
rounded-3xl shadow-soft
ring-1 ring-gray-900/5 dark:ring-white/10
p-10 max-w-[440px]
```

### Champ de saisie (Input)

```
bg-gray-50 dark:bg-gray-800
border border-gray-200 dark:border-gray-700
rounded-xl py-3 pl-10 pr-4
text-[15px] text-gray-900 dark:text-white
focus:ring-2 focus:ring-accent/40 focus:border-accent
```

→ Icône positionnée en absolu à gauche (`pl-3.5`)

### Bouton principal (CTA)

```
bg-accent hover:bg-accent-hover text-white
font-semibold py-3.5 rounded-xl
hover:shadow-floating active:scale-[0.98]
transition-all
```

### Bouton social (Google / Facebook)

```
bg-gray-50 dark:bg-gray-800
border border-gray-200 dark:border-gray-700
rounded-xl py-2.5 px-4
text-sm font-semibold
hover:bg-gray-100 dark:hover:bg-gray-700
```

### Sidebar item (conversation)

```
flex items-center gap-3
p-3 rounded-2xl
hover:bg-gray-100 dark:hover:bg-gray-800/70
transition-colors cursor-pointer group
```

### Bulle de message (envoyé)

```
bg-accent text-white
rounded-[18px] rounded-br-[4px]
px-4 py-2.5 text-[14px]
shadow-sm
```

### Bulle de message (reçu)

```
bg-white dark:bg-gray-800
text-gray-900 dark:text-gray-100
rounded-[18px] rounded-bl-[4px]
border border-gray-100 dark:border-gray-700/60
px-4 py-2.5 text-[14px]
```

---

## 🖥️ Pages et layouts

### Pages d'auth (Login / Register)

```
Layout : flex-col items-center justify-center gap-6 min-h-screen
Background : gradient from-slate-50 to-slate-200 (light) / from-gray-950 to-gray-900 (dark)
Contenu : Card centrée max-w-[440px] + liens footer en-dessous
```

### Interface de chat (SPA)

```
Layout : h-screen flex overflow-hidden
├── Sidebar : w-[340px] flex-col, border-r
│   ├── Header (titre + boutons)
│   ├── Search input
│   ├── Stories row (overflow-x scroll)
│   ├── Tabs (Tout / Non lus / Groupes)
│   ├── Liste conversations (flex-1 overflow-y-auto)
│   │   └── Section contacts (si contacts présents)
│   └── Footer profil (avatar + nom + lien settings)
│
└── Zone chat principale (flex-1 flex-col)
    ├── Header (avatar + nom + statut + actions)
    ├── Liste messages (flex-1 overflow-y)
    └── Barre de saisie (input + bouton envoyer)
```

### Page Paramètres (Profile)

```
Layout : flex-col items-center min-h-screen bg-gray-100 pt-8
├── Header page (titre + bouton retour)
├── Card profil (avatar + nom + email + date)
├── Section préférences (dark mode toggle, notifications, confidentialité)
└── Section actions (déconnexion, suppression)
```

---

## 🔌 Fonctionnalités temps réel

- **WebSocket** via Django Channels (Daphne ASGI)  
- Protocole : `ws://` en dev, `wss://` en prod  
- Route : `/ws/chat/<discussion_id>/`  
- Consumer : `ChatConsumer` (async, vérifie participation avant connexion)  
- Envoi : `{ message: "..." }`  
- Réception : `{ message, expediteur_id, expediteur_nom, date }`  

---

## 📋 Écrans Stitch (référence)

| Écran | ID | Description |
|---|---|---|
| Authentication Page | `18e6f2689e6043d3990b7785c4ab92ba` | Page de login/register |
| Main Messaging Interface | `ec9e354bd31e44cd806326a48c5fc5fc` | Interface de chat principale |
| Profile Settings | `dc102dc9c316492ea5bdf1f18a8b7cc6` | Page des paramètres |
| Group Management | `13a7eb306e95476a86812910ac88b910` | Gestion des groupes |
| Story View | `6d2a443e97e346aea0151f6865cb6751` | Vue plein écran des statuts |

---

## 📁 Structure des fichiers templates

```
whatsapp-app/
├── templates/
│   └── base.html                    ← Base HTML, Tailwind CDN, toasts, dark mode
├── accounts/templates/accounts/
│   ├── login.html                   ← Page connexion
│   ├── register.html                ← Page inscription
│   └── profile.html                 ← Paramètres utilisateur
├── chat/templates/chat/
│   └── index.html                   ← Interface de chat SPA (WebSocket)
└── static/
    └── (assets statiques)
```

---

*Dernière mise à jour : 06 mars 2026*
