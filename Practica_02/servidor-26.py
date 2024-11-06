"""2. Servidor de maiúsculas.
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
- (Non obrigatorio) Unha captura de pantalla na que se poida ver que o cliente e servidor de maiúsculas se están executando en distinto ordenador (ou máquina virtual)."""

import socket
import sys
import argparse


def servidor(args: argparse.Namespace):
    # Procesar el argumento -p (Número de puerto)
    puerto = args.port if args.port else 1026

    # Crear el socket TCP
    try:
        servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print(f"Error al crear el socket: {e}")
        sys.exit(1)

    # Dirección IP y puerto a usar
    servidor_ip = "0.0.0.0"  # Escuchar en todas las interfaces

    # Asignar dirección IP y puerto al socket
    try:
        servidor_socket.bind((servidor_ip, puerto))
    except socket.error as e:
        print(f"Error al asignar la dirección y el puerto: {e}")
        servidor_socket.close()
        sys.exit(1)

    # Configurar el servidor para escuchar conexiones
    try:
        servidor_socket.listen(5)
        print(f"Servidor escuchando en {servidor_ip}:{puerto}...")
    except socket.error as e:
        print(f"Error al configurar el servidor para escuchar: {e}")
        servidor_socket.close()
        sys.exit(1)

    # Aceptar la conexión del cliente
    try:
        conn, address = servidor_socket.accept()
        print(f"Conexión aceptada de {address[0]}:{address[1]}")
    except socket.error as e:
        print(f"Error al aceptar la conexión del cliente: {e}")
        servidor_socket.close()
        sys.exit(1)

    texto = []

    # Recepción de datos y procesamiento
    while True:
        try:
            datos = conn.recv(20).decode()  # Buffer de recepción de 20 bytes
        except socket.error as e:
            print(f"Error al recibir datos: {e}")
            conn.close()
            servidor_socket.close()
            sys.exit(1)

        if not datos:  # Si no hay más datos, salir del bucle
            break

        # Convertir la línea a mayúsculas
        datos_mayus = datos.upper()
        texto.append(datos_mayus)
        print(
            f"Mensaje procesado: {datos_mayus} (Longitud: {len(datos_mayus.encode('utf-8'))} bytes)"
        )

        # Enviar respuesta al cliente
        try:
            conn.send(datos_mayus.encode("utf-8"))
        except socket.error as e:
            print(f"Error al enviar datos al cliente: {e}")
            conn.close()
            servidor_socket.close()
            sys.exit(1)

    # Cerrar la conexión
    print("Cerrando conexión servidor-25")
    try:
        conn.close()
        servidor_socket.close()
    except socket.error as e:
        print(f"Error al cerrar el socket: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Crear el parser de argumentos
    parser = argparse.ArgumentParser(description="Servidor de mayúsculas.")
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        help="Número de puerto para escuchar las conexiones del cliente.",
    )
    args = parser.parse_args()
    servidor(args=args)
