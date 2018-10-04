import hmac, sys
from treatment import mycrypt
from proto.respose_pb2 import Respose
from proto.request_pb2 import Request
from proto.men_size_pb2 import Men_size

def valida_resposta(resp, secrete_key):
    #FAZ UMA COPIA DA ASSINATURA
    msg_sign = resp.signature
    resp.signature = bytes()

    #CRIA O OBJETO DO HMAC E FAZ AS OPERAÇOES NECESSARIAS PARA A VALIDAÇÃO DA ASSINATURA
    sign = hmac.HMAC(secrete_key.to_bytes(16, "big"))
    sign.update(resp.SerializeToString())
    sign = sign.digest()
    return hmac.compare_digest(msg_sign, sign)

def select_resp(resp, command, valido):
    if(valido):
        if(command == "GET"):
            resp_get(resp)
        if(command == "POST"):
            resp_post(resp)
        if(command == "DELETE"):
            resp_del(resp)
    else:
        print("Assinatura invalida, mensagem ignorada")

def recebe_resposta(secrete_key, connection, command):

    resp = Respose() #CRIA O OBJETO QUE RECEBERA A RESPOSTA
    men_size = Men_size() #CRIA O OBJETO QUE RECEBERA O TAMANHO DA RESPOSTA


    men_size.ParseFromString( connection.recv(5) ) #RECEBE O TAMANHO DA RESPOSTA
    resp.ParseFromString(connection.recv(men_size.size)) #RECEBE A RESPOSTA

    valido = valida_resposta(resp, secrete_key) # O METODO DO HMAC

    resp.content = mycrypt.decrypt(secrete_key, resp.content) #DECRIPTOGRAFA O CONTEUDO


    select_resp(resp, command, valido) # CHAMA A SELIÇÃO DO TRATADOR DE RESPOSTAS


# TRATA A MENSAGEM DE RESPOSTA DO GET
def resp_get(msg):
    if(msg.status == Respose.OK):
        try:
            file = open(msg.url, "w")
            file.write(msg.content.decode())
            file.close()
            print("Arquivo baixado e gravado com sucesso")
        except:
            print("Erro na gravação do arquivo")
    else:
        print("Erro no download do arquivo, favor requisitar novamente")

# TRATA A MENSAGEM DE RESPOSTA DO POST
def resp_post(msg):
    if(msg.status == Respose.OK):
        print("Arquivo Enviado com sucesso")
    else:
        print("Problema durante o envio, tente novamente")

# TRATA A MENSAGEM DE RESPOSTA DO DELETE
def resp_del(msg):
    if(msg.status == Respose.OK):
        print("Arquivo apagado com sucesso")
    else:
        print("Arquivo invalido ou sem permição de deleção")
