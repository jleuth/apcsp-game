import pygame
from animatronic import Animatronic
from door import Door

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("FNAF Horror")
clock = pygame.time.Clock()

# Game state
STATE_MENU = 0
STATE_GAME = 1
game_state = STATE_MENU

# Assets
map_image = pygame.image.load('map.png')

# Game objects
waypoints = [(100, 100), (700, 100), (700, 500), (100, 500)]
anim = Animatronic(100, 100, waypoints)
doors = [
    Door(362, 542, 7, 33, "Left door"),
    Door(448, 542, 7, 33, "Right door"),
]

def handle_menu_input(event):
    global game_state
    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        game_state = STATE_GAME

def handle_game_input(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a:
            doors[0].toggle()
        elif event.key == pygame.K_d:
            doors[1].toggle()

def draw_menu():
    font_title = pygame.font.SysFont(None, 64)
    font_instr = pygame.font.SysFont(None, 36)
    title = font_title.render("FNAF Clone", True, (255, 255, 255))
    instr = font_instr.render("Press ENTER to Start", True, (255, 255, 255))
    
    screen.blit(title, title.get_rect(center=(400, 200)))
    screen.blit(instr, instr.get_rect(center=(400, 300)))

def draw_game():
    screen.blit(map_image, (0, 0))
    anim.draw(screen)
    for door in doors:
        door.draw(screen)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif game_state == STATE_MENU:
            handle_menu_input(event)
        elif game_state == STATE_GAME:
            handle_game_input(event)
    
    # Update
    if game_state == STATE_GAME:
        anim.move_toward_waypoint()
    
    # Draw
    screen.fill((0, 0, 0))
    if game_state == STATE_MENU:
        draw_menu()
    elif game_state == STATE_GAME:
        draw_game()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()