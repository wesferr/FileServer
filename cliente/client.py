#!/usr/bin/python3

#   Authors: Wesley Ferreira de Ferreira and Willian Ferreira de Ferreira
#   Date: 6/9/2018
#   All Rights Reserved
#   V0.1

import sys, socket
from treatment.mycrypt import key_exchange
from Crypto.Random.random import getrandbits
import treatment.request as req
import treatment.respose as resp

msg_inicio = \
"\
Como usar:\n\
    <comando> <nome_do_arquivo>z\n\
    Comandos: GET, POST, DELETE\n\
        GET: baixa arquivo do servidor\n\
        POST: envia arquivo para o servidor\n\
        DELETE: deleta um arquivo enviado para o servidor\n\
        EXIT(Não precisa de arquivo): sair do programa*\n"

def main():

    #VALIDA SE O USR PASSOU INDETEÇO E PORTA
    if(len(sys.argv) < 3):
        print("Porfavor execute como: ./client.py <ip_do_servido> <numero_da_porta>")
        exit()

    #DEFINE OS PARAMETROS DE CONEXÃO
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    DESTINATION = (HOST, PORT)

    #INICIA A CONEXÃO
    try:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect(DESTINATION)
    except:
        print("Problema com conexão, verifique as informações e tente novamente.")
        exit()

    #MOSTRA INSTRUÇOES DE INICIO DO PROGRAMA
    print(msg_inicio)

    #DEFINE O CLIENTID
    clientid = getrandbits(31)

    #DIFFIE HELMAN
    secrete_key = key_exchange(connection)
    print("Troca de chaves concluida")

    while True:
        msg = input("digite o comando: ").split()
        if(msg[0] == "EXIT"):
            connection.close()
            exit()
        try:
            result = req.gera_requisicao(msg[0], secrete_key, connection, msg[1], clientid)
            if(result):
                resp.recebe_resposta(secrete_key, connection, msg[0])
        except:
            print("Comando invalido, tente assim")
            print("<comando> <nome_do_arquivo>\nComandos: GET, POST, DELETE, EXIT\n")


if __name__ == "__main__":
    main()
