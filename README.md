# 
A principio não avia entendido o funcionamento da assinatura Tive problemas de transferencia de dados sem o protobuf, resultando em gerar varios para coisas diferentes
Implementei encriptação de mensagem ainda que fora dos requisitos A chave secreta compartilhada é gerada apartir de troca de chave Diffie-Helman, porem poderia ser estatica no cliente e no servidor.


Para rodar baixe a biblioteca Crypto usando:

pip3 install pycripto


Cliente/Servidor HTTP simplificado com conexção TCP com troca de chaves Diffie-Hellman e Encriptação AES e validação de assinatura usando HMAC(MD5 HASH)

COMO USAR:

Servidor:

    Executar: ./server.py <numero_da_porta>

    Para disponibilizar arquivos para os clientes coloque na pasta http, os clientes terão sua propria pasta e não excluirão arquivos desta pasta

Client:

    Executar: ./client.py <ip_de_conexão> <numero_da_porta>

    Como usar:

        '''
        <comando> <nome_do_arquivo>
    
        Comandos: GET, POST, DELETE
        GET: baixa arquivo do servidor
        POST: envia arquivo para o servidor
        DELETE: deleta um arquivo enviado para o servidor
        '''
