# AstroPaws 🐾🚀

![Work in progress](https://img.shields.io/badge/status-work--in--progress-yellow)
![Licence](https://img.shields.io/badge/license-CC--BY--NC--4.0-blue)
![Made with Python](https://img.shields.io/badge/made%20with-Python-blue)

## Sommaire

- [Fonctionnalités](#fonctionnalités)
- [Synopsis du jeu](#synopsis-du-jeu)
- [Contrôles du jeu](#contrôles-du-jeu)
- [Développement en cours](#développement-en-cours)
- [Roadmap à court terme](#roadmap-à-court-terme)
- [Installation](#installation)
- [Création & Musique](#création--musique)
- [Licence](#licence)

**AstroPaws** est un jeu vidéo rétro inspiré du style Atari 7800.  
Vous incarnez AstroPaws, un courageux chat astronaute qui explore l’espace pour collecter des croquettes cosmiques et créer la légendaire "pâtée de l’espace".

🎮 **Fonctionnalités :**
- Graphismes simples et pixelisés façon Atari.
- Contrôles fluides et gameplay accessible.
- Ennemis robotiques et dangers spatiaux.
- Système de score et d'explosions vintage.
- Jeu 100 % open source sous licence CC BY-NC 4.0.

## Synopsis du jeu :

**Lointain secteur L-88.**  
Depuis la station Alpha-Felis, un signal d’alerte retentit dans le vide spatial : la dernière réserve de Pâtée Galactique™ a disparu !

Le Capitaine AstroPaws — félin gourmet et astronaute légendaire — s’élance dans le cosmos avec son Jetpack Cosmique. Sa mission ? Récupérer les sept ingrédients sacrés pour concocter la légendaire pâtée de l’espace.

Mais l’univers est loin d’être paisible…  
Chiens errants, rats mutants, et souris robotiques patrouillent les confins stellaires. Chaque tir d’eau est précieux, chaque croquette compte, et chaque réserve d’eau sauvée peut faire la différence.

Parviendrez-vous à éviter les collisions, à viser juste, à gérer vos ressources, et à vaincre les gardiens de l’espace pour restaurer le festin sacré ?

🧪 Collecte. 💧 Précision. 🐾 Survie.  
Bienvenue dans **AstroPaws: Gourmet Quest**.

➡️ Retrouvez tous les détails du gameplay dans le fichier [GAMEPLAY.md](GAMEPLAY.md).

🎮 **Contrôles du jeu :**

- Flèches du clavier : déplacer AstroPaws dans l’espace.
- Barre espace : tirer un jet d’eau vers l’avant.
- Flèche directionnelle + espace : tirer un jet d’eau dans la direction choisie.

Tout cela est en cours d’élaboration et le jeu va évoluer rapidement, avec des nouveautés prévues chaque semaine.

🚧 **Développement en cours :**

AstroPaws est actuellement en phase de construction et d’expérimentation.  
Le jeu est loin d’être terminé : il s’agit des premières étapes d’un projet qui va évoluer régulièrement, avec des améliorations chaque semaine.  
Tout le développement est disponible en ligne en toute transparence pour partager l’avancée du projet avec la communauté.

## 🗺️ Roadmap à court terme :

✅ **Fonctionnalités déjà implémentées :**

1. **Mouvements et tirs**
   - Déplacement d’AstroPaws avec les flèches (4 directions + diagonales).
   - Tir directionnel (haut/bas/gauche/droite) avec la barre Espace, limité par un cooldown (300 ms).

2. **Ressources et UI**
   - Score : collecte de croquettes normales (+1) et rares (+5).
   - Eau : réservoir initial à 50 L, chaque tir en consomme 1 L, recharge de +10 L via des réserves d’eau aléatoires.
   - Vies : 9 vies représentées par des cœurs en haut à droite ; perte d’une vie au contact d’un chien.

3. **Ennemis avec santé**
   - Trois types d’ennemis (souris, rats, chiens) avec 1–2–3 tirs nécessaires pour les éliminer.
   - Récompenses à la destruction : +10 / +20 / +30 points.
   - Pénalités en collision : –5 / –10 points (souris / rat), –1 vie (chien) + grosse explosion.

4. **Décor et effets**
   - Fond spatial procédural (étoiles + planètes colorées, effet parallaxe).
   - Effets d’explosion (20 particules standard, 50 pour les chiens).

5. **Menus et écrans**
   - MENU : fond étoilé animé, image d’accueil redimensionnée, invites clignotantes (“PRESS SPACE TO START”, “PRESS S FOR STORY”, “PRESS Q TO QUIT”).
   - STORY : texte défilant façon Star Wars, wrapping automatique, vitesse ralentie, retour automatique ou touche Espace / Échap.
   - PLAYING : boucle de jeu active.
   - PAUSE : touche P, écran noir avec statistiques (score, eau, vies), titre clignotant, options pour reprendre ou quitter, image du chat qui dort.
   - GAME OVER : message “GAME OVER” à l’écran et fin de la partie.

---

🚀 **Feuille de route à venir :**

1. **Musique et effets sonores 8-bit**
   - Charger et jouer des fichiers .ogg (boucle de fond + effets : tir, explosion, collecte).
   - Menu Options pour régler volume musique / effets.

2. **Animation des sprites**
   - AstroPaws : orientation selon la direction (flip ou sprites dédiés).
   - Ennemis : remplacement des rectangles par des sprites pixel art, avec animation.

3. **Écran d’accueil et sous-menus**
   - Ajouter un sous-menu Options (volume, contrôles).
   - Améliorer les transitions entre écrans (fondu, balayage…).

4. **Boss et niveaux**
   - Ajouter un ou plusieurs boss finaux avec mécaniques uniques.
   - Créer plusieurs zones/niveaux (champs d’astéroïdes, nébuleuses, etc.).

5. **Mini-carte & HUD avancé**
   - Implémenter une mini-carte indiquant la position d’AstroPaws et des ennemis.
   - Afficher des indicateurs de progression ou barres de santé des boss.

6. **Polish et équilibrage**
   - Ajuster fréquences d’apparition, vitesses, coût en eau, points.
   - Corriger les éventuels bugs de collision ou de logique.

7. **Fonctionnalités supplémentaires**
   - Sauvegarde et gestion des high-scores.
   - Support manette.
   - Écrans de victoire et crédits de fin.

💾 **Installation :**

Clonez ce dépôt :

```bash
git clone https://github.com/Dr-John-8bit/AstroPaws
```

🎨 Création & Musique :

Ce jeu est développé par Dr John 8bit.
La bande-son et les bruitages sont faits maison pour une immersion totale dans l’univers d’AstroPaws.

🧩 Licence :

Ce projet est sous licence Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
Vous êtes libres de le modifier et de le partager en citant l’auteur, mais l’utilisation commerciale est interdite.

⸻

🐈‍⬛ “AstroPaws partira à la conquête de la galaxie, une croquette à la fois !”