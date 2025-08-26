import pygame
import sys

# dino_simple.py
# Juego tipo "dinosaurio" simplificado usando Pygame
# - El "dinosaurio" es un cuadro rojo que salta
# - Los obstáculos son rectángulos azules
# Controles: Espacio o Flecha ↑ para saltar. R para reiniciar cuando pierdes. ESC para salir.

import sys
import random
import pygame

# ---------------------------- Configuración básica ----------------------------
ANCHO = 800
ALTO = 400
SUELO_Y = 320         # línea del suelo
TAM_JUGADOR = 40      # tamaño del cuadro rojo
GRAVEDAD = 0.9
IMPULSO_SALTO = -16
VEL_INICIAL = 6
VEL_MAX = 17
AUMENTO_VEL_CADA = 8  # cada cuántos puntos sube la velocidad
FPS = 60

COLOR_FONDO = (245, 245, 245)
COLOR_SUELO = (200, 200, 200)
COLOR_JUGADOR = (220, 20, 60)   # rojo
COLOR_OBSTACULO = (30, 144, 255) # azul
COLOR_TEXTO = (20, 20, 20)

# Evento de temporizador para crear obstáculos
SPAWN_OBST = pygame.USEREVENT + 1

class Jugador:
    def __init__(self):
        self.rect = pygame.Rect(80, SUELO_Y - TAM_JUGADOR, TAM_JUGADOR, TAM_JUGADOR)
        self.vel_y = 0
        self.en_suelo = True

    def saltar(self):
        if self.en_suelo:
            self.vel_y = IMPULSO_SALTO
            self.en_suelo = False

    def actualizar(self):
        # aplicar gravedad
        self.vel_y += GRAVEDAD
        self.rect.y += int(self.vel_y)
        # limitar al suelo
        if self.rect.bottom >= SUELO_Y:
            self.rect.bottom = SUELO_Y
            self.vel_y = 0
            self.en_suelo = True

    def dibujar(self, surface):
        pygame.draw.rect(surface, COLOR_JUGADOR, self.rect, border_radius=6)

class Obstaculo:
    def __init__(self, x, ancho, alto):
        self.rect = pygame.Rect(x, SUELO_Y - alto, ancho, alto)

    def actualizar(self, vel):
        self.rect.x -= vel

    def fuera_de_pantalla(self):
        return self.rect.right < 0

    def dibujar(self, surface):
        pygame.draw.rect(surface, COLOR_OBSTACULO, self.rect, border_radius=3)

def crear_obstaculo():
    # alturas y anchos básicos para variar
    alto = random.choice([30, 45, 60, 75])
    ancho = random.choice([20, 26, 32, 44])
    x = ANCHO + random.randint(0, 80)
    return Obstaculo(x, ancho, alto)

def texto(surface, fuente, msg, x, y):
    img = fuente.render(msg, True, COLOR_TEXTO)
    surface.blit(img, (x, y))

def bucle_juego():
    pygame.init()
    pygame.display.set_caption("Cuadro Rojo vs Rectángulos Azules")
    screen = pygame.display.set_mode((ANCHO, ALTO))
    clock = pygame.time.Clock()
    fuente = pygame.font.SysFont(None, 32)
    fuente_grande = pygame.font.SysFont(None, 54)

    jugador = Jugador()
    obstaculos = []
    puntuacion = 0
    velocidad = VEL_INICIAL
    vivo = True

    # Temporizador: cada 1200–1700 ms aparece un obstáculo
    pygame.time.set_timer(SPAWN_OBST, random.randint(1200, 1700))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    if vivo:
                        jugador.saltar()
                    else:
                        # reiniciar con espacio/arriba
                        jugador = Jugador()
                        obstaculos.clear()
                        puntuacion = 0
                        velocidad = VEL_INICIAL
                        vivo = True
                        pygame.time.set_timer(SPAWN_OBST, random.randint(1200, 1700))
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r and not vivo:
                    # reiniciar con R
                    jugador = Jugador()
                    obstaculos.clear()
                    puntuacion = 0
                    velocidad = VEL_INICIAL
                    vivo = True
                    pygame.time.set_timer(SPAWN_OBST, random.randint(1200, 1700))
            if event.type == SPAWN_OBST and vivo:
                obstaculos.append(crear_obstaculo())
                # reprogramar el próximo spawn con leve aleatoriedad
                pygame.time.set_timer(SPAWN_OBST, random.randint(900, 1500))

        # Lógica del juego
        if vivo:
            jugador.actualizar()
            for obs in list(obstaculos):
                obs.actualizar(velocidad)
                if obs.fuera_de_pantalla():
                    obstaculos.remove(obs)
                    puntuacion += 1
                    # cada ciertos puntos aumenta un poco la velocidad
                    if puntuacion % AUMENTO_VEL_CADA == 0 and velocidad < VEL_MAX:
                        velocidad += 1

            # Colisiones
            for obs in obstaculos:
                if jugador.rect.colliderect(obs.rect):
                    vivo = False
                    break

        # Dibujo
        screen.fill(COLOR_FONDO)

        # suelo
        pygame.draw.line(screen, COLOR_SUELO, (0, SUELO_Y), (ANCHO, SUELO_Y), 3)

        # elementos
        for obs in obstaculos:
            obs.dibujar(screen)
        jugador.dibujar(screen)

        # UI
        texto(screen, fuente, f"Puntos: {puntuacion}", 16, 12)
        if not vivo:
            mensaje = "¡Perdiste! Pulsa R o Espacio para reiniciar."
            w = fuente.size(mensaje)[0]
            texto(screen, fuente, mensaje, (ANCHO - w)//2, 70)
            titulo = "Cuadro Rojo vs Rectángulos Azules"
            w2 = fuente_grande.size(titulo)[0]
            img = fuente_grande.render(titulo, True, COLOR_TEXTO)
            screen.blit(img, ((ANCHO - w2)//2, 22))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    bucle_juego()
