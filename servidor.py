from socket import *
import hashlib
import os

FILE_DIR = 'files'

IP = '127.0.0.1'
PORT = 2000

# Cria o socket UDP (IPv4, Datagrama)
S_SOCKET = socket(AF_INET, SOCK_DGRAM)

# Padronização das ações:
# - GET arquivo.ext
# - DATA seq bytes
# - ACK seq
# - END

def parse_msg(msg):
    parts = msg.split()
    if not parts:
        return None, None
    
    # 0: ação, 1-N: outros argumentos
    return parts[0], parts[1:]

def start_transfer(filename, addr):
    if not filename:
        S_SOCKET.sendto('400: Nome do arquivo invalido!'.encode(), addr)
        return

    if filename[0] != '/':
        filename = '/' + filename
    
    if not os.path.isfile(FILE_DIR + filename):
        S_SOCKET.sendto('404: Arquivo nao encontrado!'.encode(), addr)
        return

    S_SOCKET.sendto(f'Iniciado {filename}!'.encode(), addr)
    # Buscar arquivo

def send_segment(file, seq):
    # TODO: Enviar próximo seguimento
    pass

# Protocolo simples para receber a requisição
def handle_req(msg, addr):
    action, args = parse_msg(msg)

    if action == 'GET':
        filename = args[0] if args else None
        start_transfer(filename, addr)
    elif action == 'ACK':
        S_SOCKET.sendto('ACK'.encode(), addr)
        # TODO: Criar outro handler (enviar próximo pacote ou lidar com perdas)
        pass

def main():
    # Porta: número maior que 1024
    # Fixa a porta (’’ escuta em todas as interfaces de rede)
    S_SOCKET.bind((IP, PORT))
    print(f'Servidor escutando no endereco: {IP}:{PORT}')

    while True:
        # Aguardar conexões/mensagens de clientes.
        # Bloqueia e aguarda pacote. Salva dados e IP/Porta de origem
        msg, addr = S_SOCKET.recvfrom(2048)
        handle_req(msg.decode(), addr)

        # serverSocket.sendto(res.encode(), addr)

if __name__ == "__main__":
    main()