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
import time


def cliente(args: argparse.Namespace):

    # Parámetros de entrada con valores predeterminados
    cliente_ip = args.ip if args.ip else "127.0.0.1"
    puerto = args.port if args.port else 1026
    archivo_entrada = args.file if args.file else "archivo.txt"

    # Abrir el archivo de entrada en modo lectura
    try:
        with open(archivo_entrada, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
    except FileNotFoundError:
        print(f"Error: El archivo {archivo_entrada} no se encontró.")
        sys.exit(1)

    # Se eliminan los espacios en blanco al inicio y al final de cada frase
    frases = [frase.strip() for frase in contenido.split(".") if frase.strip()]

    # Imprimir la lista de frases
    print("Frases extraídas del archivo")
    # for i, frase in enumerate(frases, 1):
    # print(f"{i}: {frase}")

    # Crear el socket TCP del cliente
    try:
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print(f"Error al crear el socket: {e}")
        sys.exit(1)

    # Conectarse al servidor
    try:
        cliente_socket.connect((cliente_ip, puerto))
        print(f"Conectado al servidor {cliente_ip} en el puerto {puerto}.")
    except socket.error as e:
        print(f"Error: No se pudo conectar al servidor en {cliente_ip}:{puerto} - {e}")
        sys.exit(1)

    # Enviar las frases al servidor
    for frase in frases:
        frase_con_punto = frase + "."  # Agregar un punto al final de la frase
        try:
            print(
                f"Enviando frase: {frase_con_punto} (Longitud: {len(frase_con_punto.encode('utf-8'))} bytes)"
            )
            cliente_socket.send(frase_con_punto.encode("utf-8"))
        except socket.error as e:
            print(f"Error al enviar datos: {e}")
            cliente_socket.close()
            sys.exit(1)
        time.sleep(2)  # Esperar 2 segundos antes de enviar la siguiente

    # Usar shutdown para indicar que ya no se enviarán más datos
    try:
        cliente_socket.shutdown(socket.SHUT_WR)
    except socket.error as e:
        print(f"Error al cerrar la conexión de escritura: {e}")
        cliente_socket.close()
        sys.exit(1)

    # Recibir la respuesta del servidor

    texto = []
    while True:
        try:
            mensaje = cliente_socket.recv(
                10
            ).decode()  # Buffer de recepción de 1024 bytes
        except socket.error as e:
            print(f"Error al recibir datos: {e}")
            cliente_socket.close()
            sys.exit(1)
        if len(mensaje) == 0:
            print("El servidor cerró la conexión.")
            break
        else:
            # Imprimir el mensaje y su longitud en bytes
            texto.append(mensaje)
            print(
                f"Mensaje recibido del servidor: {mensaje} (Longitud: {len(mensaje.encode('utf-8'))} bytes)"
            )

    # Cerrar la conexión
    print("Cerrando conexión cliente-25")
    try:
        cliente_socket.close()
    except socket.error as e:
        print(f"Error al cerrar el socket: {e}")
        sys.exit(1)

    # Guardar la respuesta en un archivo de salida
    archivo_salida = "archivo.cap"
    contenido = ""
    for linea in texto:
        contenido += linea  # Concatenar cada línea

    frases = contenido.split(".")

    try:
        with open(archivo_salida, "w", encoding="utf-8") as archivo_out:
            for frase in frases:
                frase = (
                    frase.strip()
                )  # Eliminar espacios en blanco al inicio y al final
                if frase:  # Si la frase no está vacía
                    archivo_out.write(
                        frase.upper() + ".\n"
                    )  # Escribir en mayúsculas, con punto y salto de línea
    except IOError as e:
        print(f"Error al escribir en el archivo de salida: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Crear el parser de argumentos
    parser = argparse.ArgumentParser(
        description="Cliente para enviar archivo al servidor y recibir en mayúsculas."
    )
    parser.add_argument(
        "-i", "--ip", type=str, help="Dirección IP del servidor", required=False
    )
    parser.add_argument(
        "-p", "--port", type=int, help="Puerto del servidor", required=False
    )
    parser.add_argument(
        "-f", "--file", type=str, help="Archivo de texto de entrada", required=False
    )
    args = parser.parse_args()
    cliente(args)
