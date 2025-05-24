# Configuration des niveaux pour AstroPaws
levels = [
    {
        "name": "Les souris mutantes de l'espace",
        "spawn_weights": {"mouse": 0.85, "rat": 0.05, "dog": 0.01},
        "target_score": 25,
        "item": {"type": "shield", "cooldown": 30000},
        "end_item": "ingredient_poulet",
        "bg_tint": (10, 10, 50),  # bleu foncé pour niveau 1
        "music": "gameplay_loop_level1.ogg",
    },
    {
        "name": "Les rats radioactifs de l'espace",
        "spawn_weights": {"mouse": 0.6, "rat": 0.5, "dog": 0.1},
        "target_score": 80,
        "item": {"type": "hyperdrive", "cooldown": 60000},
        "end_item": "ingredient_thon",
        "bg_tint": (30, 30, 100),    # bleu intermédiaire pour niveau 2
        "music": "gameplay_loop_level2.ogg",
    },
    {
        "name": "Les chiens d'la casse de l'espace",
        "spawn_weights": {"mouse": 0.5, "rat": 0.5, "dog": 0.9},
        "target_score": 120,
        "item": {"type": "supershield", "cooldown": 90000},
        "end_item": "ingredient_carotte",
        "bg_tint": (0, 0, 0),        # noir pour niveau 3
        "music": "gameplay_loop_level3.ogg",
    },
]