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

import socket
import sys
import argparse
import struct


def recv_all(socket: socket.socket, tamano: int) -> bytes:
    data = b""  # Inicializar data a un byte vacío
    while len(data) < tamano:  # Mientras no se haya recibido el tamaño completo
        paquete = socket.recv(tamano - len(data))  # Recibir el tamaño restante de datos
        if not paquete:  # Si no se recibe nada la conexión está rota
            raise RuntimeError("Conexión rota")
        data += paquete  # Añadir el paquete recibido a los datos
    return data  # Devolver los datos recibidos, en formato bytes


def recv_all_with_size(socket: socket.socket) -> str:
    # Primero recibimos los 4 bytes que contienen el tamaño del mensaje
    size_data = recv_all(socket, 4)
    size = struct.unpack("!I", size_data)[0]
    """struct.unpack('!I', size_data): Este comando convierte los 4 bytes que se recibieron en un número entero.
    '!I' es un formato utilizado por la biblioteca struct para desempaquetar datos binarios:
        '!': Indica que los datos están en formato big-endian (es decir, el byte más significativo viene primero). El formato de bytes en TCP/IP suele ser big-endian.
        'I': Significa que estamos desempaquetando un entero de 4 bytes sin signo (unsigned int), que es el formato estándar para representar el tamaño de los datos en muchos protocolos.
    size_data: Es el conjunto de 4 bytes que acabamos de recibir y que queremos convertir en un número entero.
    [0]: Como struct.unpack() devuelve una tupla, se usa [0] para acceder al primer (y único) elemento de la tupla, que es el número entero que representa el tamaño de los datos que estamos por recibir.
    """
    return recv_all(
        socket, size
    ).decode()  # Devolver los datos recibidos, en formato texto


def cliente():
    s = None
    parser = argparse.ArgumentParser(
        description="Cliente TCP: [IP y puerto del servidor]"
    )
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
        mensaje = recv_all_with_size(s)
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
