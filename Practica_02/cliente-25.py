""" 
2. Servidor de maiúsculas.
v.- Facer un programa servidor e un programa cliente no que o cliente lea un arquivo de texto de entrada (pasándolle o nome en liña de comandos), e se llo envíe liña a liña ao servidor usando a mesma conexión. O servidor debe pasar os caracteres de cada liña a maiúsculas e devolverlle ao cliente as liñas convertidas (ver función toupper() en C e upper() en Python). Chamade aos programas ''cliente-25.py'' e ''servidor-25.py''. Por último, o cliente vai recibindo as liñas e as vai escribindo nun arquivo de saída, que debe ter o mesmo nome que o arquivo de entrada pero engadindolle a terminación 'CAP', e ser igual ao arquivo orixinal pero coas letras en maiúsculas. O funcionamento debe ser o seguinte: unha vez establecida a conexión:

a.- o cliente le unha liña do arquivo de entrada e se lla envía ao servidor (imprimir por pantalla o número de bytes enviados)
b.- o servidor devolve a liña ao cliente pasada a maiúsculas (imprimir por pantalla o número de bytes recibidos e enviados)
c.- o cliente a escribe no arquivo de saída (imprimir por pantalla o número de bytes recibidos)
d.- de volta ao paso a, ata que se termine o arquivo.

Ademáis, o servidor debe aceptar como parámetro de entrada o número de porto polo que atende as solicitudes e o cliente a IP e porto do servidor ademáis do nome do ficheiro de entrada. Usade buffers de 1024

vi.- Cambiade os buffers de recepción a 10 e 20 (para ques sexan diferentes no servidor e cliente). Segue funcionando ben? Modificade o programa para que funcione corectamente con buffers pequenos e diferentes (unha solución é usando socket.shutdow(), e xa non ten porque ser liña a liña). Chamade aos programas ''cliente-26.py'' e ''servidor-26.py''.


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
- (Non obrigatorio) Unha captura de pantalla na que se poida ver que o cliente e servidor de maiúsculas se están executando en distinto ordenador (ou máquina virtual).
"""

import socket
import sys
import argparse


def recv_all(socket: socket.socket, tamano: int) -> bytes:
    data = b""  # Inicializar data a un byte vacío
    while len(data) < tamano:  # Mientras no se haya recibido el tamaño completo
        paquete = socket.recv(tamano - len(data))  # Recibir el tamaño restante de datos
        if not paquete:  # Si no se recibe nada, la conexión está rota
            raise RuntimeError("Conexión rota")
        data += paquete  # Añadir el paquete recibido a los datos
    return data  # Devolver los datos recibidos, en formato bytes


def cliente():
    s = None
    parser = argparse.ArgumentParser(
        description="Cliente para enviar archivo y recibir en mayúsculas del servidor"
    )
    parser.add_argument(
        "-i",
        "--ip",
        type=str,
        dest="ip",
        action="store",
        help="Dirección IP del servidor",
        default="127.0.0.1",
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
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        dest="file",
        action="store",
        help="Archivo de texto de entrada",
        default="archivo.txt",
    )
    args = parser.parse_args()

    # Confirmación de argumentos ingresados
    print("IP del servidor:", args.ip)
    print("Puerto del servidor:", args.porto)
    print("Archivo de entrada:", args.file)

    try:
        # Cargar contenido del archivo
        with open(args.file, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()
    except FileNotFoundError:
        print(f"Error: El archivo '{args.file}' no se encontró.")
        sys.exit(1)

    # Crear el socket TCP
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((args.ip, args.porto))
        print(f"Conectado al servidor {args.ip}:{args.porto}")
    except socket.error as e:
        print(f"Error en la conexión: {e}")
        if s:
            s.close()
        sys.exit(1)

    # Preparar el archivo de salida
    archivo_salida = args.file + ".CAP"
    with open(archivo_salida, "w", encoding="utf-8") as salida:
        for linea in lineas:
            mensaje = linea.strip()
            print(f"Enviando mensaje: {mensaje} ({len(mensaje.encode('utf-8'))} bytes)")
            s.sendall(mensaje.encode("utf-8"))

            # Recibir respuesta del servidor
            respuesta = s.recv(1024).decode("utf-8")
            print(
                f"Mensaje recibido del servidor: {respuesta} ({len(respuesta.encode('utf-8'))} bytes)"
            )

            # Escribir la respuesta en el archivo de salida
            salida.write(respuesta + "\n")

    print("Cerrando conexión con el servidor.")
    s.close()


if __name__ == "__main__":
    cliente()