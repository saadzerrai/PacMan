import os
import pygame
import random

# === CONFIGURATION GÉNÉRALE ===
pygame.init()
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Pac-Man")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# === DOSSIER DES IMAGES ===
assets_dir = r"C:\Users\Dell Latitude\Desktop\Projets python pro 1  2024-2025\Raid Mrsbahi\project\assets"

def clean_asset_folder(folder_path):
    for fname in os.listdir(folder_path):
        if fname.startswith("._"):
            os.remove(os.path.join(folder_path, fname))
            print(f"[INFO] Fichier inutile supprimé : {fname}")

def load_image(filepath, scale=None, fill_screen=False):
    if not os.path.exists(filepath):
        print(f"[ERREUR] Fichier introuvable : {filepath}")
        raise FileNotFoundError(filepath)
    try:
        image = pygame.image.load(filepath).convert_alpha()
        if scale:
            image = pygame.transform.scale(image, scale)
        if fill_screen:
            image = pygame.transform.scale(image, (WIDTH, HEIGHT))
        print(f"[OK] Image chargée : {os.path.basename(filepath)}")
        return image
    except pygame.error as e:
        print(f"[ERREUR] Chargement échoué : {filepath} - {e}")
        raise SystemExit(e)

clean_asset_folder(assets_dir)

# === CHARGEMENT DES IMAGES ===
bg_img = load_image(os.path.join(assets_dir, "bg.png"), fill_screen=True)
victory_img = load_image(os.path.join(assets_dir, "win.png"), fill_screen=True)
game_over_img = load_image(os.path.join(assets_dir, "ggs.jpeg"), fill_screen=True)
pacman_img = load_image(os.path.join(assets_dir, "pacman.png"), scale=(30, 30))
ghost_img = load_image(os.path.join(assets_dir, "ghost.png"), scale=(30, 30))
food_img = load_image(os.path.join(assets_dir, "food.png"), scale=(10, 10))

# === ENTITÉS DU JEU ===
pacman = pygame.Rect(50, 50, 30, 30)
pacman_speed = 5

ghost_size = 30
ghost = pygame.Rect(0, 0, ghost_size, ghost_size)
ghost_speed = 2

food = pygame.Rect(random.randint(0, WIDTH - 10), random.randint(0, HEIGHT - 10), 10, 10)

def generate_ghost_position(obstacles, size, min_distance):
    while True:
        x = random.randint(0, WIDTH - size)
        y = random.randint(0, HEIGHT - size)
        ghost_rect = pygame.Rect(x, y, size, size)
        if all(not ghost_rect.colliderect(ob.inflate(min_distance * 2, min_distance * 2)) for ob in obstacles):
            return x, y

def generate_food_position(obstacles, size, min_distance):
    while True:
        x = random.randint(0, WIDTH - size)
        y = random.randint(0, HEIGHT - size)
        food_rect = pygame.Rect(x, y, size, size)
        if all(not food_rect.colliderect(ob.inflate(min_distance * 2, min_distance * 2)) for ob in obstacles):
            return x, y

def teleport_pacman():
    pacman.x = random.randint(0, WIDTH - pacman.width)
    pacman.y = random.randint(0, HEIGHT - pacman.height)

def generate_maze(width, height, bar_length, bar_width):
    maze = []
    for y in range(0, height, bar_length * 2):
        x = random.randint(0, width - bar_length)
        maze.append(pygame.Rect(x, y, bar_length, bar_width))
    for x in range(0, width, bar_length * 2):
        y = random.randint(0, height - bar_length)
        maze.append(pygame.Rect(x, y, bar_width, bar_length))
    return maze

def move_ghost(ghost, pacman, speed, obstacles):
    dx = ghost_speed if ghost.x < pacman.x else -ghost_speed if ghost.x > pacman.x else 0
    dy = ghost_speed if ghost.y < pacman.y else -ghost_speed if ghost.y > pacman.y else 0

    new_x = ghost.move(dx, 0)
    new_y = ghost.move(0, dy)

    if all(not new_x.colliderect(ob) for ob in obstacles):
        ghost.x += dx
    if all(not new_y.colliderect(ob) for ob in obstacles):
        ghost.y += dy

def show_end_screen(image):
    screen.blit(image, (0, 0))
    pygame.display.flip()
    pygame.time.delay(3000)

# === INITIALISATION DU LABYRINTHE ET GHOST ===
bar_length = 100
bar_width = 10
obstacles = generate_maze(WIDTH, HEIGHT, bar_length, bar_width)
ghost.x, ghost.y = generate_ghost_position(obstacles, ghost_size, 20)

# === LOGIQUE DU JEU ===
score = 0
win_score = 5
running = True

while running:
    screen.blit(bg_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: pacman.x -= pacman_speed
    if keys[pygame.K_RIGHT]: pacman.x += pacman_speed
    if keys[pygame.K_UP]: pacman.y -= pacman_speed
    if keys[pygame.K_DOWN]: pacman.y += pacman_speed

    if pacman.x < 0 or pacman.x > WIDTH - pacman.width or pacman.y < 0 or pacman.y > HEIGHT - pacman.height:
        teleport_pacman()

    for obstacle in obstacles:
        if pacman.colliderect(obstacle):
            teleport_pacman()

    move_ghost(ghost, pacman, ghost_speed, obstacles)

    if pacman.colliderect(food):
        score += 1
        food.x, food.y = generate_food_position(obstacles, 10, 20)
        if score >= win_score:
            show_end_screen(victory_img)
            break

    if pacman.colliderect(ghost):
        show_end_screen(game_over_img)
        break

    screen.blit(pacman_img, (pacman.x, pacman.y))
    screen.blit(ghost_img, (ghost.x, ghost.y))
    screen.blit(food_img, (food.x, food.y))
    for obstacle in obstacles:
        pygame.draw.rect(screen, (128, 128, 128), obstacle)

    score_text = font.render(f"Score : {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
