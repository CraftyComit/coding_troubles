import pygame
from pygame.locals import *
import sys
import random
import time
vec = pygame.math.Vector2 #2 for two dimensional
blue = (0,54,92)
white = (255, 255, 255)
green = (0, 255, 0)
HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60
screen = 1
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        #self.image = pygame.image.load("character.png")
        self.surf = pygame.Surface((30, 30))
        self.surfs = pygame.Surface((30, 30))
        self.surf.fill((150,150,150))
        self.surfs.fill((250,0,0))
        self.rect = self.surf.get_rect()
        self.rect = self.surfs.get_rect()
   
        self.pos = vec((10, 360))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.jumping = False
 
    def move(self):
        self.acc = vec(0,0.5)
    
        pressed_keys = pygame.key.get_pressed()
                
        if pressed_keys[K_a]:
            self.acc.x = -ACC
        if pressed_keys[K_d]:
            self.acc.x = ACC
                 
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
         
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
             
        self.rect.midbottom = self.pos
 
    def jump(self, platforms): 
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
           self.jumping = True
           self.vel.y = -15
 
    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3
 
    def update(self, platforms):
        hits = pygame.sprite.spritecollide(self ,platforms, False)
        if self.vel.y > 0:        
            if hits:
                if self.pos.y < hits[0].rect.bottom:               
                    self.pos.y = hits[0].rect.top +1
                    self.vel.y = 0
                    self.jumping = False
 
 
class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((random.randint(50,100), 12))
        self.surf.fill((128,128,0))
        self.rect = self.surf.get_rect(center = (random.randint(0,WIDTH-10),
                                                 random.randint(0, HEIGHT-30)))
 
    def move(self):
        pass
def check(platform, groupies):
    if pygame.sprite.spritecollideany(platform,groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom) < 40) and (abs(platform.rect.bottom - entity.rect.top) < 40):
                return True
        C = False
 
def plat_gen(platforms, all_sprites):
    while len(platforms) < 6:
        width = random.randrange(50,100)
        p  = platform()      
        C = True
         
        while C:
             p = platform()
             p.rect.center = (random.randrange(0, WIDTH - width),
                              random.randrange(-50, 0))
             C = check(p, platforms)
        platforms.add(p)
        all_sprites.add(p)
 
def main():
    pygame.init()
    vec = pygame.math.Vector2 #2 for two dimensional
    blue = (0,54,92)
    white = (255, 255, 255)
    green = (0, 255, 0)
    HEIGHT = 450
    WIDTH = 400
    ACC = 0.5
    FRIC = -0.12
    FPS = 60
    screen = 1
    pressed_keys = pygame.key.get_pressed()
    font = pygame.font.Font('freesansbold.ttf', 22)
    text = font.render('YOU DIED', True, green, blue)
    textRect = text.get_rect()
    ont = pygame.font.Font('freesansbold.ttf', 32)
    ext = font.render('press j to restart', True, green, blue)
    extRect = text.get_rect()
    fon = pygame.font.Font('freesansbold.ttf', 32)
    tex = font.render('From LB programing studios', True, green, blue)
    tet = font.render('press space to play', True, green, blue)
    textRet = text.get_rect()
    textRet.center = (WIDTH // 2.7, HEIGHT // 2)
    textRec = text.get_rect()
    textRec.center = (WIDTH // 4.5, HEIGHT // 2)
    FramePerSec = pygame.time.Clock()
    #button_surface = pygame.surface((100, 30))
    # button_text = font.render("click me", True, (0,0,0))
    displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("programming torture")
    if screen == 1:
        displaysurface.fill((0,54,92))
        displaysurface.blit(tex, textRec)
        pygame.display.update()
        time.sleep(2)
        screen = 4
    if screen == 4:
        displaysurface.fill((0,54,92))
        displaysurface.blit(tet, textRet)
        pygame.display.update()
        time.sleep(2)


        pygame.init()
    textRect.center = (WIDTH // 2, HEIGHT // 2)
    extRect.center = (WIDTH // 2.5, HEIGHT // 1.75)

    PT1 = platform()
    P1 = Player()
    
    PT1.surf = pygame.Surface((WIDTH, 20))
    PT1.surf.fill((0,0,0))
    PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))
    
    all_sprites = pygame.sprite.Group()
    all_sprites.add(PT1)
    all_sprites.add(P1)
    
    platforms = pygame.sprite.Group()
    platforms.add(PT1)
    
    for x in range(random.randint(4,5)):
        C = True
        pl = platform()
        while C:
            pl = platform()
            C = check(pl, platforms)
        platforms.add(pl)
        all_sprites.add(pl)
 
    while True:
        P1.update(platforms)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:    
                if event.key == pygame.K_w:
                    P1.jump(platforms)
            if event.type == pygame.KEYUP:    
                if event.key == pygame.K_w:
                    P1.cancel_jump()  
    
        if P1.rect.top <= HEIGHT / 3:
            P1.pos.y += abs(P1.vel.y)
            for plat in platforms:
                plat.rect.y += abs(P1.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
        if P1.rect.top > HEIGHT:
            for entity in all_sprites:
                entity.kill()
            displaysurface.fill((0,54,92))
            pygame.display.update()
            screen = 3
            displaysurface.blit(text, textRect)
            displaysurface.blit(ext, extRect)
            pygame.display.update()
            time.sleep(0.25)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN: 
                        if event.key == pygame.K_j:
                            main()
                        elif event.key == pygame.K_q:        
                            pygame.quit()
                            sys.exit()
                

        plat_gen(platforms,all_sprites)
        displaysurface.fill((0,64,92))
        
        for entity in all_sprites:
            displaysurface.blit(entity.surf, entity.rect)
            entity.move()
    
        pygame.display.update()
        FramePerSec.tick(FPS)

if __name__ == "__main__":
    main()