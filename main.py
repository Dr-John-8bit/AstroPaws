import pygame
import sys
import random
import math
import textwrap

# Importer la configuration des niveaux
import levels
# Index du niveau courant (initialisé à 0 localement)
level_idx = 0

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre (agrandies)
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("AstroPaws")

# Définition de quelques couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
GOLD = (255, 223, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)
CYAN  = (0, 255, 255)

# Ajout des listes pour les ennemis et explosions
enemy_list = []
explosion_list = []

def create_explosion(x, y, color=YELLOW, num_particles=20):
    for i in range(num_particles):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, 3)
        dx = math.cos(angle) * speed
        dy = math.sin(angle) * speed
        lifetime = random.randint(20, 40)
        explosion_list.append({'x': x, 'y': y, 'dx': dx, 'dy': dy, 'lifetime': lifetime, 'color': color})

# Effet de warp d'étoiles suivi d'un flash blanc
def warp_effect():
    # Tunnel d'étoiles puis flash blanc
    center_x, center_y = screen_width // 2, screen_height // 2
    # Effet warp encore plus dense et plus lent
    for _ in range(30):  # plus d'étapes pour densifier
        screen.fill(BLACK)
        # Déplacer et dessiner les étoiles principales
        for star in star_list:
            dx = star['x'] - center_x
            dy = star['y'] - center_y
            star['x'] = center_x + dx * 1.15
            star['y'] = center_y + dy * 1.15
            pygame.draw.circle(screen, WHITE, (int(star['x']), int(star['y'])), 1)
        # Ajouter des étoiles supplémentaires pour saturer l'effet
        for _ in range(200):  # étoile bonus
            rx = random.randint(0, screen_width)
            ry = random.randint(0, screen_height)
            ddx = rx - center_x
            ddy = ry - center_y
            x2 = center_x + ddx * 1.15
            y2 = center_y + ddy * 1.15
            pygame.draw.circle(screen, WHITE, (int(x2), int(y2)), 1)
        pygame.display.flip()
        pygame.time.delay(70)  # délai encore un peu plus long pour percevoir l'effet
    # Flash blanc
    screen.fill(WHITE)
    pygame.display.flip()
    pygame.time.delay(100)
    # Régénérer les étoiles pour le prochain level
    for star in star_list:
        star['x'] = random.randint(0, screen_width)
        star['y'] = random.randint(0, screen_height)

croquette_size = 10
croquette_lifetime = 5000  # Durée de vie en millisecondes (5 secondes)
croquette_list = []
for i in range(5):
    x = random.randint(0, screen_width - croquette_size)
    y = random.randint(0, screen_height - croquette_size)
    spawn_time = pygame.time.get_ticks()
    if random.random() < 0.1:
        croquette_type = "rare"
    else:
        croquette_type = "normal"
    croquette_list.append({'x': x, 'y': y, 'spawn_time': spawn_time, 'type': croquette_type})

# Création des réserves d'eau (objets à collecter pour augmenter l'eau)
water_item_list = []

# Génération d'un fond spatial procédural
num_stars = 50
star_list = []
for i in range(num_stars):
    x = random.randint(0, screen_width)
    y = random.randint(0, screen_height)
    speed = random.uniform(0.2, 1.0)
    star_list.append({'x': x, 'y': y, 'speed': speed})

# Modification pour générer des planètes avec des couleurs aléatoires

num_planets = 3
planet_list = []
for i in range(num_planets):
    x = random.randint(0, screen_width)
    y = random.randint(0, screen_height)
    size = random.randint(8, 20)
    speed = random.uniform(0.1, 0.5)
    color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    planet_list.append({'x': x, 'y': y, 'size': size, 'speed': speed, 'color': color})

# ==== OVNIs décoratifs ====
class UFO:
    def __init__(self, x, y, scale=1.0, speed=0.5, color=(150, 200, 255)):
        self.x = x
        self.y = y
        self.scale = scale
        self.speed = speed
        self.angle = random.uniform(0, 2 * math.pi)
        # Contour vectoriel d'un saucer (disque + dôme)
        self.pointlist = [(-9,0),(-3,-3),(-2,-6),(2,-6),(3,-3),(9,0),(-9,0),(-3,4),(3,4),(9,0)]
        self.color = color
    def update(self):
        # Avance et oscille légèrement
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.angle += random.uniform(-0.05, 0.05)
        # Wrap-around de l'UFO
        if self.x < 0: self.x = screen_width
        elif self.x > screen_width: self.x = 0
        if self.y < 0: self.y = screen_height
        elif self.y > screen_height: self.y = 0
    def draw(self):
        # Calculer et tracer le contour
        transformed = []
        for px, py in self.pointlist:
            tx = px * self.scale
            ty = py * self.scale
            rx = tx * math.cos(self.angle) - ty * math.sin(self.angle)
            ry = tx * math.sin(self.angle) + ty * math.cos(self.angle)
            transformed.append((self.x + rx, self.y + ry))
        pygame.draw.aalines(screen, self.color, True, transformed)

# Créer quelques OVNIs décoratifs
ufo_list = []
for _ in range(2):
    ufo_list.append(
        UFO(
            random.uniform(0, screen_width),
            random.uniform(0, screen_height),
            scale=random.uniform(0.5, 1.0),
            speed=random.uniform(0.2, 0.7),
            color=(random.randint(100,255), random.randint(100,255), random.randint(100,255))
        )
    )


# Charger le sprite d'AstroPaws et ses versions gauche/droite/haut/bas
astro_sprite_right = pygame.image.load("images/astro_paws.png").convert_alpha()
astro_sprite_right = pygame.transform.scale(astro_sprite_right, (80, 80))
astro_sprite_left = pygame.transform.flip(astro_sprite_right, True, False)
# Créer les versions pour haut et bas en pivotant la version droite
astro_sprite_up = pygame.transform.rotate(astro_sprite_right, 90)
astro_sprite_down = pygame.transform.rotate(astro_sprite_right, -90)
# Direction initiale
astro_facing = "right"

# Charger les sprites des croquettes et de l'eau
# Agrandir les sprites de croquettes et d'eau
# Agrandir les sprites de croquettes
brown_croquette_sprite = pygame.image.load("images/browncroquette.png").convert_alpha()
brown_croquette_sprite = pygame.transform.scale(brown_croquette_sprite, (30, 30))  # croquette normale agrandie
# Agrandir la croquette dorée
gold_croquette_sprite  = pygame.image.load("images/goldcroquette.png").convert_alpha()
gold_croquette_sprite  = pygame.transform.scale(gold_croquette_sprite,  (40, 40))  # croquette rare encore plus grande
# Agrandir la réserve d'eau
water_sprite           = pygame.image.load("images/water.png").convert_alpha()
water_sprite           = pygame.transform.scale(water_sprite,           (30, 30))


# Charger l'image du coeur pour les vies
heart_sprite = pygame.image.load("images/heart.png").convert_alpha()
heart_sprite = pygame.transform.scale(heart_sprite, (20, 20))

# Charger l'image de l'écran d'accueil
welcome_image = pygame.image.load("images/ecranaccueil.png").convert_alpha()
welcome_image = pygame.transform.scale(welcome_image, (400, 300))  # taille réduite

chat_sleep_image = pygame.image.load("images/chatdort.png").convert_alpha()
chat_sleep_image = pygame.transform.scale(chat_sleep_image, (360, 240))

# Charger la tête d’AstroPaws pour l’écran VS
astro_head = pygame.image.load("images/astro_paws_head.png").convert_alpha()
astro_head = pygame.transform.scale(astro_head, (120, 120))

# Charger les sprites des ennemis
mouse_sprite = pygame.image.load("images/badguymouse.png").convert_alpha()
mouse_sprite = pygame.transform.scale(mouse_sprite, (20, 20))
rat_sprite   = pygame.image.load("images/badguyrat.png").convert_alpha()
rat_sprite   = pygame.transform.scale(rat_sprite,   (30, 30))
dog_sprite   = pygame.image.load("images/badguydog.png").convert_alpha()
dog_sprite   = pygame.transform.scale(dog_sprite,   (50, 50))

# Charger les sprites morts pour la transition de niveau
# Mettre les sprites morts à la taille d'AstroPaws (astro_head)
mouse_dead_sprite = pygame.image.load("images/badguymouse_dead.png").convert_alpha()
rat_dead_sprite   = pygame.image.load("images/badguyrat_dead.png").convert_alpha()
dog_dead_sprite   = pygame.image.load("images/badguydog_dog.png").convert_alpha()
dead_size = astro_head.get_size()
mouse_dead_sprite = pygame.transform.scale(mouse_dead_sprite, dead_size)
rat_dead_sprite   = pygame.transform.scale(rat_dead_sprite,   dead_size)
dog_dead_sprite   = pygame.transform.scale(dog_dead_sprite,   dead_size)

# Charger l'image de Game Over
gameover_image = pygame.image.load("images/gameover.png").convert_alpha()
gameover_image = pygame.transform.scale(gameover_image, (400, 200))
 # Charger l'image de victoire de niveau
youwin_image = pygame.image.load("images/youwin.png").convert_alpha()
youwin_image = pygame.transform.scale(youwin_image, (400, 200))

# Charger l'image du guide (doc)
doctor_image = pygame.image.load("images/astropaws_doctor.png").convert_alpha()
doctor_image = pygame.transform.scale(doctor_image, (150, 150))

# Charger les icônes d'inventaire
# Agrandissement des icônes d'inventaire
shield_icon = pygame.image.load("images/shield_icon.png").convert_alpha()
shield_icon = pygame.transform.scale(shield_icon, (48, 48))
hyper_icon  = pygame.image.load("images/hyper_icon.png").convert_alpha()
hyper_icon  = pygame.transform.scale(hyper_icon,  (48, 48))

ingredient_icon = pygame.image.load("images/ingredient_icon.png").convert_alpha()
ingredient_icon = pygame.transform.scale(ingredient_icon, (48, 48))

# Sprites spécifiques des ingrédients
poulet_sprite   = pygame.image.load("images/ingredient_poulet.png").convert_alpha()
poulet_sprite   = pygame.transform.scale(poulet_sprite, (48, 48))
thon_sprite     = pygame.image.load("images/ingredient_thon.png").convert_alpha()
thon_sprite     = pygame.transform.scale(thon_sprite, (48, 48))
carotte_sprite  = pygame.image.load("images/ingredient_carotte.png").convert_alpha()
carotte_sprite  = pygame.transform.scale(carotte_sprite, (48, 48))
fragment_sprite = pygame.image.load("images/ingredient_fragment_croquette.png").convert_alpha()
fragment_sprite = pygame.transform.scale(fragment_sprite, (48, 48))

# Mapping clé → sprite pour l’inventaire
ingredient_sprites = {
    'ingredient_poulet': poulet_sprite,
    'ingredient_thon': thon_sprite,
    'ingredient_carotte': carotte_sprite,
    'ingredient_fragment_croquette': fragment_sprite,
}

# Position initiale d'AstroPaws
astro_x = screen_width // 2
astro_y = screen_height // 2
speed = 5  # Vitesse de déplacement

# Gestion des tirs
bullet_list = []
bullet_speed = 10
bullet_width = 10
bullet_height = 4

# Initialiser le score, les vies et le font
score = 0
lives = 9
water_ammo = 10
pygame.font.init()
# Augmentation de la taille de la police pour une meilleure lisibilité
score_font = pygame.font.SysFont(None, 48)
# Police plus petite pour les sous-titres et les blagues
subtitle_font = pygame.font.SysFont(None, 32)

next_shot_allowed_time = 0
cooldown_time = 300

# Horloge pour contrôler le taux de rafraîchissement (60 FPS)
clock = pygame.time.Clock()

#
#
# État du jeu : MENU, STORY, ou PLAYING
game_state = "MENU"
menu_blink = True
menu_blink_time = pygame.time.get_ticks()

# Variables de clignotement pour l'écran PAUSE
pause_blink = True

pause_blink_time = pygame.time.get_ticks()

# Variables d'animation pour vie, score et eau
life_anim = {'active': False, 'index': None, 'start': 0, 'duration': 500}
score_blink = False
score_blink_time = pygame.time.get_ticks()
water_anim = {'active': False, 'start': 0, 'duration': 500}

# Variables pour le menu étendu
story_lines = [
    "AstroPaws: Gourmet Quest",
    "",
    "Quelque part dans le secteur L-88...",
    "Un signal d’urgence retentit depuis la station Alpha-Felis : la dernière réserve de Pâtée Galactique™ a disparu !",
    "Heureusement, AstroPaws — félin gourmet, cosmonaute téméraire et dernier espoir du Conseil des Chats — répond à l’appel.",
    "",
    "Sa mission ?",
    "Explorer les confins de l’espace, affronter une faune hostile et récupérer les 4 ingrédients sacrés de la recette ultime.",
    "",
    "Souris mutantes, rats radioactifs et chiens d’la casse n’ont qu’à bien se tenir...",
    "Car AstroPaws est en route, armé de son Jetpack et de ses jets d’eau ultra-puissants.",
    "",
    "Mais attention, chaque tir consomme de l’eau pure, précieuse et limitée.",
    "Et chaque erreur peut vous coûter des points… ou une vie.",
    "Ramassez des croquettes, évitez les pièges, et préparez-vous à affronter l’Impératrice Zibeline en personne.",
    "",
    "Gameplay",
    "   - Déplacez AstroPaws avec les flèches directionnelles.",
    "   - Tirez avec la barre Espace (consomme de l’eau).",
    "   - Ramassez des croquettes (points) et de l’eau (munitions).",
    "   - Esquivez les ennemis ou éliminez-les avec vos jets d’eau.",
    "   - Le jeu se termine si AstroPaws perd ses 9 vies.",
    "",
    "AstroPaws n’est pas un héros.",
    "C’est un chat.",
    "Mais parfois… c’est tout ce dont l’univers a besoin."
]
story_scroll_y = float(screen_height)
story_speed = 0.5  # pixels par frame

running = True
# --- Variables pour le chronomètre, bouclier, récompense ---
game_start_time = None
reward_shown = False
shield_charges = 0
shield_active = False
shield_start_time = None
shield_duration = 5000  # 5 secondes en ms
shield_last_granted_time = None  # timestamp de dernière attribution de charge
shield_cooldown = 30000         # 30 secondes de recharge
# Animation clignotante pour bouclier dans l'inventaire
shield_inv_anim = {'active': False, 'start': 0, 'duration': 1000}  # 1 seconde
hyper_charges = 0               # charges d'hyperespace
ingredients_collected = []      # liste des ingrédients collectés
ing_anim_active = False  # indique qu'un nouvel ingrédient doit être animé
ing_anim_start = 0       # timestamp du début de l'animation
ing_anim_duration = 1500  # durée de l'animation en ms
paused_time_accum = 0       # temps total passé en pause (ms)
pause_start_time = None     # timestamp du début de la pause
level_win_start_time = None  # timestamp du début de l'écran LEVEL_WIN
now = 0
while running:
    # Limiter le jeu à 60 images par seconde
    clock.tick(60)
    # Temps courant
    now = pygame.time.get_ticks()
    # Initialiser le chronomètre au début du jeu
    if game_state == "PLAYING" and game_start_time is None:
        game_start_time = now
    # Déclencher la récompense à 30 secondes
    if game_state == "PLAYING" and not reward_shown and game_start_time is not None and now - game_start_time >= 30000:
        game_state = "REWARD"
        continue
    # Recharge automatique du bouclier toutes les shield_cooldown ms
    if game_state == "PLAYING" and reward_shown and shield_last_granted_time is not None and now - shield_last_granted_time >= shield_cooldown:
        shield_charges += 1
        shield_last_granted_time = now
        # Animer l'icône de bouclier dans l'inventaire
        shield_inv_anim['active'] = True
        shield_inv_anim['start'] = now

    # === Écran INFO ===
    if game_state == "INFO":
        # Événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_state = "MENU"
        # Fond uni pour l'écran INFO
        screen.fill(BLACK)
        # Animation de Dr Chat (bob vertical + rotation)
        now = pygame.time.get_ticks()
        angle = 5 * math.sin(now / 500)           # amplitude 5° en 1s
        y_bob = 10 + 10 * math.sin(now / 400)     # amplitude 10px en 0.8s
        rotated_doc = pygame.transform.rotate(doctor_image, angle)
        doc_rect = rotated_doc.get_rect(topright=(screen_width - 10, y_bob))
        screen.blit(rotated_doc, doc_rect)
        # Liste des entrées
        entries = [
            (heart_sprite,  "Vie : perdre 1 vie si touché par un chien."),
            (water_sprite,  "Eau : -1L par tir, ramasse bidon pour +10L."),
            (shield_icon,   "Bouclier (H) : 5s de protection, cooldown 30s."),
            (hyper_icon,    "Hyperdrive (J) : dash en avant. WIP"),
            (ingredient_icon, "Ingrédient : collecte pour pâtée cosmique."),
            ((brown_croquette_sprite, gold_croquette_sprite), "Croquettes : +3pts (marron), +10pts (dorée)."),
            (mouse_sprite,  "Souris : 1 tir pour tuer, +10pts, collision -5pts."),
            (rat_sprite,    "Rat : 1 tir pour tuer, +20pts, collision -10pts."),
            (dog_sprite,    "Chien : 3 tirs pour tuer, +30pts, collision -1 vie."),
            (None,          f"Score requis : {levels.levels[0]['target_score']} -> N2, {levels.levels[1]['target_score']}-> N3, {levels.levels[2]['target_score']}-> Fin")
        ]
        # Affichage
        y = 60
        for icon, text in entries:
            if icon:
                # si tuple d'icônes (croquettes marron+dorée)
                if isinstance(icon, tuple):
                    first, second = icon
                    # dessiner marron puis dorée
                    screen.blit(first, (50, y))
                    screen.blit(second, (50 + first.get_width() + 10, y))
                    x_text = 50 + first.get_width() + 10 + second.get_width() + 20
                else:
                    # cœur plus grand et ennemis à taille du chien
                    if icon == heart_sprite:
                        display_icon = pygame.transform.scale(icon, (40, 40))
                    elif icon in (mouse_sprite, rat_sprite):
                        display_icon = pygame.transform.scale(icon, dog_sprite.get_size())
                    else:
                        display_icon = icon
                    screen.blit(display_icon, (50, y))
                    x_text = 50 + display_icon.get_width() + 20
            else:
                x_text = 50
            # texte
            txt_surf = subtitle_font.render(text, True, WHITE)
            screen.blit(txt_surf, (x_text, y + 8))
            y += 50
        # Bas de page
        hint = subtitle_font.render("Press SPACE to return", True, GREEN)
        # Remonter le message pour éviter chevauchement
        hint_rect = hint.get_rect(midbottom=(screen_width//2, screen_height - 10))
        screen.blit(hint, hint_rect)
        pygame.display.flip()
        continue

    # === Écran STORY ===
    if game_state == "STORY":
        # Gestion des événements pour sortir de la Story
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_ESCAPE, pygame.K_RETURN):
                    story_scroll_y = float(screen_height)
                    game_state = "MENU"
        # Animer fond (étoiles+planètes)
        for star in star_list:
            star['x'] += star['speed']
            star['y'] += star['speed'] * 0.5
            if star['x'] > screen_width:
                star['x'] = 0
                star['y'] = random.randint(0, screen_height)
        for planet in planet_list:
            planet['x'] += planet['speed']
            planet['y'] += planet['speed'] * 0.2
            if planet['x'] > screen_width:
                planet['x'] = 0
                planet['y'] = random.randint(0, screen_height)
        screen.fill(BLACK)
        for star in star_list:
            pygame.draw.circle(screen, WHITE, (int(star['x']), int(star['y'])), 1)
        for planet in planet_list:
            pygame.draw.circle(screen, planet['color'], (int(planet['x']), int(planet['y'])), planet['size'])
        # Préparer le texte wrapé
        display_lines = []
        for idx, line in enumerate(story_lines):
            color = GOLD if idx == 0 else WHITE
            if line == "":
                display_lines.append(("", color))
            else:
                for sub in textwrap.wrap(line, width=40):
                    display_lines.append((sub, color))
        # Afficher lignes défilantes
        line_height = 36
        for i, (text, color) in enumerate(display_lines):
            surf = score_font.render(text, True, color)
            rect = surf.get_rect(center=(screen_width//2, int(story_scroll_y + i*line_height)))
            screen.blit(surf, rect)
        story_scroll_y -= story_speed
        # Retour menu quand fini
        if story_scroll_y + len(display_lines)*line_height < 0:
            story_scroll_y = float(screen_height)
            game_state = "MENU"
        pygame.display.flip()
        continue

    # === Écran MENU ===
    if game_state == "MENU":
        # Gestion des événements pour quitter, démarrer ou story/info
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Aller à l'écran d'intro du niveau 1
                    level_idx = 0
                    game_state = "LEVEL_INTRO"
                elif event.key == pygame.K_s:
                    story_scroll_y = float(screen_height)
                    game_state = "STORY"
                elif event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_i:
                    game_state = "INFO"
        # Animation de fond (étoiles et planètes)
        for star in star_list:
            star['x'] += star['speed']
            star['y'] += star['speed'] * 0.5
            if star['x'] > screen_width:
                star['x'] = 0
                star['y'] = random.randint(0, screen_height)
        for planet in planet_list:
            planet['x'] += planet['speed']
            planet['y'] += planet['speed'] * 0.2
            if planet['x'] > screen_width:
                planet['x'] = 0
                planet['y'] = random.randint(0, screen_height)
        # Affichage du fond étoilé
        screen.fill(BLACK)
        for star in star_list:
            pygame.draw.circle(screen, WHITE, (int(star['x']), int(star['y'])), 1)
        for planet in planet_list:
            pygame.draw.circle(screen, planet['color'], (int(planet['x']), int(planet['y'])), planet['size'])
        # Afficher l'image d'accueil
        image_rect = welcome_image.get_rect(midtop=(screen_width//2, 50))
        screen.blit(welcome_image, image_rect)
        # Clignotement du texte
        now = pygame.time.get_ticks()
        if now - menu_blink_time > 500:
            menu_blink = not menu_blink
            menu_blink_time = now
        prompt_y_base = 50 + welcome_image.get_height() + 30
        if menu_blink:
            prompt = score_font.render("PRESS SPACE TO START", True, WHITE)
            prompt_rect = prompt.get_rect(center=(screen_width//2, prompt_y_base))
            screen.blit(prompt, prompt_rect)
        prompt2 = score_font.render("PRESS S FOR STORY", True, WHITE)
        prompt2_rect = prompt2.get_rect(center=(screen_width//2, prompt_y_base + 40))
        screen.blit(prompt2, prompt2_rect)
        prompt3 = score_font.render("PRESS Q TO QUIT", True, WHITE)
        prompt3_rect = prompt3.get_rect(center=(screen_width//2, prompt_y_base + 80))
        screen.blit(prompt3, prompt3_rect)
        prompt4 = score_font.render("PRESS I FOR INFO", True, WHITE)
        prompt4_rect = prompt4.get_rect(center=(screen_width//2, prompt_y_base + 120))
        screen.blit(prompt4, prompt4_rect)
        # Affichage de la version (date.build) en bas à droite du menu
        version_surf = subtitle_font.render("Version 2025-05-25.1", True, WHITE)
        version_rect = version_surf.get_rect(bottomright=(screen_width - 10, screen_height - 10))
        screen.blit(version_surf, version_rect)
        pygame.display.flip()
        continue
    # === Écran LEVEL_INTRO ===
    if game_state == "LEVEL_INTRO":
        # Gérer la sortie ou continuer
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    # Warp spatial avant de démarrer le niveau
                    warp_effect()
                    game_state = "PLAYING"
                elif event.key == pygame.K_q:
                    running = False
        # Fond étoilé
        screen.fill(BLACK)
        for star in star_list:
            pygame.draw.circle(screen, WHITE, (int(star['x']), int(star['y'])), 1)
        for planet in planet_list:
            pygame.draw.circle(screen, planet['color'], (int(planet['x']), int(planet['y'])), planet['size'])
        # Numérotation du niveau
        level_str = f"Niveau {level_idx+1}"
        level_surf = score_font.render(level_str, True, WHITE)
        level_rect = level_surf.get_rect(center=(screen_width//2, 30))
        screen.blit(level_surf, level_rect)
        # Offset vertical pour placer le duel
        y_offset = 80

        # VS layout sous le titre
        # Animation de hochement de tête d'AstroPaws
        head_angle = 10 * math.sin(now / 300)  # amplitude 10°, période ~600ms
        rotated_head = pygame.transform.rotate(astro_head, head_angle)
        ah_rect = rotated_head.get_rect(center=(screen_width//4, y_offset + 80))
        screen.blit(rotated_head, ah_rect)
        vs_surf = score_font.render("VS.", True, YELLOW)
        vs_rect = vs_surf.get_rect(center=(screen_width//2, y_offset + 80))
        screen.blit(vs_surf, vs_rect)
        # Ennemi à droite avec animation de pulsation pour faire peur
        enemy_sprite = mouse_sprite if level_idx == 0 else rat_sprite if level_idx == 1 else dog_sprite
        # Calculer un facteur de pulsation sinusoïdal
        pulse = 1 + 0.1 * math.sin(now / 200)
        base_w, base_h = astro_head.get_size()
        anim_size = (int(base_w * pulse), int(base_h * pulse))
        animated_enemy = pygame.transform.scale(enemy_sprite, anim_size)
        eh_rect = animated_enemy.get_rect(center=(3 * screen_width // 4, y_offset + 80))
        screen.blit(animated_enemy, eh_rect)

        # Sous-titre descriptif (wrap si nécessaire)
        level_name = levels.levels[level_idx]['name']
        desc = f"AstroPaws contre {level_name}"
        wrapped_desc = textwrap.wrap(desc, width=60)
        for j, line in enumerate(wrapped_desc):
            surf = subtitle_font.render(line, True, WHITE)
            rect = surf.get_rect(center=(screen_width//2, y_offset + 160 + j*40))
            screen.blit(surf, rect)

        # Texte rigolo (wrap automatique)
        jokes = [
            "Elles viennes de la Lune Fromagère... et elles sont affamées !",
            "Une fuite nucléaire a réveillé leur appétit galactique.",
            "La langue pendante et les crocs acérés prêts à bouffer !",
        ]
        wrapped_joke = textwrap.wrap(jokes[level_idx], width=50)
        for k, line in enumerate(wrapped_joke):
            surf = subtitle_font.render(line, True, WHITE)
            rect = surf.get_rect(center=(screen_width//2, y_offset + 240 + k*40))
            screen.blit(surf, rect)

        # Poursuivre
        cont_surf = score_font.render("Press C to continue", True, GREEN)
        cont_rect = cont_surf.get_rect(center=(screen_width//2, screen_height - 50))
        screen.blit(cont_surf, cont_rect)
        pygame.display.flip()
        continue

    # === Écran REWARD (Bouclier acquis) ===
    if game_state == "REWARD":
        # Fond étoilé
        screen.fill(BLACK)
        for star in star_list:
            pygame.draw.circle(screen, WHITE, (int(star['x']), int(star['y'])), 1)
        for planet in planet_list:
            pygame.draw.circle(screen, planet['color'], (int(planet['x']), int(planet['y'])), planet['size'])
        # Texte de récompense
        text = score_font.render("Bouclier acquis !", True, CYAN)
        rect = text.get_rect(center=(screen_width//2, screen_height//2 - 50))
        screen.blit(text, rect)
        # Cercle bouclier
        pygame.draw.circle(screen, CYAN, (screen_width//2, screen_height//2 + 10), 50, 4)
        # Petite tête d'AstroPaws
        small = pygame.transform.scale(astro_sprite_right, (40, 40))
        srect = small.get_rect(center=(screen_width//2, screen_height//2 + 10))
        screen.blit(small, srect)
        # Informations sur le bouclier
        info1 = score_font.render("Appuyez sur H pour activer le bouclier", True, WHITE)
        info1_rect = info1.get_rect(center=(screen_width//2, screen_height//2 + 80))
        screen.blit(info1, info1_rect)
        info2 = score_font.render(f"Durée: {shield_duration//1000}s   Utilisations: 1", True, WHITE)
        info2_rect = info2.get_rect(center=(screen_width//2, screen_height//2 + 120))
        screen.blit(info2, info2_rect)
        pygame.display.flip()
        pygame.time.delay(2000)
        # Octroi de la charge de bouclier
        shield_charges = 1
        shield_last_granted_time = now
        reward_shown = True
        shield_inv_anim['active'] = True
        shield_inv_anim['start'] = now
        game_state = "PLAYING"
        continue
    # === Écran PAUSE ===
    if game_state == "PAUSE":
        # Gestion des événements pour reprendre ou quitter
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused_time_accum += now - pause_start_time
                    pause_start_time = None
                    game_state = "PLAYING"
                elif event.key == pygame.K_q:
                    running = False
        # Affichage du menu pause
        screen.fill(BLACK)
        # Clignotement du titre PAUSE
        now = pygame.time.get_ticks()
        if now - pause_blink_time > 500:
            pause_blink = not pause_blink
            pause_blink_time = now
        # Stats en pause
        score_surface = score_font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surface, (10, 10))
        # Afficher la quantité d'eau avec icône
        screen.blit(water_sprite, (10, 50))
        water_count = score_font.render(f"x{water_ammo}", True, WHITE)
        screen.blit(water_count, (10 + water_sprite.get_width() + 10, 50 + (water_sprite.get_height() - water_count.get_height())//2))
        # Afficher les vies sous forme de cœurs
        for i in range(lives):
            hx = 10 + i * (heart_sprite.get_width() + 5)
            hy = 50 + water_sprite.get_height() + 10
            screen.blit(heart_sprite, (hx, hy))
        # Inventaire en pause : icônes + compteurs
        inv_x = 10
        inv_y = 130
        # Bouclier
        screen.blit(shield_icon, (inv_x, inv_y))
        shield_count = score_font.render(f"x{shield_charges}", True, WHITE)
        screen.blit(shield_count, (inv_x + shield_icon.get_width() + 10, inv_y + 12))
        # Hyperdrive
        screen.blit(hyper_icon, (inv_x + 120, inv_y))
        hyper_count = score_font.render(f"x{hyper_charges}", True, WHITE)
        screen.blit(hyper_count, (inv_x + 120 + hyper_icon.get_width() + 10, inv_y + 12))
        # Ingrédients collectés : icône générique + sprites spécifiques clignotants
        base_x = inv_x + 240
        screen.blit(ingredient_icon, (base_x, inv_y))
        offset_x = base_x + ingredient_icon.get_width() + 10
        # Clignotement à 500ms
        blink_on = ((now // 500) % 2) == 0
        for idx, ing_key in enumerate(ingredients_collected):
            if not blink_on:
                break  # tout clignote ensemble, on peut stopper si off
            ing_sprite = ingredient_sprites.get(ing_key, ingredient_icon)
            x = offset_x + idx * (ing_sprite.get_width() + 10)
            screen.blit(ing_sprite, (x, inv_y))
        # Titre PAUSE clignotant
        if pause_blink:
            pause_surf = score_font.render("PAUSE", True, WHITE)
            pause_rect = pause_surf.get_rect(center=(screen_width//2, screen_height//3))
            screen.blit(pause_surf, pause_rect)
        # Options colorées
        resume_surf = score_font.render("Press P to resume", True, GREEN)
        resume_rect = resume_surf.get_rect(center=(screen_width//2, screen_height//2))
        screen.blit(resume_surf, resume_rect)
        quit_surf = score_font.render("Press Q to quit", True, RED)
        # Placer le texte "Quit" juste sous "Resume"
        quit_rect = quit_surf.get_rect(center=(screen_width//2, screen_height//2 + 60))
        screen.blit(quit_surf, quit_rect)
        # Afficher le chat endormi en bas de l'écran de pause
        chat_rect = chat_sleep_image.get_rect(midbottom=(screen_width//2, screen_height - 10))
        screen.blit(chat_sleep_image, chat_rect)
        pygame.display.flip()
        continue

    # === Écran GAME_OVER ===
    if game_state == "GAME_OVER":
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Réinitialiser le jeu
                    score = 0
                    lives = 9
                    water_ammo = 50
                    astro_x = screen_width // 2
                    astro_y = screen_height // 2
                    enemy_list.clear()
                    explosion_list.clear()
                    bullet_list.clear()
                    water_item_list.clear()
                    croquette_list.clear()
                    # Recréer quelques croquettes initiales
                    for i in range(5):
                        x = random.randint(0, screen_width - croquette_size)
                        y = random.randint(0, screen_height - croquette_size)
                        spawn_time = pygame.time.get_ticks()
                        croquette_type = "rare" if random.random() < 0.1 else "normal"
                        croquette_list.append({'x': x, 'y': y, 'spawn_time': spawn_time, 'type': croquette_type})
                    game_state = "MENU"
                elif event.key == pygame.K_q:
                    running = False
        # Affichage du fond spatial
        screen.fill(BLACK)
        for star in star_list:
            pygame.draw.circle(screen, WHITE, (int(star['x']), int(star['y'])), 1)
        for planet in planet_list:
            pygame.draw.circle(screen, planet['color'], (int(planet['x']), int(planet['y'])), planet['size'])
        # Afficher l'image Game Over
        go_rect = gameover_image.get_rect(center=(screen_width//2, screen_height//2 - 50))
        screen.blit(gameover_image, go_rect)
        # Afficher les stats
        screen.blit(score_font.render(f"Score: {score}", True, WHITE), (10, 10))
        screen.blit(score_font.render(f"Water: {water_ammo}", True, WHITE), (10, 50))
        screen.blit(score_font.render(f"Lives: {lives}", True, WHITE), (10, 90))
        # Afficher les options
        r_surf = score_font.render("Press R to return to menu", True, GREEN)
        q_surf = score_font.render("Press Q to quit", True, RED)
        screen.blit(r_surf, r_surf.get_rect(center=(screen_width//2, screen_height//2 + 50)))
        screen.blit(q_surf, q_surf.get_rect(center=(screen_width//2, screen_height//2 + 100)))
        pygame.display.flip()
        continue

    # === Écran JEU (PLAYING) ===
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pause_start_time = now
                game_state = "PAUSE"
                break
            if event.key == pygame.K_h and shield_charges > 0 and not shield_active:
                shield_active = True
                shield_start_time = now
                shield_charges -= 1
                create_explosion(astro_x + 40, astro_y + 40, color=BLUE, num_particles=20)
            if event.key == pygame.K_SPACE:
                current_time = pygame.time.get_ticks()
                if current_time >= next_shot_allowed_time and water_ammo > 0:
                    # Déterminer la direction du tir à partir des touches fléchées
                    keys = pygame.key.get_pressed()
                    dx = 0
                    dy = 0
                    if keys[pygame.K_LEFT]:
                        dx -= 1
                    if keys[pygame.K_RIGHT]:
                        dx += 1
                    if keys[pygame.K_UP]:
                        dy -= 1
                    if keys[pygame.K_DOWN]:
                        dy += 1
                    if dx == 0 and dy == 0:
                        # Tirer dans la dernière direction de déplacement
                        if astro_facing == "left":
                            dx = -bullet_speed
                            dy = 0
                        elif astro_facing == "right":
                            dx = bullet_speed
                            dy = 0
                        elif astro_facing == "up":
                            dx = 0
                            dy = -bullet_speed
                        else:  # "down"
                            dx = 0
                            dy = bullet_speed
                    mag = math.sqrt(dx*dx + dy*dy)
                    dx = dx / mag * bullet_speed
                    dy = dy / mag * bullet_speed
                    # Positionner le tir au centre d'AstroPaws
                    bullet_rect = pygame.Rect(astro_x + 25 - bullet_width//2, astro_y + 25 - bullet_height//2, bullet_width, bullet_height)
                    bullet = {'rect': bullet_rect, 'dx': dx, 'dy': dy}
                    bullet_list.append(bullet)
                    next_shot_allowed_time = current_time + cooldown_time
                    water_ammo -= 1

    # Gestion continue des touches (pour détecter plusieurs touches en même temps)
    keys = pygame.key.get_pressed()
    # Gestion du déplacement avec diagonales
    dx = dy = 0
    if keys[pygame.K_LEFT]:
        dx -= speed
        astro_facing = "left"
    if keys[pygame.K_RIGHT]:
        dx += speed
        astro_facing = "right"
    if keys[pygame.K_UP]:
        dy -= speed
        astro_facing = "up"
    if keys[pygame.K_DOWN]:
        dy += speed
        astro_facing = "down"
    # Normaliser la vitesse en diagonale
    if dx != 0 and dy != 0:
        dx *= 0.7071  # 1/sqrt(2)
        dy *= 0.7071
    astro_x += dx
    astro_y += dy

    # Wrap-around : traverser d'un bord à l'autre
    sprite_w = astro_sprite_right.get_width()
    sprite_h = astro_sprite_right.get_height()
    if astro_x > screen_width:
        astro_x = -sprite_w
    elif astro_x < -sprite_w:
        astro_x = screen_width
    if astro_y > screen_height:
        astro_y = -sprite_h
    elif astro_y < -sprite_h:
        astro_y = screen_height

    # Mise à jour de la position des tirs
    for bullet in bullet_list:
        bullet['rect'].x += bullet['dx']
        bullet['rect'].y += bullet['dy']
    bullet_list = [bullet for bullet in bullet_list if bullet['rect'].right > 0 and bullet['rect'].left < screen_width and bullet['rect'].bottom > 0 and bullet['rect'].top < screen_height]

    # Mise à jour des positions des étoiles pour effet parallaxe
    for star in star_list:
        star['x'] += star['speed']
        star['y'] += star['speed'] * 0.5
        if star['x'] > screen_width:
            star['x'] = 0
            star['y'] = random.randint(0, screen_height)

    # Mise à jour des positions des planètes
    for planet in planet_list:
        planet['x'] += planet['speed']
        planet['y'] += planet['speed'] * 0.2
        if planet['x'] > screen_width:
            planet['x'] = 0
            planet['y'] = random.randint(0, screen_height)

    # Spawn d'ennemis selon configuration du niveau
    level_conf = levels.levels[level_idx]
    spawn_chance = 0.02
    if random.random() < spawn_chance:
        # Choisir le type en fonction des poids du niveau
        spawn_weights = level_conf['spawn_weights']
        enemy_type = random.choices(
            population=list(spawn_weights.keys()),
            weights=list(spawn_weights.values())
        )[0]
        # Propriétés selon le type
        if enemy_type == 'dog':
            enemy_width, enemy_height, enemy_speed, enemy_health = 50, 50, 2, 3
        elif enemy_type == 'rat':
            enemy_width, enemy_height, enemy_speed, enemy_health = 30, 30, 3, 1  # rat tué en 1 jet
        else:  # 'mouse'
            enemy_width, enemy_height, enemy_speed, enemy_health = 20, 20, 4, 1
        # Déterminer le côté d'apparition
        side = random.choice(['left', 'right', 'top', 'bottom'])
        if side == 'left':
            x, y, dx, dy = -enemy_width, random.randint(0, screen_height - enemy_height), enemy_speed, 0
        elif side == 'right':
            x, y, dx, dy = screen_width, random.randint(0, screen_height - enemy_height), -enemy_speed, 0
        elif side == 'top':
            x, y, dx, dy = random.randint(0, screen_width - enemy_width), -enemy_height, 0, enemy_speed
        else:  # 'bottom'
            x, y, dx, dy = random.randint(0, screen_width - enemy_width), screen_height, 0, -enemy_speed
        # Ajouter l'ennemi
        enemy_list.append({
            'x': x, 'y': y, 'width': enemy_width, 'height': enemy_height,
            'type': enemy_type, 'dx': dx, 'dy': dy,
            'speed': enemy_speed, 'health': enemy_health,
            'bob_phase': random.uniform(0, 2 * math.pi)
        })
    # Mise à jour des ennemis
    new_enemy_list = []
    for enemy in enemy_list:
        enemy['x'] += enemy['dx']
        enemy['y'] += enemy['dy']
        if enemy['x'] + enemy['width'] > 0 and enemy['x'] < screen_width and enemy['y'] + enemy['height'] > 0 and enemy['y'] < screen_height:
            new_enemy_list.append(enemy)
    enemy_list = new_enemy_list

    # Collision entre les tirs (jet d'eau) et les ennemis
    new_bullet_list = []
    for bullet in bullet_list:
        bullet_rect = bullet['rect']  # Le tir est maintenant dans bullet['rect']
        hit_enemy = False
        for enemy in enemy_list[:]:
            enemy_rect = pygame.Rect(enemy['x'], enemy['y'], enemy['width'], enemy['height'])
            if bullet_rect.colliderect(enemy_rect):
                # Décrémenter la santé de l'ennemi à chaque tir
                enemy['health'] -= 1
                # Si la santé tombe à zéro, l'ennemi est détruit
                if enemy['health'] <= 0:
                    if enemy['type'] == "rat":
                        enemy_color = (200, 0, 0)  # rouge foncé pour les rats
                        score += 20
                    elif enemy['type'] == "mouse":
                        enemy_color = (255, 100, 100)  # rouge clair pour les souris
                        score += 10
                    elif enemy['type'] == "dog":
                        enemy_color = (255, 0, 0)  # rouge pour les chiens
                        score += 30
                    create_explosion(enemy['x'] + enemy['width'] // 2, enemy['y'] + enemy['height'] // 2, color=enemy_color)
                    enemy_list.remove(enemy)
                hit_enemy = True
                break
        if not hit_enemy:
            new_bullet_list.append(bullet)
    bullet_list = new_bullet_list

    # Collision entre AstroPaws et les ennemis
    for enemy in enemy_list[:]:
        enemy_rect = pygame.Rect(enemy['x'], enemy['y'], enemy['width'], enemy['height'])
        player_rect = pygame.Rect(astro_x, astro_y, 50, 50)
        if player_rect.colliderect(enemy_rect):
            # Bouclier actif : élimination sans malus
            if shield_active:
                create_explosion(enemy['x'] + enemy['width']//2, enemy['y'] + enemy['height']//2, color=CYAN, num_particles=20)
                enemy_list.remove(enemy)
                continue
            if enemy['type'] == "dog":
                lives -= 1
                # Déclencher explosion du cœur retiré
                life_anim['active'] = True
                life_anim['index'] = lives  # index du cœur supprimé
                life_anim['start'] = pygame.time.get_ticks()
                # Explosion visuelle sur le cœur
                heart_x = screen_width - (heart_sprite.get_width() + 10) * (life_anim['index'] + 1) + heart_sprite.get_width()//2
                heart_y = 10 + heart_sprite.get_height()//2
                create_explosion(heart_x, heart_y, color=RED, num_particles=30)
                create_explosion(astro_x + 25, astro_y + 25, color=(255, 0, 0), num_particles=50)
                lost_life_surface = score_font.render("Vous avez perdu une vie!", True, WHITE)
                screen.blit(lost_life_surface, (screen_width//2 - 100, screen_height//2))
                pygame.display.flip()
                pygame.time.delay(1000)
            elif enemy['type'] == "rat":
                score -= 10
                create_explosion(astro_x + 25, astro_y + 25)
            else:  # mouse
                score -= 5
                create_explosion(astro_x + 25, astro_y + 25)
            enemy_list.remove(enemy)

    # Vérifier Game Over: si les vies tombent à 0
    if lives <= 0:
        # Passer en écran de Game Over
        game_state = "GAME_OVER"
        continue

    # Mise à jour de la liste des croquettes
    current_time = pygame.time.get_ticks()
    croquette_list = [croquette for croquette in croquette_list if current_time - croquette['spawn_time'] < croquette_lifetime]

    # Apparition de nouvelles croquettes
    if random.random() < 0.01:  # environ 1% de chance par frame
        x = random.randint(0, screen_width - croquette_size)
        y = random.randint(0, screen_height - croquette_size)
        spawn_time = pygame.time.get_ticks()
        if random.random() < 0.1:
            croquette_type = "rare"
        else:
            croquette_type = "normal"
        croquette_list.append({'x': x, 'y': y, 'spawn_time': spawn_time, 'type': croquette_type})

    # Collision entre AstroPaws et les croquettes
    player_rect = pygame.Rect(astro_x, astro_y, 50, 50)
    new_croquette_list = []
    for croquette in croquette_list:
        croquette_rect = pygame.Rect(croquette['x'], croquette['y'], croquette_size, croquette_size)
        if player_rect.colliderect(croquette_rect):
            if croquette.get('type') == "rare":
                score += 10  # croquette rare désormais 10 points
            else:
                score += 3   # croquette normale désormais 3 points
        else:
            new_croquette_list.append(croquette)
    croquette_list = new_croquette_list

    # Vérifier si on atteint le score cible du niveau
    target = levels.levels[level_idx]['target_score']
    if score >= target:
        # Animation de disparition du sprite mort sur 2 secondes
        # Préparez le message statique
        msg = score_font.render(f"{levels.levels[level_idx]['name']} terminé !", True, WHITE)
        msg_rect = msg.get_rect(center=(screen_width//2, screen_height//2 + 50))
        # Choisir le sprite mort
        if level_idx == 0:
            dead = mouse_dead_sprite
        elif level_idx == 1:
            dead = rat_dead_sprite
        else:
            dead = dog_dead_sprite
        # Animation
        anim_start = pygame.time.get_ticks()
        anim_duration = 2000  # ms
        while True:
            t = pygame.time.get_ticks() - anim_start
            if t >= anim_duration:
                break
            progress = t / anim_duration
            # Calculer la taille et l'alpha
            scale = 1.0 - 0.5 * progress
            w = max(1, int(dead.get_width() * scale))
            h = max(1, int(dead.get_height() * scale))
            anim_img = pygame.transform.scale(dead, (w, h))
            anim_img.set_alpha(int(255 * (1 - progress)))
            # Dessiner fond et sprite animé
            screen.fill(BLACK)
            # étoiles de fond
            for star in star_list:
                pygame.draw.circle(screen, WHITE, (int(star['x']), int(star['y'])), 1)
            for planet in planet_list:
                pygame.draw.circle(screen, planet['color'], (int(planet['x']), int(planet['y'])), planet['size'])
            # sprite mort animé
            rect = anim_img.get_rect(center=(screen_width//2, screen_height//2 - 50))
            screen.blit(anim_img, rect)
            # message
            screen.blit(msg, msg_rect)
            pygame.display.flip()
            clock.tick(60)
        # Animer l'ajout de l'ingrédient
        ingredients_collected.append(levels.levels[level_idx]['end_item'])
        ing_anim_active = True
        ing_anim_start = now
        # Mettre à jour l'inventaire et passer directement à l'intro du niveau suivant
        if level_idx < len(levels.levels) - 1:
            level_idx += 1
        enemy_list.clear()
        croquette_list.clear()
        water_item_list.clear()
        game_start_time = None
        game_state = "LEVEL_INTRO"
        continue
    # === Écran LEVEL_WIN ===
    if game_state == "LEVEL_WIN":
        # Affichage du même écran de victoire
        screen.fill(BLACK)
        for star in star_list:
            pygame.draw.circle(screen, WHITE, (int(star['x']), int(star['y'])), 1)
        for planet in planet_list:
            pygame.draw.circle(screen, planet['color'], (int(planet['x']), int(planet['y'])), planet['size'])
        win_msg = score_font.render("Vous avez passé le niveau !", True, WHITE)
        win_rect = win_msg.get_rect(center=(screen_width//2, 60))
        screen.blit(win_msg, win_rect)
        yw_rect = youwin_image.get_rect(center=(screen_width//2, screen_height//2))
        screen.blit(youwin_image, yw_rect)
        next_name = levels.levels[level_idx]['name'] if level_idx < len(levels.levels) else "Fin du jeu"
        sub_surf = score_font.render(f"Prochain : {next_name}", True, WHITE)
        sub_rect = sub_surf.get_rect(center=(screen_width//2, screen_height//2 + 140))
        screen.blit(sub_surf, sub_rect)
        cont_surf = score_font.render("(Patientez...)", True, GREEN)
        cont_rect = cont_surf.get_rect(center=(screen_width//2, screen_height - 50))
        screen.blit(cont_surf, cont_rect)
        pygame.display.flip()
        # Transition automatique après 5 secondes
        if level_win_start_time is not None and now - level_win_start_time >= 5000:
            game_state = "LEVEL_INTRO"
        else:
            # Permettre de quitter la fenêtre
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        continue

    # Mise à jour des réserves d'eau (water items)
    current_time = pygame.time.get_ticks()
    water_item_list = [item for item in water_item_list if current_time - item['spawn_time'] < 7000]  # durée de vie de 7 sec
    
    # Collision entre AstroPaws et les réserves d'eau
    for item in water_item_list[:]:
        # Utiliser la taille réelle du sprite pour la collision
        width = water_sprite.get_width()
        height = water_sprite.get_height()
        water_rect = pygame.Rect(item['x'], item['y'], width, height)
        if player_rect.colliderect(water_rect):
            water_ammo += 10
            # Déclencher clignotement du compteur d'eau
            water_anim['active'] = True
            water_anim['start'] = pygame.time.get_ticks()
            water_item_list.remove(item)
    
    # Apparition de nouvelles réserves d'eau
    if random.random() < 0.005:  # environ 0.5% de chance par frame
        x = random.randint(0, screen_width - 10)
        y = random.randint(0, screen_height - 10)
        spawn_time = pygame.time.get_ticks()
        water_item_list.append({'x': x, 'y': y, 'spawn_time': spawn_time})

    # Mise à jour des particules d'explosion
    new_explosion_list = []
    for particle in explosion_list:
        particle['x'] += particle['dx']
        particle['y'] += particle['dy']
        particle['lifetime'] -= 1
        if particle['lifetime'] > 0:
            new_explosion_list.append(particle)
    explosion_list = new_explosion_list

    # Mettre à jour animations de score et d'eau
    now = pygame.time.get_ticks()
    # Score blink si négatif
    if score < 0:
        if now - score_blink_time > 500:
            score_blink = not score_blink
            score_blink_time = now
    else:
        score_blink = False
    # Arrêter animation eau
    if water_anim['active'] and now - water_anim['start'] > water_anim['duration']:
        water_anim['active'] = False
    # Arrêter animation inventaire bouclier
    if shield_inv_anim['active'] and now - shield_inv_anim['start'] > shield_inv_anim['duration']:
        shield_inv_anim['active'] = False

    # Affichage du fond spatial procédural avec teinte de niveau
    bg = levels.levels[level_idx]['bg_tint']
    screen.fill(bg)
    # Chronomètre mm:ss en haut-centre
    if game_start_time is not None:
        elapsed = (now - game_start_time - paused_time_accum) // 1000
        mins, secs = divmod(elapsed, 60)
        timer_surf = score_font.render(f"{mins:02d}:{secs:02d}", True, WHITE)
        timer_rect = timer_surf.get_rect(midtop=(screen_width//2, 10))
        screen.blit(timer_surf, timer_rect)
    # Dessiner les étoiles
    for star in star_list:
        pygame.draw.circle(screen, WHITE, (int(star['x']), int(star['y'])), 1)
    # Dessiner les planètes
    for planet in planet_list:
        pygame.draw.circle(screen, planet['color'], (int(planet['x']), int(planet['y'])), planet['size'])

    # Mettre à jour et dessiner les OVNIs décoratifs
    for ufo in ufo_list:
        ufo.update()
    for ufo in ufo_list:
        ufo.draw()

    # Dessiner les croquettes avec sprites
    for croquette in croquette_list:
        if croquette.get('type') == "rare":
            sprite = gold_croquette_sprite
        else:
            sprite = brown_croquette_sprite
        screen.blit(sprite, (croquette['x'], croquette['y']))
    # Dessiner les réserves d'eau avec sprite
    for item in water_item_list:
        screen.blit(water_sprite, (item['x'], item['y']))
    # Dessiner les ennemis avec des sprites et animation de flottement (bob)
    current_time = pygame.time.get_ticks()
    for enemy in enemy_list:
        # Choisir le sprite selon le type
        if enemy['type'] == "mouse":
            sprite = mouse_sprite
        elif enemy['type'] == "rat":
            sprite = rat_sprite
        else:  # dog
            sprite = dog_sprite
        # Calculer un décalage vertical (bob) plus marqué et plus rapide
        bob_offset = math.sin(current_time / 300 + enemy.get('bob_phase', 0)) * 15
        # Dessiner le sprite avec le bob vertical
        screen.blit(sprite, (enemy['x'], enemy['y'] + bob_offset))
    # Dessiner les particules d'explosion
    for particle in explosion_list:
        pygame.draw.circle(screen, particle['color'], (int(particle['x']), int(particle['y'])), 2)
    # Afficher les tirs (jet d'eau bleu)
    for bullet in bullet_list:
        pygame.draw.rect(screen, BLUE, bullet['rect'])
    # Afficher AstroPaws selon la direction
    if astro_facing == "left":
        screen.blit(astro_sprite_left, (astro_x, astro_y))
    elif astro_facing == "right":
        screen.blit(astro_sprite_right, (astro_x, astro_y))
    elif astro_facing == "up":
        screen.blit(astro_sprite_up, (astro_x, astro_y))
    else:  # "down"
        screen.blit(astro_sprite_down, (astro_x, astro_y))
    # Dessiner un cercle de bouclier autour d'AstroPaws si actif
    if shield_active:
        # Déterminer le centre du sprite
        sprite_w = astro_sprite_right.get_width()
        sprite_h = astro_sprite_right.get_height()
        center_x = astro_x + sprite_w // 2
        center_y = astro_y + sprite_h // 2
        # Rayon légèrement supérieur à la moitié du sprite
        radius = max(sprite_w, sprite_h) // 2 + 5
        # Tracer un cercle en CYAN d'épaisseur 3 px
        pygame.draw.circle(screen, CYAN, (center_x, center_y), radius, 3)
    
    # Afficher Score (clignote en rouge si score négatif)
    score_color = RED if (score < 0 and score_blink) else WHITE
    score_surface = score_font.render(f"Score: {score}", True, score_color)
    screen.blit(score_surface, (10, 10))
    # Afficher eau (clignote en bleu lors de collecte)
    water_color = BLUE if water_anim['active'] else WHITE
    water_surface = score_font.render(f"Water: {water_ammo}", True, water_color)
    screen.blit(water_surface, (10, 50))
    # Afficher les vies sous forme de cœurs en haut à droite
    for i in range(lives):
        x = screen_width - (heart_sprite.get_width() + 10) * (i + 1)
        screen.blit(heart_sprite, (x, 10))
    # Barre de bouclier si actif
    if shield_active:
        remaining = shield_duration - (now - shield_start_time)
        ratio = max(0, remaining) / shield_duration
        bw, bh = 200, 10
        bx, by = screen_width//2 - bw//2, 70
        pygame.draw.rect(screen, WHITE, (bx, by, bw, bh), 2)
        pygame.draw.rect(screen, BLUE, (bx, by, int(bw * ratio), bh))
        if remaining <= 0:
            shield_active = False

    # Affichage de l'inventaire en bas à gauche (icônes + compteurs)
    x0 = 10
    # Positionner l'inventaire 10px au-dessus du bord inférieur, en fonction de la hauteur de l'icône
    y0 = screen_height - shield_icon.get_height() - 10

    # Bouclier
    screen.blit(shield_icon, (x0, y0))
    # Clignotement du compteur de bouclier
    shield_color = CYAN if shield_inv_anim['active'] and ((now - shield_inv_anim['start']) // 250) % 2 == 0 else WHITE
    shield_count = score_font.render(f"x{shield_charges}", True, shield_color)
    # Position dynamique à droite de l'icône
    screen.blit(shield_count, (x0 + shield_icon.get_width() + 10, y0 + 4))

    # Hyperdrive
    screen.blit(hyper_icon, (x0 + 100, y0))
    hyper_count = score_font.render(f"x{hyper_charges}", True, WHITE)
    # Position dynamique à droite de l'icône
    screen.blit(hyper_count, (x0 + 100 + hyper_icon.get_width() + 10, y0 + 4))

    # Icône générique d'ingrédient (toujours présente)
    inv_base_x = x0 + 200
    screen.blit(ingredient_icon, (inv_base_x, y0))
    # Afficher les ingrédients collectés à droite de cette icône
    offset_x = inv_base_x + ingredient_icon.get_width() + 10
    for idx, ing_key in enumerate(ingredients_collected):
        ing_sprite = ingredient_sprites.get(ing_key, ingredient_icon)
        draw_sprite = ing_sprite
        # Animation de zoom pour le dernier ingrédient acquis
        if ing_anim_active and idx == len(ingredients_collected) - 1:
            t = now - ing_anim_start
            if t <= ing_anim_duration:
                factor = 1 + 1.0 * math.sin(math.pi * t / ing_anim_duration)
                w = int(ing_sprite.get_width() * factor)
                h = int(ing_sprite.get_height() * factor)
                draw_sprite = pygame.transform.scale(ing_sprite, (w, h))
            else:
                ing_anim_active = False
        # Calculer position centrée
        rect = draw_sprite.get_rect()
        pos_x = offset_x + idx * (ing_sprite.get_width() + 10) + (ing_sprite.get_width() - rect.width) // 2
        pos_y = y0 + (ing_sprite.get_height() - rect.height) // 2
        rect.topleft = (pos_x, pos_y)
        screen.blit(draw_sprite, rect)

    # Afficher le numéro de niveau en bas à droite
    lvl_surf = score_font.render(f"Level {level_idx+1}", True, WHITE)
    lvl_rect = lvl_surf.get_rect(bottomright=(screen_width - 10, screen_height - 10))
    screen.blit(lvl_surf, lvl_rect)

    # Actualiser l'affichage
    pygame.display.flip()

# Quitter Pygame proprement
pygame.quit()
sys.exit()