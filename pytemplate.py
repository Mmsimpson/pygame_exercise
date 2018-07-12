import pygame
import random

def main(): # can set up a timer. timer = 0     everytime loop runs
    width = 700
    height = 700
#game initialization below
# initialize sound - uncomment if you're using sound

    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Asteroid Crusher')
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()

    turret_x = 350 # position
    turret_y = 675 #position
    t_width = 35
    t_height = 25
    velocity = 7
    #asteroid_radius = 30
   
    #class asteroid(object):
        #def __init__(self, speed, size)

    running = True
    #start the game loop
    while running:
        clock.tick(60)
        # process inputs (events)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running= False
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RIGHT] and turret_x < width - t_width - velocity:
            turret_x += velocity
        if pressed[pygame.K_LEFT] and turret_x > velocity:
            turret_x -= velocity
       # if keys[pygame.K_SPACE]: 
        
        
        #update - figure out which each sprite what do do
        all_sprites.update()
        pygame.display.update()
        
        # Draw / render
        screen.fill((0, 0, 0)) #this is a tuple
        all_sprites.draw(screen)
        pygame.draw.circle(screen, (255, 0 , 0), (turret_x, turret_y), t_width, t_height)
        
    pygame.quit()
main()


