import pygame
import sys

ANCHO, LARGO = 1080, 720

#setup
pygame.init()

screen = pygame.display.set_mode((ANCHO, LARGO))
pygame.display.set_caption("Demo")
clock  = pygame.time.Clock()

vec  = pygame.math.Vector2  #do dimensiones
DT   = 0
FRIC = -0.12
ACC  = 0.5

font = pygame.font.Font(None, 36)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill("red")
        self.rect = self.surf.get_rect()

        self.pos = vec((ANCHO//2, LARGO//2))
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def move(self):
        self.acc = vec(0, 0.5)
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_a]:
            self.acc.x = -ACC
        if pressed_keys[pygame.K_d]:
            self.acc.x = ACC
        
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > ANCHO:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = ANCHO

        self.rect.midbottom = self.pos

    def update(self):
        hits = pygame.sprite.spritecollide(P1, platforms, False)
        if P1.vel.y > 0:
            if hits:
                self.pos.y = hits[0].rect.top + 1
                self.vel.y = 0

    def jump(self):
        hits = pygame.sprite.spritecollide(P1, platforms, False)
        if hits:
            self.vel.y = -12


class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((200, 30))
        self.surf.fill("green")
        self.rect = self.surf.get_rect()
        
        self.pos = vec((ANCHO//2, LARGO))

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_LEFT]:
            self.pos.x -= 10
        if pressed_keys[pygame.K_RIGHT]:
            self.pos.x += 10

        self.rect.midbottom = self.pos

Pl1 = Platform()
P1 = Player()

all_sprites = pygame.sprite.Group()
all_sprites.add(Pl1)
all_sprites.add(P1)

platforms = pygame.sprite.Group()
platforms.add(Pl1)

while True:
    #eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #actualizar pantalla
    screen.fill("white")
    
    #renderizar el juego
    P1.move()
    P1.update()

    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_SPACE]:
        P1.jump()

    Pl1.move()

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)


    text = font.render(f"Pos player: {int(P1.pos.x)}, {int(P1.pos.y)}", True, (0, 0, 0))
    screen.blit(text, (10, 10))
    
    #flip() para actualizar algo
    pygame.display.flip()

    #limitar los PFS a 60
    #delta time, usado para el framerate
    pygame.display.update()
    clock.tick(60)