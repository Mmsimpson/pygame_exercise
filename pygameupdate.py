import pygame
import random

WHITE = (250, 250, 250)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WIDTH = 750
HEIGHT = 850


#game initialization below
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Saban Crusher')
clock = pygame.time.Clock()

font_name = pygame.font.match_font('times')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface,text_rect)

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 15
    fill = (pct / 150 * BAR_LENGTH)
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, BLUE, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 3)

class Player(pygame.sprite.Sprite): 
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (75, 90))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 40
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 28
        self.speedx = 0
        self.shield = 150
        
    def update(self):
        self.speedx = 0
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_d]:
            self.speedx = 17
        if pressed[pygame.K_a]:
            self.speedx = -17
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0: 
            self.rect.left = 0
    
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = saban_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 32
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(3, 8)
        self.speedx = random.randrange(-4, 4)
    
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 20 or self.rect.left < -80 or self.rect.right > WIDTH + 80:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(6, 14)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = football_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -13

    def update(self):
        self.rect.y += self.speedy
        #kill if moved pass screen
        if self.rect.bottom < 0:
            self.kill()

#class Explosion(pygame.sprite.Sprite):
    #def __init__(self, center,):
        #pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.transform.scale(expl_anim, (40, 40))
        #self.rect = self.image.get_rect()
        #self.rect.center = center
        #self.frame = 0
        #self.last_update = pygame.time.get_ticks()
        #self.frame_rate = 50
    #def update(self):
        #now = pygame.time.get_ticks()
        #if now - self.last_update > self.frame_rate:
            #self.last_update = now
            #self.frame += 1
            #if self.frame == self.rect:
                #self.kill()
    
#def main(): # can set up a timer. timer = 0     everytime loop runs

#Load all game graphics
background = pygame.image.load('img/football-field_art.png').convert()
background_rect = background.get_rect()
player_img = pygame.image.load('img/Kirby-Smart.png').convert()
saban_img = pygame.image.load('img/Nick_Saban_in_2009_(cropped).png').convert()
football_img = pygame.image.load('img/football.png').convert()
#expl_anim = pygame.image.load('img/flash05.png').convert()

# game sounds
shoot_sound = pygame.mixer.Sound('snd/sfx_throw.wav')
snd1 = pygame.mixer.Sound('snd/ogalaughter_2(1).ogg')
pygame.mixer.music.load('snd/TownTheme.mp3')
pygame.mixer.music.set_volume(0.3)


all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(9):
   newmob()
   m = Mob()
   all_sprites.add(m)
   mobs.add(m)
score = 0
snd1.play(loops = -1)
pygame.mixer.music.play(loops = -1)

end_it=False
while (end_it == False):
    screen.fill(BLACK)
    myfont = pygame.font.SysFont("Britannic Bold", 40)
    nlabel = myfont.render("Welcome to the 'Saban Crusher' Start Screen", 1, (WHITE))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            end_it=True
    screen.blit(nlabel,(50,100))
    pygame.display.flip()

#game loop
running = True
while running:
    clock.tick(60)
    # process inputs (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running= False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    #update - figure out which each sprite what do do
    all_sprites.update()
    pygame.display.update()
    
    # see if a football hits a Saban
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 10
        #dead_sound.play()
        #expl = Explosion(hit.rect.center)
        #all_sprites.add(expl)
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
    #see if a Saban hits the kirb
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= 20
        newmob()
        if player.shield <= 0:
            running = False
        
    # Draw / render
    screen.fill((20, 20, 20)) #this is a tuple
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 25, WIDTH / 2, 15)
    draw_shield_bar(screen, 10, 10, player.shield)

pygame.quit()
#main()


