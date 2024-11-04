"""Crear un programa (en Python ou C, prioridade Python) , chamado ''practica-1.py'' que a partires dun nome de host/nome de servizo/dirección IP/número de porto nos proporcione a información asociada. É dicir:

1 - Nome de host: debe indicar a información do host, empezando polo nome canónico e seguindo por todas as IPs (v4 y v6) asociadas (e en Python, o seu valor en binario ou hexadecimal, ao lado).

$ python3 practica-1.py -n www.google.es
****************************************************************
Nombre canónico: www.google.es
Dirección IPv4: 216.58.211.35 D83AD323
Dirección IPv6: 2a00:1450:4003:809::2003 2a001450400308090000000000002003
****************************************************************

2 - Nome de servizo: debe indicar o porto asociado ao servizo:

$ python3 practica-1.py -s ssh
****************************************************************
Servizo ssh: puerto 22
****************************************************************

3 - Dirección IP: debe indicar o nome de host asociado, aceptando tanto direccións en formato IPv4 como IPv6 (e en Python, o seu valor en binario, como hexadecimal, nunca en decimal, por exemplo C16E80C8 ou 2A001450400308090000000000002003, usar binascii.unhexlify() para pasar a binario o argumento de argv ou getopt, podedes usalo sempre e se da erro é porque igual é unha dirección en formato IPv4 ou IPv6, e facedes coma antes). Podedes usar o porto 80 para as funcións que requirades.

$ python3 practica-1.py -i 216.58.211.35
****************************************************************
Dirección IPv4 216.58.211.35: D83AD323 : host muc03s14-in-f3.1e100.net
****************************************************************
$ python3 practica-1.py -i 2a00:1450:4003:809::2003
****************************************************************
Dirección IPv6 2a00:1450:4003:809::2003: 2a001450400308090000000000002003 : host mad08s05-in-x03.1e100.net
****************************************************************
$ python3 practica-1.py -i D83AD323
****************************************************************
Dirección IPv4 216.58.211.35: D83AD323 : host muc03s14-in-f3.1e100.net
****************************************************************
$ python3 practica-1.py -i 2A001450400308090000000000002003
****************************************************************
Dirección IPv6 2a00:1450:4003:809::2003: 2a001450400308090000000000002003 : host mad08s05-in-x03.1e100.net
****************************************************************

4 - Número de porto: debe indicar o nome do servizo asociado

$ python3 practica-1.py -p 443
****************************************************************
Puerto 443: servicio https
****************************************************************

Debense permitir facer diferentes consultas nunha chamada:

$ python3 practica-1.py -n www.google.es -i 193.144.75.9 -s https -p 22
****************************************************************
Nome canónico: www.google.es
Dirección IPv4: 216.58.211.35 D83AD323
Dirección IPv6: 2a00:1450:4003:804::2003 2a001450400308090000000000002003
****************************************************************
Servicio https: puerto 443
****************************************************************
Dirección IPv4 193.144.75.9: host secus.usc.es
****************************************************************
Puerto 22: servicio ssh
****************************************************************


Requisitos
O non cumplimento de algun destes requisitos suporá unha penalización na nota da práctica.
1. Debense facer uso das funciones vistas na clase, en concreto, getaddrinfo y getnameinfo, xunto con funciones auxiliares como inet_ntop/inet_pton, etc.
2. Toda chamada a unha función do sistema debe ter o seu correspondente chequeo de erro.
3. Toda función debe sair coa mensaxe de erro e o código apropiado en caso de erro.
4. O código non pode fallar aínda que se usen datos de entrada incorrectos.
5. Toda memoria reservada dinámicamente debe liberarse correctamente (so C).
6. O código debe de estar adecuadamente estruturado, creando funcións diferentes para os diferentes apartados.
7. O código debe de estar adecuadamente comentado, indicándose de forma clara qué se fai en todas as funcións definidas, xunto coa explicación dos parámetros de entrada e saída das mesmas.
8. O código deberá estar correctamente formateado e tabulado.
9. O código debe compilar nun sistema Linux con gcc. Se se usa Windows, debese convertir o ficheiro co código a formato Unix.
10. Penalizarase que aparezcan mensaxes de Warning na compilación (coa opción -Wall) (so C)"""

import socket
import binascii
import argparse


# Función que obtiene el nombre del servicio asociado a un puerto.
def get_service_name(port: int) -> str:
    try:
        # Obtiene el nombre del servicio mediante el puerto
        service_name = socket.getservbyport(port)
        print("****************************************************************")
        print(f"Puerto {port}: servicio {service_name}")
        print("****************************************************************")
        return service_name
    except (OSError, socket.gaierror):
        return "Desconocido"


# Función que resuelve un nombre de host o dirección IP (IPv4 o IPv6).
def resolve_hostname(ip_input: str) -> str:
    """Resuelve el nombre de host dado una dirección IP o hexadecimal."""

    def is_hex(s: str) -> bool:
        """Verifica si una cadena es hexadecimal."""
        try:
            int(s, 16)
            return True
        except ValueError:
            return False

    def hex_to_ipv4(hex_str: str) -> str:
        """Convierte una dirección IPv4 en formato hexadecimal a decimal."""
        try:
            ip_bin = binascii.unhexlify(hex_str)
            return socket.inet_ntoa(ip_bin)
        except (binascii.Error, socket.error):
            return "Desconocido"

    def hex_to_ipv6(hex_str: str) -> str:
        """Convierte una dirección IPv6 en formato hexadecimal."""
        try:
            # Convierte la dirección hexadecimal en binario
            ip_bin = binascii.unhexlify(hex_str)
            return socket.inet_ntop(socket.AF_INET6, ip_bin)
        except (binascii.Error, socket.error):
            return "Desconocido"

    try:
        # Detectamos si la entrada es IPv4 o IPv6
        if (
            ":" in ip_input or "." in ip_input
        ):  # Si contiene ':' o '.' es una dirección IP, sino es hexadecimal
            hostname = socket.gethostbyaddr(ip_input)[0]
        elif is_hex(ip_input):
            if len(ip_input) == 8:  # IPv4 en hexadecimal tiene 8 caracteres
                ipv4_address = hex_to_ipv4(ip_input)
                if ipv4_address != "Desconocido":
                    hostname = socket.gethostbyaddr(ipv4_address)[0]
                else:
                    hostname = "Desconocido"
            elif len(ip_input) == 32:  # IPv6 en hexadecimal tiene 32 caracteres
                ipv6_address = hex_to_ipv6(ip_input)
                if ipv6_address != "Desconocido":
                    hostname = socket.gethostbyaddr(ipv6_address)[0]
                else:
                    hostname = "Desconocido"
            else:
                hostname = "Formato de dirección hexadecimal inválido"
        else:
            hostname = "Formato de entrada inválido"
    except (socket.herror, socket.gaierror):
        hostname = "Desconocido"

    return hostname


# Función principal que analiza y procesa los argumentos
def main():
    # Configuramos el parser de argumentos
    parser = argparse.ArgumentParser(description="Práctica 1 de Redes e Comunicacións")

    # Añadimos los diferentes argumentos posibles
    parser.add_argument(
        "-n",
        "--nome_host",
        type=str,
        dest="nome_host",
        action="store",
        help="Un nome de dirección de internet, coma www.usc.es",
    )

    parser.add_argument(
        "-s", "--servizo", type=str, help="Un nome de servizo, coma ssh"
    )

    parser.add_argument("-p", "--porto", type=int, help="Un número de porto, coma 22")

    parser.add_argument(
        "-i", "--ip", type=str, help="Unha ip, en IPv4, IPv6 ou hexadecimal"
    )

    args = parser.parse_args()

    # Procesamos el nombre de host
    if args.nome_host:
        print(f"Introduciuse un nome de host: {args.nome_host}")
        try:
            # Usamos getaddrinfo para obtener información del host
            info = socket.getaddrinfo(args.nome_host, None)
            print("****************************************************************")
            print(f"Nome canónico: {args.nome_host}")
            for res in info:
                ip = res[4][0]
                if ":" not in ip:  # Si es IPv4
                    hex_ip = (
                        binascii.hexlify(socket.inet_pton(socket.AF_INET, ip))
                        .decode()
                        .upper()
                    )
                    print(f"Dirección IPv4: {ip} {hex_ip}")
                else:  # Si es IPv6
                    hex_ip = (
                        binascii.hexlify(socket.inet_pton(socket.AF_INET6, ip))
                        .decode()
                        .upper()
                    )
                    print(f"Dirección IPv6: {ip} {hex_ip}")
            print("****************************************************************")
        except socket.gaierror as e:
            print(f"Erro resolvendo o host {args.nome_host}: {e}")

    # Procesamos el nombre de servicio
    if args.servizo:
        print(f"Introduciuse un nome de servizo: {args.servizo}")
        try:
            port = socket.getservbyname(args.servizo)
            print(f"Servizo {args.servizo}: puerto {port}")
        except OSError as e:
            print(f"Erro atopando o servizo {args.servizo}: {e}")

    # Procesamos el número de puerto
    if args.porto:
        print(f"Introduciuse un número de porto: {args.porto}")
        get_service_name(args.porto)

    # Procesamos la dirección IP
    if args.ip:
        print(f"Introduciuse unha IP: {args.ip}")
        hostname = resolve_hostname(args.ip)
        print(f"Host asociado: {hostname}")


if __name__ == "__main__":
    main()
