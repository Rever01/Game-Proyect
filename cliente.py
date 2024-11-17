import socket
import pickle
import pygame
import math
from interfaz import mostrar_interfaz
from arma import Arma  
from bala import Bala, BalaPistola, BalaRifle, BalaEscopeta 
from jugador import Jugador 
from constantes import *

def juego():
    # Conectar al servidor
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(("26.249.69.40", 5555))

    # Recibir mensaje del servidor para ingresar nombre
    mensaje = pickle.loads(cliente.recv(1024))
    print(mensaje)
    nombre = input("Introduce tu nombre: ")
    cliente.send(pickle.dumps(nombre))  # Enviar el nombre al servidor

    # Recibir la lista de jugadores inicial
    jugadores = []
    try:
        jugadores_datos = pickle.loads(cliente.recv(4096))
        for datos_jugador in jugadores_datos:
            if datos_jugador:  # Asegúrate de que los datos del jugador no estén vacíos
                pos_x, pos_y, angulo, activo, salud, nombre, balas, tipo_arma = datos_jugador
                jugador = Jugador(pos_x, pos_y, angulo, activo, salud, nombre, id_jugador=len(jugadores))  
                
                # Asignar balas y arma al jugador
                jugador.balas = [
                    Bala(bala_x, bala_y, bala_angulo) for bala_x, bala_y, bala_angulo, _ in balas
                ]  # Asegúrate de que balas contenga la información correcta
                jugador.cambiar_arma(tipo_arma)  # Usar el método cambiar_arma
                
                jugadores.append(jugador)
    except (EOFError, pickle.UnpicklingError) as e:
        print(f"Error al recibir datos de jugadores: {e}")
        return  # Salir si no se pueden recibir datos

    # Inicializar Pygame
    pygame.init()

    # Configurar la ventana del juego
    pantalla = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Juego Multijugador")

    # Cargar las imágenes del jugador y fondo
    imagen_personaje = pygame.image.load("assets/imagenes/characters/Player/nave.png")
    imagen_personaje = pygame.transform.scale(imagen_personaje, (100, 100))

    fondo = pygame.image.load("assets/imagenes/characters/Player/Fondo.jpg")
    fondo = pygame.transform.scale(fondo, (2000, 2000))

    # Crear un reloj para controlar los FPS
    reloj = pygame.time.Clock()

    # Inicializar la cámara
    camera_x = 0
    camera_y = 0

    # Obtener jugador local
    jugador_id = len(jugadores) - 1
    jugador_local = jugadores[jugador_id]

    # Ciclo principal del juego
    jugando = True
    while jugando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:  # Click izquierdo
                jugador_local.disparar()  
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:  # Recargar
                    jugador_local.recargar()  
                if evento.key == pygame.K_1:  
                    jugador_local.cambiar_arma("pistola")
                if evento.key == pygame.K_2:  
                    jugador_local.cambiar_arma("rifle")
                if evento.key == pygame.K_3:  
                    jugador_local.cambiar_arma("escopeta")
            
        # Actualizar la posición del jugador y la cámara
        mouse_x, mouse_y = pygame.mouse.get_pos()
        delta_x = mouse_x + camera_x - jugador_local.pos_x
        delta_y = mouse_y + camera_y - jugador_local.pos_y
        jugador_local.angulo = (180 / math.pi) * -math.atan2(delta_y, delta_x)

        teclas = pygame.key.get_pressed()
        jugador_local.mover(teclas, 5)

        camera_x = max(0, min(jugador_local.pos_x - WIDTH // 2, fondo.get_width() - WIDTH))
        camera_y = max(0, min(jugador_local.pos_y - HEIGHT // 2, fondo.get_height() - HEIGHT))

        jugador_local.actualizar_balas()

        # Enviar datos al servidor
        if cliente:
            try:
                datos_jugador = (
                    jugador_local.pos_x, 
                    jugador_local.pos_y, 
                    jugador_local.angulo, 
                    True, 
                    jugador_local.salud, 
                    nombre,
                    [(bala.pos_x, bala.pos_y, bala.angulo, bala.tipo_bala) for bala in jugador_local.balas],  # Enviar tipo de bala
                    jugador_local.arma.tipo_arma  # Enviar tipo de arma
                )
                cliente.send(pickle.dumps(datos_jugador))
            except (BrokenPipeError, ConnectionResetError):
                print("Conexión con el servidor perdida.")
                jugando = False

        # Recibir datos del servidor
        try:
            jugadores_datos = pickle.loads(cliente.recv(4096))  
            jugadores = []
            for datos_jugador in jugadores_datos:
                if datos_jugador:  # Asegúrate de que los datos del jugador no estén vacíos
                    pos_x, pos_y, angulo, activo, salud, nombre, balas, tipo_arma = datos_jugador
                    jugador = Jugador(pos_x, pos_y, angulo, activo, salud, nombre, id_jugador=len(jugadores))
                    jugador.balas = [
                        Bala(bala_x, bala_y, bala_angulo, tipo_bala) for bala_x, bala_y, bala_angulo, tipo_bala in balas
                    ]  # Asegúrate de que el servidor envíe el tipo de bala
                    jugador.cambiar_arma(tipo_arma)
                    jugadores.append(jugador)
        except (EOFError, pickle.UnpicklingError) as e:
            print(f"Error al recibir datos de jugadores: {e}")
            jugando = False

        # Colisiones de balas
        for jugador in jugadores:
            for bala in jugador.balas[:]:
                # Verifica si la bala colisiona con el jugador local
                if bala.rect.colliderect(jugador_local.rect):
                    # Verifica que la bala no pertenezca al jugador local
                    if bala.id_jugador != jugador_local.id_jugador:
                        jugador_local.recibir_dano(10, bala.id_jugador)  # Pasa el ID del jugador que disparó
                        jugador.balas.remove(bala)
                        break
            
        # Dibujar jugadores y balas
        pantalla.fill(COLOR_BG)
        pantalla.blit(fondo, (-camera_x, -camera_y))
        for jugador in jugadores:
            jugador.dibujar(pantalla, camera_x, camera_y, imagen_personaje)

        pygame.display.update()
        reloj.tick(FPS)

    # Desconectar jugador
    if cliente:  # Asegúrate de que cliente esté definido
        try:
            cliente.send(pickle.dumps((0, 0, 0, False, jugador_local.salud, nombre)))  
        except Exception as e:
            print(f"Error al enviar datos de desconexión: {e}")

    pygame.quit()
    cliente.close()

mostrar_interfaz()
juego()
