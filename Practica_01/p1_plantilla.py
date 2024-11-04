import socket
import sys
import binascii
import time

# import getopt, sys #getopt úsase porque é similar ao de C, para Python pódese usar tamén argparse
import argparse


def main():
    # con isto preparamos para obter argumentos, a opción --help e -h créase automáticamente
    parser = argparse.ArgumentParser(description="Práctica 1 de Redes e Comunicacións")
    # con isto engadimos argumentos, pódense meter de 2 maneiras, opción curta (con guión) e longa (con dous guións)
    # con dest dámoslle un nome co que se gardará ao facer a función parse_args(), se non o poñemos o colle das opcións
    parser.add_argument(
        "-n",
        "--nome_host",
        type=str,
        dest="nome_host",
        action="store",
        help="Un nome de dirección de internet, coma www.usc.es",
    )  # a action='store' é o comportamnteto por defecto
    parser.add_argument("-s", "--servizo", type=str, help="Un nome de sevizo, coma ssh")
    parser.add_argument("-p", "--porto", type=int, help="Un numero de porto, coma 22")
    parser.add_argument(
        "-i", "--ip", type=str, help="Unha ip, en IPv4, IPv6 ou enteiro hexadecimal"
    )
    args = parser.parse_args()
    # print(args)

    if args.nome_host:
        print("Introduciuse un nome de host: ", args.nome_host)
    if args.servizo:
        print("Introduciuse un nome de servizo: ", args.servizo)
    if args.porto:
        print("Introduciuse un número de porto: ", args.porto)
    if args.ip:
        print("Introduciuse unha ip ", args.ip)
        try:  # aqui imos a intentar facer algo que igual da erro (non é un número hexadecimal válido)
            bin = binascii.unhexlify(args.ip)
            print("  É un valor en hexadecimal, en binario é: ", bin)
        except:  # se hai un erro execútase isto (será entón que é unha dirección textual)
            print("  É un valor en IPv4 ou IPv6")
        # except binascii.Error as e: #así é como se captura a mensaxe de erro, podedes ter varios 'except' para diferentes erros, e acabar cun baleiro como o anterior por si acaso
        # print('Non se pode convertir a binario: ', e)

if __name__ == "__main__":
    main()
