#Game was created by following a Tutorial on Youtube from a channel called Tech With Tim.

import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900,500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)
HEALTH_FONT = pygame.font.SysFont('arial', 30)
WINNER_FONT = pygame.font.SysFont('arial', 90)

BULLET_HIT_SOUND = pygame.mixer.Sound(
    os.path.join('Assets', 'explosion.wav'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(
    os.path.join('Assets', 'laser.wav'))
BACKGROUND_MUSIC = pygame.mixer.Sound(os.path.join('Assets','background.wav'))

FPS = 60
#VEL = 5
#VEL2 = 8
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55,40
BULLET_VEL = 8
MAX_BULLETS = 6

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(      ##"Bug: module 'pygame.image' has no attribute rotate -> pygame.transform"
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90) 

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

BACKGROUND_IMAGE = pygame.image.load(
    os.path.join('Assets', 'space.png'))
BACKGROUND = pygame.transform.scale(
    (BACKGROUND_IMAGE), (WIDTH,HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    #WIN.fill((WHITE))#
    WIN.blit(BACKGROUND, (0,0))

    red_health_text = HEALTH_FONT.render("Red Health:" + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Yellow Health:" + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    pygame.draw.rect(WIN, BLACK, BORDER) #Create border
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    

    for bullets in red_bullets:
        pygame.draw.rect(WIN,RED,bullets)

    for bullets in yellow_bullets:
        pygame.draw.rect(WIN,YELLOW,bullets)

    pygame.display.update() # Updates the display

def yellow_handle_movement(keys_pressed, yellow):
    VEL = 5 
    VEL2 = 8

    if keys_pressed[pygame.K_LSHIFT]:
        VEL = VEL2
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: #LEFT
            yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: #RIGHT
            yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: #UP
            yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT: #DOWN
            yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    VEL = 5
    VEL2 = 8
    
    if keys_pressed[pygame.K_RSHIFT]:
        VEL = VEL2
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x : #LEFT
            red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: #RIGHT
            red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: #UP
            red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT: #DOWN
            red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red): #Handles the moving of bullets, collision, and removal of bullets
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL 
        if red.colliderect(bullet): # Returns true or false for collision (if both objects are rectangles)
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL 
        if yellow.colliderect(bullet): # Returns true or false for collision (if both objects are rectangles)
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)            
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE) # Bug: WINNER_FONT.render = (text) -> AttributeError, object attribute is read-only
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2 , HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

## Create window
def main():
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    BACKGROUND_MUSIC.play(-1)

    # Empty list for bullets
    yellow_bullets = []
    red_bullets = [] 

    yellow_health = 5
    red_health = 5

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN: # Fire a bullet if key is pressed
                if event.key == pygame.K_f and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_SLASH and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                #BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -=1
                #BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break #SOMEONE WON

        #print(red_bullets, yellow_bullets) #Printing x and y coordinates of the bullets, not required
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed,yellow)
        red_handle_movement(keys_pressed,red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health) ##"Bug: missing 2 required positional arguments, remember to pass arguments"

    main()

if __name__ == "__main__":
    main()