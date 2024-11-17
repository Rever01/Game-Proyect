import pygame
from arma import Arma

class Pistola(Arma):
    def __init__(self, jugador, capacidad_municion=6, dano=10, cooldown_disparo=500):
        imagen = pygame.image.load("assets/imagenes/weapons/pistola.png")  # Cambia a la ruta correcta
        tamaño_deseado = (1, 1)  # Ancho y alto deseados
        imagen = pygame.transform.scale(imagen, tamaño_deseado)
        super().__init__(jugador, imagen)
        self.municion = capacidad_municion  # Capacidad de munición de la pistola
        self.dano = dano  # Daño por disparo
        self.cooldown_disparo = cooldown_disparo  # Cooldown entre disparos
        self.tiempo_ultimo_disparo = 0  # Inicializa el tiempo del último disparo

    def disparar(self):
        tiempo_actual = pygame.time.get_ticks()  # Obtener el tiempo actual
        # Verificar si ha pasado el cooldown
        if tiempo_actual - self.tiempo_ultimo_disparo >= self.cooldown_disparo:
            if self.municion > 0:
                self.municion -= 1  # Disminuir munición al disparar
                self.tiempo_ultimo_disparo = tiempo_actual  # Actualizar el tiempo del último disparo
                print("Disparo exitoso!")
                return self.dano
            else:
                print("¡Sin munición! Debes recargar.")
                return 0
        else:
            print("¡Cooldown activo! Espera para disparar.")
            return 0

    def recargar(self, cantidad=6):
        self.municion += cantidad
        if self.municion > 6:  # Asumiendo que la capacidad máxima es 6
            self.municion = 6
        print("Recargada! Munición actual:", self.municion)
