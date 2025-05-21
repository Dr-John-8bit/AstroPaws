import pygame
import sys
import random
import math
import textwrap

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

# Charger l'image du sprite d'AstroPaws
astro_sprite = pygame.image.load("images/astro_paws.png").convert_alpha()
astro_sprite = pygame.transform.scale(astro_sprite, (80, 80))


# Charger l'image du coeur pour les vies
heart_sprite = pygame.image.load("images/heart.png").convert_alpha()
heart_sprite = pygame.transform.scale(heart_sprite, (20, 20))

# Charger l'image de l'écran d'accueil
welcome_image = pygame.image.load("images/ecranaccueil.png").convert_alpha()
welcome_image = pygame.transform.scale(welcome_image, (400, 300))  # taille réduite

# Charger l'image du chat endormi pour la pause
chat_sleep_image = pygame.image.load("images/chatdort.png").convert_alpha()
chat_sleep_image = pygame.transform.scale(chat_sleep_image, (360, 240))

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
water_ammo = 50
pygame.font.init()
score_font = pygame.font.SysFont(None, 36)

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

# Variables pour le menu étendu
story_lines = [
    "AstroPaws: Gourmet Quest",
    "",
    "Lointain secteur de la Cuisine.",
    "Depuis la station Alpha-Felis, un signal d’alerte retentit dans le vide spatial. La dernière réserve de Pâtée Galactique™ a disparu !",
    "Le Capitaine AstroPaws — félin courageux, gourmet interstellaire, et dernier espoir du Conseil des Chats — prend le contrôle de son Jetpack Cosmique.",
    "Sa mission ? Traverser des champs d’astéroïdes, esquiver les ennemis de toujours (chiens errants, rats radioactifs, souris mutantes), et rassembler les 7 ingrédients sacrés de la pâtée de l’espace.",
    "",
    "Mais attention :",
    "Chaque tir consomme de l’eau pure, rare et précieuse.",
    "Chaque ennemi peut faire chuter votre score… ou vos vies.",
    "Ramassez les réserves, visez juste, évitez les croquettes piégées !",
    "",
    "Gameplay",
    "   - Déplacez AstroPaws avec les flèches directionnelles.",
    "   - Tirez avec la barre Espace (consomme de l’eau).",
    "   - Ramassez des croquettes (points) et de l’eau (munitions).",
    "   - Esquivez les ennemis ou détruisez-les avec des jets d’eau !",
    "   - Le jeu se termine si AstroPaws perd ses 9 vies.",
    "",
    "AstroPaws n’est pas un héros.",
    "C’est un chat.",
    "Mais parfois… c’est tout ce dont l’univers a besoin."
]
story_scroll_y = float(screen_height)
story_speed = 0.5  # pixels par frame

running = True
while running:
    # Limiter le jeu à 60 images par seconde
    clock.tick(60)

    # === Écran STORY ===
    if game_state == "STORY":
        # Gestion des événements pour sortir de la Story
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_ESCAPE, pygame.K_RETURN):
                    story_scroll_y = float(screen_width)
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
                for sub in textwrap.wrap(line, width=60):
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
        # Gestion des événements pour quitter, démarrer ou story
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_state = "PLAYING"
                elif event.key == pygame.K_s:
                    story_scroll_y = float(screen_height)
                    game_state = "STORY"
                elif event.key == pygame.K_q:
                    running = False
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
        # Afficher le fond étoilé
        screen.fill(BLACK)
        for star in star_list:
            pygame.draw.circle(screen, WHITE, (int(star['x']), int(star['y'])), 1)
        for planet in planet_list:
            pygame.draw.circle(screen, planet['color'], (int(planet['x']), int(planet['y'])), planet['size'])
        # Afficher l'image d'accueil centrée en haut
        image_rect = welcome_image.get_rect(midtop=(screen_width//2, 50))
        screen.blit(welcome_image, image_rect)
        # Clignotement du texte "PRESS SPACE TO START"
        now = pygame.time.get_ticks()
        if now - menu_blink_time > 500:
            menu_blink = not menu_blink
            menu_blink_time = now
        prompt_y_base = 50 + 300 + 30  # image top + image height + marge
        if menu_blink:
            prompt = score_font.render("PRESS SPACE TO START", True, WHITE)
            prompt_rect = prompt.get_rect(center=(screen_width//2, prompt_y_base))
            screen.blit(prompt, prompt_rect)
        # Prompt supplémentaire pour la Story
        prompt2 = score_font.render("PRESS S FOR STORY", True, WHITE)
        prompt2_rect = prompt2.get_rect(center=(screen_width//2, prompt_y_base + 40))
        screen.blit(prompt2, prompt2_rect)
        # Prompt pour quitter
        prompt3 = score_font.render("PRESS Q TO QUIT", True, WHITE)
        prompt3_rect = prompt3.get_rect(center=(screen_width//2, prompt_y_base + 80))
        screen.blit(prompt3, prompt3_rect)
        pygame.display.flip()
        continue

    # === Écran PAUSE ===
    if game_state == "PAUSE":
        # Gestion des événements pour reprendre ou quitter
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
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
        water_surface = score_font.render(f"Water: {water_ammo}", True, WHITE)
        screen.blit(water_surface, (10, 50))
        lives_surface = score_font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(lives_surface, (10, 90))
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
        quit_rect = quit_surf.get_rect(center=(screen_width//2, screen_height*2//3))
        screen.blit(quit_surf, quit_rect)
        # Afficher le chat endormi en bas de l'écran de pause
        chat_rect = chat_sleep_image.get_rect(midbottom=(screen_width//2, screen_height - 10))
        screen.blit(chat_sleep_image, chat_rect)
        pygame.display.flip()
        continue

    # === Écran JEU (PLAYING) ===
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                game_state = "PAUSE"
                break
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
                        dy = -1  # par défaut, tirer vers le haut
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
    if keys[pygame.K_LEFT]:
        astro_x -= speed
    if keys[pygame.K_RIGHT]:
        astro_x += speed
    if keys[pygame.K_UP]:
        astro_y -= speed
    if keys[pygame.K_DOWN]:
        astro_y += speed

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

    # Spawn d'ennemis
    if random.random() < 0.02:  # 2% de chance par frame
        side = random.choice(['left', 'right', 'top', 'bottom'])
        r = random.random()
        if r < 0.15:
            enemy_type = "dog"
            enemy_width = 50
            enemy_height = 50
            enemy_speed = 2
            enemy_health = 3
        elif r < 0.5:
            enemy_type = "rat"
            enemy_width = 30
            enemy_height = 30
            enemy_speed = 3
            enemy_health = 2
        else:
            enemy_type = "mouse"
            enemy_width = 20
            enemy_height = 20
            enemy_speed = 4
            enemy_health = 1
        if side == 'left':
            x = -enemy_width
            y = random.randint(0, screen_height - enemy_height)
            dx = enemy_speed  # se dirige vers la droite
            dy = 0
        elif side == 'right':
            x = screen_width
            y = random.randint(0, screen_height - enemy_height)
            dx = -enemy_speed  # se dirige vers la gauche
            dy = 0
        elif side == 'top':
            x = random.randint(0, screen_width - enemy_width)
            y = -enemy_height
            dx = 0
            dy = enemy_speed  # se dirige vers le bas
        elif side == 'bottom':
            x = random.randint(0, screen_width - enemy_width)
            y = screen_height
            dx = 0
            dy = -enemy_speed  # se dirige vers le haut
        enemy_list.append({'x': x, 'y': y, 'width': enemy_width, 'height': enemy_height,
                           'type': enemy_type, 'dx': dx, 'dy': dy, 'speed': enemy_speed, 'health': enemy_health})
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
            if enemy['type'] == "dog":
                lives -= 1
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
        game_over_surface = score_font.render("GAME OVER", True, WHITE)
        screen.blit(game_over_surface, (screen_width//2 - 50, screen_height//2))
        pygame.display.flip()
        pygame.time.delay(2000)
        running = False

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
                score += 5
            else:
                score += 1
        else:
            new_croquette_list.append(croquette)
    croquette_list = new_croquette_list

    # Mise à jour des réserves d'eau (water items)
    current_time = pygame.time.get_ticks()
    water_item_list = [item for item in water_item_list if current_time - item['spawn_time'] < 7000]  # durée de vie de 7 sec
    
    # Collision entre AstroPaws et les réserves d'eau
    for item in water_item_list[:]:
        water_rect = pygame.Rect(item['x'], item['y'], 10, 10)
        if player_rect.colliderect(water_rect):
            water_ammo += 10
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

    # Affichage du fond spatial procédural
    screen.fill(BLACK)
    # Dessiner les étoiles
    for star in star_list:
        pygame.draw.circle(screen, WHITE, (int(star['x']), int(star['y'])), 1)
    # Dessiner les planètes
    for planet in planet_list:
        pygame.draw.circle(screen, planet['color'], (int(planet['x']), int(planet['y'])), planet['size'])
    # Dessiner les croquettes
    for croquette in croquette_list:
        if croquette.get('type') == "rare":
            color = GOLD
        else:
            color = ORANGE
        pygame.draw.rect(screen, color, (croquette['x'], croquette['y'], croquette_size, croquette_size))
    # Dessiner les réserves d'eau (objets d'acquisition d'eau)
    for item in water_item_list:
        pygame.draw.rect(screen, (0, 200, 255), (item['x'], item['y'], 10, 10))
    # Dessiner les ennemis
    for enemy in enemy_list:
        if enemy['type'] == "rat":
            enemy_color = (200, 0, 0)  # rouge plus foncé pour les rats
        elif enemy['type'] == "dog":
            enemy_color = (255, 0, 0)  # rouge pour les chiens
        else:
            enemy_color = (255, 100, 100)  # rouge clair pour les souris
        pygame.draw.rect(screen, enemy_color, (enemy['x'], enemy['y'], enemy['width'], enemy['height']))
    # Dessiner les particules d'explosion
    for particle in explosion_list:
        pygame.draw.circle(screen, particle['color'], (int(particle['x']), int(particle['y'])), 2)
    # Afficher les tirs (jet d'eau bleu)
    for bullet in bullet_list:
        pygame.draw.rect(screen, BLUE, bullet['rect'])
    # Afficher le sprite d'AstroPaws à sa position
    screen.blit(astro_sprite, (astro_x, astro_y))
    
    # Afficher le score et les vies
    score_surface = score_font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_surface, (10, 10))
    # Afficher les vies sous forme de cœurs en haut à droite
    for i in range(lives):
         screen.blit(heart_sprite, (screen_width - (heart_sprite.get_width() + 10) * (i + 1), 10))
    # Afficher le score, l'eau et les vies
    score_surface = score_font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_surface, (10, 10))
    water_surface = score_font.render("Water: " + str(water_ammo), True, WHITE)
    screen.blit(water_surface, (10, 50))

    # Actualiser l'affichage
    pygame.display.flip()

# Quitter Pygame proprement
pygame.quit()
sys.exit()