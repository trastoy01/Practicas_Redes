import sys
import socket
import argparse

# Crear el parser de argumentos
parser = argparse.ArgumentParser(description="Script para obtener información de host, servicio, IP o puerto.")
parser.add_argument('-p', '--port', type=int, help='Número de puerto para obtener el nombre del servicio asociado')
parser.add_argument('-i', '--ip', type=str, help='Dirección IP (IPv4 o IPv6) para obtener el nombre del host asociado')
args = parser.parse_args()

# Procesar el argumento -p (Número de puerto)
puerto = args.port if args.port else 1024
servidor_ip = args.ip if args.ip else '127.0.0.1'

# Crear el socket TCP del cliente
try:
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as e:
    print(f"Error al crear el socket: {e}")
    sys.exit(1)

# Conectarse al servidor
try:
    cliente_socket.connect((servidor_ip, puerto))
    print(f"Conectado al servidor {servidor_ip} en el puerto {puerto}.")
except ConnectionRefusedError:
    print("No se pudo conectar al servidor.")
    cliente_socket.close()
    sys.exit(1)
except socket.error as e:
    print(f"Error al intentar conectar al servidor: {e}")
    cliente_socket.close()
    sys.exit(1)

contador = 0

try:
    while True:
        # Recibir el mensaje de saludo del servidor
        mensaje = cliente_socket.recv(100)  # Tamaño del buffer para recibir datos
        if len(mensaje) == 0:
            print("El servidor cerró la conexión.")
            break
        else:
            print(f"Mensaje recibido: {mensaje.decode('utf-8')} (Longitud: {len(mensaje)} bytes)")
except socket.error as e:
    print(f"Error al recibir datos del servidor: {e}")
finally:
    # Cerrar la conexión
    print("Vamos a cerrar conexión cliente_11.")
    cliente_socket.close()
