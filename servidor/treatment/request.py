import hmac
import treatment.mycrypt
from proto.request_pb2 import Request
from proto.men_size_pb2 import Men_size

def recebe_requisicao(secrete_key, source):
    msg = Request() #CRIA O OBJETO DE REQUISIÇÃO
    msg_size = Men_size() # CRIA O OBJETO QUE RECEBE O TAMNHO DA MENSAGEM

    msg_size.ParseFromString( source.recv(5) ) #RECEBE O TAMANHO DA MENSAGEM
    msg.ParseFromString( source.recv(msg_size.size) ) #RECEBE MENSAGEM

    #CRIA UMA COPIA DA SIGNATURE
    msg_sign = msg.signature
    msg.signature = bytes()

    #CRIA O OBJETO DO HMAC E FAZ AS OPERAÇOES NECESSARIAS PARA A VALIDAÇÃO DA ASSINATURA
    sign = hmac.HMAC(secrete_key.to_bytes(16, "big"))
    sign.update(msg.SerializeToString())
    sign = sign.digest()

    #RETORNA A MENSAGEM E A VALIDADE DA ASSINATURA
    return msg, hmac.compare_digest(msg_sign, sign)
