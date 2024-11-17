import pygame
import sys
from constantes import *

# Inicializar Pygame y la ventana gráfica
pygame.init()
pygame.display.set_caption("David es Gay")
window = pygame.display.set_mode((WIDTH, HEIGHT))

def escalar_img(imagen, escala):
    w = imagen.get_width()
    h = imagen.get_height()
    nueva_imagen = pygame.transform.scale(imagen, (w * escala, h * escala))
    return nueva_imagen

def crear_boton_jugar():
    font = pygame.font.SysFont(None, 55)
    texto = font.render('JUGAR', True, (255, 255, 255))
    rect_texto = texto.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    return texto, rect_texto

def crear_boton_salir():
    font = pygame.font.SysFont(None, 55)
    texto = font.render('SALIR', True, (255, 0, 0))
    rect_texto = texto.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
    return texto, rect_texto

def mostrar_interfaz():
    run_interfaz = True
    boton_jugar, rect_boton = crear_boton_jugar()
    boton_salir, rect_boton_salir = crear_boton_salir()

    imagen_fondo_interfaz = pygame.image.load("assets/imagenes/background.jpg")
    imagen_fondo_interfaz = escalar_img(imagen_fondo_interfaz, 1.5)
    fondo_y = 0
    velocidad_fondo = 1

    while run_interfaz:
        window.fill((0, 0, 0))

        fondo_y += velocidad_fondo
        if fondo_y >= imagen_fondo_interfaz.get_height():
            fondo_y = 0

        window.blit(imagen_fondo_interfaz, (0, fondo_y - imagen_fondo_interfaz.get_height()))
        window.blit(imagen_fondo_interfaz, (0, fondo_y))

        window.blit(boton_jugar, rect_boton)
        window.blit(boton_salir, rect_boton_salir)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_interfaz = False  # Salir de la interfaz
                sys.exit()  # Finaliza el programa
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_boton.collidepoint(event.pos):
                    run_interfaz = False  # Salir de la interfaz para iniciar el juego
                if rect_boton_salir.collidepoint(event.pos):
                    run_interfaz = False  # Salir de la interfaz
                    sys.exit()  # Finaliza el programa

        pygame.display.update()

    pygame.quit()
