import os
import pygame
import random


print("HELLO EVERYONE")

print("MADE BY RAID MESBAHI update by Lina : DO NOT USE THIS PROJECT WITHOUT CONSENT FROM ME HERE IS MY GMAIL : herobrineraid@gmail.com")

# Initialize pygame
pygame.init()

print("HELLO EVERYONE")

print("MADE BY RAID MESBAHI : DO NOT USE THIS PROJECT WITHOUT CONSENT FROM ME HERE IS MY GMAIL : herobrineraid@gmail.com")

# Screen settings
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Pac-Man")

# Assets directory - using relative path
assets_dir = os.path.join(os.path.dirname(__file__), "..", "assets")

def clean_asset_folder(folder_path):
    for fname in os.listdir(folder_path):
        if fname.startswith("._"):
            os.remove(os.path.join(folder_path, fname))
            print(f"[INFO] Removed temporary file: {fname}")

def load_image(filepath, scale=None, fill_screen=False):
    if not os.path.exists(filepath):
        print(f"[ERROR] File not found: {filepath}")
        raise FileNotFoundError(filepath)
    try:
        image = pygame.image.load(filepath).convert_alpha()
        if scale:
            image = pygame.transform.scale(image, scale)
        if fill_screen:
            image = pygame.transform.scale(image, (WIDTH, HEIGHT))
        print(f"[OK] Loaded image: {os.path.basename(filepath)}")
        return image
    except pygame.error as e:
        print(f"[ERROR] Failed to load: {filepath} - {e}")
        raise SystemExit(e)

# Clean up any temporary files in assets folder
clean_asset_folder(assets_dir)

# Load images using proper path joining
bg_img = load_image(os.path.join(assets_dir, "bg.png"), fill_screen=True)
victory_img = load_image(os.path.join(assets_dir, "win.png"), fill_screen=True)
game_over_img = load_image(os.path.join(assets_dir, "ggs.jpeg"), fill_screen=True)
pacman_img = load_image(os.path.join(assets_dir, "pacman.png"), scale=(30, 30))
ghost_img = load_image(os.path.join(assets_dir, "ghost.png"), scale=(30, 30))
food_img = load_image(os.path.join(assets_dir, "food.png"), scale=(10, 10))

# Pac-Man settings
pacman = pygame.Rect(50, 50, 30, 30)
pacman_speed = 5

# Function to generate a valid ghost position
def generate_ghost_position(obstacles, ghost_size, min_distance):
    while True:
        x = random.randint(0, WIDTH - ghost_size)
        y = random.randint(0, HEIGHT - ghost_size)
        ghost_rect = pygame.Rect(x, y, ghost_size, ghost_size)
        valid_position = True
        for obstacle in obstacles:
            if ghost_rect.colliderect(obstacle.inflate(min_distance * 2, min_distance * 2)):
                valid_position = False
                break
        if valid_position:
            return x, y

# Ghost settings
ghost_size = 30
ghost = pygame.Rect(0, 0, ghost_size, ghost_size)
ghost.x, ghost.y = generate_ghost_position([], ghost_size, 20)
ghost_speed = 2

# Food settings
food = pygame.Rect(random.randint(0, WIDTH - 10), random.randint(0, HEIGHT - 10), 10, 10)

# Maze generation (using long bars)
def generate_maze(width, height, bar_length, bar_width):
    maze = []
    for y in range(0, height, bar_length * 2):
        x = random.randint(0, width - bar_length)
        maze.append(pygame.Rect(x, y, bar_length, bar_width))
    for x in range(0, width, bar_length * 2):
        y = random.randint(0, height - bar_length)
        maze.append(pygame.Rect(x, y, bar_width, bar_length))
    return maze

bar_length = 100
bar_width = 10
obstacles = generate_maze(WIDTH, HEIGHT, bar_length, bar_width)

ghost.x, ghost.y = generate_ghost_position(obstacles, ghost_size, 20)

# Game variables
running = True
score = 0
clock = pygame.time.Clock()
win_score = 5

# Font
font = pygame.font.Font(None, 36)

def show_end_screen(image):
    screen.blit(image, (0, 0))
    pygame.display.flip()
    pygame.time.delay(3000)

def generate_food_position(obstacles, food_size, min_distance):
    while True:
        x = random.randint(0, WIDTH - food_size)
        y = random.randint(0, HEIGHT - food_size)
        food_rect = pygame.Rect(x, y, food_size, food_size)
        valid_position = True
        for obstacle in obstacles:
            if food_rect.colliderect(obstacle.inflate(min_distance * 2, min_distance * 2)):
                valid_position = False
                break
        if valid_position:
            return x, y

def teleport_pacman():
    pacman.x = random.randint(0, WIDTH - pacman.width)
    pacman.y = random.randint(0, HEIGHT - pacman.height)

def move_ghost(ghost, pacman, ghost_speed, obstacles):
    dx = 0
    dy = 0

    if ghost.x < pacman.x:
        dx = ghost_speed
    elif ghost.x > pacman.x:
        dx = -ghost_speed

    if ghost.y < pacman.y:
        dy = ghost_speed
    elif ghost.y > pacman.y:
        dy = -ghost_speed

    new_ghost_rect_x = ghost.move(dx, 0)
    new_ghost_rect_y = ghost.move(0, dy)

    valid_x = True
    valid_y = True

    for obstacle in obstacles:
        if new_ghost_rect_x.colliderect(obstacle):
            valid_x = False
        if new_ghost_rect_y.colliderect(obstacle):
            valid_y = False

    if valid_x:
        ghost.x += dx
    if valid_y:
        ghost.y += dy

while running:
    screen.blit(bg_img, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move Pac-Man
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        pacman.x -= pacman_speed
    if keys[pygame.K_RIGHT]:
        pacman.x += pacman_speed
    if keys[pygame.K_UP]:
        pacman.y -= pacman_speed
    if keys[pygame.K_DOWN]:
        pacman.y += pacman_speed

    # Teleport Pac-Man if touches border
    if pacman.x < 0 or pacman.x > WIDTH - pacman.width or pacman.y < 0 or pacman.y > HEIGHT - pacman.height:
        teleport_pacman()

    # Collision with obstacles
    for obstacle in obstacles:
        if pacman.colliderect(obstacle):
            teleport_pacman()

    # Move Ghost toward Pac-Man
    move_ghost(ghost, pacman, ghost_speed, obstacles)

    # Check collision with food
    if pacman.colliderect(food):
        score += 1
        new_food_pos = generate_food_position(obstacles, 10, 20)
        food.x, food.y = new_food_pos
        if score >= win_score:
            show_end_screen(victory_img)
            running = False

    # Check collision with ghost
    if pacman.colliderect(ghost):
        show_end_screen(game_over_img)
        running = False

    # Draw objects
    screen.blit(pacman_img, (pacman.x, pacman.y))
    screen.blit(ghost_img, (ghost.x, ghost.y))
    screen.blit(food_img, (food.x, food.y))
    for obstacle in obstacles:
        pygame.draw.rect(screen, (128, 128, 128), obstacle)

    # Display score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
