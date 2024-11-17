import pygame
import json

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test Shoot Animation")

# Load the JSON data
with open('sprites/slash.json') as f:
    shoot_data = json.load(f)

# Load the sprite sheet
sprite_sheet = pygame.image.load(shoot_data["spriteSheetURL"]).convert_alpha()

# Extract the frames
frames = []
frame_width = shoot_data["sprites"][0]["xsize"]
frame_height = shoot_data["sprites"][0]["ysize"]
for image in shoot_data["sprites"][0]["images"]:
    x = image["x"]
    y = image["y"]
    frame = sprite_sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
    frames.append(frame)

# Animation settings
interval_time = shoot_data["sprites"][0]["interval_time"]
current_frame = 0
timer = 0

# Main loop
running = True
clock = pygame.time.Clock()
while running:
    dt = clock.tick(60) / 1000  # Delta time in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update animation
    timer += dt
    if timer > interval_time:
        timer = 0
        current_frame = (current_frame + 1) % len(frames)

    # Clear screen
    screen.fill((0, 0, 0))

    # Draw current frame
    screen.blit(frames[current_frame], (WIDTH // 2 - frame_width // 2, HEIGHT // 2 - frame_height // 2))

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()