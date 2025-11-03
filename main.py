import pygame
import random
import math
import sys
import os

pygame.init()

# --- Helper for standalone .exe ---
def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# --- Window setup ---
WIDTH, HEIGHT = 600, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Egg Catcher")

# --- Load assets ---
egg_img = pygame.image.load(resource_path("assets/egg.png"))
basket_img = pygame.image.load(resource_path("assets/basket.png"))
bg_img = pygame.image.load(resource_path("assets/bg.jpg"))

egg_size = 50
basket_size = 80
egg_img = pygame.transform.scale(egg_img, (egg_size, egg_size))
basket_img = pygame.transform.scale(basket_img, (basket_size, basket_size))
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

# --- Sounds ---
pygame.mixer.music.load(resource_path("assets/music.mp3"))
catch_sound = pygame.mixer.Sound(resource_path("assets/catch.wav"))
miss_sound = pygame.mixer.Sound(resource_path("assets/miss.wav"))

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 70)
clock = pygame.time.Clock()

# --- Color cycling for menu ---
def color_cycle(t):
    r = int((1 + math.sin(t * 0.002)) * 127)
    g = int((1 + math.sin(t * 0.002 + 2)) * 127)
    b = int((1 + math.sin(t * 0.002 + 4)) * 127)
    return (r, g, b)

# --- Game states ---
MENU, TUTORIAL, GAME = "menu", "tutorial", "game"
state = MENU

# --- Reset game ---
def reset_game():
    return {
        "basket_x": WIDTH // 2,
        "basket_y": HEIGHT - 100,
        "basket_speed": 7,
        "egg_x": random.randint(0, WIDTH - egg_size),
        "egg_y": -egg_size,
        "egg_speed": 5,
        "score": 0,
        "lives": 3
    }

game = reset_game()
pygame.mixer.music.play(-1)

# --- Main loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if state == MENU:
        t = pygame.time.get_ticks()
        window.fill(color_cycle(t))
        title = big_font.render("EGG CATCHER", True, WHITE)
        play_text = font.render("Press [P] to Play", True, WHITE)
        tutorial_text = font.render("Press [T] for Tutorial", True, WHITE)
        window.blit(title, (WIDTH//2 - title.get_width()//2, 200))
        window.blit(play_text, (WIDTH//2 - play_text.get_width()//2, 400))
        window.blit(tutorial_text, (WIDTH//2 - tutorial_text.get_width()//2, 460))

        if keys[pygame.K_p]:
            state = GAME
            game = reset_game()
        if keys[pygame.K_t]:
            state = TUTORIAL

    elif state == TUTORIAL:
        t = pygame.time.get_ticks()
        window.fill(color_cycle(t))
        lines = [
            "Catch eggs with your basket.",
            "Use arrow keys or A/D to move.",
            "Each caught egg makes you faster.",
            "Missing eggs slows you down.",
            "You have 3 lives total.",
            "Press [M] to return to Menu."
        ]
        for i, line in enumerate(lines):
            text = font.render(line, True, WHITE)
            window.blit(text, (WIDTH//2 - text.get_width()//2, 200 + i * 50))
        if keys[pygame.K_m]:
            state = MENU

    elif state == GAME:
        # Movement
        if keys[pygame.K_LEFT] and game["basket_x"] > 0:
            game["basket_x"] -= game["basket_speed"]
        if keys[pygame.K_RIGHT] and game["basket_x"] < WIDTH - basket_size:
            game["basket_x"] += game["basket_speed"]

        # Egg fall
        game["egg_y"] += game["egg_speed"]

        # Catch check
        if (game["basket_x"] < game["egg_x"] + egg_size and
            game["basket_x"] + basket_size > game["egg_x"] and
            game["basket_y"] < game["egg_y"] + egg_size < game["basket_y"] + basket_size):
            catch_sound.play()
            game["score"] += 1
            game["egg_x"] = random.randint(0, WIDTH - egg_size)
            game["egg_y"] = -egg_size
            game["egg_speed"] += 0.2
            game["basket_speed"] += 0.1

        # Miss check
        if game["egg_y"] > HEIGHT:
            miss_sound.play()
            game["lives"] -= 1
            game["egg_x"] = random.randint(0, WIDTH - egg_size)
            game["egg_y"] = -egg_size
            game["egg_speed"] = max(5, game["egg_speed"] - 0.3)
            game["basket_speed"] = max(4, game["basket_speed"] - 0.3)
            if game["lives"] <= 0:
                state = MENU

        # Draw
        window.blit(bg_img, (0, 0))
        window.blit(egg_img, (game["egg_x"], game["egg_y"]))
        window.blit(basket_img, (game["basket_x"], game["basket_y"]))

        score_text = font.render(f"Score: {game['score']}", True, BLACK)
        lives_text = font.render(f"Lives: {game['lives']}", True, BLACK)
        window.blit(score_text, (10, 10))
        window.blit(lives_text, (10, 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
