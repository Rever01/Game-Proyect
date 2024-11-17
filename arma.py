import pygame

class Arma:
    def __init__(self, jugador, imagen):
        self.imagen = imagen
        self.angulo = 0  # Ángulo de rotación del arma
        self.rect = self.imagen.get_rect(center=(jugador.pos_x + jugador.ancho // 2, jugador.pos_y + jugador.alto // 2))
        self.tipo_arma = self.__class__.__name__.lower()  # Asigna el nombre de la clase como tipo de arma

    def centrar_en_jugador(self, jugador):
        # Actualiza el centro del rect del arma para que esté centrado en el jugador
        self.rect.center = (jugador.pos_x + jugador.ancho // 2, jugador.pos_y + jugador.alto // 2)

    def dibujar(self, pantalla, camera_x, camera_y):
        # Dibuja el arma rotada en su posición centrada
        imagen_rotada = pygame.transform.rotate(self.imagen, self.angulo)
        nueva_rect = imagen_rotada.get_rect(center=self.rect.center)
        pantalla.blit(imagen_rotada, (nueva_rect.x - camera_x, nueva_rect.y - camera_y))

