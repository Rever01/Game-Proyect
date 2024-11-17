
import pygame
import math
from abc import ABC, abstractmethod

fondo = pygame.image.load("assets/imagenes/characters/Player/nesto.png")
fondo = pygame.transform.scale(fondo, (2000, 2000))

import pygame
import math

class Bala:
    def __init__(self, x, y, angulo, id_jugador, velocidad=10, duracion=2000):
        self.pos_x = x
        self.pos_y = y
        self.angulo = angulo
        self.id_jugador = id_jugador
        self.velocidad = velocidad
        self.duracion = duracion
        self.creado = pygame.time.get_ticks()
        self.rect = pygame.Rect(x, y, 10, 10)

    @abstractmethod
    def mover(self):
        # Actualiza la posición de la bala
        self.pos_x += self.velocidad * math.cos(math.radians(self.angulo))
        self.pos_y -= self.velocidad * math.sin(math.radians(self.angulo))

        # Actualiza la hitbox de la bala
        self.rect.topleft = (self.pos_x, self.pos_y)

        # Verificar si la bala ha superado su duración
        if pygame.time.get_ticks() - self.creado > self.duracion:
            return False  # Indica que la bala debe ser eliminada

        # Eliminar bala si sale de los límites del mapa
        if (self.pos_x < 0 or self.pos_x > fondo.get_width() or
            self.pos_y < 0 or self.pos_y > fondo.get_height()):
            return False  # Indica que la bala debe ser eliminada

        return True  # La bala sigue activa

    @abstractmethod
    def dibujar(self, pantalla, camera_x, camera_y):
        # Dibuja la bala
        pygame.draw.circle(pantalla, (255, 0, 0), (int(self.pos_x - camera_x), int(self.pos_y - camera_y)), 5)

        # Opcional: Dibuja un borde para mejorar la visibilidad
        pygame.draw.circle(pantalla, (0, 0, 0), (int(self.pos_x - camera_x), int(self.pos_y - camera_y)), 6, 1)  # Borde negro


class BalaPistola(Bala):
     def __init__(self, x, y, angulo, id_jugador):
        super().__init__(x, y, angulo, id_jugador, velocidad=15, duracion=500)
        self.tipo_bala = "pistola"
        
class BalaRifle(Bala):
    def __init__(self, x, y, angulo, id_jugador):
        super().__init__(x, y, angulo, id_jugador, velocidad=25, duracion=1500)
        self.tipo_bala = "rifle"

class BalaEscopeta(Bala):
    def __init__(self, x, y, angulo, id_jugador):
        super().__init__(x, y, angulo, id_jugador, velocidad=10, duracion=2000)
        self.tipo_bala = "escopeta"

