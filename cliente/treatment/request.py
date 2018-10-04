import hmac
from treatment import mycrypt
from proto.respose_pb2 import Respose
from proto.request_pb2 import Request
from proto.men_size_pb2 import Men_size

def gera_requisicao(command, secrete_key, connection, file, clientid):
    msg, sign = select_req(command, secrete_key, file, clientid) #GERA A MENSAGEM
    if(msg == None and sign == None):
        return False
    men_size = Men_size(size=msg.ByteSize()) #GERA UMA MENSAGEM DE TAMANHO
    connection.send(men_size.SerializeToString()) #ENVIA O TAMANHO DA MENSAGEM
    connection.send(msg.SerializeToString()) #ENVIA A MENSAGEM
    return True

#SELECIONA MENSAGEM COM BASE NO PARAMETRO
def select_req(command, secrete_key, file, clientid):
    if(command == "GET"):
        #GERA UMA MENSAGEM DE GET
        msg, sign = gen_get(secrete_key, file, clientId=clientid)
    if(command == "POST"):
        # GERA UMA MENSAGEM DE POST
        msg, sign = gen_post(secrete_key, file, clientId=clientid)
    if(command == "DELETE"):
        # GERA UMA MENSAGEM DE DELETE
        msg, sign = gen_del(secrete_key, file, clientId=clientid)

    if(msg == None and sign == None):
        return None, None

    return msg, sign

def gen_close():

    pass

#FUNÇÃO DE GERAÇÃO DA ASSINATURA
def gen_sign(req, secrete_key):
    sign = hmac.HMAC(secrete_key.to_bytes(16, "big"))
    sign.update(req.SerializeToString())
    sign = sign.digest()
    req.signature = sign
    return sign

#FUNÇÃO QUE GERA A REQUISIÇÃO DE GET
def gen_get( secrete_key, url="index.html", command=Request.GET,
    protocolVersion = "HTTP/1.1", clientInfo = "python_client v1",
    clientId = 0 , encoding = "utf8" ):

    #GERAÇÃO DA REQUISIÇÃO
    req = Request( command = command, url = url, signature = bytes(),
                  protocolVersion = protocolVersion, clientId = clientId,
                  clientInfo = clientInfo, encoding = encoding )

    #GERA A ASSINATURA DA MENSAGEM
    sign = gen_sign(req, secrete_key)
    return req, sign

#FUNÇÃO QUE GERA A REQUISIÇÃO DE POST
def gen_post( secrete_key, url="index.html", command=Request.POST,
             protocolVersion = "HTTP/1.1", clientInfo = "python_client v1",
             clientId = 0 , encoding = "utf8" ):

    try:
        #ABRE E LE O ARQUIVO A SER ENVIADO
        file = open(url, "r")
        data = file.read()
        file.close()

        #GERAÇÃO DA REQUISIÇÃO
        req = Request( command = command, url = url, signature = bytes(),
            protocolVersion = protocolVersion, clientId = clientId,
            clientInfo = clientInfo, encoding = encoding, content =
            mycrypt.crypt(secrete_key, data) )

        #GERA A ASSINATURA DA MENSAGEM
        sign = gen_sign(req, secrete_key)
        return req, sign
    except:
        print("Arquivo não encontrado")
        return None, None

#FUNÇÃO QUE GERA A REQUISIÇÃO DE DELETE
def gen_del( secrete_key, url="index.html", command=Request.DELETE,
            protocolVersion = "HTTP/1.1", clientInfo = "python_client v1",
            clientId = 0 , encoding = "utf8" ):

    #GERAÇÃO DA REQUISIÇÃO
    req = Request( command = command, url = url, signature = bytes(),
                  protocolVersion = protocolVersion, clientId = clientId,
                  clientInfo = clientInfo, encoding = encoding )

    #GERA A ASSINATURA DA MENSAGEM
    sign = gen_sign(req, secrete_key)
    return req, sign
