#!/usr/bin/python3

#   Authors: Wesley Ferreira de Ferreira and Willian Ferreira de Ferreira
#   Date: 6/9/2018
#   All Rights Reserved
#   V0.1

import sys, socket
from multiprocessing import Process
from treatment.mycrypt import key_exchange
from treatment.request import recebe_requisicao
from treatment.respose import envia_resposta

def recieve_message(source, cliente):
    print("connection from: {}".format(cliente))

    #DIFFIE-HELMAN
    secrete_key = key_exchange(source)
    print("Troca de chaves concluida")

    #FICA ESCUTANDO AS REQUISIÇÕES DO CLIENTE
    try:
        while True:
            msg, valid = recebe_requisicao(secrete_key, source)
            print("Requisição recebida de {}".format(cliente))
            envia_resposta(secrete_key, msg, valid, source)
    except:
        print("Conexão encerrada")

    source.close()

def main():

    if(len(sys.argv) < 2):
        print("Porfavor execute como: ./server.py <numero da porta>")
        exit()

    #DEFINE OS PARAMETROS DE CONEXÃO
    HOST = ""
    PORT = int(sys.argv[1])
    ORIGIN = (HOST, PORT)

    #INICIA A CONEXÃO
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.bind(ORIGIN)
    connection.listen(5)


    #LOOP DE REQUISIÇÕES DO SERVIDOR
    while True:
        source, cliente = connection.accept()
        p = Process(target=recieve_message, args=(source, cliente)) #DISPARA O PROCESSO PRA A REQUISIÇÃO
        p.start() #INICIA A EXECUÇÃO

    connection.close() #FECHA A CONEXÃO

if __name__ == "__main__":
    main()
