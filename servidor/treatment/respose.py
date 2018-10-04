import hmac, os
from treatment.mycrypt import crypt, decrypt
from proto.men_size_pb2 import Men_size
from proto.respose_pb2 import Respose
from proto.request_pb2 import Request

def envia_resposta(secrete_key, msg, valid, source):

    #SE A ASSINATURA BATER
    if(valid):

        #PROCESSA O COMANDO DE GET
        if(msg.command == Request.GET):
            resp = get(msg, secrete_key,source)

        #PROCESSA O COMANDO DE POST
        if(msg.command == Request.POST):
            resp = post(msg, secrete_key, source)

        #PROCESSA O COMANDO DE DELETE
        if(msg.command == Request.DELETE):
            resp = delete(msg, secrete_key, source)

        #GERA A ASSINATURA DA MENSAGEM
        sign = gen_sign(resp, secrete_key)
        send_msg(resp, secrete_key, source)

        print("Resposta enviada ")

    else:
        print("Assinatura invalida, mensagem ignorada")


#METODO QUE PROCESSA UMA REQUISIÇÃO DE GET
def get(msg, secrete_key, connection, signature = bytes(), content = b"",
    serverInfo = "python_server", protocolVersion = "HTTP/1.1"):

    try:
        #CARREGA O ARQUIVO PARA MANDAR
        url = "./http/"
        if(msg.url == ""):
            msg.url = "index.html"
        url = url + msg.url
        file = open(url, "r")
        data = file.read()
        file.close()

        #GERA A RESPOSTA
        return Respose(status = Respose.OK, url = msg.url, signature=signature,
        content = crypt(secrete_key, data), serverInfo=serverInfo,
        protocolVersion=protocolVersion)

    except:
        #GERA A RESPOSTA
        return Respose(status = Respose.ERROR, url = msg.url, signature=signature,
        content = content, serverInfo=serverInfo,
        protocolVersion=protocolVersion)



#METODO QUE PROCESSA UMA REQUISIÇÃO DE POST
def post(msg, secrete_key, connection, signature = bytes(), content = b"",
    serverInfo = "python_server", protocolVersion = "HTTP/1.1"):

    try:
        #SALVA O ARQUIVO ENVIADO PELO CLIENTE
        try:
            os.mkdir(str(msg.clientId))
        except:
            pass

        file = open( "./" + str(msg.clientId) + "/" + msg.url, "w")
        file.write(decrypt(secrete_key, msg.content).decode())
        file.close()

        #GERA A RESPOSTA
        return Respose(status = Respose.OK, url = msg.url, signature=signature,
        content = content, serverInfo=serverInfo, protocolVersion=protocolVersion)
    except:
        return Respose(status = Respose.ERROR, url = msg.url, signature=signature,
        content = content, serverInfo=serverInfo, protocolVersion=protocolVersion)

#METODO QUE PROCESSA UMA REQUISIÇÃO DE DELETE
def delete(msg, secrete_key, connection, signature = bytes(), content = b"",
    serverInfo = "python_server", protocolVersion = "HTTP/1.1"):

    try:
        #GERA A RESPOSTA
        os.remove( "./" + str(msg.clientId) + "/" + msg.url)
        return Respose(status = Respose.OK, url = msg.url, signature=signature,
        content = content, serverInfo=serverInfo, protocolVersion=protocolVersion)

    except:
        return Respose(status = Respose.ERROR, url = msg.url, signature=signature, content = content, serverInfo=serverInfo, protocolVersion=protocolVersion)


#FUNÇÃO DE GERAÇÃO DA ASSINATURA
def gen_sign(resp, secrete_key):
    sign = hmac.HMAC(secrete_key.to_bytes(16, "big"))
    sign.update(resp.SerializeToString())
    sign = sign.digest()
    resp.signature = sign
    return sign

#FUNÇÃO QUE FAZ O ENVIO DA MENSAGEM PROCESSADA
def send_msg(resp, secrete_key, connection):
    # SEREALIZA A MENSAGEM E CALCULA O TAMANHO
    msg = resp.SerializeToString()
    men_size = Men_size(size=resp.ByteSize())

    #MANDA O TAMANHO E A MENSAGEM
    connection.send(men_size.SerializeToString())
    connection.send(msg)
