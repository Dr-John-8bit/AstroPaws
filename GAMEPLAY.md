# Synthèse du Gameplay de AstroPaws

Voici une synthèse complète du gameplay tel qu’il est implémenté dans le fichier `main.py`, ainsi qu’une explication détaillée du fonctionnement de chaque système :

---

## 1. AstroPaws, ton personnage

### Apparence et déplacement
- **Sprite** : AstroPaws est représenté par un sprite (image `astro_paws.png` redimensionnée à 80×80 pixels).
- **Déplacement** : Se déplace sur une fenêtre de 800×600 pixels grâce aux flèches du clavier.
- **Vitesse** : 5 pixels par frame.

---

## 2. Gestion des vies

### Initialisation
- Le joueur débute avec **9 vies**.
- Chaque vie est affichée sous forme d’un petit cœur (image `heart.png` redimensionnée à 20×20 pixels) en haut à droite de l’écran.

### Perte de vies
- **Chien** : Si AstroPaws est touché par un chien (`dog`), le joueur perd **1 vie**.
- **Rat et Souris** : Pour ces ennemis, la perte se fait au niveau du score (pas de perte de vie).

### Game Over
- Le jeu se termine lorsque le nombre de vies atteint **0**.
- Un message **"GAME OVER"** apparaît brièvement avant la fin de la partie.

---

## 3. Système de score

### Début
- Le score initial est **0**.

### Récompenses lors de la collecte de croquettes
- **Croquette normale** : rapporte **+1 point**.
- **Croquette rare** : rapporte **+5 points**.

### Récompenses lors de l’élimination d’ennemis avec les tirs d’eau
Chaque ennemi possède une **santé** (health) qui détermine le nombre de tirs nécessaires pour le détruire.

#### Mouse (souris)
- **Santé initiale** : 1 (un tir suffit pour la détruire).
- **Récompense** : +10 points.

#### Rat
- **Santé initiale** : 2 (deux tirs nécessaires).
- **Récompense** : +20 points.

#### Dog (chien)
- **Santé initiale** : 3 (trois tirs nécessaires).
- **Récompense** : +30 points.

### Pénalités
- **Rat** : En collision avec AstroPaws, le score est réduit de **10 points**.
- **Souris** : En collision, le score est réduit de **5 points**.
- **Chien** : En collision, le joueur perd **1 vie** (aucune pénalité au score).

---

## 4. Système de tirs et gestion de l’eau

### Tirs d’eau
- Le tir est déclenché lorsque le joueur appuie sur la barre **Espace**.
- **Consommation** : Chaque tir consomme **1 litre d’eau** (la variable `water_ammo`), qui débute à **50**.
- **Cooldown** : Un délai de **300 ms** est imposé entre deux tirs (un seul tir par appui).

### Limitation
- Si la quantité d’eau (`water_ammo`) atteint **0**, AstroPaws ne peut plus tirer, ce qui impose d’en récupérer pour continuer à se défendre.

---

## 5. Gestion des objets à collecter

### Croquettes
- **Apparition** : Les croquettes apparaissent aléatoirement.
- **Durée de vie** : 5 secondes.
- **Collecte** : Lorsqu’AstroPaws entre en collision avec une croquette, celle-ci est récoltée et disparaît.
- **Récompenses** :
  - **Normal** : +1 point.
  - **Rare** : +5 points.

### Réserves d’eau
- **Fonction** : Permettent de recharger le compteur de tirs.
- **Apparition** : Faible probabilité (environ 0,5 % par frame).
- **Durée de vie** : 7 secondes.
- **Collecte** : Lorsqu’AstroPaws collecte une réserve d’eau (représentée par un petit carré bleu clair de 10×10 pixels), la variable `water_ammo` augmente de **10 litres**.

---

## 6. Les ennemis

Les ennemis apparaissent aléatoirement sur les bords de l’écran et se déplacent vers l’intérieur.

### Types d’ennemis et caractéristiques

#### Dog (chien)
- **Apparition** : 15 % des cas.
- **Taille** : 50×50 pixels.
- **Vitesse** : 2.
- **Santé** : 3 (il faut 3 tirs pour le détruire).
- **Pénalité en collision** : perte de 1 vie.
- **Récompense à la destruction** : +30 points.
- **Effet** : En collision, déclenche une grosse explosion (50 particules) et affiche *"Vous avez perdu une vie!"*.

#### Rat
- **Apparition** : Environ 35 % des cas (si le tirage `r` est inférieur à 0.5, après dévolu le chien).
- **Taille** : 30×30 pixels.
- **Vitesse** : 3.
- **Santé** : 2 (il faut 2 tirs pour le détruire).
- **Pénalité en collision** : -10 points.
- **Récompense à la destruction** : +20 points.

#### Mouse (souris)
- **Apparition** : 50 % des cas.
- **Taille** : 20×20 pixels.
- **Vitesse** : 4.
- **Santé** : 1 (1 tir suffit pour la détruire).
- **Pénalité en collision** : -5 points.
- **Récompense à la destruction** : +10 points.

### Mécanique d’interaction avec les tirs
- Lorsqu’un tir d’eau (variable `bullet`) touche un ennemi, sa **santé** est décrémentée de 1 pour chaque tir.
- L’ennemi n’est détruit et ne rapporte des points que lorsque sa santé atteint **0**.

### Collision entre AstroPaws et les ennemis
- La collision se produit lorsque le rectangle d’AstroPaws (positionné à (`astro_x`, `astro_y`) avec une taille de 50×50 pixels) entre en contact avec celui de l’ennemi.
- L’effet de la collision dépend du type d’ennemi, comme décrit ci-dessus.

---

## 7. Autres éléments visuels

### Fond spatial procédural
- L’arrière-plan est composé d’étoiles (petits cercles blancs avec effet de parallaxe) et de planètes colorées générées aléatoirement.

### Effets d’explosion
- Lorsqu’un ennemi est détruit par les tirs, une explosion est générée à sa position.
- **Explosion standard** : utilise 20 particules.
- **Explosion pour chien** : une explosion plus importante (50 particules).

---

## En résumé

- Le joueur contrôle **AstroPaws** dans un environnement spatial.
- Le joueur dispose initialement de **9 vies**, d’un score de **0** et de **50 litres d’eau** pour tirer des jets d’eau.
- **Tirs d’eau** : Consomment l’eau et sont limités par un cooldown de **300 ms** par tir.
- **Objets à collecter** : Des croquettes et des réserves d’eau apparaissent aléatoirement pour permettre de gagner des points et de recharger les tirs.
- **Ennemis** : Des ennemis (chien, rat, souris) apparaissent aléatoirement sur les bords et se déplacent vers l’intérieur. Leur élimination rapporte des points, tandis que leur collision affecte soit le score (rat et souris), soit les vies (chien).
- Le gameplay propose un défi équilibré entre le déplacement, le tir, la gestion des ressources et l’évitement des ennemis, renforcé par des effets visuels grâce aux explosions et à l’arrière-plan dynamique.


---

## ✅ Fonctionnalités déjà implémentées

### 1. Mouvements et tirs
- Déplacement d’AstroPaws avec les flèches (4 directions + diagonales).
- Tir directionnel (haut/bas/gauche/droite) avec la barre **Espace**, limité par un cooldown de **300 ms**.

### 2. Ressources et UI
- **Score** : collecte de croquettes normales (+1) et rares (+5).
- **Eau** : réservoir initial à 50 L, chaque tir en consomme 1 L, recharge de +10 L via des réserves d’eau aléatoires.
- **Vies** : 9 vies représentées par des cœurs en haut à droite ; perte d’une vie au contact d’un chien.

### 3. Ennemis avec santé
- Trois types d’ennemis (souris, rats, chiens) avec **santé** respective de 1, 2, et 3 tirs.
- Récompenses à la destruction : +10 / +20 / +30 points.
- Pénalités en collision : –5 / –10 points pour souris / rat, –1 vie + grosse explosion pour chien.

### 4. Décor et effets
- Fond spatial procédural (étoiles + planètes colorées, effet parallaxe).
- Effets d’explosion (20 particules standard, 50 pour les chiens).

### 5. Menus et écrans
- **MENU** : fond étoilé animé, image d’accueil redimensionnée, invites clignotantes : “PRESS SPACE TO START”, “PRESS S FOR STORY”, “PRESS Q TO QUIT”.
- **STORY** : texte défilant façon *Star Wars*, wrapping automatique, vitesse ralentie, retour automatique ou touche Espace / Échap.
- **PLAYING** : boucle de jeu active.
- **PAUSE** : touche **P**, écran noir avec stats (score, eau, vies), titre “PAUSE” clignotant, options “Press P to resume” (vert) et “Press Q to quit” (rouge), image du chat qui dort en bas.
- **GAME OVER** : apparition d’un message “GAME OVER” et fin de la partie.

---

## 🚀 Feuille de route mise à jour

### 1. Musique et effets sonores 8-bit
- Charger et jouer des fichiers `.ogg` (musique de fond en boucle + effets : tir, explosion, collecte).
- Ajouter un menu **Options** pour régler le volume de la musique / des effets.

### 2. Animation des sprites
- AstroPaws : gestion de l’orientation (flip ou sprites dédiés) selon la direction.
- Ennemis : remplacer les rectangles par des sprites pixel art, ajouter quelques frames d’animation.

### 3. Écran d’accueil et sous-menus
- Ajouter un sous-menu **Options** (volume, contrôles).
- Améliorer les transitions (fondu, balayage…) entre les différents écrans.

### 4. Boss et niveaux
- Concevoir un ou plusieurs boss finaux avec mécaniques spéciales.
- Ajouter des zones / niveaux différents (champs d’astéroïdes, nébuleuses…).

### 5. Mini-carte & HUD avancé
- Implémenter une mini-carte pour visualiser la position d’AstroPaws et des ennemis.
- Afficher des indicateurs de progression ou barres de santé pour les boss.

### 6. Polish et équilibrage
- Ajuster les fréquences d’apparition, vitesses, coûts en eau, récompenses.
- Tester et corriger les bugs de collision ou de logique.

### 7. Fonctionnalités supplémentaires
- Système de **sauvegarde** et **high-scores**.
- **Support manette**.
- Ajout d’écrans de **victoire** et de **crédits**.