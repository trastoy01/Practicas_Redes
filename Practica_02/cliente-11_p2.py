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

import socket  # Importación de la librería socket para la comunicación por red
import sys
import argparse  # Importación de la librería argparse para el manejo de argumentos por línea de comandos
import struct  # Importación de la librería struct para el manejo de datos binarios
from time import (
    sleep,
)  # Importación de la función sleep de la librería time para pausar la ejecución del programa


def recv_all(sock: socket.socket, tamano: int) -> bytes:
    """Función que recibe una cantidad específica de datos de un socket

    Args:
        sock (socket.socket): Socket del que se recibirán los datos
        tamano (int): Cantidad de datos a recibir en bytes

    Returns:
        bytes: Datos recibidos en formato bytes
    """
    chunks = []  # Inicializar una lista para almacenar los trozos de datos
    bytes_recd = 0  # Inicializar el contador de bytes recibidos

    while bytes_recd < tamano:  # Mientras no se haya recibido el tamaño completo
        try:
            # Recibir el tamaño restante de datos, limitando a 2048 bytes
            chunk = sock.recv(min(tamano - bytes_recd, 2048))
            if chunk == b"":  # Si no se recibe nada, la conexión está rota
                raise RuntimeError("Conexión rota")
            chunks.append(chunk)  # Añadir el trozo recibido a la lista
            bytes_recd += len(chunk)  # Actualizar el contador de bytes recibidos
        except socket.error as e:  # Manejo de errores de socket
            print(f"Error al recibir datos: {e}")
            break  # Salir del bucle en caso de error

    return b"".join(chunks)  # Devolver todos los datos recibidos en formato bytes


def recv_all_with_size(sock: socket.socket) -> str:
    """Función que recibe un mensaje de un socket, primero recibiendo el tamaño del mensaje y luego el mensaje en sí

    Args:
        sock (socket.socket): Socket del que se recibirá el mensaje

    Returns:
        str: Mensaje recibido en formato texto
    """
    # Primero recibimos los 4 bytes que contienen el tamaño del mensaje
    size_data = recv_all(sock, 4)
    size = struct.unpack("!I", size_data)[0]
    """struct.unpack('!I', size_data): Este comando convierte los 4 bytes que se recibieron en un número entero.
    '!I' es un formato utilizado por la biblioteca struct para desempaquetar datos binarios:
        '!': Indica que los datos están en formato big-endian (es decir, el byte más significativo viene primero). El formato de bytes en TCP/IP suele ser big-endian.
        'I': Significa que estamos desempaquetando un entero de 4 bytes sin signo (unsigned int), que es el formato estándar para representar el tamaño de los datos en muchos protocolos.
    size_data: Es el conjunto de 4 bytes que acabamos de recibir y que queremos convertir en un número entero.
    [0]: Como struct.unpack() devuelve una tupla, se usa [0] para acceder al primer (y único) elemento de la tupla, que es el número entero que representa el tamaño de los datos que estamos por recibir.
    """
    return recv_all(
        sock, size
    ).decode()  # Devolver los datos recibidos, en formato texto


def cliente():
    s = None  # Inicializar el socket a None
    parser = argparse.ArgumentParser(
        description="Cliente TCP: [IP y puerto del servidor]"
    )
    # Añadir los argumentos de IP y puerto del servidor
    parser.add_argument(
        "-i",
        "--ip",
        type=str,
        dest="ip",
        action="store",
        help="IP del servidor",
        default="127.0.0.0",
    )
    parser.add_argument(
        "-p",
        "--porto",
        type=int,
        dest="porto",
        action="store",
        help="Puerto del servidor",
        default=1026,
    )
    args = parser.parse_args()
    if args.ip:
        print("Introduciuse unha ip ", args.ip)
    if args.porto:
        print("Introduciuse un número de porto: ", args.porto)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((args.ip, args.porto))
        print("Conexión establecida con el servidor")
        """
        iii.- Comproba se e posíbel que o servidor envíe dúas mensaxes con sendas funcións send() e que o cliente reciba (despois dun tempo prudencial, usar a función sleep()) ambas mensaxes cunha única sentencia recv(). Describe as modificacións introducidas nos códigos e o resultado obtido (número de bytes recibidos e a mensaxe).
        
        Se envían dos mensajes al cliente con send() y se reciben con una única llamada a recv() después de un tiempo prudencial, pues estos mensajes se envían de manera secuencial y se almacenan en el buffer de recepción del cliente: mientras el buffer cuente con un tamaño mayor o igual al de los mensajes enviados, estos se recibirán en una única llamada a recv(). Aún con esto no se garantiza que los mensajes se reciban juntos, pues el buffer de recepción puede ser vaciado en cualquier momento; ni en el orden en que se enviaron, pues el sistema operativo puede decidir en qué orden se reciben los mensajes. Es critico entonces ajustar el tamaño y frecuanecia de los mensajes enviados y recibidos para garantizar que se reciban juntos y en el orden correcto.
        
        iv.- Proba a usar no cliente un bucle de tipo  while len(mensaxe_recibida) > 0: e cambiar o seu buffer de recepción a 8. Describe as modificacións introducidas nos códigos e o resultado obtido. (En python igual é máis sinxelo usar while(true) e if len(mensaxe_recibida) == 0: break;)
        De esta manera se ejecuta el recv con un buffer de 8 bytes y se sale del bucle cuando se recibe un mensaje vacío. ::: esto se puede realizar de una manera mas ortodoxa con las funciones que se implemetan rcv_all_with_size y rcv_all
        while True:
            mensaje = s.recv(8)
            if len(mensaje) == 0:
                break
        """
        sleep(1)
        mensaje = s.recv(1024).decode()
        print("Mensaxe recibida: ", mensaje, " (", len(mensaje), " bytes)")
        s.close()
    except socket.error as e:
        print("Error en la conexión: ", e)
        if s:
            s.close()
        sys.exit(1)
    except KeyboardInterrupt:
        print("Saliendo del programa...")
        if s:
            s.close()
        sys.exit(1)
    except:
        print("Error inesperado: ", sys.exc_info()[0])
        if s:
            s.close()
        sys.exit(1)
    finally:
        if s:
            s.close()
        sys.exit(0)


if __name__ == "__main__":
    cliente()
