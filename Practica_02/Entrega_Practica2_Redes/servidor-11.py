import socket
import sys
import argparse
import time

# Crear el parser de argumentos
parser = argparse.ArgumentParser(description="Script para obtener información de host, servicio, IP o puerto.")
parser.add_argument('-p', '--port', type=int, help='Número de puerto para obtener el nombre del servicio asociado')
args = parser.parse_args()

# Procesar el argumento -p (Número de puerto)
puerto = args.port if args.port else 1024

try:
    # Crear el socket TCP
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as e:
    print(f"Error al crear el socket: {e}")
    sys.exit(1)

# Dirección IP y puerto a usar
direccion_ip = '0.0.0.0'  # Escuchar en todas las interfaces

try:
    # Asignar dirección IP y puerto al socket
    servidor_socket.bind((direccion_ip, puerto))
except socket.error as e:
    print(f"Error al asignar dirección y puerto: {e}")
    servidor_socket.close()
    sys.exit(1)

print(f"Servidor escuchando en {direccion_ip}:{puerto}...")

try:
    # Comenzar a escuchar conexiones
    servidor_socket.listen(5)
except socket.error as e:
    print(f"Error al iniciar escucha de conexiones: {e}")
    servidor_socket.close()
    sys.exit(1)

contador = 1

while contador < 5:
    try:
        # Aceptar conexiones entrantes
        print("Esperando una nueva conexión...")
        conn, address = servidor_socket.accept()  # Bloquea hasta que un cliente se conecte
        print(f"Conexión aceptada de {address[0]}:{address[1]}")
        
        # Enviar el primer mensaje
        mensaje1 = "Hola, cliente! Este es el primer mensaje.".encode('utf-8')
        conn.send(mensaje1)
        time.sleep(2)  # Esperar 2 segundos antes de enviar el segundo mensaje

        # Enviar el segundo mensaje
        mensaje2 = "Este es el segundo mensaje.".encode('utf-8')
        conn.send(mensaje2)
    except socket.error as e:
        print(f"Error durante la conexión con el cliente: {e}")
    finally:
        # Cerrar conexión con el cliente
        conn.close()
        print("Conexión cerrada.")
        print(f"Clientes atendidos hasta ahora: {contador}\n")

    contador += 1

print("Vamos a cerrar la conexión del servidor.")
servidor_socket.close()
