""" 
Obxectivo da práctica
Crear un programa servidor e un programa cliente en TCP e entender o seu funcionamento.

1. Cliente/servidor básicos. Sigue os pasos do documento adxunto para crear unha conexión TCP cliente/servidor na que o servidor envíe unha mensaxe de saudo ao cliente. Usar buffers de recepción e envío de 1024. Recoméndase probar que todo funciona en diferentes computadores.

i.-Programa servidor TCP:

    Debe escoitar por todas as suas interfaces usando un número de porto indicado como parámetro na liña de comandos (ver exemplo_argv.py da P1).
    Debe poder atender múltiples conexións SECUENCIAIS de clientes (non á vez).
    Para cada cliente que se conecte, debe imprimir en pantalla a IP do cliente e enviarlle unha mensaxe de saudo (unha cadena de polo menos 20 caracteres), despois pechar a conexión. Chamade ao programa ''servidor-11.py''.

ii.- Facer un programa cliente TCP:

    Debe permitir indicar a IP e o porto do servidor como parámetros na liña de comandos (ver exemplo_argv.py da P1).
    Debese conectar ao servidor e recibir a mensaxe do mesmo.
    Debe imprimir a mensaxe recibida e o número de bytes que se recibiron, despois pechar a conexión. Chamade ao programa ''cliente-11.py''.

iii.- Comproba se e posíbel que o servidor envíe dúas mensaxes con sendas funcións send() e que o cliente reciba (despois dun tempo prudencial, usar a función sleep()) ambas mensaxes cunha única sentencia recv(). Describe as modificacións introducidas nos códigos e o resultado obtido (número de bytes recibidos e a mensaxe).

iv.- Proba a usar no cliente un bucle de tipo  while len(mensaxe_recibida) > 0: e cambiar o seu buffer de recepción a 8. Describe as modificacións introducidas nos códigos e o resultado obtido. (En python igual é máis sinxelo usar while(true) e if len(mensaxe_recibida) == 0: break;)

Requisitos mínimos:
Os programas poden programarse en C ou Python. Se se fai todo en Python (o recomendado).

Débese facer uso das funcións vistas na clase.
Toda chamada a unha función do sistema debe ter o seu correspondente chequeo de erro.
Toda función debe sair co mensaxe de erro e o código apropiado en caso de erro (se o hai).
O código non pode fallar aínda qu se usen datos de entrada incorrectos.
Toda memoria reservada dinámicamente debe liberarse correctamente (so para C).
O código debe de estar adecuadamente comentado,  indicándose de forma clara qué se fai en todas as funcións definidas, xunto coa explicación dos parámetros de entrada e saída das mesmas.
O código deberá estar correctamente formateado e tabulado.
O código debe compilar nun sistema Linux con gcc (para C). Se se usa Windows, débese convertir o ficheiro co código a formato Unix.
Os programas deben funcionar aínda que o cliente e o servidor se executen en computadores diferentes
Os parámetros de entrada necesarios deben ser proporcionados como argumentos do main.
Penalizarase que aparezan mensaxes de Warning na compilación (coa opción -Wall)(so C)

Entrega. Un arquivo comprimido zip con:
- Os códigos (non os executables) dos puntos 1.1 (servidor básico), 1.2 (cliente básico) e 2 (servidor e cliente de maiúsculas, punto 2.6, se non se ten feito vale o 2.5).
- Informe sobre os puntos 1.3 e 1.4. Chamadeo ''informe.txt''
- (Non obrigatorio) Unha captura de pantalla na que se poida ver que o cliente e servidor de maiúsculas se están executando en distinto ordenador (ou máquina virtual). """

import socket  # Para manejar la comunicación en red
import argparse  # Para gestionar argumentos de entrada
import struct  # Para empaquetar y desempaquetar datos


def send_all(
    sock: socket.socket, data: bytes
):  # Función para enviar todos los datos, segmentando el tamaño de cada send en paquetes de 1024 bytes. Si alguno de los envíos falla se vuelve a intentar.
    total_sent = 0
    while total_sent < len(data):
        sent = sock.send(data[total_sent :: total_sent + 1024], 1024)
        if sent == 0:
            raise RuntimeError("send failed")
        total_sent += sent


def send_with_size(
    sock: socket.socket, data: str
):  # Función para enviar datos con un tamaño previo
    # Empaquetamos el tamaño del mensaje en 4 bytes (entero sin signo)
    size = struct.pack("!I", len(data))
    # Primero enviamos el tamaño, luego los datos
    send_all(sock, size)
    send_all(sock, data.encode())


def servidor(args: argparse.Namespace):
    s = None  # Inicializar s a None
    try:
        # Se crea un socket TCP: family=AF_INET (IPv4), type=SOCK_STREAM (orientado a la conexión (TCP))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Obtener la IP local
        hostname = socket.gethostname()  # Obtiene el nombre del host
        ip_local = socket.gethostbyname(
            hostname
        )  # Obtiene la IP local a partir del nombre del host
        print(f"IP local do servidor: {ip_local}")
        # Se enlaza el socket al puerto de escucha
        s.bind(("", args.port))  # Se enlaza a todas las interfaces (dirección IP vacía)
        # Se pone el servidor a escuchar conexiones
        s.listen(
            5
        )  # Se permite hasta 5 conexiones en espera, son secuenciales por defecto
        print("Servidor TCP listo y esperando conexiones en el puerto", args.port)

        while True:
            try:
                # Se acepta una conexión
                conn, addr = (
                    s.accept()
                )  # conn es el socket conectado al cliente, addr es la dirección del cliente
                print("Conexión aceptada de", addr)

                # Se envía un mensaje de saludo al cliente
                mensaje1 = "¡Bienvenido al servidor TCP! Soy un servidor de prueba. Primero envío este mensaje."
                mensaje2 = "Y ahora envío un segundo mensaje."

                conn.send(mensaje1.encode())
                conn.send(mensaje2.encode())

                # Se cierra la conexión con el cliente una vez que la comunicacion ha finalizado.
                conn.close()
                print("Conexión cerrada con", addr)

            except socket.error as e:
                # Manejo de errores de socket: DEVUELVE UNA TUPLA (errno, strerror)
                print("Error en la conexión con el cliente:", e)

            except KeyboardInterrupt:
                print("Servidor TCP finalizado por el usuario")
                break  # Sale del bucle en caso de interrupción del teclado

            except Exception as e:
                # Captura de otros errores inesperados
                print("Error inesperado:", e)
                break  # Puede ser útil salir del bucle en caso de error crítico

    except OSError as e:
        # Manejo de errores al crear el socket o enlazarlo OSError determina el tipo de error en el sistema operativo (errno, strerror)
        """Listado de mensajes de OSError:
        [Errno 98] Address already in use: El puerto ya está en uso
        [Errno 99] Cannot assign requested address: La dirección no es válida en este host
        """
        print(
            f"Error de sistema: {e}. Asegúrate de que el puerto {args.port} está disponible."
        )

    except Exception as e:
        # Captura de otros errores en la inicialización
        print("Error al iniciar el servidor:", e)

    finally:  # Se ejecuta siempre, haya o no errores
        if s is not None:
            try:
                s.close()  # Asegúrate de cerrar el socket al final
                print("Socket del servidor cerrado.")
            except NameError:
                # Si el socket nunca fue creado, esto evitará un error
                print("Socket no fue creado, no se puede cerrar.")


if __name__ == "__main__":
    # Primero se crea un analizador de argumentos: el servidor TCP acepta un argumento de línea de comandos, el puerto de escucha, que es un número entero
    parser = argparse.ArgumentParser(description="Servidor TCP")
    parser.add_argument(
        "-p", "--port", type=int, help="Puerto de escucha", dest="port", action="store"
    )
    parser.set_defaults(port=12345)  # Si no se especifica el puerto, se usará el 12345
    args = parser.parse_args()
    servidor(args=args)
