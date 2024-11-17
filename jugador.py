import pygame
import math
from pistola import Pistola
from rifle import Rifle
from bala import Bala
from constantes import *
import random
from escopeta import Escopeta
from bala import BalaPistola, BalaRifle, BalaEscopeta
# Cargar el fondo
fondo = pygame.image.load("assets/imagenes/characters/Player/nesto.png")
fondo = pygame.transform.scale(fondo, (2000, 2000))

class Jugador:
    def __init__(self, x, y, angulo, activo, salud, nombre, id_jugador, tipo_arma="pistola"):
        self.pos_x = x
        self.pos_y = y
        self.angulo = angulo
        self.activo = activo
        self.salud = salud
        self.nombre = nombre
        self.id_jugador = id_jugador
        self.ancho = 100
        self.alto = 100
        self.balas = []
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.ancho, self.alto)
       

        self.cambiar_arma(tipo_arma)  # Inicializar arma

    def cambiar_arma(self, tipo_arma):
        """Cambia el tipo de arma del jugador."""
        if tipo_arma.lower() == "pistola":
            self.arma = Pistola(self)
        elif tipo_arma.lower() == "rifle":
            self.arma = Rifle(self)
        elif tipo_arma.lower() == "escopeta":
            self.arma = Escopeta(self)
        else:
            self.arma = Pistola(self)  # Arma predeterminada

    def mover(self, teclas, velocidad):
        if teclas[pygame.K_w]:  # Arriba
            self.pos_y -= velocidad
        if teclas[pygame.K_s]:  # Abajo
            self.pos_y += velocidad
        if teclas[pygame.K_a]:  # Izquierda
            self.pos_x -= velocidad
        if teclas[pygame.K_d]:  # Derecha
            self.pos_x += velocidad

        # Restringir movimiento
        self.pos_x = max(0, min(self.pos_x, fondo.get_width() - self.ancho))
        self.pos_y = max(0, min(self.pos_y, fondo.get_height() - self.alto))

        # Actualizar el rect del jugador
        self.rect.topleft = (self.pos_x, self.pos_y)

        # Centrar el arma en el jugador
        self.arma.centrar_en_jugador(self)

    def disparar(self):
            dano = self.arma.disparar()  # Intentar disparar
            if dano > 0:  # Si se disparó exitosamente, crear una bala
                # Ajusta el offset según el tipo de arma y el ángulo
                offset_x = 70 * math.cos(math.radians(self.angulo))  
                offset_y = -70 * math.sin(math.radians(self.angulo))  
                
                # Crear una nueva bala según el tipo de arma
                if isinstance(self.arma, Pistola):
                    nueva_bala = BalaPistola(self.pos_x + self.ancho // 2 + offset_x, 
                                              self.pos_y + self.alto // 2 + offset_y, 
                                              self.angulo, self.id_jugador)
                elif isinstance(self.arma, Rifle):
                    nueva_bala = BalaRifle(self.pos_x + self.ancho // 2 + offset_x, 
                                            self.pos_y + self.alto // 2 + offset_y, 
                                            self.angulo, self.id_jugador)
                elif isinstance(self.arma, Escopeta):
                    nueva_bala = BalaEscopeta(self.pos_x + self.ancho // 2 + offset_x, 
                                               self.pos_y + self.alto // 2 + offset_y, 
                                               self.angulo, self.id_jugador)

                self.balas.append(nueva_bala)


    def recargar(self):
        self.arma.recargar()  # Llama al método de recarga del arma

    def actualizar_balas(self):
        # Mover las balas y eliminar las que han durado demasiado
        for bala in self.balas[:]:
            if not bala.mover():  # Mueve la bala y verifica si debe ser eliminada
                self.balas.remove(bala)

    def recibir_dano(self, dano, atacante_id):
        if self.id_jugador != atacante_id:  # Verifica que el atacante no sea el mismo jugador
            self.salud -= dano
            if self.salud <= 0:
                self.salud = 100  # Reinicia la salud
                self.pos_x = random.randint(0, fondo.get_width() - self.ancho)  # Nueva posición aleatoria
                self.pos_y = random.randint(0, fondo.get_height() - self.alto)  # Nueva posición aleatoria
                self.rect.topleft = (self.pos_x, self.pos_y)  # Actualiza la hitbox

    def dibujar(self, pantalla, camera_x, camera_y, imagen_personaje):
        if self.activo:
            # Rotar la imagen del personaje para su visualización
            imagen_rotada = pygame.transform.rotate(imagen_personaje, self.angulo)
            imagen_rect = imagen_rotada.get_rect(center=(self.pos_x - camera_x + self.ancho // 2, self.pos_y - camera_y + self.alto // 2))  # Centra la imagen

            # Dibuja la imagen rotada
            pantalla.blit(imagen_rotada, imagen_rect.topleft)

            # Actualiza la hitbox (rect) basándote en la posición original y el tamaño, sin depender de la rotación
            self.rect.topleft = (self.pos_x - camera_x, self.pos_y - camera_y)

            # Dibuja el arma
            self.arma.angulo = self.angulo  # Ajusta el ángulo del arma
            self.arma.centrar_en_jugador(self)  # Centra el arma en el jugador
            self.arma.dibujar(pantalla, camera_x, camera_y)

            # Dibujar la barra de salud
            self.dibujar_barra_salud(pantalla, camera_x, camera_y)

            # Dibujar la hitbox exacta del personaje sin depender de la rotación
            pygame.draw.rect(pantalla, (0, 255, 0, 128), self.rect, 2)  # Hitbox visible  

        # Dibujar las balas
        for bala in self.balas:
            bala.dibujar(pantalla, camera_x, camera_y)

    def dibujar_barra_salud(self, pantalla, camera_x, camera_y):
        ancho_barra = 50
        alto_barra = 5
        margen = 5
        salud_porcentaje = self.salud / 100

        # Calcular la posición de la barra de vida
        x_barra = self.pos_x - camera_x + (self.ancho - ancho_barra) // 2
        y_barra = self.pos_y - camera_y - 30 - margen - alto_barra

        # Dibujar la barra de vida
        pygame.draw.rect(pantalla, (255, 0, 0), (x_barra, y_barra, ancho_barra, alto_barra))  # Fondo rojo
        pygame.draw.rect(pantalla, (0, 255, 0), (x_barra, y_barra, ancho_barra * salud_porcentaje, alto_barra))  # Parte verde 
