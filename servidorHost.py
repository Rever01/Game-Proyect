import socket
import pickle
import threading

# Configuración del servidor
HOST = '0.0.0.0'  
PORT = 5555
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))
servidor.listen()

# Lista para almacenar la posición, ángulo, estado, salud, nombre, balas y tipo de arma de los jugadores
jugadores = [None] * 5  # Inicializa la lista con espacios vacíos
conexiones = []
ids_nombres = {}  # Mapa de ID a nombre
id_counter = 0  # Contador para los IDs de jugadores
MAX_JUGADORES = 10  # Limitar el número de jugadores a 5

def inicializar_jugador(nombre_jugador, id_jugador):
    """Inicializa la información del jugador."""
    return (100 + id_jugador+1, 100 + id_jugador * 50, 0, True, 100, nombre_jugador, [], "pistola")

def recibir_datos(conexion):
    datos = b""
    while True:
        parte = conexion.recv(4096)
        if not parte:  # Si no se recibe más datos, se ha cerrado la conexión
            return None
        datos += parte
        if len(parte) < 4096:  # Si recibimos menos de lo esperado, podría significar que no hay más datos.
            break
    return pickle.loads(datos)

def manejar_cliente(conexion, jugador_id):
    global jugadores, conexiones, ids_nombres
    try:
        # Enviar las posiciones iniciales de todos los jugadores
        conexion.send(pickle.dumps(jugadores))

        while True:
            # Recibir datos del cliente (posición, ángulo, estado, salud, nombre, balas y tipo de arma)
            datos = recibir_datos(conexion)
            if datos is None:  # Si los datos son None, el cliente se ha desconectado
                print(f"Jugador {jugador_id} se ha desconectado.")
                break
            
            # Asegurarse de recibir 8 datos (incluyendo balas y tipo de arma)
            if len(datos) == 8:  # Verificamos que se reciban todos los datos
                pos_x, pos_y, angulo, activo, salud, nombre, balas, tipo_arma = datos
                jugadores[jugador_id] = (pos_x, pos_y, angulo, activo, salud, ids_nombres[jugador_id], balas, tipo_arma)  # Actualizar información del jugador

                # Enviar los datos de todos los jugadores a todos los clientes
                for conn in conexiones:
                    try:
                        conn.send(pickle.dumps(jugadores))
                    except (ConnectionResetError, BrokenPipeError):
                        print(f"Error al enviar datos al cliente: {conn}")
                        conexiones.remove(conn)  # Eliminar cliente de la lista si hay un error
            else:
                print(f"Datos incompletos recibidos del jugador {jugador_id}")

    except (pickle.UnpicklingError, EOFError):
        print(f"Error al deserializar datos del jugador {jugador_id}")
    except Exception as e:
        print(f"Error en el manejo del jugador {jugador_id}: {str(e)}")
    finally:
        # Eliminar al jugador de la lista
        if 0 <= jugador_id < MAX_JUGADORES and jugadores[jugador_id] is not None:
            nombre_jugador = ids_nombres[jugador_id]  # Usar el nombre del ID
            jugadores[jugador_id] = None  # Eliminar referencia al jugador
            del ids_nombres[jugador_id]  # Eliminar el nombre del jugador del mapa
            print(f"Jugador {nombre_jugador} ha sido eliminado del servidor.") 

        # Actualizar las conexiones
        if conexion in conexiones:
            conexiones.remove(conexion)
        
        # Notificar a los demás jugadores que un jugador se ha desconectado
        for conn in conexiones:
            try:
                conn.send(pickle.dumps(jugadores))
            except Exception as e:
                print(f"Error al enviar datos a la conexión: {str(e)}")
        
        conexion.close()  # Cerrar la conexión

def recibir_nombre_jugador(conexion):
    while True:
        conexion.send(pickle.dumps("Introduce tu nombre:"))
        nombre = pickle.loads(conexion.recv(1024))
        
        # Verificar si el nombre ya está en uso
        if nombre not in ids_nombres.values():
            return nombre
        else:
            conexion.send(pickle.dumps("Nombre ya en uso, elige otro nombre."))

# Ciclo para aceptar conexiones
print("Esperando jugadores...")
while True:
    try:
        conexion, addr = servidor.accept()

        if len(conexiones) < MAX_JUGADORES:  # Limitar a 5 jugadores
            print(f"Jugador conectado desde {addr}")

            # Recibir el nombre del jugador
            nombre_jugador = recibir_nombre_jugador(conexion)

            # Asignar el nuevo jugador a la lista
            for i in range(MAX_JUGADORES):
                if jugadores[i] is None:
                    # Guardar el nombre en el diccionario
                    ids_nombres[i] = nombre_jugador

                    # Inicializar el nuevo jugador
                    jugadores[i] = inicializar_jugador(nombre_jugador, i)
                    conexiones.append(conexion)

                    # Iniciar un nuevo hilo para manejar al cliente
                    threading.Thread(target=manejar_cliente, args=(conexion, i)).start()
                    break
        else:
            conexion.send(pickle.dumps("Servidor lleno. No puedes unirte."))
            conexion.close()
    except Exception as e:
        print(f"Error al aceptar la conexión: {str(e)}")
