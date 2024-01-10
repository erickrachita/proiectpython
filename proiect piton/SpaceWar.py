import pygame
import time
import random
import math

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACE WAR")

BG = pygame.transform.scale(pygame.image.load("bg.jpg"), (WIDTH, HEIGHT))

PLAYER_RADIUS = 20
PLAYER_VEL = 5
STAR_RADIUS = 15
STAR_WIDTH = 20
STAR_HEIGHT = 30
STAR_VEL = 5

FONT = pygame.font.SysFont("impact", 30)

pygame.mixer.music.load("5 Minute ScienceSpace Theme Timer with Music.mp3")
pygame.mixer.music.play(-1)

def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    # Drawing the player as a circle on top of a rectangle
    pygame.draw.rect(WIN, "yellow", player["rect"])
    pygame.draw.circle(WIN, "red", player["circle"][0], player["circle"][1])

    for star in stars:
        # Drawing each star as a circle on top of a rectangle
        pygame.draw.rect(WIN, "yellow", star["rect"])
        pygame.draw.circle(WIN, "red", star["circle"][0], star["circle"][1])

    pygame.display.update()

def ellipse_collision(player, ellipse):
    player_radius = player["rect"].width // 2
    player_center = (player["rect"].x + player_radius, player["rect"].y + player_radius)

    ellipse_radius_x = ellipse["rect"].width // 2
    ellipse_radius_y = ellipse["rect"].height // 2
    ellipse_center = (ellipse["rect"].x + ellipse_radius_x, ellipse["rect"].y + ellipse_radius_y)

    distance = math.sqrt((ellipse_center[0] - player_center[0]) ** 2 + (ellipse_center[1] - player_center[1]) ** 2)

    return distance < (player_radius + max(ellipse_radius_x, ellipse_radius_y))

def main():
    run = True

    player = {
        "rect": pygame.Rect(200, HEIGHT - PLAYER_RADIUS * 2, PLAYER_RADIUS * 2, PLAYER_RADIUS * 2),
        "circle": ((0, 0), PLAYER_RADIUS)  # Placeholder values, will be updated in the loop
    }

    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0

    stars = []
    hit = False

    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(5):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star_rect = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                star_circle = ((star_rect.centerx, star_rect.y), STAR_RADIUS)
                stars.append({"rect": star_rect, "circle": star_circle})

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player["rect"].x - PLAYER_VEL >= 0:
            player["rect"].x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player["rect"].x + PLAYER_VEL + player["rect"].width <= WIDTH:
            player["rect"].x += PLAYER_VEL

        # Update the circle position for the player
        player["circle"] = ((player["rect"].centerx, player["rect"].y), PLAYER_RADIUS)

        for star in stars[:]:
            star["rect"].y += STAR_VEL
            if star["rect"].y > HEIGHT:
                stars.remove(star)
            elif ellipse_collision(player, star):
                stars.remove(star)
                hit = True
                break

        if hit:
            pygame.mixer.music.stop()
            lost_text = FONT.render("Ai pierdut!", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(player, elapsed_time, stars)

    pygame.quit()

if __name__ == "__main__":
    main()
