# Cliente e Servidor de arquivos similiar ao HTTP


## Para rodar baixe a biblioteca Crypto usando:

    pip3 install pycripto


Cliente/Servidor HTTP simplificado com conexção TCP com troca de chaves Diffie-Hellman e Encriptação AES e validação de assinatura usando HMAC(MD5 HASH)

## COMO USAR:

### Servidor:

Executar:

    ./server.py <numero_da_porta>

Para disponibilizar arquivos para os clientes coloque na pasta http, os clientes terão sua propria pasta e não excluirão arquivos desta pasta

### Client:

Executar:

    ./client.py <ip_de_conexão> <numero_da_porta>

Como usar:

    <comando> <nome_do_arquivo>

    Comandos: GET, POST, DELETE
    GET: baixa arquivo do servidor
    POST: envia arquivo para o servidor
    DELETE: deleta um arquivo enviado para o servidor
